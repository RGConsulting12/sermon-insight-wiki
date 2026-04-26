"""Minimal Flask API for hybrid sermon query."""

from __future__ import annotations

import os

from flask import Flask, jsonify, request

from sermon_insight_wiki.semantic_search import SemanticSearch
from sermon_insight_wiki.wiki_query import run_query

app = Flask(__name__)
_semantic: SemanticSearch | None = None


def get_semantic() -> SemanticSearch:
    global _semantic
    if _semantic is None:
        _semantic = SemanticSearch()
    return _semantic


@app.get("/health")
def health():
    return jsonify({"ok": True})


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


def create_app():
    return app


def main():
    port = int(os.environ.get("PORT", "8025"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
