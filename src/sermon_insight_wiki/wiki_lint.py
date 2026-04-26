"""Structural wiki lint + semantic issues via LLM."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

from openai import OpenAI

from sermon_insight_wiki.config import CHAT_MODEL, WIKI_DIR, load_env

load_env()


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def all_pages(wiki_dir: Path) -> List[Path]:
    return [p for p in wiki_dir.rglob("*.md") if p.name not in ("index.md", "log.md", "lint-report.md")]


def extract_wikilinks(content: str) -> List[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def resolve(link: str, pages: List[Path], wiki_dir: Path) -> List[Path]:
    return [p for p in pages if p.stem.lower() == link.lower() or p.stem == link]


def find_orphans(pages: List[Path], wiki_dir: Path) -> List[Path]:
    inbound = defaultdict(int)
    for p in pages:
        for lk in extract_wikilinks(_read(p)):
            for r in resolve(lk, pages, wiki_dir):
                inbound[r] += 1
    return [p for p in pages if inbound[p] == 0 and p.name != "overview.md"]


def find_broken(pages: List[Path], wiki_dir: Path) -> List[Tuple[Path, str]]:
    out: List[Tuple[Path, str]] = []
    for p in pages:
        for lk in extract_wikilinks(_read(p)):
            if not resolve(lk, pages, wiki_dir):
                out.append((p, lk))
    return out


def run_lint(*, wiki_dir: Path | None = None, save: bool = False) -> str:
    wiki_dir = wiki_dir or WIKI_DIR
    pages = all_pages(wiki_dir)
    today = date.today().isoformat()
    if not pages:
        return "Wiki empty."

    orphans = find_orphans(pages, wiki_dir)
    broken = find_broken(pages, wiki_dir)

    sample = "\n\n".join(f"### {p.relative_to(wiki_dir)}\n{_read(p)[:1200]}" for p in pages[:15])
    client = OpenAI()
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": f"""Lint this sermon wiki (sample). Report markdown sections:
## Contradictions
## Stale or thin content
## Data gaps

Sample:\n{sample}""",
            }
        ],
    )
    semantic = resp.choices[0].message.content or ""

    lines = [
        f"# Lint — {today}",
        "",
        "## Structural",
        f"- orphan pages: {len(orphans)}",
        f"- broken wikilinks: {len(broken)}",
        "",
    ]
    if orphans:
        lines += [f"- `{p.relative_to(wiki_dir)}`" for p in orphans[:40]]
        lines.append("")
    if broken:
        for p, lk in broken[:40]:
            lines.append(f"- `{p.relative_to(wiki_dir)}` → [[{lk}]] missing")
        lines.append("")
    lines.append("---\n")
    lines.append(semantic)
    report = "\n".join(lines)
    if save:
        (wiki_dir / "lint-report.md").write_text(report, encoding="utf-8")
    return report


def main_argv(argv: Optional[List[str]] = None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--save", action="store_true")
    args = p.parse_args(argv)
    print(run_lint(save=args.save))


if __name__ == "__main__":
    main_argv()
