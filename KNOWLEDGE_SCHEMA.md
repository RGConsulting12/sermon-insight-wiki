# Sermon Insight Wiki — Schema

This file defines how the wiki is structured and how agents/tools should maintain it.

## Page types (YAML frontmatter)

Every wiki page except `index.md` and `log.md` starts with:

```yaml
---
title: "Human title"
type: source | entity | concept | synthesis
tags: []
sources: []          # video_ids or source slugs this page draws from
last_updated: YYYY-MM-DD
---
```

## Wikilinks

Use `[[PageName]]` for cross-references. The graph builder resolves `PageName` to `wiki/**/PageName.md` (case-insensitive stem match).

## Source pages (`wiki/sources/<slug>.md`)

- `slug` is kebab-case, typically derived from YouTube `video_id` or filename stem.
- Body must include a **Evidence** section listing chunk references the compiler used:

```markdown
## Evidence
- `VID123:0` — short gloss of chunk
- `VID123:4`
```

## Entity pages (`wiki/entities/`)

People, places, organizations mentioned across sermons. Link to `[[sources/slug]]` where they appear.

## Concept pages (`wiki/concepts/`)

Themes, doctrines, recurring ideas. Same linking rules.

## Syntheses (`wiki/syntheses/`)

Saved answers from `/wiki-query` or the API. Must cite `[[...]]` and list chunk evidence where applicable.

## Contradictions

On ingest, list under `## Contradictions` any claim that conflicts with existing wiki pages, with links.

## Scripture cross-check (bundled translations)

When ingest runs, the pipeline may detect `Book 1:2` style references in the transcript and attach **parallel passages** from local XML (KJV, NIV, NKJ, NLT by default). Source pages should include `## Scripture cross-check` comparing the sermon’s use of each passage to those wordings, naming the translation for each quote.

## Relationship to RAG

- **Vectors** live in `data/embeddings.json` (chunk text + embeddings).
- **Evidence IDs** are `{video_id}:{chunk_index}` strings aligned with embedding chunks.
- The wiki is a **compiled** layer; it never replaces transcript ground truth.
