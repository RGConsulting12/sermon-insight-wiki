"""Chunking, OpenAI embeddings, and cosine retrieval (compatible with sermon-insights-extractor)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from openai import OpenAI

from sermon_insight_wiki.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    EMBEDDINGS_PATH,
    TRANSCRIPTS_DIR,
    load_env,
)

load_env()


def evidence_id(video_id: str, chunk_index: int) -> str:
    return f"{video_id}:{chunk_index}"


def parse_evidence_id(eid: str) -> Tuple[str, int]:
    if ":" not in eid:
        raise ValueError(f"Invalid evidence id: {eid}")
    vid, idx = eid.rsplit(":", 1)
    return vid, int(idx)


def embedded_video_ids(cache: Dict[str, List[Dict[str, Any]]]) -> set:
    """Video IDs that have at least one non-empty embedding chunk."""
    return {
        vid
        for vid, rows in cache.items()
        if isinstance(rows, list) and len(rows) > 0
    }


class SemanticSearch:
    def __init__(
        self,
        transcripts_dir: Optional[Path] = None,
        embeddings_path: Optional[Path] = None,
    ):
        self.transcripts_dir = Path(transcripts_dir or TRANSCRIPTS_DIR)
        self.embeddings_path = Path(embeddings_path or EMBEDDINGS_PATH)
        self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._load()
        self._client: Optional[OpenAI] = None

    def _openai(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI()
        return self._client

    @property
    def embeddings_file(self) -> Path:
        return self.embeddings_path

    @property
    def embeddings_cache(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._cache

    def _load(self) -> None:
        if self.embeddings_path.exists():
            try:
                raw = json.loads(self.embeddings_path.read_text(encoding="utf-8"))
                self._cache = raw if isinstance(raw, dict) else {}
            except (json.JSONDecodeError, OSError):
                self._cache = {}
        else:
            self._cache = {}

    def _save(self) -> None:
        self.embeddings_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _chunk_text(self, text: str) -> List[Tuple[str, int, int]]:
        chunks: List[Tuple[str, int, int]] = []
        start = 0
        n = len(text)
        while start < n:
            end = min(start + CHUNK_SIZE, n)
            chunk = text[start:end]
            if end < n:
                for punct in [". ", ".\n", "! ", "?\n"]:
                    j = chunk.rfind(punct)
                    if j > CHUNK_SIZE * 0.5:
                        chunk = chunk[: j + len(punct)]
                        end = start + len(chunk)
                        break
            chunks.append((chunk, start, end))
            nxt = end - CHUNK_OVERLAP
            start = end if nxt <= start else nxt
        return chunks

    def _embed(self, text: str) -> Optional[List[float]]:
        r = self._openai().embeddings.create(model=EMBEDDING_MODEL, input=text)
        return list(r.data[0].embedding)

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        va, vb = np.array(a), np.array(b)
        denom = np.linalg.norm(va) * np.linalg.norm(vb)
        if denom == 0:
            return 0.0
        return float(np.dot(va, vb) / denom)

    def generate_embeddings_for_video(
        self, video_id: str, force: bool = False, transcript_path: Optional[Path] = None
    ) -> bool:
        path = transcript_path or (self.transcripts_dir / f"{video_id}.txt")
        if not path.is_file():
            return False
        if not force and self._cache.get(video_id):
            return True
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            return False
        rows: List[Dict[str, Any]] = []
        for i, (chunk, sp, ep) in enumerate(self._chunk_text(text)):
            emb = self._embed(chunk)
            if not emb:
                continue
            rows.append(
                {
                    "chunk_index": i,
                    "text": chunk,
                    "start_pos": sp,
                    "end_pos": ep,
                    "embedding": emb,
                }
            )
        if not rows:
            return False
        self._cache[video_id] = rows
        self._save()
        return True

    def search(
        self, query: str, top_k: int = 20, video_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        qe = self._embed(query.strip())
        if not qe:
            return []
        vids = video_ids or list(self._cache.keys())
        scored: List[Dict[str, Any]] = []
        for vid in vids:
            for row in self._cache.get(vid, []):
                sim = self._cosine(qe, row["embedding"])
                scored.append(
                    {
                        "video_id": vid,
                        "chunk_index": row["chunk_index"],
                        "evidence_id": evidence_id(vid, row["chunk_index"]),
                        "text": row["text"],
                        "similarity": sim,
                        "start_pos": row["start_pos"],
                        "end_pos": row["end_pos"],
                    }
                )
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]
