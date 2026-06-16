"""Wiki query save_under integration tests."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sermon_insight_wiki.wiki_query import run_query


def _mock_openai_response() -> MagicMock:
    payload = {
        "answer_markdown": "Answer body [vid:0]",
        "absence_markdown": "Nothing missing.",
        "counterfactual_markdown": "Opposite unlikely.",
        "blocking_analysis": "No blockers.",
    }
    choice = MagicMock()
    choice.message.content = json.dumps(payload)
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@pytest.fixture
def query_mocks(monkeypatch: pytest.MonkeyPatch):
    sem = MagicMock()
    monkeypatch.setattr(
        "sermon_insight_wiki.wiki_query.hybrid_retrieve",
        lambda _sem, _q, top_k=10: [],
    )
    monkeypatch.setattr(
        "sermon_insight_wiki.wiki_query.wiki_link_closure",
        lambda _sem, _seeds, neighbor_chunks=1: [],
    )
    monkeypatch.setattr(
        "sermon_insight_wiki.wiki_query.build_absence_report",
        lambda _q, _fused: MagicMock(to_dict=lambda: {}),
    )
    monkeypatch.setattr(
        "sermon_insight_wiki.wiki_query.build_scripture_context_block",
        lambda _q, _blob: ("", []),
    )
    monkeypatch.setattr(
        "sermon_insight_wiki.wiki_query._select_wiki_pages",
        lambda _q, limit=8: "",
    )
    client = MagicMock()
    client.chat.completions.create.return_value = _mock_openai_response()
    monkeypatch.setattr("sermon_insight_wiki.wiki_query.OpenAI", lambda: client)
    return sem


@pytest.mark.parametrize(
    "save_under,expected_rel",
    [
        ("concepts/foo.md", "concepts/foo.md"),
        ("sources/bar/Q-test.md", "sources/bar/Q-test.md"),
        ("entities/valid_page.md", "entities/valid_page.md"),
    ],
)
def test_run_query_saves_under_valid_paths(
    wiki_tmp: Path,
    query_mocks: MagicMock,
    save_under: str,
    expected_rel: str,
):
    run_query("How is repentance described?", semantic=query_mocks, save_under=save_under)
    saved = wiki_tmp / expected_rel
    assert saved.is_file()
    text = saved.read_text(encoding="utf-8")
    assert "Answer body" in text
    assert "type: synthesis" in text


def test_run_query_api_success_valid_path(
    wiki_tmp: Path,
    query_mocks: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
):
    from sermon_insight_wiki.app import create_app

    monkeypatch.setattr(
        "sermon_insight_wiki.app.get_semantic",
        lambda: query_mocks,
    )
    monkeypatch.setattr(
        "sermon_insight_wiki.app.run_query",
        lambda q, semantic=None, top_k=10, save_under=None: run_query(
            q, semantic=semantic or query_mocks, top_k=top_k, save_under=save_under
        ),
    )

    app = create_app()
    with app.test_client() as client:
        resp = client.post(
            "/api/query",
            json={
                "question": "How is repentance described?",
                "save_under": "concepts/foo.md",
            },
        )

    assert resp.status_code == 200
    body = resp.get_json()
    assert "answer_markdown" in body
    assert (wiki_tmp / "concepts/foo.md").is_file()
