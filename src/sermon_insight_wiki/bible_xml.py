"""Load Beblia-style Bible XML and fetch verse ranges by global book number (1..66)."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from sermon_insight_wiki.config import BIBLES_XML_DIR, load_env

load_env()

# Short keys → filenames in data/bibles/xml/
DEFAULT_TRANSLATION_FILES: Dict[str, str] = {
    "KJV": "EnglishKJBible.xml",
    "NIV": "EnglishNIVBible.xml",
    "NKJ": "EnglishNKJBible.xml",
    "NLT": "EnglishNLTBible.xml",
}


class BibleXmlLibrary:
    """Lazy-parsed trees; book elements cached by (translation, book_number)."""

    def __init__(self, xml_dir: Optional[Path] = None, files: Optional[Dict[str, str]] = None):
        self.xml_dir = Path(xml_dir or BIBLES_XML_DIR)
        self.files = dict(files or DEFAULT_TRANSLATION_FILES)
        self._book_el: Dict[Tuple[str, int], ET.Element] = {}

    def available_translations(self) -> List[str]:
        out = []
        for key, fname in self.files.items():
            if (self.xml_dir / fname).is_file():
                out.append(key)
        return sorted(out)

    def _index_translation(self, trans: str) -> None:
        fname = self.files.get(trans)
        if not fname:
            return
        path = self.xml_dir / fname
        if not path.is_file():
            return
        root = ET.parse(path).getroot()
        for t in root.findall("testament"):
            for b in t.findall("book"):
                num = int(b.get("number", "0") or 0)
                if 1 <= num <= 66:
                    self._book_el[(trans, num)] = b

    def _book(self, trans: str, book_num: int) -> Optional[ET.Element]:
        if (trans, book_num) not in self._book_el:
            self._index_translation(trans)
        return self._book_el.get((trans, book_num))

    def fetch_range(
        self,
        trans: str,
        book_num: int,
        chapter: int,
        verse_lo: int,
        verse_hi: int,
        *,
        max_verses: int = 14,
    ) -> str:
        """Return plain text for inclusive verse range (capped)."""
        b = self._book(trans, book_num)
        if b is None:
            return ""
        ch_el = None
        for c in b.findall("chapter"):
            if int(c.get("number", 0) or 0) == chapter:
                ch_el = c
                break
        if ch_el is None:
            return ""
        lines: List[str] = []
        hi = min(verse_hi, verse_lo + max_verses - 1)
        truncated = verse_hi > hi
        for ve in ch_el.findall("verse"):
            vn = int(ve.get("number", 0) or 0)
            if verse_lo <= vn <= hi:
                txt = (ve.text or "").strip()
                lines.append(f"{vn}. {txt}")
        if truncated:
            lines.append(f"[… truncated after {max_verses} verses …]")
        return "\n".join(lines)

    def parallel_passage(
        self,
        book_num: int,
        chapter: int,
        verse_lo: int,
        verse_hi: int,
        translations: Iterable[str],
    ) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for t in translations:
            if t in self.files:
                text = self.fetch_range(t, book_num, chapter, verse_lo, verse_hi)
                if text:
                    out[t] = text
        return out


@lru_cache(maxsize=1)
def default_library() -> BibleXmlLibrary:
    return BibleXmlLibrary()
