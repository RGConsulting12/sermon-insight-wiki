"""Compile a sermon transcript into wiki pages (sources, entities, concepts)."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from openai import OpenAI

from sermon_insight_wiki.config import (
    CHAT_MODEL,
    SCHEMA_PATH,
    WIKI_DIR,
    load_env,
)
from sermon_insight_wiki.evidence import append_claims
from sermon_insight_wiki.semantic_search import SemanticSearch, evidence_id

load_env()


def _parse_json_obj(text: str) -> Dict[str, Any]:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise ValueError("No JSON object in model response")
    return json.loads(m.group())


def _update_index(index_path: Path, entry: str, section: str = "Sources") -> None:
    content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    header = f"## {section}"
    if header in content:
        content = content.replace(header + "\n", header + "\n" + entry + "\n", 1)
    else:
        content += f"\n{header}\n{entry}\n"
    index_path.write_text(content, encoding="utf-8")


def _append_log(log_path: Path, entry: str) -> None:
    prev = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    log_path.write_text(entry.strip() + "\n\n" + prev, encoding="utf-8")


def ingest_transcript_path(
    transcript_path: Path,
    *,
    semantic: Optional[SemanticSearch] = None,
    video_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Ingest one `.txt` transcript. Uses filename stem as `video_id` if not provided.
    Ensures embeddings exist for evidence listing when `semantic` is passed.
    """
    transcript_path = transcript_path.resolve()
    if not transcript_path.is_file():
        raise FileNotFoundError(transcript_path)

    vid = video_id or transcript_path.stem
    schema = SCHEMA_PATH.read_text(encoding="utf-8") if SCHEMA_PATH.exists() else ""
    body = transcript_path.read_text(encoding="utf-8", errors="replace")
    today = date.today().isoformat()

    sem = semantic or SemanticSearch()
    sem.generate_embeddings_for_video(vid, transcript_path=transcript_path)
    top_chunks = sem.search(body[:2000], top_k=8, video_ids=[vid])
    evidence_lines = "\n".join(
        f"- `{evidence_id(vid, c['chunk_index'])}` — excerpt: {c['text'][:120].replace(chr(10), ' ')}..."
        for c in top_chunks
    )

    client = OpenAI()
    prompt = f"""You maintain a sermon insight wiki. Schema / rules:
{schema}

Video id (slug base): {vid}
Today's date: {today}

Transcript (may be truncated in this message; file path: {transcript_path}):
=== TRANSCRIPT START ===
{body[:24000]}
=== TRANSCRIPT END ===

Suggested evidence chunk anchors (use these ids in the source page Evidence section):
{evidence_lines}

Return a SINGLE JSON object with keys:
- title (string)
- slug (kebab-case, usually same as video id {vid} unless unsafe for filenames)
- source_page (full markdown with YAML frontmatter type: source, include ## Summary, ## Key insights, ## Golden nuggets, ## Evidence using the chunk ids above, ## Contradictions if any)
- index_entry (string like: - [Title](sources/slug.md) — one line)
- overview_update (string or null) full replacement for wiki/overview.md body after frontmatter if corpus themes changed; null to skip
- entity_pages (array of {{path, content}})
- concept_pages (array of {{path, content}})
- contradictions (array of strings)
- log_entry (markdown block for wiki/log.md)
- claims (array of {{text, evidence_ids string array}}) — optional structured claims for manifest

JSON only, no markdown fences."""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.choices[0].message.content or ""
    data = _parse_json_obj(raw)

    slug = data.get("slug") or vid
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    (WIKI_DIR / "sources").mkdir(exist_ok=True)
    (WIKI_DIR / "entities").mkdir(exist_ok=True)
    (WIKI_DIR / "concepts").mkdir(exist_ok=True)

    (WIKI_DIR / "sources" / f"{slug}.md").write_text(data["source_page"], encoding="utf-8")
    for ep in data.get("entity_pages", []):
        p = WIKI_DIR / ep["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(ep["content"], encoding="utf-8")
    for cp in data.get("concept_pages", []):
        p = WIKI_DIR / cp["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(cp["content"], encoding="utf-8")

    if data.get("overview_update"):
        overview = WIKI_DIR / "overview.md"
        fm = """---
title: "Corpus overview"
type: synthesis
tags: []
sources: []
last_updated: %s
---

""" % today
        overview.write_text(fm + data["overview_update"], encoding="utf-8")

    idx = WIKI_DIR / "index.md"
    if not idx.exists():
        idx.write_text("# Index\n\n## Sources\n\n", encoding="utf-8")
    _update_index(idx, data["index_entry"], "Sources")
    _append_log(WIKI_DIR / "log.md", data.get("log_entry", f"## [{today}] ingest | {data.get('title', slug)}"))

    claims = data.get("claims") or []
    if claims:
        append_claims(vid, claims)

    return {"slug": slug, "title": data.get("title"), "contradictions": data.get("contradictions", [])}
