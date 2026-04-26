"""Detect scripture references in text and attach parallel translation passages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple

from sermon_insight_wiki.bible_books import CANONICAL, REF_RE, book_number_from_name
from sermon_insight_wiki.bible_xml import BibleXmlLibrary, default_library
from sermon_insight_wiki.config import (
    SIW_BIBLE_TRANSLATIONS,
    SIW_SCRIPTURE_ENABLED,
    SIW_SCRIPTURE_MAX_REFS,
    SIW_SCRIPTURE_MAX_VERSES_PER_RANGE,
    load_env,
)

load_env()


@dataclass(frozen=True)
class ScriptureRef:
    book_num: int
    chapter: int
    verse_lo: int
    verse_hi: int
    label: str


def extract_scripture_refs(text: str, max_refs: int | None = None) -> List[ScriptureRef]:
    if not text:
        return []
    cap = max_refs if max_refs is not None else SIW_SCRIPTURE_MAX_REFS
    seen: set[Tuple[int, int, int, int]] = set()
    out: List[ScriptureRef] = []
    for m in REF_RE.finditer(text):
        bk = m.group("bk")
        ch = int(m.group("ch"))
        v1 = int(m.group("v"))
        v2 = int(m.group("v2") or v1)
        num = book_number_from_name(bk)
        if num is None:
            continue
        lo, hi = sorted((v1, v2))
        key = (num, ch, lo, hi)
        if key in seen:
            continue
        seen.add(key)
        nm = CANONICAL[num - 1]
        label = f"{nm} {ch}:{lo}" + (f"–{hi}" if hi != lo else "")
        out.append(ScriptureRef(book_num=num, chapter=ch, verse_lo=lo, verse_hi=hi, label=label))
        if len(out) >= cap:
            break
    return out


def build_scripture_context_block(
    *text_sources: str,
    library: BibleXmlLibrary | None = None,
    translations: Sequence[str] | None = None,
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Returns (markdown_block, citation_metadata) for LLM prompts.
    Empty string if disabled or no XML / no refs found.
    """
    if not SIW_SCRIPTURE_ENABLED:
        return "", []

    lib = library or default_library()
    trans = list(translations) if translations is not None else list(SIW_BIBLE_TRANSLATIONS)
    trans = [t for t in trans if t in lib.files]
    trans = [t for t in trans if t in lib.available_translations()]
    if not trans:
        return "", []

    blob = "\n\n".join(s for s in text_sources if s)
    refs = extract_scripture_refs(blob)
    if not refs:
        return "", []

    sections: List[str] = []
    meta: List[Dict[str, Any]] = []
    for r in refs:
        parts = [f"### {r.label} ({', '.join(trans)})"]
        for t in trans:
            body = lib.fetch_range(
                t,
                r.book_num,
                r.chapter,
                r.verse_lo,
                r.verse_hi,
                max_verses=SIW_SCRIPTURE_MAX_VERSES_PER_RANGE,
            )
            if body:
                parts.append(f"**{t}**\n{body}")
        block = "\n\n".join(parts)
        sections.append(block)
        meta.append(
            {
                "label": r.label,
                "book": CANONICAL[r.book_num - 1],
                "chapter": r.chapter,
                "verse_lo": r.verse_lo,
                "verse_hi": r.verse_hi,
                "translations": trans,
            }
        )

    intro = (
        "The following scripture passages were detected in the sermon/question text. "
        "Use them to compare wording and narrative context with the sermon. "
        "Always name which translation each phrase comes from."
    )
    return intro + "\n\n" + "\n\n---\n\n".join(sections), meta
