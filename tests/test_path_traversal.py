"""Path traversal guards for wiki save_under."""

from __future__ import annotations

from pathlib import Path

import pytest

from sermon_insight_wiki.wiki_query import (
    INVALID_WIKI_PATH_MESSAGE,
    InvalidWikiPath,
    safe_wiki_relative_path,
)


@pytest.mark.parametrize(
    "path",
    [
        "concepts/foo.md",
        "sources/bar/Q-test.md",
        "entities/valid_page.md",
        "concepts/foo/../bar.md",
        "concepts\\foo.md",
        "concepts/💣/evil.md",
    ],
)
def test_safe_wiki_relative_path_accepts_valid_paths(wiki_tmp: Path, path: str):
    rel = safe_wiki_relative_path(path)
    assert not Path(rel).is_absolute()
    target = (wiki_tmp / rel).resolve()
    assert target.is_relative_to(wiki_tmp.resolve())
    if "foo/../bar" in path.replace("\\", "/"):
        assert rel == "concepts/bar.md"
    if path == "concepts\\foo.md":
        assert rel == "concepts/foo.md"


@pytest.mark.parametrize(
    "path",
    [
        "../escaping.md",
        "/etc/passwd",
        "concepts/../../etc/passwd",
    ],
)
def test_safe_wiki_relative_path_rejects_traversal(wiki_tmp: Path, path: str):
    with pytest.raises(ValueError):
        safe_wiki_relative_path(path)


def test_safe_wiki_relative_path_rejects_symlink_escape(wiki_tmp: Path):
    outside = wiki_tmp.parent / "outside.md"
    outside.write_text("secret", encoding="utf-8")
    link = wiki_tmp / "escape-link.md"
    link.symlink_to(outside)
    with pytest.raises(ValueError):
        safe_wiki_relative_path("escape-link.md")


def test_invalid_wiki_path_exception_is_json_400():
    from flask import Flask

    app = Flask(__name__)

    @app.post("/probe")
    def probe():
        raise InvalidWikiPath()

    with app.test_client() as client:
        resp = client.post("/probe")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": INVALID_WIKI_PATH_MESSAGE}
    assert "wiki" not in resp.get_data(as_text=True).lower()
    assert "/etc" not in resp.get_data(as_text=True)


def test_api_query_rejects_traversal_path(wiki_tmp: Path, monkeypatch: pytest.MonkeyPatch):
    from sermon_insight_wiki.app import create_app

    monkeypatch.setattr(
        "sermon_insight_wiki.app.get_semantic",
        lambda: None,
    )

    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/api/query",
            json={"question": "test question", "save_under": "../escaping.md"},
        )

    assert resp.status_code == 400
    assert resp.get_json() == {"error": INVALID_WIKI_PATH_MESSAGE}


def test_api_query_rejects_absolute_path(wiki_tmp: Path, monkeypatch: pytest.MonkeyPatch):
    from sermon_insight_wiki.app import create_app

    monkeypatch.setattr(
        "sermon_insight_wiki.app.get_semantic",
        lambda: None,
    )

    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/api/query",
            json={"question": "test question", "save_under": "/etc/passwd"},
        )

    assert resp.status_code == 400
    assert resp.get_json() == {"error": INVALID_WIKI_PATH_MESSAGE}


def test_api_query_rejects_nested_traversal(wiki_tmp: Path, monkeypatch: pytest.MonkeyPatch):
    from sermon_insight_wiki.app import create_app

    monkeypatch.setattr(
        "sermon_insight_wiki.app.get_semantic",
        lambda: None,
    )

    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/api/query",
            json={
                "question": "test question",
                "save_under": "concepts/../../etc/passwd",
            },
        )

    assert resp.status_code == 400
    assert resp.get_json() == {"error": INVALID_WIKI_PATH_MESSAGE}
