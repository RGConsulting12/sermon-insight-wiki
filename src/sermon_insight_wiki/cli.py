"""Console entry points: siw-ingest, siw-graph, siw-query, siw-lint."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def ingest_main() -> None:
    if len(sys.argv) < 2:
        print("Usage: siw-ingest <path-to-transcript.txt> [video_id]", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    vid = sys.argv[2] if len(sys.argv) > 2 else None
    from sermon_insight_wiki.wiki_ingest import ingest_transcript_path

    info = ingest_transcript_path(path, video_id=vid)
    print(json.dumps(info, indent=2))


def graph_main() -> None:
    from sermon_insight_wiki.graph_builder import main_argv

    main_argv(sys.argv[1:])


def query_main() -> None:
    import argparse

    p = argparse.ArgumentParser(prog="siw-query")
    p.add_argument("question", nargs="+", help="Natural language question")
    p.add_argument(
        "--save",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help="Save synthesis under wiki/ (e.g. syntheses/my-note.md)",
    )
    a = p.parse_args(sys.argv[1:])
    question = " ".join(a.question).strip()
    if not question:
        p.error("question required")
    save = a.save
    from sermon_insight_wiki.wiki_query import run_query

    out = run_query(question, save_under=save if save is not None else None)
    slim = {k: v for k, v in out.items() if k not in ("retrieval",)}
    print(json.dumps(slim, indent=2))
    print("\n--- retrieval (first 5) ---\n")
    for row in out.get("retrieval", [])[:5]:
        print(row.get("evidence_id"), row.get("similarity"), row.get("text", "")[:120], "...")


def lint_main() -> None:
    from sermon_insight_wiki.wiki_lint import main_argv

    main_argv(sys.argv[1:])
