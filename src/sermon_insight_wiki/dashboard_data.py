"""Build JSON payloads compatible with sermon-insights-extractor Phase-1 React API."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from sermon_insight_wiki.config import (
    CHAT_MODEL,
    DATA_DIR,
    TRANSCRIPTS_DIR,
    WIKI_DIR,
    repo_root,
)
from sermon_insight_wiki.semantic_search import SemanticSearch, embedded_video_ids

TITLE_STORE_PATH = DATA_DIR / "display_titles.json"


def validate_video_id(video_id: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{1,80}", video_id or ""))


def _load_title_store() -> Dict[str, Any]:
    if not TITLE_STORE_PATH.exists():
        return {}
    try:
        raw = json.loads(TITLE_STORE_PATH.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_title_store(data: Dict[str, Any]) -> None:
    TITLE_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TITLE_STORE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def get_title_info(video_id: str) -> Dict[str, Any]:
    store = _load_title_store()
    row = store.get(video_id, {})
    user_title = (row.get("user_title") or "").strip() or None
    llm_theme = (row.get("llm_theme") or "").strip() or None
    youtube_title = video_id
    if user_title:
        display = user_title
        source = "user"
    elif llm_theme:
        display = llm_theme
        source = "llm"
    else:
        display = youtube_title
        source = "youtube"
    return {
        "display_title": display,
        "source": source,
        "youtube_title": youtube_title,
        "user_title": user_title,
        "llm_theme": llm_theme,
        "user_updated_at": row.get("user_updated_at"),
        "llm_extracted_at": row.get("llm_extracted_at"),
    }


def set_user_title(video_id: str, title: str) -> Dict[str, Any]:
    store = _load_title_store()
    row = store.setdefault(video_id, {})
    row["user_title"] = title.strip()
    row["user_updated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    _save_title_store(store)
    return get_title_info(video_id)


def clear_user_title(video_id: str) -> Dict[str, Any]:
    store = _load_title_store()
    if video_id in store:
        store[video_id].pop("user_title", None)
        store[video_id].pop("user_updated_at", None)
    _save_title_store(store)
    return get_title_info(video_id)


def set_llm_theme(video_id: str, theme: str) -> None:
    store = _load_title_store()
    row = store.setdefault(video_id, {})
    row["llm_theme"] = theme.strip()
    row["llm_extracted_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    _save_title_store(store)


def extract_sermon_theme_title(transcript: str, video_id: str) -> Optional[str]:
    """One-line title from transcript opening (OpenAI)."""
    try:
        from openai import OpenAI

        sample = (transcript or "")[:4000]
        if not sample.strip():
            return None
        client = OpenAI()
        r = client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=0.2,
            max_tokens=80,
            messages=[
                {
                    "role": "user",
                    "content": f'Return a single short sermon title (max 12 words), no quotes, for this transcript opening. If unclear, use "Untitled sermon".\n\n{sample}',
                }
            ],
        )
        t = (r.choices[0].message.content or "").strip().split("\n")[0].strip()
        return t[:200] if t else None
    except Exception:
        return None


def list_transcript_video_ids() -> List[str]:
    if not TRANSCRIPTS_DIR.exists():
        return []
    return sorted({p.stem for p in TRANSCRIPTS_DIR.glob("*.txt")})


def get_all_videos(semantic: SemanticSearch) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for video_id in list_transcript_video_ids():
        path = TRANSCRIPTS_DIR / f"{video_id}.txt"
        ti = get_title_info(video_id)
        summary = ""
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            summary = " ".join(text.split())[:220]
        except OSError:
            pass
        tlen = path.stat().st_size if path.is_file() else 0
        out.append(
            {
                "video_id": video_id,
                "title": ti["display_title"],
                "title_source": ti["source"],
                "youtube_title": ti["youtube_title"],
                "llm_theme": ti["llm_theme"],
                "user_title": ti["user_title"],
                "summary": summary,
                "insights_count": 0,
                "nuggets_count": 0,
                "published_at": "",
                "transcript_length": tlen,
                "metadata": {
                    "title": ti["display_title"],
                    "description": "",
                    "published_at": "",
                    "channel_title": "",
                    "tags": [],
                },
            }
        )
    out.sort(key=lambda x: x["transcript_length"], reverse=True)
    return out


def get_video_insights(video_id: str) -> Optional[Dict[str, Any]]:
    if not validate_video_id(video_id):
        return None
    path = TRANSCRIPTS_DIR / f"{video_id}.txt"
    if not path.is_file():
        return None
    transcript = path.read_text(encoding="utf-8", errors="replace")
    ti = get_title_info(video_id)
    return {
        "video_id": video_id,
        "insights": {
            "summary": "",
            "insights": [],
            "golden_nuggets": [],
            "video_id": video_id,
        },
        "metadata": {
            "title": ti["display_title"],
            "description": "",
            "published_at": "",
            "channel_title": "",
            "tags": [],
        },
        "transcript": transcript,
        "title_info": {
            "display_title": ti["display_title"],
            "source": ti["source"],
            "youtube_title": ti["youtube_title"],
            "user_title": ti["user_title"],
            "llm_theme": ti["llm_theme"],
            "user_updated_at": ti["user_updated_at"],
            "llm_extracted_at": ti["llm_extracted_at"],
        },
    }


def get_statistics(semantic: SemanticSearch) -> Dict[str, Any]:
    videos = get_all_videos(semantic)
    total_transcript_length = sum(v.get("transcript_length", 0) for v in videos)
    num = len(videos)
    cost_file = DATA_DIR / "costs.json"
    cost_data: Dict[str, Any] = {}
    if cost_file.exists():
        try:
            cost_data = json.loads(cost_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    summary = cost_data.get("summary", {}) if isinstance(cost_data, dict) else {}
    return {
        "total_videos": num,
        "total_insights": 0,
        "total_nuggets": 0,
        "total_transcript_length": total_transcript_length,
        "avg_insights_per_video": 0.0,
        "avg_nuggets_per_video": 0.0,
        "cost_data": summary if isinstance(summary, dict) else {},
    }


def collect_repository_index(embedded: Set[str]) -> Dict[str, Any]:
    """Rows mirror extractor `RepositoryInsightFile` for transcript + wiki index."""
    rows: List[Dict[str, Any]] = []
    root = repo_root()
    for video_id in list_transcript_video_ids():
        tpath = TRANSCRIPTS_DIR / f"{video_id}.txt"
        stat = tpath.stat()
        ti = get_title_info(video_id)
        tsize = stat.st_size
        src_dir = WIKI_DIR / "sources"
        wiki_source: Optional[Path] = None
        if src_dir.is_dir():
            p1 = src_dir / f"{video_id}.md"
            if p1.is_file():
                wiki_source = p1
            else:
                matches = sorted(src_dir.glob(f"{video_id}*.md"))
                wiki_source = matches[0] if matches else None
        has_wiki = wiki_source is not None
        rows.append(
            {
                "video_id": video_id,
                "title": ti["display_title"],
                "published_at": "",
                "channel_title": "",
                "filename": tpath.name,
                "path": str(tpath.relative_to(root)),
                "size": tsize,
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "insights_count": 0,
                "nuggets_count": 0,
                "has_transcript": True,
                "transcript_size": tsize,
                "has_chunks": False,
                "chunk_count": 0,
                "has_chunk_transcripts": False,
                "has_audio": False,
                "audio_size": 0,
                "has_embeddings": video_id in embedded,
                "has_insights": bool(has_wiki),
                "has_metadata": False,
                "row_source": "transcript",
            }
        )
    total_size = sum(r["size"] for r in rows)
    total_tx = sum(r["transcript_size"] for r in rows)
    return {
        "insight_files": rows,
        "insights_dir": str(WIKI_DIR),
        "total_size": total_size,
        "total_transcripts_size": total_tx,
        "total_audio_size": 0,
    }
