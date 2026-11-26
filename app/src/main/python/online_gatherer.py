"""
Online Knowledge Gatherer for Maya.
When the device is online, fetches real open-knowledge data from:
1. Free Dictionary API (https://api.dictionaryapi.dev) for English words/definitions/synonyms
2. Wikipedia REST Summary & MediaWiki Search APIs (https://en.wikipedia.org) for general,
   Horticulture, Computer Science, and Mathematics topics.
Stores fetched knowledge directly into local SQLite (source='online_cached') so it remains
permanently available when the user goes 100% offline.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


_USER_AGENT = "MayaOfflineAssistant/1.0 (Android Educational App)"
_TIMEOUT_SEC = 8


def _http_get_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=_TIMEOUT_SEC) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def _infer_category(text: str, default: str = "General") -> str:
    tl = text.lower()
    hort_kw = (
        "plant", "crop", "soil", "coffee", "horticulture", "photosynthesis", "seed",
        "irrigation", "fertilizer", "fruit", "vegetable", "fungus", "leaf", "botany", "agriculture",
    )
    cs_kw = (
        "algorithm", "computer", "software", "database", "network", "protocol", "programming",
        "encryption", "compiler", "operating system", "tcp", "http", "linux", "memory", "cpu", "data structure",
    )
    math_kw = ("theorem", "algebra", "calculus", "geometry", "matrix", "equation", "probability", "statistics")
    if any(k in tl for k in hort_kw):
        return "Horticulture"
    if any(k in tl for k in cs_kw):
        return "Computer Science"
    if any(k in tl for k in math_kw):
        return "Math"
    return default


def fetch_english_dictionary(word: str) -> Optional[Dict[str, str]]:
    clean = re.sub(r"[^a-zA-Z\-]", "", word.strip().lower())
    if not clean:
        return None
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(clean)}"
    try:
        data = _http_get_json(url)
        if not isinstance(data, list) or not data:
            return None
        entry = data[0]
        phonetic = entry.get("phonetic", "")
        meanings = entry.get("meanings", [])
        if not meanings:
            return None

        lines: List[str] = [f"**{clean.capitalize()}** {phonetic}".strip()]
        all_syns: List[str] = []
        for m in meanings[:3]:
            pos = m.get("partOfSpeech", "")
            defs = m.get("definitions", [])
            if defs:
                d0 = defs[0]
                lines.append(f"• *({pos})* {d0.get('definition', '')}")
                ex = d0.get("example")
                if ex:
                    lines.append(f"  *Example:* \"{ex}\"")
            for s in m.get("synonyms", [])[:4]:
                if s not in all_syns:
                    all_syns.append(s)

        if all_syns:
            lines.append(f"• **Synonyms:** {', '.join(all_syns[:6])}")

        return {
            "question": f"Define {clean} meaning of {clean}",
            "answer": "\n".join(lines),
            "category": "English",
            "tags": f"define meaning dictionary {clean} {' '.join(all_syns[:5])}",
            "source_label": "Free Dictionary API",
        }
    except Exception:
        return None


def fetch_wikipedia_summary(topic: str) -> Optional[Dict[str, str]]:
    clean_topic = re.sub(
        r"^(?:what\s+is|who\s+is|explain|tell\s+me\s+about|define|describe)\s+",
        "",
        topic.strip(),
        flags=re.IGNORECASE,
    ).strip(" ?.!\"'")
    if not clean_topic:
        return None

    # 1. Direct summary lookup
    slug = urllib.parse.quote(clean_topic.replace(" ", "_"))
    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}"
    data: Optional[Dict[str, Any]] = None
    try:
        cand = _http_get_json(summary_url)
        if isinstance(cand, dict) and cand.get("extract") and cand.get("type") != "disambiguation":
            data = cand
    except Exception:
        data = None

    # 2. Fallback to MediaWiki search if direct slug didn't match
    if data is None:
        search_url = (
            "https://en.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={urllib.parse.quote(clean_topic)}&srlimit=1&format=json&utf8=1"
        )
        try:
            s_res = _http_get_json(search_url)
            hits = s_res.get("query", {}).get("search", [])
            if hits:
                best_title = hits[0]["title"]
                slug2 = urllib.parse.quote(best_title.replace(" ", "_"))
                cand2 = _http_get_json(f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug2}")
                if isinstance(cand2, dict) and cand2.get("extract"):
                    data = cand2
        except Exception:
            data = None

    if not data:
        return None

    title = data.get("title", clean_topic)
    extract = data.get("extract", "").strip()
    desc = data.get("description", "").strip()
    if not extract:
        return None

    header = f"**{title}**" + (f" *({desc})*" if desc else "")
    answer = f"{header}\n{extract}\n\n*Cached online from Wikipedia for offline use.*"
    category = _infer_category(f"{title} {desc} {extract}")
    tags = f"{clean_topic.lower()} {title.lower()} wikipedia cached"

    return {
        "question": f"What is {title}? ({clean_topic})",
        "answer": answer,
        "category": category,
        "tags": tags,
        "source_label": "Wikipedia",
    }


def gather_topic_online(query: str) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
    """
    Fetch either an English Dictionary entry or a Wikipedia summary for the given query.
    Returns (entry_dict, error_message).
    """
    ql = query.lower().strip().rstrip("?.!")
    dict_match = re.match(
        r"^(?:define|definition\s+of|meaning\s+of|synonym(?:s)?\s+(?:of|for))\s+([a-zA-Z\-]+)$",
        ql,
    )
    if dict_match:
        word = dict_match.group(1)
        res = fetch_english_dictionary(word)
        if res:
            return res, None

    # Single English lowercase word -> try Dictionary first, then Wikipedia
    if re.fullmatch(r"[a-z]{3,20}", ql):
        res = fetch_english_dictionary(ql)
        if res:
            return res, None

    wiki = fetch_wikipedia_summary(query)
    if wiki:
        return wiki, None

    return None, "No matching online summary found (check internet connection or try a clearer topic name)."


CURATED_STUDY_PACKS: Dict[str, List[str]] = {
    "Horticulture Pack": [
        "Photosynthesis",
        "Coffea arabica",
        "Integrated pest management",
        "Drip irrigation",
        "Soil pH",
    ],
    "Computer Science Pack": [
        "Dynamic programming",
        "Public-key cryptography",
        "SQL",
        "Virtual memory",
        "Transmission Control Protocol",
    ],
    "English Vocabulary Pack": [
        "define eloquent",
        "define ubiquitous",
        "define resilience",
        "define meticulous",
        "define catalyst",
    ],
}
