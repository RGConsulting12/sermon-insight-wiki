"""Hybrid query: retrieval + graph-aware context + absence + counterfactual blocking."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI

from sermon_insight_wiki.config import CHAT_MODEL, SCHEMA_PATH, WIKI_DIR, load_env
from sermon_insight_wiki.evidence import build_absence_report
from sermon_insight_wiki.retrieval import hybrid_retrieve, wiki_link_closure
from sermon_insight_wiki.scripture_context import build_scripture_context_block
from sermon_insight_wiki.semantic_search import SemanticSearch

load_env()


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _select_wiki_pages(question: str, limit: int = 8) -> str:
    index = _read(WIKI_DIR / "index.md")
    if not index.strip():
        return ""
    q = question.lower()
    buf = []
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", index):
        title, href = m.group(1), m.group(2)
        if any(len(w) > 3 and w in q for w in title.lower().split()):
            p = WIKI_DIR / href
            if p.is_file():
                buf.append(f"### {href}\n{_read(p)[:4000]}")
        if len(buf) >= limit:
            break
    if not buf:
        ov = WIKI_DIR / "overview.md"
        if ov.is_file():
            buf.append(f"### overview.md\n{_read(ov)[:6000]}")
    return "\n\n".join(buf)


def run_query(
    question: str,
    *,
    semantic: Optional[SemanticSearch] = None,
    top_k: int = 10,
    save_under: Optional[str] = None,
) -> Dict[str, Any]:
    sem = semantic or SemanticSearch()
    hits = hybrid_retrieve(sem, question, top_k=top_k)
    seeds = {h["video_id"] for h in hits[:6]}
    neighbors = wiki_link_closure(sem, seeds, neighbor_chunks=1)
    by_eid = {h["evidence_id"]: h for h in hits}
    for n in neighbors:
        by_eid.setdefault(n["evidence_id"], n)
    fused = list(by_eid.values())[: top_k + len(neighbors)]

    absence = build_absence_report(question, fused)
    wiki_ctx = _select_wiki_pages(question)
    schema = _read(Path(SCHEMA_PATH))[:8000]

    evidence_block = "\n\n".join(
        f"[{h['evidence_id']}] (sim={h.get('similarity', 0):.3f}, rrf={h.get('rrf_score', 0):.4f})\n{h['text'][:900]}"
        for h in fused[:14]
    )

    chunk_blob = "\n\n".join(h["text"][:700] for h in fused[:10])
    sc_block, sc_meta = build_scripture_context_block(question, chunk_blob)
    scripture_section = (
        f"\n\n## Scripture (parallel translations)\n{sc_block}\n"
        if sc_block
        else ""
    )

    client = OpenAI()
    prompt = f"""You answer questions about a sermon corpus using evidence chunks and optional wiki pages.

Schema excerpt:
{schema}

Wiki pages (may be empty):
{wiki_ctx if wiki_ctx else "(no wiki pages matched)"}
{scripture_section}
Evidence chunks:
{evidence_block}

Question: {question}

Write JSON with keys:
- answer_markdown: full answer with ### headers, bullet points. Every factual sentence must end with a bracket citation like [videoId:chunkIndex] matching evidence ids above.
- absence_markdown: short section: what was NOT found or weakly supported in the evidence (use the similarity hints honestly).
- counterfactual_markdown: what would need to be true for the opposite conclusion; which evidence_ids BLOCK that counterfactual (contradict or fail to support), or state if absence means no blocker exists.
- blocking_analysis: one paragraph plain text summary of blocking / non-support.

When scripture passages are provided above, relate sermon claims to those passages explicitly (translation + verse).

Return ONLY valid JSON."""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.25,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.choices[0].message.content or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {
            "answer_markdown": raw,
            "absence_markdown": "",
            "counterfactual_markdown": "",
            "blocking_analysis": "",
        }

    out: Dict[str, Any] = {
        "answer_markdown": parsed.get("answer_markdown", ""),
        "absence_markdown": parsed.get("absence_markdown", ""),
        "counterfactual_markdown": parsed.get("counterfactual_markdown", ""),
        "blocking_analysis": parsed.get("blocking_analysis", ""),
        "retrieval": fused,
        "absence_report": absence.to_dict(),
        "scripture": {"refs": sc_meta, "context_included": bool(sc_block)},
    }

    if save_under:
        today = date.today().isoformat()
        rel = save_under.strip().strip("/")
        if not rel.endswith(".md"):
            rel = f"syntheses/{rel}.md"
        path = WIKI_DIR / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        fm = f"""---
title: "{question[:80].replace('"', "'")}"
type: synthesis
tags: []
sources: []
last_updated: {today}
---

"""
        body = "\n\n".join(
            [
                parsed.get("answer_markdown", ""),
                "## Absence reasoning",
                parsed.get("absence_markdown", ""),
                "## Counterfactual / blocking",
                parsed.get("counterfactual_markdown", ""),
            ]
        )
        path.write_text(fm + body, encoding="utf-8")
        idx = WIKI_DIR / "index.md"
        if idx.exists():
            content = _read(idx)
            entry = f"- [{question[:50]}]({rel}) — synthesis"
            if "## Syntheses" in content:
                content = content.replace("## Syntheses\n", f"## Syntheses\n{entry}\n", 1)
            else:
                content += f"\n## Syntheses\n{entry}\n"
            idx.write_text(content, encoding="utf-8")
        log = WIKI_DIR / "log.md"
        log.write_text(f"## [{today}] query | {question[:70]}\n\nSaved `{rel}`.\n\n" + _read(log), encoding="utf-8")

    return out
