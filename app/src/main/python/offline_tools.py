"""
Offline intelligence utilities for Maya:
1. Conversational & Common English Engine (greetings, farewells, small talk, polite phrases, encouragement)
2. Offline Extractive TextRank/TF-IDF Summarizer & Keyword Extractor (pure NumPy)
3. Built-in Offline English Dictionary & Synonym/Antonym Helper
4. Offline Study Quiz & Flashcard Generator backed by SQLite
"""

from __future__ import annotations

import difflib
import math
import random
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


# --- 1. Conversational & Common English Patterns ---

_GREETING_EXACT: Dict[str, Tuple[str, str]] = {
    "hi": (
        "Hi there! I'm **Maya**, your offline-capable assistant. How can I help you today with English, Math, Horticulture, or Computer Science?",
        "Greeting",
    ),
    "hello": (
        "Hello! Welcome back. Ask Maya any question, run a calculation, summarize notes, or teach me something new!",
        "Greeting",
    ),
    "hey": (
        "Hey! Maya is ready. What would you like to explore or calculate today?",
        "Greeting",
    ),
    "selam": (
        "Selam! I'm **Maya**. Ask me anything in English, Math, Horticulture, or Computer Science—completely offline!",
        "Greeting",
    ),
    "selam new": (
        "Selam new! Egziabher yimesgen, dehna negn. How can I assist you today?",
        "Greeting",
    ),
    "tena yistilign": (
        "Tena yistilign! Wishing you health and focus today. What would you like to learn with Maya?",
        "Greeting",
    ),
    "good morning": (
        "Good morning! Fresh mind, fresh knowledge. What are we studying or solving today?",
        "Greeting",
    ),
    "endemin aderk": (
        "Egziabher yimesgen, dehna aderk! Good morning—what can Maya help you with today?",
        "Greeting",
    ),
    "endemin adersh": (
        "Egziabher yimesgen, dehna adersh! Good morning—what can Maya help you with today?",
        "Greeting",
    ),
    "good afternoon": (
        "Good afternoon! Hope your day is going well. Ask Maya anything or try a quick calculation.",
        "Greeting",
    ),
    "endemin walk": (
        "Egziabher yimesgen, dehna walk! Good afternoon—how can Maya support your work?",
        "Greeting",
    ),
    "endemin walsh": (
        "Egziabher yimesgen, dehna walsh! Good afternoon—how can Maya support your work?",
        "Greeting",
    ),
    "good evening": (
        "Good evening! Ready for an evening study session or quick answers?",
        "Greeting",
    ),
    "good night": (
        "Good night! Rest well—all the knowledge you taught Maya stays safely stored in SQLite for tomorrow.",
        "Farewell",
    ),
    "how are you": (
        "I'm doing great and running smoothly right on your device! How are you doing today?",
        "Small Talk",
    ),
    "how r u": (
        "I'm doing great, thanks for asking! How are you, and what can we tackle together?",
        "Small Talk",
    ),
    "hows it going": (
        "Everything is running fast and sharp! How is your day going?",
        "Small Talk",
    ),
    "whats up": (
        "All systems online in my local brain! Ask me a question, paste text with `summarize: ...`, or try `quiz me`.",
        "Small Talk",
    ),
    "endemin neh": (
        "Egziabher yimesgen, dehna negn! How are you doing today?",
        "Greeting",
    ),
    "endemin nesh": (
        "Egziabher yimesgen, dehna negn! How are you doing today?",
        "Greeting",
    ),
    "dehna neh": (
        "Dehna negn, ameseginalehu! What can Maya help you with?",
        "Greeting",
    ),
    "nice to meet you": (
        "Nice to meet you too! I'm Maya—an assistant that works offline and remembers everything you teach me.",
        "Polite",
    ),
    "thank you": (
        "You're very welcome! Anytime you want to save a custom note or fix an answer, just tap **Teach Maya**.",
        "Polite",
    ),
    "thanks": (
        "You're welcome! Happy to help.",
        "Polite",
    ),
    "thank u": (
        "You're welcome! Let me know what's next.",
        "Polite",
    ),
    "ameseginalehu": (
        "Menim aydel! You're always welcome.",
        "Polite",
    ),
    "sorry": (
        "No problem at all! Take your time and ask whenever you're ready.",
        "Polite",
    ),
    "excuse me": (
        "Yes, how can Maya help you?",
        "Polite",
    ),
    "bye": (
        "Goodbye! Keep learning and come back anytime—your offline SQLite knowledge is always here.",
        "Farewell",
    ),
    "goodbye": (
        "Goodbye! Wishing you a productive day ahead.",
        "Farewell",
    ),
    "see you": (
        "See you soon! Have a great day.",
        "Farewell",
    ),
    "see you later": (
        "See you later! Stay curious.",
        "Farewell",
    ),
    "chaw": (
        "Chaw! Dehna hun/huni—see you next time.",
        "Farewell",
    ),
    "ok": (
        "Got it! Let me know your next question or command.",
        "Conversational",
    ),
    "okay": (
        "Sounds good! What would you like to do next?",
        "Conversational",
    ),
    "yes": (
        "Great! Go ahead and type your question or topic.",
        "Conversational",
    ),
    "no": (
        "Alright, no problem! Let me know if you need anything else.",
        "Conversational",
    ),
    "good job": (
        "Thank you! Feel free to tap **Helpful (+Boost)** on great answers so I prioritize them even better.",
        "Feedback",
    ),
    "well done": (
        "Thank you! Maya gets sharper every time you reinforce or teach new knowledge.",
        "Feedback",
    ),
    "i am tired": (
        "Take a 10-minute break, drink some water, and stretch! When you return, try a 25-minute Pomodoro block—slow steady progress wins.",
        "Motivation",
    ),
    "im tired": (
        "Rest is part of learning too. Step away for a few minutes, breathe deeply, and come back refreshed.",
        "Motivation",
    ),
    "motivate me": (
        "Every expert was once a beginner who refused to quit. One concept, one formula, one small step today compounds into mastery tomorrow!",
        "Motivation",
    ),
    "tell me a joke": (
        "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛💻",
        "Fun",
    ),
    "what is your name": (
        "My name is **Maya**! I am your offline-first, self-learning AI assistant for English, Math, Horticulture, and Computer Science.",
        "Identity",
    ),
    "who are you": (
        "I am **Maya**, an offline-capable, self-learning AI built without cloud LLMs or neural networks. "
        "I use an AST math engine, a hybrid NumPy TF-IDF + fuzzy brain, an offline summarizer & quiz engine, and—when you're online—I can gather Wikipedia & Dictionary knowledge into SQLite for future offline use.",
        "Identity",
    ),
    "help": (
        "**What Maya Can Do Offline & Online:**\n"
        "• **Everyday English:** Greetings, definitions (`define resilience`), synonyms (`synonym of abundant`), grammar & writing tips.\n"
        "• **Summarizer:** Paste text as `summarize: <paragraph>` for instant offline key bullet points.\n"
        "• **Study Quiz:** Type `quiz me` or `quiz horticulture` / `quiz computer science`.\n"
        "• **Math & Domain Calcs:** `solve 2x^2 - 5x + 2 = 0`, `matrix [[2,1],[5,3]]`, `fertilizer urea 100 kg/ha 2 timad`, `subnet 192.168.1.0/26`.\n"
        "• **Online → Offline Sync:** Tap the cloud-download icon to cache Wikipedia & Dictionary topics for offline study!",
        "Help",
    ),
}

_GREETING_PREFIXES = (
    "hello maya", "hi maya", "hey maya", "selam maya",
    "good morning maya", "good afternoon maya", "good evening maya",
    "how are you maya", "thank you maya", "thanks maya", "bye maya",
)


def try_conversational_intent(query: str) -> Optional[Dict[str, Any]]:
    norm = re.sub(r"[^\w\s]", "", query.lower()).strip()
    norm = re.sub(r"\s+", " ", norm)

    # Strip trailing "maya" or leading "maya"
    stripped = re.sub(r"^(?:maya\s+)|(?:\s+maya)$", "", norm).strip()

    for candidate in (norm, stripped):
        if candidate in _GREETING_EXACT:
            ans, tag = _GREETING_EXACT[candidate]
            return {
                "answer": ans,
                "confidence": 1.0,
                "route": "conversational",
                "category": "General",
                "matched_id": None,
                "matched_question": None,
                "needs_teaching": False,
                "closest_guess": None,
                "formula_steps": "",
                "tag": tag,
            }

    # Natural phrase starts (e.g., "hello my friend", "good morning everyone")
    for prefix in ("good morning", "good afternoon", "good evening", "hello ", "hi ", "hey ", "selam ", "thank you ", "thanks "):
        if stripped.startswith(prefix) and len(stripped.split()) <= 5:
            base = prefix.strip()
            if base in _GREETING_EXACT:
                ans, tag = _GREETING_EXACT[base]
                return {
                    "answer": ans,
                    "confidence": 0.96,
                    "route": "conversational",
                    "category": "General",
                    "matched_id": None,
                    "matched_question": None,
                    "needs_teaching": False,
                    "closest_guess": None,
                    "formula_steps": "",
                    "tag": tag,
                }

    # Date / time awareness
    if any(
        p in norm
        for p in (
            "what time is it", "current time", "what is the time", "whats the time",
            "todays date", "what is the date", "whats the date", "what day is today", "current date",
        )
    ):
        now = datetime.now()
        return {
            "answer": (
                f"**Local Device Date & Time**\n"
                f"• Date: {now.strftime('%A, %B %d, %Y')}\n"
                f"• Time: {now.strftime('%I:%M %p (%H:%M:%S)')}"
            ),
            "confidence": 1.0,
            "route": "datetime",
            "category": "General",
            "matched_id": None,
            "matched_question": None,
            "needs_teaching": False,
            "closest_guess": None,
            "formula_steps": "",
            "tag": "System Clock",
        }

    return None


# --- 2. Built-in Offline English Dictionary & Thesaurus ---

_MINI_DICTIONARY: Dict[str, Dict[str, Any]] = {
    "resilience": {
        "pos": "noun",
        "def": "The capacity to recover quickly from difficulties, stress, or adversity; toughness.",
        "syn": ["toughness", "adaptability", "strength", "flexibility"],
        "ant": ["fragility", "weakness"],
        "ex": "Enset shows remarkable resilience during highland droughts.",
    },
    "abundant": {
        "pos": "adjective",
        "def": "Existing or available in large quantities; plentiful.",
        "syn": ["plentiful", "ample", "copious", "rich"],
        "ant": ["scarce", "rare", "insufficient"],
        "ex": "Ethiopia's southwestern forests support abundant wild Arabica coffee.",
    },
    "ubiquitous": {
        "pos": "adjective",
        "def": "Present, appearing, or found everywhere at the same time.",
        "syn": ["omnipresent", "pervasive", "universal"],
        "ant": ["rare", "scarce"],
        "ex": "SQLite is ubiquitous in mobile phones and embedded systems.",
    },
    "pragmatic": {
        "pos": "adjective",
        "def": "Dealing with things sensibly and realistically in a practical way rather than purely theoretically.",
        "syn": ["practical", "realistic", "sensible"],
        "ant": ["idealistic", "impractical"],
        "ex": "Integrated Pest Management takes a pragmatic approach to crop protection.",
    },
    "concise": {
        "pos": "adjective",
        "def": "Giving a lot of information clearly and in a few words; brief but comprehensive.",
        "syn": ["brief", "succinct", "compact", "terse"],
        "ant": ["verbose", "wordy", "lengthy"],
        "ex": "Write concise variable names and clear documentation.",
    },
    "hypothesis": {
        "pos": "noun",
        "def": "A proposed, testable explanation made on the basis of limited evidence as a starting point for investigation.",
        "syn": ["theory", "proposition", "assumption"],
        "ant": ["fact", "proof"],
        "ex": "Our null hypothesis states that fertilizer treatments produce equal yields.",
    },
    "mitigate": {
        "pos": "verb",
        "def": "To make something less severe, harmful, or painful.",
        "syn": ["alleviate", "reduce", "lessen", "ease"],
        "ant": ["aggravate", "worsen", "intensify"],
        "ex": "Shade trees help mitigate heat stress in coffee orchards.",
    },
    "sustainable": {
        "pos": "adjective",
        "def": "Able to be maintained at a certain rate or level without depleting natural resources or causing ecological damage.",
        "syn": ["maintainable", "viable", "eco-friendly"],
        "ant": ["unsustainable", "destructive"],
        "ex": "Crop rotation supports sustainable soil fertility.",
    },
    "ambiguous": {
        "pos": "adjective",
        "def": "Open to more than one interpretation; unclear or inexact.",
        "syn": ["vague", "unclear", "equivocal"],
        "ant": ["clear", "explicit", "unambiguous"],
        "ex": "Avoid ambiguous requirements in software engineering specifications.",
    },
    "deterministic": {
        "pos": "adjective",
        "def": "Producing the exact same output every time for a given input, with no randomness.",
        "syn": ["predictable", "exact", "repeatable"],
        "ant": ["random", "stochastic", "probabilistic"],
        "ex": "Maya's AST math engine is 100% deterministic.",
    },
    "redundant": {
        "pos": "adjective",
        "def": "Not or no longer needed or useful; duplicated unnecessarily (or duplicated intentionally for fault tolerance).",
        "syn": ["superfluous", "unnecessary", "excess"],
        "ant": ["essential", "necessary"],
        "ex": "Database normalization eliminates redundant data across tables.",
    },
    "optimize": {
        "pos": "verb",
        "def": "To make the best or most effective use of a situation, resource, or algorithm.",
        "syn": ["improve", "refine", "streamline", "maximize"],
        "ant": ["degrade", "worsen"],
        "ex": "Use an index to optimize slow SQL queries.",
    },
    "coherent": {
        "pos": "adjective",
        "def": "Logical, consistent, and clearly connected as a unified whole.",
        "syn": ["logical", "clear", "consistent"],
        "ant": ["incoherent", "disjointed", "confusing"],
        "ex": "Present a coherent argument in your thesis introduction.",
    },
    "empathy": {
        "pos": "noun",
        "def": "The ability to understand and share the feelings or perspective of another person.",
        "syn": ["compassion", "understanding", "sensitivity"],
        "ant": ["apathy", "indifference"],
        "ex": "User-centered design begins with empathy for the user.",
    },
    "perseverance": {
        "pos": "noun",
        "def": "Persistence in doing something despite difficulty or delay in achieving success.",
        "syn": ["persistence", "determination", "tenacity"],
        "ant": ["quitting", "laziness"],
        "ex": "Mastering algorithms takes steady practice and perseverance.",
    },
    "paradigm": {
        "pos": "noun",
        "def": "A typical example, pattern, or distinct framework of thought or programming.",
        "syn": ["model", "pattern", "framework"],
        "ant": ["anomaly"],
        "ex": "Object-Oriented Programming and Functional Programming are major paradigms.",
    },
    "synthesize": {
        "pos": "verb",
        "def": "To combine multiple ideas, parts, or elements into a coherent whole.",
        "syn": ["combine", "integrate", "merge"],
        "ant": ["separate", "dissect"],
        "ex": "Good research papers synthesize findings from multiple studies.",
    },
    "ephemeral": {
        "pos": "adjective",
        "def": "Lasting for a very short time.",
        "syn": ["transient", "fleeting", "short-lived"],
        "ant": ["permanent", "eternal"],
        "ex": "TLS uses ephemeral session keys for forward secrecy.",
    },
    "heuristic": {
        "pos": "noun",
        "def": "A practical problem-solving shortcut or rule of thumb that is fast and sufficient for immediate goals.",
        "syn": ["rule of thumb", "shortcut", "approximation"],
        "ant": ["exact proof"],
        "ex": "Stemming is a lightweight heuristic for matching word variations.",
    },
    "germinate": {
        "pos": "verb",
        "def": "To begin to grow and put out shoots after a period of dormancy (of a seed or spore).",
        "syn": ["sprout", "bud", "develop"],
        "ant": ["wither", "decay"],
        "ex": "Fresh coffee seeds germinate best within 4–6 weeks in moist sand beds.",
    },
    "chlorosis": {
        "pos": "noun",
        "def": "Yellowing of normally green plant tissue caused by insufficient chlorophyll, often due to nitrogen or iron deficiency.",
        "syn": ["yellowing", "bleaching"],
        "ant": ["verdancy"],
        "ex": "Interveinal chlorosis on young leaves often indicates iron or zinc deficiency.",
    },
    "fertile": {
        "pos": "adjective",
        "def": "Capable of producing abundant vegetation, crops, or creative ideas.",
        "syn": ["productive", "rich", "fruitful"],
        "ant": ["barren", "infertile", "sterile"],
        "ex": "Volcanic Nitisols in Ethiopia are deep and fertile for highland crops.",
    },
}


def try_offline_dictionary(query: str) -> Optional[Dict[str, Any]]:
    ql = query.lower().strip().rstrip("?.!")
    m = re.match(
        r"^(?:define|definition\s+of|meaning\s+of|what\s+does|synonym(?:s)?\s+(?:of|for)|antonym(?:s)?\s+(?:of|for))\s+([a-z\-]+)(?:\s+mean)?$",
        ql,
    )
    if not m:
        return None
    word = m.group(1).strip()
    if word in _MINI_DICTIONARY:
        entry = _MINI_DICTIONARY[word]
        syns = ", ".join(entry["syn"])
        ants = ", ".join(entry["ant"])
        answer = (
            f"**{word.capitalize()}** *({entry['pos']})*\n"
            f"• **Meaning:** {entry['def']}\n"
            f"• **Synonyms:** {syns}\n"
            f"• **Antonyms:** {ants}\n"
            f"• **Example:** *\"{entry['ex']}\"*"
        )
        return {
            "answer": answer,
            "confidence": 0.98,
            "route": "dictionary",
            "category": "English",
            "matched_id": None,
            "matched_question": None,
            "needs_teaching": False,
            "closest_guess": None,
            "formula_steps": "Offline Core English Lexicon",
            "tag": "English Dictionary",
        }
    return None


# --- 3. Offline Extractive Text Summarizer & Keyword Extractor (NumPy TF-IDF) ---

_SUMM_STOP = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "to", "of",
    "and", "or", "in", "on", "at", "for", "with", "by", "from", "as", "that", "this",
    "it", "its", "which", "who", "whom", "their", "they", "them", "we", "our", "you",
    "your", "he", "she", "his", "her", "but", "not", "can", "will", "would", "have",
    "has", "had", "do", "does", "did", "into", "about", "than", "then", "also",
}


def try_offline_summarizer(query: str) -> Optional[Dict[str, Any]]:
    m = re.match(r"^(?:summarize|summarise|summary|tldr|tl;dr|key\s*points?)\s*[:\-]\s*(.+)$", query.strip(), re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    text = m.group(1).strip()
    if len(text.split()) < 15:
        return {
            "answer": "Please provide a longer paragraph (at least 15 words) after `summarize:` so Maya can extract the key sentences and keywords.",
            "confidence": 1.0,
            "route": "summarizer",
            "category": "English",
            "matched_id": None,
            "matched_question": None,
            "needs_teaching": False,
            "closest_guess": None,
            "formula_steps": "",
            "tag": "Offline Summarizer",
        }

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 10]
    if len(sentences) <= 2:
        words = re.findall(r"[a-zA-Z]{3,}", text.lower())
        top_kw = [w for w, _ in Counter(w for w in words if w not in _SUMM_STOP).most_common(5)]
        return {
            "answer": (
                f"**Offline Summary**\n• {text}\n\n"
                f"**Key Terms:** {', '.join(top_kw)}"
            ),
            "confidence": 1.0,
            "route": "summarizer",
            "category": "English",
            "matched_id": None,
            "matched_question": None,
            "needs_teaching": False,
            "closest_guess": None,
            "formula_steps": "Extractive TF-IDF Sentence Scorer",
            "tag": "Offline Summarizer",
        }

    # Build sentence-term TF-IDF matrix in NumPy
    sent_tokens: List[List[str]] = []
    df: Counter[str] = Counter()
    for sent in sentences:
        toks = [w for w in re.findall(r"[a-zA-Z0-9]{2,}", sent.lower()) if w not in _SUMM_STOP]
        sent_tokens.append(toks)
        for u in set(toks):
            df[u] += 1

    vocab = {w: i for i, w in enumerate(sorted(df.keys()))}
    n_s = len(sentences)
    n_v = len(vocab)
    if n_v == 0:
        return None

    mat = np.zeros((n_s, n_v), dtype=np.float64)
    for r, toks in enumerate(sent_tokens):
        counts = Counter(toks)
        for w, c in counts.items():
            idf = math.log((1.0 + n_s) / (1.0 + df[w])) + 1.0
            mat[r, vocab[w]] = (1.0 + math.log(c)) * idf

    # Score sentences by TF-IDF energy + centrality (cosine similarity to centroid) + lead position bonus
    centroid = mat.mean(axis=0)
    c_norm = np.linalg.norm(centroid) or 1.0
    scores: List[Tuple[int, float]] = []
    for idx in range(n_s):
        row = mat[idx]
        r_norm = np.linalg.norm(row) or 1.0
        centrality = float(np.dot(row, centroid) / (r_norm * c_norm))
        pos_bonus = 0.12 if idx == 0 else (0.05 if idx == n_s - 1 else 0.0)
        scores.append((idx, centrality + pos_bonus))

    k = min(3, max(2, n_s // 2))
    top_indices = sorted([idx for idx, _ in sorted(scores, key=lambda x: x[1], reverse=True)[:k]])
    bullets = "\n".join(f"• {sentences[i]}" for i in top_indices)

    all_toks = [t for sub in sent_tokens for t in sub]
    top_keywords = [w for w, _ in Counter(all_toks).most_common(6)]
    word_count = len(text.split())
    read_sec = max(5, int(round(word_count / 3.3)))

    answer = (
        f"**Offline Extractive Summary** *({word_count} words → {k} key points, ~{read_sec}s read)*\n"
        f"{bullets}\n\n"
        f"**Top Keywords:** {', '.join(top_keywords)}"
    )
    return {
        "answer": answer,
        "confidence": 1.0,
        "route": "summarizer",
        "category": "English",
        "matched_id": None,
        "matched_question": None,
        "needs_teaching": False,
        "closest_guess": None,
        "formula_steps": f"NumPy TF-IDF sentence centrality across {n_s} sentences",
        "tag": "Offline Summarizer",
    }


# --- 4. Offline Study Quiz / Flashcard Generator ---

def try_study_quiz(query: str, memory: Any) -> Optional[Dict[str, Any]]:
    ql = query.lower().strip()
    if not re.search(r"\b(quiz|flashcard|test me)\b", ql):
        return None

    cat = "All"
    if "horticulture" in ql or "coffee" in ql or "plant" in ql:
        cat = "Horticulture"
    elif "cs" in ql or "computer" in ql or "network" in ql or "sql" in ql:
        cat = "Computer Science"
    elif "english" in ql or "grammar" in ql:
        cat = "English"

    entry = memory.get_random_quiz_entry(cat)
    if not entry:
        return None

    # Create an active-recall prompt with a helpful hint
    ans_lines = [line.strip() for line in entry["answer"].splitlines() if line.strip()]
    hint_words = [w for w in re.findall(r"[A-Za-z0-9]{4,}", ans_lines[0])[:4]]
    hint = ", ".join(hint_words) if hint_words else entry["category"]

    answer = (
        f"**Offline Study Flashcard ({entry['category']})**\n\n"
        f"**Question:** {entry['question']}\n\n"
        f"**Recall Hint:** `{hint}`\n\n"
        f"**Full Answer:**\n{entry['answer']}\n\n"
        f"*Tip: Type `quiz {entry['category'].lower()}` again for another card!*"
    )
    return {
        "answer": answer,
        "confidence": 1.0,
        "route": "quiz",
        "category": entry["category"],
        "matched_id": int(entry["id"]),
        "matched_question": entry["question"],
        "needs_teaching": False,
        "closest_guess": None,
        "formula_steps": "Random active-recall sampling from SQLite knowledge base",
        "tag": "Study Quiz",
    }


def suggest_closest_spelling(word: str, vocab_terms: List[str]) -> Optional[str]:
    clean_vocab = [t for t in vocab_terms if "_" not in t and len(t) >= 3]
    matches = difflib.get_close_matches(word.lower(), clean_vocab, n=1, cutoff=0.72)
    return matches[0] if matches else None
