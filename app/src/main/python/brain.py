"""
Maya's Incremental Slow-Learning Brain built from scratch using pure Python + NumPy.
Capabilities:
- Conversational & common English intent engine (greetings, polite phrases, small talk, time/date)
- Offline extractive NumPy TF-IDF summarizer & study quiz generator
- Offline English dictionary + typo-tolerant character trigram fuzzy similarity
- Safe AST math, matrix, statistics, Horticulture & CS calculators (math_engine.py)
- Hybrid NumPy TF-IDF + synonym expansion + reinforcement-weighted retrieval
- Multi-turn session context memory for follow-up questions
- Optional Online -> Offline Wikipedia & Dictionary caching into SQLite
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from math_engine import evaluate_query
from memory import KnowledgeMemory
from offline_tools import (
    suggest_closest_spelling,
    try_conversational_intent,
    try_offline_dictionary,
    try_offline_summarizer,
    try_study_quiz,
)
from online_gatherer import CURATED_STUDY_PACKS, gather_topic_online
from seed_data import SEED_KNOWLEDGE
from vault import KnowledgeVault


CONFIDENCE_THRESHOLD = 0.65

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "am", "be", "been", "being",
    "do", "does", "did", "have", "has", "had", "will", "would", "could", "should",
    "can", "may", "might", "must", "shall",
    "i", "me", "my", "myself", "we", "our", "you", "your", "he", "she", "it", "they", "them",
    "this", "that", "these", "those", "there", "here",
    "in", "on", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "of", "off", "over", "under", "again", "further", "then", "once",
    "and", "but", "or", "nor", "so", "yet", "if", "because", "as", "until", "while",
    "what", "which", "who", "whom", "whose", "where", "when", "why", "how",
    "please", "tell", "explain", "define", "describe", "give", "show", "know",
    "very", "just", "more", "most", "some", "any", "all", "each", "both",
}

_SYNONYMS: Dict[str, str] = {
    "algo": "algorithm",
    "algos": "algorithm",
    "db": "database",
    "dbs": "database",
    "fert": "fertilizer",
    "veg": "vegetable",
    "net": "network",
    "eth": "ethiopia",
    "ethiopian": "ethiopia",
    "calc": "calculate",
    "oop": "object",
    "os": "operating",
    "norm": "normalization",
    "vocab": "vocabulary",
    "eng": "english",
    "prog": "programming",
    "sec": "security",
    "crypto": "cryptography",
}


def light_stem(token: str) -> str:
    if len(token) <= 3 or token.isdigit():
        return token
    if token in {
        "1nf", "2nf", "3nf", "bcnf", "acid", "http", "https", "dhcp",
        "ipv4", "cidr", "fifo", "lifo", "enset", "npk", "ipm", "sdlc", "maya",
    }:
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith("ves") and len(token) > 4:
        return token[:-3] + "f"
    if token.endswith("ing") and len(token) > 5:
        base = token[:-3]
        if len(base) >= 3 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    if token.endswith("tion") and len(token) > 6:
        return token[:-4] + "t"
    if token.endswith("ation") and len(token) > 7:
        return token[:-5] + "e"
    if token.endswith("ment") and len(token) > 6:
        return token[:-4]
    if token.endswith("ness") and len(token) > 6:
        return token[:-4]
    if token.endswith("ed") and len(token) > 4:
        base = token[:-2]
        if len(base) >= 3 and base[-1] == base[-2]:
            base = base[:-1]
        return base
    if token.endswith("es") and len(token) > 4 and not token.endswith("ss"):
        return token[:-2]
    if token.endswith("s") and len(token) > 3 and not token.endswith(("ss", "us", "is", "os", "cs")):
        return token[:-1]
    return token


def preprocess_text(text: str, include_bigrams: bool = True) -> List[str]:
    cleaned = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    raw_tokens = cleaned.split()
    stems: List[str] = []
    for tok in raw_tokens:
        if tok in _STOPWORDS:
            continue
        if len(tok) == 1 and tok not in {"n", "p", "k", "c", "x", "y"}:
            continue
        expanded = _SYNONYMS.get(tok, tok)
        stems.append(light_stem(expanded))

    if not stems:
        stems = [light_stem(_SYNONYMS.get(t, t)) for t in raw_tokens if t]

    if not include_bigrams or len(stems) < 2:
        return stems

    bigrams = [f"{stems[i]}_{stems[i + 1]}" for i in range(len(stems) - 1)]
    return stems + bigrams


def _char_trigrams(text: str) -> Counter[str]:
    clean = re.sub(r"[^a-z0-9]", "", text.lower())
    if len(clean) < 3:
        return Counter([clean]) if clean else Counter()
    return Counter(clean[i : i + 3] for i in range(len(clean) - 2))


def _trigram_sim(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    common = set(a.keys()) & set(b.keys())
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0


class SlowLearningBrain:
    def __init__(self, files_dir: str) -> None:
        self.memory = KnowledgeMemory(files_dir)
        self.memory.initialize_if_empty(SEED_KNOWLEDGE)
        self.vault = KnowledgeVault(files_dir)
        self.vault.start_background_hydration()
        self.entries: List[Dict[str, Any]] = []
        self.vocab: Dict[str, int] = {}
        self.idf: np.ndarray = np.array([], dtype=np.float64)
        self.doc_matrix: np.ndarray = np.zeros((0, 0), dtype=np.float64)
        self.doc_trigrams: List[Counter[str]] = []
        # Multi-turn session context memory
        self.last_topic_question: Optional[str] = None
        self.last_entry_id: Optional[int] = None
        self.rebuild_index()

    def rebuild_index(self) -> None:
        self.entries = self.memory.get_all_entries()
        n_docs = len(self.entries)
        if n_docs == 0:
            self.vocab = {}
            self.idf = np.array([], dtype=np.float64)
            self.doc_matrix = np.zeros((0, 0), dtype=np.float64)
            self.doc_trigrams = []
            self.memory.save_vocabulary({})
            return

        doc_token_lists: List[List[str]] = []
        df_counter: Counter[str] = Counter()
        self.doc_trigrams = []

        for entry in self.entries:
            q_tokens = preprocess_text(entry["question"], include_bigrams=True)
            tag_tokens = preprocess_text(entry.get("tags", ""), include_bigrams=True)
            ans_tokens = preprocess_text(entry["answer"][:280], include_bigrams=False)
            combined = q_tokens + q_tokens + tag_tokens + tag_tokens + ans_tokens
            doc_token_lists.append(combined)
            self.doc_trigrams.append(_char_trigrams(entry["question"] + " " + entry.get("tags", "")))
            for unique_tok in set(combined):
                df_counter[unique_tok] += 1

        sorted_terms = sorted(df_counter.keys())
        self.vocab = {term: idx for idx, term in enumerate(sorted_terms)}
        v_size = len(sorted_terms)

        idf_arr = np.zeros(v_size, dtype=np.float64)
        vocab_to_save: Dict[str, Tuple[float, int]] = {}
        for term, idx in self.vocab.items():
            df = df_counter[term]
            idf_val = math.log((1.0 + n_docs) / (1.0 + df)) + 1.0
            idf_arr[idx] = idf_val
            vocab_to_save[term] = (idf_val, df)

        self.idf = idf_arr
        matrix = np.zeros((n_docs, v_size), dtype=np.float64)

        for doc_idx, tokens in enumerate(doc_token_lists):
            tf_counts = Counter(tokens)
            for term, count in tf_counts.items():
                col = self.vocab.get(term)
                if col is not None:
                    matrix[doc_idx, col] = (1.0 + math.log(count)) * idf_arr[col]

        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        self.doc_matrix = matrix / norms
        self.memory.save_vocabulary(vocab_to_save)

    def _vectorize_query(self, query: str) -> Tuple[np.ndarray, List[str]]:
        tokens = preprocess_text(query, include_bigrams=True)
        vec = np.zeros(len(self.vocab), dtype=np.float64)
        if not tokens or len(self.vocab) == 0:
            return vec, tokens
        tf_counts = Counter(tokens)
        for term, count in tf_counts.items():
            idx = self.vocab.get(term)
            if idx is not None:
                vec[idx] = (1.0 + math.log(count)) * self.idf[idx]
        norm = float(np.linalg.norm(vec))
        if norm > 0.0:
            vec = vec / norm
        return vec, tokens

    def _resolve_followup(self, q_clean: str) -> str:
        ql = q_clean.lower().strip().rstrip("?.!")
        if self.last_topic_question and ql in {
            "tell me more", "explain more", "more details", "example",
            "give me an example", "why", "how does it work", "elaborate",
        }:
            return f"{self.last_topic_question} {q_clean}"
        return q_clean

    def answer_query(self, query: str, allow_online_fetch: bool = False) -> Dict[str, Any]:
        q_clean = query.strip()
        if not q_clean:
            return {
                "answer": "Please type a greeting, question, math expression, or `summarize: <text>`.",
                "confidence": 0.0,
                "route": "empty",
                "category": "General",
                "matched_id": None,
                "matched_question": None,
                "needs_teaching": False,
                "closest_guess": None,
                "formula_steps": "",
                "tag": "Prompt",
            }

        # 1. Conversational & Common English greetings/small-talk/time
        conv = try_conversational_intent(q_clean)
        if conv is not None:
            self.memory.log_interaction(q_clean, None, conv["confidence"], conv["route"])
            return conv

        # 2. Offline Extractive Summarizer
        summ = try_offline_summarizer(q_clean)
        if summ is not None:
            self.memory.log_interaction(q_clean, None, 1.0, "summarizer")
            return summ

        # 3. Offline Study Quiz / Flashcard Generator
        quiz = try_study_quiz(q_clean, self.memory)
        if quiz is not None:
            self.memory.log_interaction(q_clean, quiz.get("matched_id"), 1.0, "quiz")
            return quiz

        # 4. Offline Core English Dictionary
        dict_res = try_offline_dictionary(q_clean)
        if dict_res is not None:
            self.memory.log_interaction(q_clean, None, dict_res["confidence"], "dictionary")
            return dict_res

        # 5. Deterministic AST Math, Matrices, Units, Horticulture & CS Calculators
        math_res = evaluate_query(q_clean)
        if math_res is not None:
            self.memory.log_interaction(q_clean, None, 1.0, "math_engine")
            return {
                "answer": math_res["answer"],
                "confidence": 1.0,
                "route": "math_engine",
                "category": math_res["category"],
                "matched_id": None,
                "matched_question": None,
                "needs_teaching": False,
                "closest_guess": None,
                "formula_steps": math_res.get("steps", ""),
                "tag": math_res.get("tag", "Math Engine"),
            }

        # 5b. Fast indexed lookup in the 1.05M-record Offline Vault (e.g., 'port 443', 'unicode 4608', 'number 1729')
        vault_hit = self.vault.lookup_exact_for_chat(q_clean)
        if vault_hit is not None:
            self.memory.log_interaction(q_clean, None, 1.0, "vault")
            return {
                "answer": f"**{vault_hit['title']}**\n{vault_hit['fact']}",
                "confidence": 1.0,
                "route": "vault",
                "category": vault_hit["domain"],
                "matched_id": None,
                "matched_question": vault_hit["title"],
                "needs_teaching": False,
                "closest_guess": None,
                "formula_steps": f"Indexed Lookup • 1.05M+ Offline Vault (Row #{vault_hit['id']:,})",
                "tag": "1M+ Data Vault",
            }

        # 6. Multi-turn context expansion for short follow-ups
        effective_query = self._resolve_followup(q_clean)

        # 7. Hybrid TF-IDF + Keyword Coverage + Character Trigram Fuzzy Similarity
        best_score = 0.0
        best_entry: Optional[Dict[str, Any]] = None
        if len(self.entries) > 0 and self.doc_matrix.shape[0] > 0:
            q_vec, q_tokens = self._vectorize_query(effective_query)
            q_unigrams = {t for t in q_tokens if "_" not in t}
            q_tri = _char_trigrams(effective_query)

            cos_scores = (
                self.doc_matrix @ q_vec
                if float(np.linalg.norm(q_vec)) > 0.0
                else np.zeros(len(self.entries), dtype=np.float64)
            )

            effective_scores = np.zeros(len(self.entries), dtype=np.float64)
            for idx, entry in enumerate(self.entries):
                raw_cos = float(cos_scores[idx])
                tri_sim = _trigram_sim(q_tri, self.doc_trigrams[idx])

                entry_qt = set(
                    preprocess_text(entry["question"] + " " + entry.get("tags", ""), include_bigrams=False)
                )
                overlap_ratio = len(q_unigrams & entry_qt) / max(1, len(q_unigrams)) if q_unigrams else 0.0

                if raw_cos > 0.01:
                    base = 0.55 * raw_cos + 0.35 * overlap_ratio + 0.10 * tri_sim
                elif tri_sim >= 0.42:
                    # Typo-tolerant fallback via character trigrams
                    base = 0.85 * tri_sim
                else:
                    base = 0.0

                rw = float(entry.get("reinforcement_weight", 1.0))
                boost = 1.0 + 0.08 * max(0.0, min(rw - 1.0, 2.0))
                effective_scores[idx] = min(1.0, base * boost)

            best_idx = int(np.argmax(effective_scores))
            best_score = round(float(effective_scores[best_idx]), 4)
            best_entry = self.entries[best_idx]

        if best_entry is not None and best_score >= CONFIDENCE_THRESHOLD:
            self.last_topic_question = best_entry["question"]
            self.last_entry_id = int(best_entry["id"])
            self.memory.increment_usage(int(best_entry["id"]))
            self.memory.log_interaction(q_clean, int(best_entry["id"]), best_score, "knowledge")
            tag = (
                "Online Cached"
                if best_entry["source"] == "online_cached"
                else ("Self-Learned" if best_entry["source"] == "learned" else "Curriculum KB")
            )
            return {
                "answer": best_entry["answer"],
                "confidence": best_score,
                "route": "knowledge",
                "category": best_entry["category"],
                "matched_id": int(best_entry["id"]),
                "matched_question": best_entry["question"],
                "needs_teaching": False,
                "closest_guess": None,
                "formula_steps": "",
                "tag": tag,
            }

        # 8. Online -> Offline Auto-Gather when internet is available & enabled
        if allow_online_fetch:
            fetched, _err = gather_topic_online(q_clean)
            if fetched is not None:
                entry_id, _ = self.memory.add_or_update_knowledge(
                    question=fetched["question"],
                    answer=fetched["answer"],
                    category=fetched["category"],
                    tags=fetched["tags"],
                    source="online_cached",
                )
                self.rebuild_index()
                self.last_topic_question = fetched["question"]
                self.last_entry_id = entry_id
                self.memory.log_interaction(q_clean, entry_id, 0.92, "online_cached")
                return {
                    "answer": fetched["answer"],
                    "confidence": 0.92,
                    "route": "online_cached",
                    "category": fetched["category"],
                    "matched_id": entry_id,
                    "matched_question": fetched["question"],
                    "needs_teaching": False,
                    "closest_guess": None,
                    "formula_steps": f"Fetched from {fetched['source_label']} & saved to SQLite for offline reuse",
                    "tag": f"Cached ({fetched['source_label']})",
                }

        # 9. Honest Uncertainty + Spelling Hint + Closest Guess + Teach Prompt
        closest = None
        if best_entry is not None and best_score >= 0.22:
            snippet = best_entry["answer"]
            if len(snippet) > 220:
                snippet = snippet[:217].rstrip() + "..."
            closest = {
                "id": int(best_entry["id"]),
                "question": best_entry["question"],
                "answer": snippet,
                "category": best_entry["category"],
                "confidence": best_score,
            }

        # Offer spelling suggestion if a word looks misspelled
        spell_hint = ""
        words = re.findall(r"[a-zA-Z]{4,}", q_clean)
        if words and self.vocab:
            vocab_list = list(self.vocab.keys())
            for w in words:
                if light_stem(w.lower()) not in self.vocab:
                    sug = suggest_closest_spelling(w, vocab_list)
                    if sug and sug != w.lower():
                        spell_hint = f"\n\n*Did you mean `{sug}`?*"
                        break

        self.memory.log_interaction(
            q_clean, int(best_entry["id"]) if closest else None, best_score, "low_confidence"
        )
        return {
            "answer": (
                f"I don't know that with high confidence yet ({int(round(best_score * 100))}% match). "
                "Tap **Teach Maya** to store the answer offline—or if you're connected, tap **Search Online & Save Offline** to cache it from Wikipedia/Dictionary!"
                f"{spell_hint}"
            ),
            "confidence": best_score,
            "route": "low_confidence",
            "category": best_entry["category"] if closest else "Learned",
            "matched_id": None,
            "matched_question": None,
            "needs_teaching": True,
            "closest_guess": closest,
            "formula_steps": "",
            "tag": "Needs Teaching",
        }

    def gather_and_store_online(self, topic: str) -> Dict[str, Any]:
        fetched, err = gather_topic_online(topic)
        if fetched is None:
            return {
                "status": "error",
                "error": err or "Could not fetch topic online.",
                "stats": self.memory.get_stats(),
            }
        entry_id, action = self.memory.add_or_update_knowledge(
            question=fetched["question"],
            answer=fetched["answer"],
            category=fetched["category"],
            tags=fetched["tags"],
            source="online_cached",
        )
        self.rebuild_index()
        return {
            "status": "ok",
            "action": action,
            "entry_id": entry_id,
            "title": fetched["question"],
            "category": fetched["category"],
            "answer": fetched["answer"],
            "source_label": fetched["source_label"],
            "stats": self.memory.get_stats(),
        }

    def gather_study_pack(self, pack_name: str) -> Dict[str, Any]:
        topics = CURATED_STUDY_PACKS.get(pack_name, [])
        if not topics:
            return {"status": "error", "error": "Unknown study pack.", "saved": 0, "stats": self.memory.get_stats()}
        saved = 0
        titles: List[str] = []
        for topic in topics:
            fetched, _ = gather_topic_online(topic)
            if fetched is not None:
                self.memory.add_or_update_knowledge(
                    question=fetched["question"],
                    answer=fetched["answer"],
                    category=fetched["category"],
                    tags=fetched["tags"],
                    source="online_cached",
                )
                saved += 1
                titles.append(fetched["question"])
        if saved > 0:
            self.rebuild_index()
        return {
            "status": "ok" if saved > 0 else "error",
            "saved": saved,
            "total": len(topics),
            "titles": titles,
            "error": None if saved > 0 else "Unable to reach Wikipedia/Dictionary APIs. Check internet connection.",
            "stats": self.memory.get_stats(),
        }

    def teach(
        self,
        question: str,
        answer: str,
        category: str = "Learned",
        tags: str = "",
        replace_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        entry_id, action = self.memory.add_or_update_knowledge(
            question=question,
            answer=answer,
            category=category,
            tags=tags,
            source="learned",
            replace_id=replace_id,
        )
        self.memory.log_interaction(question, entry_id, 1.0, "teach", was_corrected=True)
        self.rebuild_index()
        return {
            "status": "ok",
            "action": action,
            "entry_id": entry_id,
            "stats": self.memory.get_stats(),
        }

    def reinforce(self, entry_id: int) -> Dict[str, Any]:
        new_weight = self.memory.reinforce_entry(entry_id, delta=0.15)
        self.rebuild_index()
        return {
            "status": "ok" if new_weight is not None else "not_found",
            "entry_id": entry_id,
            "reinforcement_weight": new_weight,
            "stats": self.memory.get_stats(),
        }
