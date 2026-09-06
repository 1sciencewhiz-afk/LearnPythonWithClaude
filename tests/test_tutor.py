"""The AI tutor must nudge, not solve - and must degrade gracefully when unset."""
from __future__ import annotations

import json

import pytest

from app.curriculum import get_lesson
from app.services import tutor


def _lesson():
    return get_lesson("hello-world")


class FakeResponse:
    def __init__(self, payload: dict):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _gemini_payload(text: str) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": text}]}}]}


# ---------- prompt construction never leaks the reference solution ----------


def test_build_contents_never_includes_the_solution():
    lesson = _lesson()
    ctx = tutor.TutorContext(lesson=lesson, code="print('hi')")
    contents = tutor.build_contents(ctx, [], "I'm stuck")
    blob = json.dumps(contents)
    assert lesson.solution not in blob


def test_build_contents_includes_goal_brief_hints_and_code():
    lesson = _lesson()
    ctx = tutor.TutorContext(lesson=lesson, code="print('hi')", error={"type": "NameError", "message": "boom"})
    contents = tutor.build_contents(ctx, [], "help")
    blob = json.dumps(contents)
    assert lesson.goal in blob
    assert lesson.hints[0] in blob
    assert "print('hi')" in blob
    assert "NameError" in blob


def test_build_contents_caps_history_length():
    lesson = _lesson()
    ctx = tutor.TutorContext(lesson=lesson)
    history = [{"role": "user", "text": f"turn {i}"} for i in range(20)]
    contents = tutor.build_contents(ctx, history, "final question")
    # 2 seed turns + up to MAX_HISTORY_TURNS + the final question
    assert len(contents) == 2 + tutor.MAX_HISTORY_TURNS + 1
    assert "turn 19" in json.dumps(contents)
    assert "turn 0" not in json.dumps(contents)


# ---------- reply sanitisation strips smuggled solutions ----------


def test_sanitize_reply_strips_multiline_code_fences():
    reply = "Think about it like this:\n```python\ndef f(x):\n    return x * 2\n```\nDoes that help?"
    cleaned = tutor.sanitize_reply(reply)
    assert "def f(x)" not in cleaned
    assert "removed a code block" in cleaned


def test_sanitize_reply_keeps_short_one_line_snippets():
    reply = "Try something like ```python\nif x > 0:\n``` as a starting shape."
    cleaned = tutor.sanitize_reply(reply)
    assert "if x > 0:" in cleaned


def test_sanitize_reply_keeps_plain_text_untouched():
    assert tutor.sanitize_reply("Just check your indentation.") == "Just check your indentation."


# ---------- ask_tutor: configuration and transport ----------


def test_ask_tutor_without_api_key_raises():
    ctx = tutor.TutorContext(lesson=_lesson())
    with pytest.raises(tutor.TutorError):
        tutor.ask_tutor({"GEMINI_API_KEY": ""}, ctx, [], "help")


def test_ask_tutor_success_returns_sanitized_reply(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse(_gemini_payload("Try printing a smaller example first."))

    monkeypatch.setattr(tutor.urllib.request, "urlopen", fake_urlopen)

    ctx = tutor.TutorContext(lesson=_lesson(), code="print(x)")
    reply = tutor.ask_tutor({"GEMINI_API_KEY": "secret-key"}, ctx, [], "why doesn't this work?")

    assert reply == "Try printing a smaller example first."
    assert "secret-key" in captured["url"]
    assert _lesson().solution not in json.dumps(captured["body"])


def test_ask_tutor_wraps_transport_errors(monkeypatch):
    import urllib.error

    def fake_urlopen(request, timeout=None):
        raise urllib.error.URLError("no network")

    monkeypatch.setattr(tutor.urllib.request, "urlopen", fake_urlopen)

    ctx = tutor.TutorContext(lesson=_lesson())
    with pytest.raises(tutor.TutorError):
        tutor.ask_tutor({"GEMINI_API_KEY": "secret-key"}, ctx, [], "hello")


def test_ask_tutor_raises_on_empty_candidates(monkeypatch):
    def fake_urlopen(request, timeout=None):
        return FakeResponse({"candidates": []})

    monkeypatch.setattr(tutor.urllib.request, "urlopen", fake_urlopen)

    ctx = tutor.TutorContext(lesson=_lesson())
    with pytest.raises(tutor.TutorError):
        tutor.ask_tutor({"GEMINI_API_KEY": "secret-key"}, ctx, [], "hello")


# ---------- the /api/tutor route ----------


def test_tutor_route_requires_login(client):
    response = client.post(f"/api/tutor/{_lesson().slug}", json={"message": "hi"})
    assert response.status_code in (302, 401)


def test_tutor_route_disabled_without_api_key(auth_client, app):
    app.config["GEMINI_API_KEY"] = ""
    response = auth_client.post(f"/api/tutor/{_lesson().slug}", json={"message": "hi"})
    assert response.status_code == 503
    assert response.get_json()["ok"] is False


def test_tutor_route_rejects_empty_message(auth_client, app):
    app.config["GEMINI_API_KEY"] = "test-key"
    response = auth_client.post(f"/api/tutor/{_lesson().slug}", json={"message": "   "})
    assert response.status_code == 400


def test_tutor_route_rejects_unknown_lesson(auth_client, app):
    app.config["GEMINI_API_KEY"] = "test-key"
    response = auth_client.post("/api/tutor/does-not-exist", json={"message": "hi"})
    assert response.status_code == 404


def test_tutor_route_success(auth_client, app, monkeypatch):
    app.config["GEMINI_API_KEY"] = "test-key"

    def fake_ask_tutor(config, ctx, history, message):
        # The lesson's solution must never reach the call that builds the prompt.
        assert ctx.lesson.solution not in message
        return "Have you checked what print() needs inside the brackets?"

    from app.blueprints import learn as learn_bp

    monkeypatch.setattr(learn_bp.tutor, "ask_tutor", fake_ask_tutor)

    response = auth_client.post(
        f"/api/tutor/{_lesson().slug}",
        json={
            "message": "what am I missing?",
            "code": "print(",
            "last_result": {
                "stdout": "",
                "error": {"type": "SyntaxError", "message": "unexpected EOF"},
                "results": [{"label": "Prints the message", "passed": False}],
            },
            "history": [],
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert "print()" in data["reply"]


def test_tutor_route_reports_upstream_failure(auth_client, app, monkeypatch):
    app.config["GEMINI_API_KEY"] = "test-key"

    def failing_ask_tutor(config, ctx, history, message):
        raise tutor.TutorError("The AI tutor could not be reached.")

    from app.blueprints import learn as learn_bp

    monkeypatch.setattr(learn_bp.tutor, "ask_tutor", failing_ask_tutor)

    response = auth_client.post(f"/api/tutor/{_lesson().slug}", json={"message": "hi"})
    assert response.status_code == 502
    assert response.get_json()["ok"] is False


def test_tutor_route_is_rate_limited(auth_client, app, monkeypatch):
    app.config["GEMINI_API_KEY"] = "test-key"
    monkeypatch.setattr(
        "app.blueprints.learn.tutor.ask_tutor", lambda *a, **k: "ok"
    )

    slug = _lesson().slug
    last = None
    for _ in range(20):
        last = auth_client.post(f"/api/tutor/{slug}", json={"message": "hi"})
    assert last.status_code == 429


def test_lesson_page_marks_tutor_enabled_in_markup(auth_client, app):
    app.config["GEMINI_API_KEY"] = "test-key"
    body = auth_client.get(f"/lesson/{_lesson().slug}").data.decode()
    assert 'data-enabled="true"' in body
    assert "tutor-sidebar" in body


def test_lesson_page_marks_tutor_disabled_in_markup(auth_client, app):
    app.config["GEMINI_API_KEY"] = ""
    body = auth_client.get(f"/lesson/{_lesson().slug}").data.decode()
    assert 'data-enabled="false"' in body
