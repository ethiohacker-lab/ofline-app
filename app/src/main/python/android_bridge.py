"""
Chaquopy entry-point bridge between Android Kotlin UI and Maya's SlowLearningBrain.
All functions return UTF-8 JSON strings for clean, typed deserialization in Kotlin.
"""

from __future__ import annotations

import json
from typing import Optional

from brain import SlowLearningBrain
from online_gatherer import CURATED_STUDY_PACKS


_BRAIN: Optional[SlowLearningBrain] = None


def _get_brain() -> SlowLearningBrain:
    if _BRAIN is None:
        raise RuntimeError("Maya AI brain is not initialized. Call init_brain(files_dir) first.")
    return _BRAIN


def _combined_stats(brain: SlowLearningBrain) -> dict:
    stats = brain.memory.get_stats()
    stats["vault"] = brain.vault.get_status()
    return stats


def init_brain(files_dir: str) -> str:
    global _BRAIN
    if _BRAIN is None:
        _BRAIN = SlowLearningBrain(files_dir)
    return json.dumps(
        {
            "status": "ready",
            "stats": _combined_stats(_BRAIN),
        },
        ensure_ascii=False,
    )


def ask(query: str, allow_online_fetch: bool = False) -> str:
    brain = _get_brain()
    result = brain.answer_query(query, allow_online_fetch=bool(allow_online_fetch))
    return json.dumps(result, ensure_ascii=False)


def gather_topic(topic: str) -> str:
    brain = _get_brain()
    result = brain.gather_and_store_online(topic)
    return json.dumps(result, ensure_ascii=False)


def gather_study_pack(pack_name: str) -> str:
    brain = _get_brain()
    result = brain.gather_study_pack(pack_name)
    return json.dumps(result, ensure_ascii=False)


def get_study_packs() -> str:
    return json.dumps(list(CURATED_STUDY_PACKS.keys()), ensure_ascii=False)


def teach(
    question: str,
    answer: str,
    category: str = "Learned",
    tags: str = "",
    replace_id: int = -1,
) -> str:
    brain = _get_brain()
    rid = replace_id if replace_id > 0 else None
    result = brain.teach(
        question=question,
        answer=answer,
        category=category,
        tags=tags,
        replace_id=rid,
    )
    return json.dumps(result, ensure_ascii=False)


def reinforce_answer(entry_id: int) -> str:
    brain = _get_brain()
    result = brain.reinforce(int(entry_id))
    return json.dumps(result, ensure_ascii=False)


def get_knowledge_entries(search: str = "", category: str = "All") -> str:
    brain = _get_brain()
    entries = brain.memory.search_entries(search=search, category=category)
    return json.dumps(entries, ensure_ascii=False)


def update_knowledge_entry(
    entry_id: int, question: str, answer: str, category: str
) -> str:
    brain = _get_brain()
    updated = brain.memory.update_entry_fields(int(entry_id), question, answer, category)
    if updated:
        brain.rebuild_index()
    return json.dumps(
        {"status": "ok" if updated else "not_found", "stats": brain.memory.get_stats()},
        ensure_ascii=False,
    )


def delete_knowledge_entry(entry_id: int) -> str:
    brain = _get_brain()
    deleted = brain.memory.delete_entry(int(entry_id))
    if deleted:
        brain.rebuild_index()
    return json.dumps(
        {"status": "ok" if deleted else "not_found", "stats": brain.memory.get_stats()},
        ensure_ascii=False,
    )


def get_stats() -> str:
    brain = _get_brain()
    return json.dumps(_combined_stats(brain), ensure_ascii=False)


def get_vault_status() -> str:
    brain = _get_brain()
    return json.dumps(brain.vault.get_status(), ensure_ascii=False)


def search_vault(query: str = "", domain: str = "All", limit: int = 25) -> str:
    brain = _get_brain()
    rows = brain.vault.search_vault(query=query, domain=domain, limit=int(limit))
    return json.dumps(rows, ensure_ascii=False)
