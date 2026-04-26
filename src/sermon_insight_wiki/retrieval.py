"""Hybrid retrieval: dense vectors + lexical overlap + reciprocal rank fusion."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from sermon_insight_wiki.evidence import tokenize
from sermon_insight_wiki.semantic_search import SemanticSearch


def _lexical_score(query: str, text: str) -> float:
    q = set(tokenize(query))
    if not q:
        return 0.0
    t = set(tokenize(text))
    if not t:
        return 0.0
    inter = len(q & t)
    union = len(q | t)
    return inter / union if union else 0.0


def _rrf(rankings: List[List[str]], k: int = 60) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for rlist in rankings:
        for rank, eid in enumerate(rlist):
            scores[eid] = scores.get(eid, 0.0) + 1.0 / (k + rank + 1)
    return scores


def hybrid_retrieve(
    semantic: SemanticSearch,
    query: str,
    top_k: int = 12,
    vector_pool: int = 40,
    video_ids: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Combine vector search with lexical re-ranking signals; fuse by RRF on evidence_id lists.
    Each result includes similarity (dense), lexical (jaccard), rrf_score (fused).
    """
    vec_hits = semantic.search(query, top_k=vector_pool, video_ids=video_ids)
    lex_list: List[tuple[str, float]] = []
    vec_ids: List[str] = []
    by_eid: Dict[str, Dict[str, Any]] = {}

    for h in vec_hits:
        eid = h["evidence_id"]
        vec_ids.append(eid)
        lex = _lexical_score(query, h["text"])
        lex_list.append((eid, lex))
        by_eid[eid] = {**h, "lexical": lex}

    lex_sorted = [eid for eid, _ in sorted(lex_list, key=lambda x: x[1], reverse=True)]
    vec_sorted = list(vec_ids)  # already similarity-sorted

    rrf_scores = _rrf([vec_sorted, lex_sorted], k=60)
    merged: List[str] = sorted(rrf_scores.keys(), key=lambda e: rrf_scores[e], reverse=True)[:top_k]

    out: List[Dict[str, Any]] = []
    for eid in merged:
        row = dict(by_eid[eid])
        row["rrf_score"] = rrf_scores[eid]
        out.append(row)
    return out


def wiki_link_closure(
    semantic: SemanticSearch,
    seed_video_ids: Set[str],
    neighbor_chunks: int = 1,
) -> List[Dict[str, Any]]:
    """Expand with adjacent chunks in same sermon for context (deterministic rule)."""
    cache = semantic.embeddings_cache
    extra: List[Dict[str, Any]] = []
    for vid in seed_video_ids:
        rows = cache.get(vid, [])
        by_idx = {r["chunk_index"]: r for r in rows}
        for r in list(rows):
            for d in range(-neighbor_chunks, neighbor_chunks + 1):
                if d == 0:
                    continue
                j = r["chunk_index"] + d
                n = by_idx.get(j)
                if not n:
                    continue
                extra.append(
                    {
                        "video_id": vid,
                        "chunk_index": n["chunk_index"],
                        "evidence_id": f"{vid}:{n['chunk_index']}",
                        "text": n["text"],
                        "similarity": 0.0,
                        "lexical": 0.0,
                        "rrf_score": 0.0,
                        "expansion": "neighbor_chunk",
                        "start_pos": n["start_pos"],
                        "end_pos": n["end_pos"],
                    }
                )
    return extra
