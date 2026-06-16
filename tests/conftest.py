"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def wiki_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Isolated wiki/ directory with monkeypatched WIKI_DIR."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "index.md").write_text("# Index\n", encoding="utf-8")
    monkeypatch.setattr("sermon_insight_wiki.wiki_query.WIKI_DIR", wiki)
    monkeypatch.setattr("sermon_insight_wiki.config.WIKI_DIR", wiki)
    return wiki
