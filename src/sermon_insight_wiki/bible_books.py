"""Protestant 66-book numbering (Beblia XML `book/@number` = 1..66) and name resolution."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# index = book number 1..66
CANONICAL: List[str] = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]


def _norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("first", "1").replace("second", "2").replace("third", "3")
    s = s.replace("i ", "1 ").replace("ii ", "2 ").replace("iii ", "3 ")
    return s


def _build_lookup_data() -> Tuple[Dict[str, int], List[str]]:
    lu: Dict[str, int] = {}
    tokens: set[str] = set()
    for i, name in enumerate(CANONICAL, start=1):
        variants = {
            name,
            name.replace(" ", ""),
            name.replace("1 ", "1").replace("2 ", "2").replace("3 ", "3"),
        }
        if name == "Song of Solomon":
            variants.update({"Song of Songs", "Canticles", "SOS"})
        if name == "Psalms":
            variants.update({"Psalm", "Ps"})
        if name == "1 Samuel":
            variants.update({"1 Sam", "I Samuel"})
        if name == "2 Samuel":
            variants.update({"2 Sam", "II Samuel"})
        if name == "1 Kings":
            variants.update({"1 Kgs", "I Kings"})
        if name == "2 Kings":
            variants.update({"2 Kgs", "II Kings"})
        if name == "1 Chronicles":
            variants.update({"1 Chr", "I Chronicles"})
        if name == "2 Chronicles":
            variants.update({"2 Chr", "II Chronicles"})
        if name == "1 Corinthians":
            variants.update({"1 Cor", "I Corinthians"})
        if name == "2 Corinthians":
            variants.update({"2 Cor", "II Corinthians"})
        if name == "1 Thessalonians":
            variants.update({"1 Thess", "I Thessalonians"})
        if name == "2 Thessalonians":
            variants.update({"2 Thess", "II Thessalonians"})
        if name == "1 Timothy":
            variants.update({"1 Tim", "I Timothy"})
        if name == "2 Timothy":
            variants.update({"2 Tim", "II Timothy"})
        if name == "1 Peter":
            variants.update({"1 Pet", "I Peter"})
        if name == "2 Peter":
            variants.update({"2 Pet", "II Peter"})
        if name == "1 John":
            variants.update({"1 Jn", "I John"})
        if name == "2 John":
            variants.update({"2 Jn", "II John"})
        if name == "3 John":
            variants.update({"3 Jn", "III John"})
        if name == "Philippians":
            variants.add("Phil")
        if name == "Philemon":
            variants.add("Phlm")
        if name == "Colossians":
            variants.add("Col")
        if name == "Genesis":
            variants.add("Gen")
        if name == "Exodus":
            variants.add("Ex")
        if name == "Leviticus":
            variants.add("Lev")
        if name == "Numbers":
            variants.add("Num")
        if name == "Deuteronomy":
            variants.add("Deut")
        if name == "Joshua":
            variants.add("Josh")
        if name == "Judges":
            variants.add("Judg")
        if name == "Matthew":
            variants.add("Matt")
        if name == "Mark":
            variants.add("Mk")
        if name == "Luke":
            variants.update({"Luk", "Lk"})
        if name == "John":
            variants.add("Jn")
        if name == "Romans":
            variants.add("Rom")
        if name == "Galatians":
            variants.add("Gal")
        if name == "Ephesians":
            variants.add("Eph")
        if name == "Hebrews":
            variants.add("Heb")
        if name == "James":
            variants.add("Jas")
        if name == "Jude":
            pass
        if name == "Revelation":
            variants.update({"Rev", "Apocalypse"})
        for v in variants:
            lu[_norm(v)] = i
            tokens.add(v)
    ordered = sorted(tokens, key=len, reverse=True)
    return lu, ordered


BOOK_LOOKUP, _REGEX_TOKENS = _build_lookup_data()


def book_number_from_name(fragment: str) -> Optional[int]:
    """Resolve a matched book substring (e.g. '1 Cor', 'Genesis') to 1..66."""
    key = _norm(fragment)
    if key in BOOK_LOOKUP:
        return BOOK_LOOKUP[key]
    key2 = _norm(re.sub(r"[\.,;]", "", fragment))
    if key2 in BOOK_LOOKUP:
        return BOOK_LOOKUP[key2]
    return None


def build_reference_regex() -> re.Pattern[str]:
    """Longest-match tokens first (e.g. 1 John before John)."""
    parts: List[str] = []
    for name in _REGEX_TOKENS:
        flex = r"\s+".join(re.escape(t) for t in name.split())
        parts.append(flex)
    book_alt = "|".join(parts)
    # Optional leading number for books like "1 John" already in name; also allow "First John" via lookup only if we add - we added in _norm variants not in regex
    # Allow optional period after abbrev tokens (e.g. "Gen.")
    return re.compile(
        rf"\b(?P<bk>{book_alt})\.?\s+(?P<ch>\d{{1,3}}):(?P<v>\d{{1,3}})(?:\s*[-–]\s*(?P<v2>\d{{1,3}}))?",
        re.IGNORECASE,
    )


REF_RE = build_reference_regex()
