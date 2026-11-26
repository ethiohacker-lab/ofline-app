"""
Offline SQLite memory store for Maya.
Stores pre-seeded, user-learned, and online-cached Q&A pairs, TF-IDF vocabulary weights,
and learning history inside Android's internal app storage (context.filesDir).
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


DB_FILENAME = "maya_knowledge.db"
LEGACY_DB_FILENAME = "meklit_knowledge.db"


class KnowledgeMemory:
    def __init__(self, files_dir: str) -> None:
        os.makedirs(files_dir, exist_ok=True)
        self.db_path = os.path.join(files_dir, DB_FILENAME)
        legacy_path = os.path.join(files_dir, LEGACY_DB_FILENAME)
        if not os.path.exists(self.db_path) and os.path.exists(legacy_path):
            shutil.copy2(legacy_path, self.db_path)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'General',
                    tags TEXT NOT NULL DEFAULT '',
                    reinforcement_weight REAL NOT NULL DEFAULT 1.0,
                    times_used INTEGER NOT NULL DEFAULT 0,
                    source TEXT NOT NULL DEFAULT 'seed',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS vocabulary (
                    term TEXT PRIMARY KEY,
                    idf REAL NOT NULL,
                    doc_freq INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS learning_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT NOT NULL,
                    matched_id INTEGER,
                    confidence REAL NOT NULL DEFAULT 0.0,
                    route TEXT NOT NULL DEFAULT 'knowledge',
                    was_corrected INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.commit()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def initialize_if_empty(self, seed_entries: List[Dict[str, str]]) -> int:
        """Seed database on first launch and sync any newly added seed items on app upgrades."""
        now = self._now_iso()
        with self._connect() as conn:
            # Upgrade legacy Meklit branding in existing seed rows if present
            conn.execute(
                "DELETE FROM knowledge WHERE source = 'seed' AND answer LIKE '%Meklit%'"
            )

            existing_rows = conn.execute(
                "SELECT LOWER(TRIM(question)) AS q FROM knowledge"
            ).fetchall()
            existing_set = {r["q"] for r in existing_rows}

            new_rows = [
                (
                    entry["question"].strip(),
                    entry["answer"].strip(),
                    entry.get("category", "General").strip(),
                    entry.get("tags", "").strip(),
                    1.0,
                    0,
                    "seed",
                    now,
                    now,
                )
                for entry in seed_entries
                if entry["question"].strip().lower() not in existing_set
            ]

            if new_rows:
                conn.executemany(
                    """
                    INSERT INTO knowledge (
                        question, answer, category, tags,
                        reinforcement_weight, times_used, source, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    new_rows,
                )
            conn.commit()
            return len(new_rows)

    def get_all_entries(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, question, answer, category, tags,
                       reinforcement_weight, times_used, source, created_at, updated_at
                FROM knowledge
                ORDER BY
                    CASE source
                        WHEN 'learned' THEN 0
                        WHEN 'online_cached' THEN 1
                        ELSE 2
                    END,
                    times_used DESC,
                    id ASC
                """
            ).fetchall()
            return [dict(r) for r in rows]

    def search_entries(self, search: str = "", category: str = "All") -> List[Dict[str, Any]]:
        query = (
            "SELECT id, question, answer, category, tags, "
            "reinforcement_weight, times_used, source, created_at, updated_at "
            "FROM knowledge WHERE 1=1"
        )
        params: List[Any] = []
        if category and category != "All":
            if category == "Online Cached":
                query += " AND source = 'online_cached'"
            else:
                query += " AND LOWER(category) = LOWER(?)"
                params.append(category.strip())
        if search and search.strip():
            like = f"%{search.strip()}%"
            query += " AND (question LIKE ? OR answer LIKE ? OR tags LIKE ?)"
            params.extend([like, like, like])
        query += (
            " ORDER BY CASE source WHEN 'learned' THEN 0 WHEN 'online_cached' THEN 1 ELSE 2 END, "
            "times_used DESC, id DESC"
        )
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def add_or_update_knowledge(
        self,
        question: str,
        answer: str,
        category: str = "Learned",
        tags: str = "",
        source: str = "learned",
        replace_id: Optional[int] = None,
    ) -> Tuple[int, str]:
        q_clean = question.strip()
        a_clean = answer.strip()
        cat_clean = category.strip() or "Learned"
        tags_clean = tags.strip()
        now = self._now_iso()

        with self._connect() as conn:
            if replace_id is not None:
                conn.execute(
                    """
                    UPDATE knowledge
                    SET question = ?, answer = ?, category = ?, tags = ?,
                        reinforcement_weight = MIN(reinforcement_weight + 0.25, 3.0),
                        source = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (q_clean, a_clean, cat_clean, tags_clean, source, now, replace_id),
                )
                conn.commit()
                return replace_id, "updated"

            existing = conn.execute(
                "SELECT id FROM knowledge WHERE LOWER(TRIM(question)) = LOWER(?)",
                (q_clean,),
            ).fetchone()
            if existing:
                entry_id = int(existing["id"])
                conn.execute(
                    """
                    UPDATE knowledge
                    SET answer = ?, category = ?, tags = ?,
                        reinforcement_weight = MIN(reinforcement_weight + 0.20, 3.0),
                        source = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (a_clean, cat_clean, tags_clean, source, now, entry_id),
                )
                conn.commit()
                return entry_id, "updated"

            cursor = conn.execute(
                """
                INSERT INTO knowledge (
                    question, answer, category, tags,
                    reinforcement_weight, times_used, source, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (q_clean, a_clean, cat_clean, tags_clean, 1.15, 0, source, now, now),
            )
            conn.commit()
            return int(cursor.lastrowid), "inserted"

    def update_entry_fields(
        self, entry_id: int, question: str, answer: str, category: str
    ) -> bool:
        now = self._now_iso()
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE knowledge
                SET question = ?, answer = ?, category = ?, updated_at = ?
                WHERE id = ?
                """,
                (question.strip(), answer.strip(), category.strip(), now, entry_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_entry(self, entry_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM knowledge WHERE id = ?", (entry_id,))
            conn.commit()
            return cur.rowcount > 0

    def reinforce_entry(self, entry_id: int, delta: float = 0.15) -> Optional[float]:
        now = self._now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE knowledge
                SET reinforcement_weight = MIN(reinforcement_weight + ?, 3.0),
                    times_used = times_used + 1,
                    updated_at = ?
                WHERE id = ?
                """,
                (delta, now, entry_id),
            )
            row = conn.execute(
                "SELECT reinforcement_weight FROM knowledge WHERE id = ?",
                (entry_id,),
            ).fetchone()
            conn.commit()
            return float(row["reinforcement_weight"]) if row else None

    def increment_usage(self, entry_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE knowledge SET times_used = times_used + 1 WHERE id = ?",
                (entry_id,),
            )
            conn.commit()

    def get_random_quiz_entry(self, category: str = "All") -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            if category and category != "All":
                row = conn.execute(
                    "SELECT * FROM knowledge WHERE LOWER(category) = LOWER(?) AND category != 'General' ORDER BY RANDOM() LIMIT 1",
                    (category,),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT * FROM knowledge WHERE category IN ('Horticulture', 'Computer Science', 'English', 'Learned') ORDER BY RANDOM() LIMIT 1"
                ).fetchone()
            return dict(row) if row else None

    def save_vocabulary(self, vocab_idf: Dict[str, Tuple[float, int]]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM vocabulary")
            conn.executemany(
                "INSERT INTO vocabulary (term, idf, doc_freq) VALUES (?, ?, ?)",
                [(term, float(idf), int(df)) for term, (idf, df) in vocab_idf.items()],
            )
            conn.commit()

    def log_interaction(
        self,
        user_query: str,
        matched_id: Optional[int],
        confidence: float,
        route: str,
        was_corrected: bool = False,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO learning_history (
                    user_query, matched_id, confidence, route, was_corrected, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_query.strip(),
                    matched_id,
                    float(confidence),
                    route,
                    1 if was_corrected else 0,
                    self._now_iso(),
                ),
            )
            conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        with self._connect() as conn:
            total_row = conn.execute("SELECT COUNT(*) AS cnt FROM knowledge").fetchone()
            learned_row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM knowledge WHERE source = 'learned'"
            ).fetchone()
            cached_row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM knowledge WHERE source = 'online_cached'"
            ).fetchone()
            vocab_row = conn.execute("SELECT COUNT(*) AS cnt FROM vocabulary").fetchone()
            hist_row = conn.execute(
                "SELECT COUNT(*) AS cnt, COALESCE(SUM(was_corrected), 0) AS corr FROM learning_history"
            ).fetchone()
            avg_row = conn.execute(
                "SELECT COALESCE(AVG(reinforcement_weight), 1.0) AS avg_w FROM knowledge"
            ).fetchone()
            cat_rows = conn.execute(
                "SELECT category, COUNT(*) AS cnt FROM knowledge GROUP BY category ORDER BY cnt DESC"
            ).fetchall()

            total_entries = int(total_row["cnt"]) if total_row else 0
            learned_count = int(learned_row["cnt"]) if learned_row else 0
            cached_count = int(cached_row["cnt"]) if cached_row else 0
            return {
                "total_entries": total_entries,
                "seeded_count": max(0, total_entries - learned_count - cached_count),
                "learned_count": learned_count,
                "online_cached_count": cached_count,
                "vocab_size": int(vocab_row["cnt"]) if vocab_row else 0,
                "total_interactions": int(hist_row["cnt"]) if hist_row else 0,
                "total_corrections": int(hist_row["corr"]) if hist_row else 0,
                "avg_reinforcement": round(float(avg_row["avg_w"]), 2) if avg_row else 1.0,
                "categories": {r["category"]: int(r["cnt"]) for r in cat_rows},
            }
