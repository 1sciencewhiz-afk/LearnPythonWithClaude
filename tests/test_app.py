"""App-wide behaviour: public pages, headers, CSRF and rate limiting."""
from __future__ import annotations

import json

from app import create_app
from app.curriculum import TRACKS

FIRST = TRACKS[0].lessons[0]


def test_public_pages_render(client):
    for path in ["/", "/safety", "/login", "/register"]:
        response = client.get(path)
        assert response.status_code == 200, path


def test_landing_page_lists_every_track(client):
    body = client.get("/").data
    for track in TRACKS:
        assert track.title.encode() in body


def test_security_headers_are_set(client):
    headers = client.get("/").headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    csp = headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


def test_missing_page_renders_the_404_template(client):
    response = client.get("/no-such-page")
    assert response.status_code == 404
    assert b"Page not found" in response.data


def test_csrf_is_enforced_outside_testing_config():
    """The testing config disables CSRF, so assert the real config enables it."""
    app = create_app("development")
    assert app.config["WTF_CSRF_ENABLED"] is True
    assert create_app("production").config["SESSION_COOKIE_SECURE"] is True


def test_session_cookie_is_http_only(client, user):
    response = client.post(
        "/login", data={"identifier": user.username, "password": "python123"}
    )
    cookies = response.headers.getlist("Set-Cookie")
    assert any("HttpOnly" in cookie for cookie in cookies)


def test_rate_limit_stops_a_flood_of_runs(auth_client):
    payload = json.dumps({"code": "print(1)", "stdin": ""})
    statuses = [
        auth_client.post(
            f"/api/run/{FIRST.slug}", data=payload, content_type="application/json"
        ).status_code
        for _ in range(45)
    ]
    assert 429 in statuses, "an unbounded run loop would burn server CPU"
    assert statuses[0] == 200


def test_index_redirects_logged_in_users_to_their_dashboard(auth_client):
    assert b"Total XP" in auth_client.get("/").data


def test_no_inline_styles_anywhere():
    """The CSP forbids inline styles, so one would silently not apply.

    This was a real bug: every progress bar rendered full because its inline
    width was blocked by the policy.
    """
    from pathlib import Path

    roots = [Path("app/templates"), Path("app/static/js")]
    offenders = []
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix not in {".html", ".js"}:
                continue
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if 'style="' in line or "style='" in line:
                    offenders.append(f"{path}:{number}")
    assert not offenders, f"inline styles are blocked by the CSP: {offenders}"


def test_progress_bars_report_their_real_value(auth_client):
    body = auth_client.get("/tracks").data.decode()
    assert 'value="0"' in body, "a fresh account must show empty progress bars"
    assert "<progress" in body


def test_hidden_attribute_is_not_defeated_by_component_styles():
    """`.btn` sets display:inline-flex, which would override [hidden]."""
    from pathlib import Path

    css = Path("app/static/css/app.css").read_text()
    assert "[hidden] { display: none !important; }" in css


def test_solution_button_is_gated_in_the_markup(auth_client):
    from app.curriculum import TRACKS

    body = auth_client.get(f"/lesson/{TRACKS[0].lessons[0].slug}").data.decode()
    button = body[body.index('id="solution-btn"'):]
    assert "hidden" in button[: button.index(">")], "solution button must start hidden"


def test_editor_gutter_preserves_newlines():
    """Line numbers are newline-separated text; without pre they render in a row."""
    from pathlib import Path

    css = Path("app/static/css/app.css").read_text()
    gutter = css[css.index(".editor-gutter {"):]
    gutter = gutter[: gutter.index("}")]
    assert "white-space: pre" in gutter
