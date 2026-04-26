"""Evidence IDs, manifests, and absence summaries."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from sermon_insight_wiki.config import EVIDENCE_MANIFEST_PATH


@dataclass
class AbsenceReport:
    """What the corpus did not support well enough."""

    query_terms_checked: List[str] = field(default_factory=list)
    sermons_touched: List[str] = field(default_factory=list)
    max_similarity_per_sermon: Dict[str, float] = field(default_factory=dict)
    global_max_similarity: float = 0.0
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_terms_checked": self.query_terms_checked,
            "sermons_touched": self.sermons_touched,
            "max_similarity_per_sermon": self.max_similarity_per_sermon,
            "global_max_similarity": self.global_max_similarity,
            "notes": self.notes,
        }


def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z]{3,}", text.lower())]


def build_absence_report(
    query: str,
    retrieval_hits: List[Dict[str, Any]],
    similarity_floor: float = 0.25,
) -> AbsenceReport:
    terms = tokenize(query)[:12]
    per_vid: Dict[str, float] = {}
    touched: Set[str] = set()
    for h in retrieval_hits:
        vid = h.get("video_id", "")
        touched.add(vid)
        sim = float(h.get("similarity", h.get("rrf_score", 0.0)))
        per_vid[vid] = max(per_vid.get(vid, 0.0), sim)
    gmax = max((float(h.get("similarity", 0.0)) for h in retrieval_hits), default=0.0)
    notes = []
    if gmax < similarity_floor:
        notes.append(
            f"No chunk exceeded similarity floor {similarity_floor} (best ~{gmax:.3f})."
        )
    return AbsenceReport(
        query_terms_checked=terms,
        sermons_touched=sorted(touched),
        max_similarity_per_sermon=per_vid,
        global_max_similarity=gmax,
        notes=" ".join(notes),
    )


def load_manifest(path: Optional[Path] = None) -> Dict[str, Any]:
    p = path or EVIDENCE_MANIFEST_PATH
    if not p.exists():
        return {"version": 1, "claims": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "claims": []}


def save_manifest(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    p = path or EVIDENCE_MANIFEST_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def append_claims(
    video_id: str,
    claims: List[Dict[str, Any]],
    path: Optional[Path] = None,
) -> None:
    """claims: list of {text, evidence_ids: [...]} ."""
    m = load_manifest(path)
    lst = m.setdefault("claims", [])
    for c in claims:
        lst.append({"video_id": video_id, **c})
    save_manifest(m, path)
