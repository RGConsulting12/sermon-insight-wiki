"""Flask API + optional production SPA (Vite build in frontend/dist)."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

from sermon_insight_wiki import dashboard_data as dd
from sermon_insight_wiki.config import TRANSCRIPTS_DIR, repo_root
from sermon_insight_wiki.semantic_search import SemanticSearch, embedded_video_ids
from sermon_insight_wiki.wiki_query import run_query

app = Flask(__name__, static_folder=None)
_semantic: SemanticSearch | None = None


def get_semantic() -> SemanticSearch:
    global _semantic
    if _semantic is None:
        _semantic = SemanticSearch()
    return _semantic


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/api/stats")
def api_stats():
    sem = get_semantic()
    payload = dd.get_statistics(sem)
    payload["embeddings_indexed_count"] = len(embedded_video_ids(sem.embeddings_cache))
    return jsonify(payload)


@app.get("/api/videos")
def api_videos():
    return jsonify(dd.get_all_videos(get_semantic()))


@app.get("/api/video/<video_id>")
def api_video(video_id: str):
    if not dd.validate_video_id(video_id):
        return jsonify({"error": "Invalid video id"}), 400
    data = dd.get_video_insights(video_id)
    if not data:
        return jsonify({"error": "Video not found"}), 404
    return jsonify(data)


@app.route("/api/video/<video_id>/title", methods=["GET", "PUT", "DELETE"])
def api_video_title(video_id: str):
    if not dd.validate_video_id(video_id):
        return jsonify({"error": "Invalid video id"}), 400
    if request.method == "GET":
        return jsonify(dd.get_title_info(video_id))
    if request.method == "PUT":
        body = request.get_json(silent=True) or {}
        t = (body.get("title") or "").strip()
        if not t:
            return jsonify({"error": 'Non-empty "title" is required (use DELETE to clear override)'}), 400
        return jsonify(dd.set_user_title(video_id, t))
    return jsonify(dd.clear_user_title(video_id))


@app.post("/api/video/<video_id>/title/extract-theme")
def api_video_extract_theme(video_id: str):
    if not dd.validate_video_id(video_id):
        return jsonify({"error": "Invalid video id"}), 400
    path = TRANSCRIPTS_DIR / f"{video_id}.txt"
    if not path.is_file():
        return jsonify({"error": "Transcript not found"}), 404
    text = path.read_text(encoding="utf-8", errors="replace")
    theme = dd.extract_sermon_theme_title(text, video_id)
    if not theme:
        return jsonify({"ok": True, "theme": None, **dd.get_title_info(video_id)})
    dd.set_llm_theme(video_id, theme)
    return jsonify({"ok": True, "theme": theme, **dd.get_title_info(video_id)})


@app.get("/api/repository")
def api_repository():
    sem = get_semantic()
    emb = embedded_video_ids(sem.embeddings_cache)
    bundle = dd.collect_repository_index(emb)
    return jsonify(
        {
            "insight_files": bundle["insight_files"],
            "insights_dir": bundle["insights_dir"],
            "total_size": bundle["total_size"],
            "total_transcripts_size": bundle["total_transcripts_size"],
            "total_audio_size": bundle["total_audio_size"],
        }
    )


@app.post("/api/query")
def api_query():
    data = request.get_json(silent=True) or {}
    q = (data.get("question") or "").strip()
    if not q:
        return jsonify({"error": "question required"}), 400
    top_k = int(data.get("top_k", 10))
    save = data.get("save_under")
    out = run_query(q, semantic=get_semantic(), top_k=top_k, save_under=save)
    return jsonify(out)


def _spa_dist() -> Path:
    return repo_root() / "frontend" / "dist"


def _register_spa() -> None:
    dist = _spa_dist()

    @app.get("/")
    def spa_index():
        index = dist / "index.html"
        if not index.is_file():
            return jsonify(
                {
                    "message": "React UI not built yet.",
                    "hint": "cd frontend && npm ci && npm run build",
                    "api": "/api/stats",
                }
            ), 503
        return send_from_directory(dist, "index.html")

    @app.get("/<path:path>")
    def spa_assets(path: str):
        if path.startswith("api"):
            abort(404)
        target = dist / path
        if target.is_file():
            return send_from_directory(dist, path)
        index = dist / "index.html"
        if index.is_file():
            return send_from_directory(dist, "index.html")
        abort(404)


_register_spa()


def create_app():
    return app


def main():
    port = int(os.environ.get("PORT", "8025"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
