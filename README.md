# Sermon Insight Wiki

**Sermon corpus RAG + structured wiki + evidence-aware answers** — a sibling project to [sermon-insights-extractor](https://github.com/RGConsulting12/sermon-insights-extractor). This repo adds:

- **Hybrid retrieval** — dense embeddings + lexical overlap + [RRF](https://en.wikipedia.org/wiki/Reciprocal_rank_fusion) fusion  
- **Evidence IDs** — stable `{video_id}:{chunk_index}` references aligned with `data/embeddings.json`  
- **Structured wiki** — `wiki/sources|entities|concepts|syntheses` with `[[wikilinks]]` (pattern from [llm-wiki-agent](https://github.com/RGConsulting12/llm-wiki-agent))  
- **Knowledge graph** — `EXTRACTED` edges from wikilinks + optional `INFERRED` / `AMBIGUOUS` edges via OpenAI; **Louvain** communities (NetworkX) with `graph/graph.html` (vis.js)  
- **Query workflow** — answers with **absence reasoning** and **counterfactual / blocking** sections (JSON-shaped model output)  
- **Lint** — orphan/broken links + semantic contradiction / gap scan  

This repository does **not** modify `sermon-insights-extractor`. Point `TRANSCRIPTS` at your existing `.txt` transcripts or copy them into `data/raw_transcripts/`.

## Requirements

- Python **3.10+**  
- `OPENAI_API_KEY` in `.env` (see `.env.example`)  

## Install

```bash
cd sermon-insight-wiki
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Layout

| Path | Purpose |
|------|---------|
| `data/raw_transcripts/` | One `{video_id}.txt` per sermon |
| `data/embeddings.json` | Chunk embeddings (generated) |
| `data/evidence_manifest.json` | Optional structured claims (from ingest) |
| `wiki/` | Markdown knowledge base |
| `graph/graph.json` / `graph.html` | Serialized graph + static visualization |
| `KNOWLEDGE_SCHEMA.md` | Conventions for agents and tools |
| `data/bibles/xml/*.xml` | Beblia-format English Bibles (KJV, NIV, NKJ, NLT) for parallel scripture context — see `data/bibles/README.md` for copyright notes |

### Scripture integration

- On **ingest** and **query**, the app scans text for common `Book chapter:verse` references, loads matching verses from the bundled XML, and injects a **parallel translations** block into the LLM prompt.
- Configure which files are used with `SIW_BIBLE_TRANSLATIONS` (comma-separated: `KJV`, `NIV`, `NKJ`, `NLT`). Disable entirely with `SIW_SCRIPTURE_ENABLED=false`.
- Query API responses include a `scripture` object listing detected references and whether context was attached.

## Commands

After `pip install -e .`:

```bash
# 1) Put transcripts in data/raw_transcripts/ then:
siw-ingest data/raw_transcripts/YOUR_VIDEO_ID.txt

# 2) Rebuild graph (Louvain recolors nodes; use --no-infer to skip LLM edge inference)
siw-graph
siw-graph --no-infer --open

# 3) Ask the corpus (prints JSON + retrieval preview)
siw-query "What themes recur about grace and forgiveness?" --save syntheses/grace-note.md

# 4) Lint wiki health
siw-lint --save
```

Equivalent scripts (without installing entry points):

```bash
make install
make ingest SRC=data/raw_transcripts/YOUR_VIDEO_ID.txt
python tools/build_graph.py
python tools/query.py What is the main message? --save syntheses/note.md
python tools/lint.py --save
```

## Web UI (React)

The **sermon-insights-extractor** Vite + React app lives in `frontend/`. It expects the Flask JSON routes under `/api/*` (same contract as Phase 1 of the extractor: `stats`, `videos`, `video`, `repository`, plus **`POST /api/query`** for hybrid RAG).

**Development (hot reload + API proxy):**

```bash
# Terminal A — API (default port 8025)
export PORT=8025
python -m sermon_insight_wiki.app

# Terminal B — UI (proxies /api → VITE_API_PROXY, see frontend/.env.development)
cd frontend && npm ci && npm run dev
```

Open the URL Vite prints (usually `http://127.0.0.1:5173`).

**Single-server (Flask serves the built SPA):**

```bash
cd frontend && npm ci && npm run build
export PORT=8025
python -m sermon_insight_wiki.app
# Open http://127.0.0.1:8025/
```

The **Pipeline** page is still mostly a UI scaffold (no YouTube pipeline wired in this repo). **Home**, **Library**, **Sermon detail**, and **Ask** use live API data where endpoints exist.

## HTTP API

```bash
export PORT=8025
python -m sermon_insight_wiki.app
```

`POST /api/query` with JSON body:

```json
{
  "question": "How is repentance described?",
  "top_k": 10,
  "save_under": "syntheses/repentance.md"
}
```

Response includes `answer_markdown`, `absence_markdown`, `counterfactual_markdown`, `blocking_analysis`, `retrieval`, `absence_report`, and `scripture` (detected refs + whether parallel Bible text was attached).

## Community detection (Louvain)

Louvain is a practical default for exploratory topic clusters. If you want stricter structure, rebuild with `siw-graph --no-infer` so communities reflect mostly explicit `[[wikilinks]]`.

## Relationship to other repos

| Repo | Role |
|------|------|
| `sermon-insights-extractor` | Original pipeline, web UI, semantic search module you can keep using in parallel |
| `llm-wiki-agent` | Inspiration for wiki layout, graph passes, and lint/query flows |
| **`sermon-insight-wiki` (this)** | Integrated hybrid RAG + wiki + graph + evidence-aware Q&A |

## License

MIT — see [LICENSE](LICENSE).
