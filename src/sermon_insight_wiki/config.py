"""Paths and environment for sermon-insight-wiki."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def repo_root() -> Path:
    return _REPO_ROOT


def load_env() -> None:
    """Load `.env` from repo root if present."""
    p = _REPO_ROOT / ".env"
    if p.is_file():
        load_dotenv(p, override=False)


load_env()

WIKI_DIR = _REPO_ROOT / "wiki"
GRAPH_DIR = _REPO_ROOT / "graph"
DATA_DIR = _REPO_ROOT / "data"
TRANSCRIPTS_DIR = DATA_DIR / "raw_transcripts"
BIBLES_XML_DIR = DATA_DIR / "bibles" / "xml"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.json"
EVIDENCE_MANIFEST_PATH = DATA_DIR / "evidence_manifest.json"
SCHEMA_PATH = _REPO_ROOT / "KNOWLEDGE_SCHEMA.md"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.environ.get("SIW_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.environ.get("SIW_CHAT_MODEL", "gpt-4o-mini")
INFERENCE_MODEL = os.environ.get("SIW_INFERENCE_MODEL", "gpt-4o-mini")

CHUNK_SIZE = int(os.environ.get("SIW_CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.environ.get("SIW_CHUNK_OVERLAP", "200"))

# Comma-separated translation keys matching bundled XML (KJV, NIV, NKJ, NLT)
SIW_BIBLE_TRANSLATIONS = [
    x.strip().upper()
    for x in os.environ.get("SIW_BIBLE_TRANSLATIONS", "KJV,NIV,NLT,NKJ").split(",")
    if x.strip()
]
SIW_SCRIPTURE_ENABLED = os.environ.get("SIW_SCRIPTURE_ENABLED", "true").lower() in (
    "1",
    "true",
    "yes",
)
SIW_SCRIPTURE_MAX_REFS = int(os.environ.get("SIW_SCRIPTURE_MAX_REFS", "14"))
SIW_SCRIPTURE_MAX_VERSES_PER_RANGE = int(os.environ.get("SIW_SCRIPTURE_MAX_VERSES_PER_RANGE", "12"))
