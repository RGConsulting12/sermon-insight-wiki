"""Knowledge graph: EXTRACTED wikilinks + optional OpenAI INFERRED edges + Louvain."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import webbrowser
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI

from sermon_insight_wiki.config import GRAPH_DIR, INFERENCE_MODEL, WIKI_DIR, load_env

load_env()

try:
    import networkx as nx
    from networkx.algorithms import community as nx_community

    HAS_NX = True
except ImportError:
    HAS_NX = False

TYPE_COLORS = {
    "source": "#4CAF50",
    "entity": "#2196F3",
    "concept": "#FF9800",
    "synthesis": "#9C27B0",
    "unknown": "#9E9E9E",
}
EDGE_COLORS = {"EXTRACTED": "#555555", "INFERRED": "#FF5722", "AMBIGUOUS": "#BDBDBD"}
COMMUNITY_COLORS = [
    "#E91E63",
    "#00BCD4",
    "#8BC34A",
    "#FF5722",
    "#673AB7",
    "#FFC107",
    "#009688",
    "#F44336",
    "#3F51B5",
    "#CDDC39",
]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def all_wiki_pages(wiki_dir: Path) -> List[Path]:
    return [
        p
        for p in wiki_dir.rglob("*.md")
        if p.name not in ("index.md", "log.md", "lint-report.md")
    ]


def extract_wikilinks(content: str) -> List[str]:
    return list(set(re.findall(r"\[\[([^\]]+)\]\]", content)))


def extract_frontmatter_type(content: str) -> str:
    m = re.search(r"^type:\s*(\S+)", content, re.MULTILINE)
    return m.group(1).strip("\"'") if m else "unknown"


def page_id(path: Path, wiki_dir: Path) -> str:
    return path.relative_to(wiki_dir).as_posix().replace(".md", "")


def build_nodes(pages: List[Path], wiki_dir: Path) -> List[Dict[str, Any]]:
    nodes = []
    for p in pages:
        content = _read(p)
        nt = extract_frontmatter_type(content)
        tm = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
        label = tm.group(1).strip() if tm else p.stem
        nodes.append(
            {
                "id": page_id(p, wiki_dir),
                "label": label,
                "type": nt,
                "color": TYPE_COLORS.get(nt, TYPE_COLORS["unknown"]),
                "path": str(p),
            }
        )
    return nodes


def build_extracted_edges(pages: List[Path], wiki_dir: Path) -> List[Dict[str, Any]]:
    stem_map = {p.stem.lower(): page_id(p, wiki_dir) for p in pages}
    edges: List[Dict[str, Any]] = []
    seen = set()
    for p in pages:
        content = _read(p)
        src = page_id(p, wiki_dir)
        for link in extract_wikilinks(content):
            tgt = stem_map.get(link.lower())
            if tgt and tgt != src:
                key = (src, tgt)
                if key not in seen:
                    seen.add(key)
                    edges.append(
                        {
                            "from": src,
                            "to": tgt,
                            "type": "EXTRACTED",
                            "color": EDGE_COLORS["EXTRACTED"],
                            "confidence": 1.0,
                        }
                    )
    return edges


def build_inferred_edges(
    pages: List[Path],
    wiki_dir: Path,
    existing_edges: List[Dict[str, Any]],
    cache: Dict[str, str],
    infer: bool,
) -> List[Dict[str, Any]]:
    if not infer:
        return []
    client = OpenAI()
    new_edges: List[Dict[str, Any]] = []
    changed: List[Path] = []
    for p in pages:
        content = _read(p)
        h = _sha256(content)
        key = str(p)
        if cache.get(key) != h:
            changed.append(p)
            cache[key] = h
    if not changed:
        return []
    node_ids = {page_id(p, wiki_dir) for p in pages}
    node_list = "\n".join(f"- {page_id(p, wiki_dir)} ({extract_frontmatter_type(_read(p))})" for p in pages)
    edge_sample = "\n".join(f"- {e['from']} → {e['to']}" for e in existing_edges[:40])
    for p in changed:
        content = _read(p)[:2000]
        src = page_id(p, wiki_dir)
        resp = client.chat.completions.create(
            model=INFERENCE_MODEL,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": f"""Wiki implicit links. Source page id: {src}
Content:
{content}

Pages:
{node_list}

Existing extracted edges (sample):
{edge_sample}

Return ONLY a JSON array of new relationships not duplicated by wikilinks:
[{{"to": "relative/page-id", "relationship": "short", "confidence": 0.0-1.0, "type": "INFERRED or AMBIGUOUS"}}]
Rules: confidence>=0.7 → INFERRED; else AMBIGUOUS. "to" must match a page id from the list. [] if none.""",
                }
            ],
        )
        raw = (resp.choices[0].message.content or "").strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        try:
            inferred = json.loads(raw)
            if not isinstance(inferred, list):
                continue
            for rel in inferred:
                if isinstance(rel, dict) and rel.get("to") in node_ids:
                    typ = rel.get("type", "INFERRED")
                    new_edges.append(
                        {
                            "from": src,
                            "to": rel["to"],
                            "type": typ,
                            "label": rel.get("relationship", ""),
                            "color": EDGE_COLORS.get(typ, EDGE_COLORS["INFERRED"]),
                            "confidence": float(rel.get("confidence", 0.7)),
                        }
                    )
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return new_edges


def louvain_communities(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, int]:
    if not HAS_NX:
        return {}
    g = nx.Graph()
    for n in nodes:
        g.add_node(n["id"])
    for e in edges:
        g.add_edge(e["from"], e["to"])
    if g.number_of_edges() == 0:
        return {}
    try:
        comms = nx_community.louvain_communities(g, seed=42)
        out: Dict[str, int] = {}
        for i, cset in enumerate(comms):
            for node in cset:
                out[node] = i
        return out
    except Exception:
        return {}


def _render_html(nodes: List[Dict], edges: List[Dict]) -> str:
    nj = json.dumps(nodes, indent=2)
    ej = json.dumps(edges, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sermon Insight Wiki — Graph</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  body {{ margin:0; background:#1a1a2e; color:#eee; font-family:sans-serif; }}
  #g {{ width:100vw; height:100vh; }}
</style>
</head>
<body>
<div id="g"></div>
<script>
const nodes = new vis.DataSet({nj});
const edges = new vis.DataSet({ej});
new vis.Network(document.getElementById("g"), {{nodes, edges}}, {{
  nodes: {{ shape:"dot", size:12, font:{{color:"#eee", size:12}} }},
  edges: {{ arrows: {{ to: {{ enabled:true, scaleFactor:0.5 }} }} }},
  physics: {{ stabilization: {{ iterations: 120 }} }},
}});
</script>
</body>
</html>"""


def build_graph(
    *,
    wiki_dir: Path | None = None,
    graph_dir: Path | None = None,
    infer: bool = True,
    open_browser: bool = False,
) -> Path:
    wiki_dir = wiki_dir or WIKI_DIR
    graph_dir = graph_dir or GRAPH_DIR
    graph_dir.mkdir(parents=True, exist_ok=True)
    cache_path = graph_dir / ".cache.json"
    cache: Dict[str, str] = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cache = {}

    pages = all_wiki_pages(wiki_dir)
    if not pages:
        raise RuntimeError("No wiki pages found. Ingest a transcript first.")

    edges = build_extracted_edges(pages, wiki_dir)
    inferred = build_inferred_edges(pages, wiki_dir, edges, cache, infer)
    edges.extend(inferred)
    if infer:
        cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")

    nodes = build_nodes(pages, wiki_dir)
    comm = louvain_communities(nodes, edges)
    for n in nodes:
        cid = comm.get(n["id"], -1)
        n["group"] = cid
        if cid >= 0:
            n["color"] = COMMUNITY_COLORS[cid % len(COMMUNITY_COLORS)]

    today = date.today().isoformat()
    payload = {"nodes": nodes, "edges": edges, "built": today}
    json_path = graph_dir / "graph.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    html_path = graph_dir / "graph.html"
    html_path.write_text(_render_html(nodes, edges), encoding="utf-8")

    log = wiki_dir / "log.md"
    log.write_text(
        f"## [{today}] graph | rebuilt\n\n{len(nodes)} nodes, {len(edges)} edges.\n\n" + _read(log),
        encoding="utf-8",
    )
    if open_browser:
        webbrowser.open(f"file://{html_path.resolve()}")
    return json_path


def main_argv(argv: List[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Build sermon wiki knowledge graph")
    p.add_argument("--no-infer", action="store_true")
    p.add_argument("--open", action="store_true")
    args = p.parse_args(argv)
    build_graph(infer=not args.no_infer, open_browser=args.open)
    print("Wrote graph/graph.json and graph/graph.html")


if __name__ == "__main__":
    main_argv()
