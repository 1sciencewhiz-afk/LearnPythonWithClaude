"""Account creation, login, and the age rules that go with a young audience."""
from __future__ import annotations

from datetime import date

from app.models import User

from conftest import make_user


def register(client, **overrides):
    year = date.today().year
    data = {
        "username": "newbie",
        "email": "newbie@example.com",
        "birth_year": str(year - 14),
        "guardian_email": "",
        "password": "python123",
        "confirm": "python123",
        "accept": "y",
    }
    data.update(overrides)
    return client.post("/register", data=data, follow_redirects=True)


def test_registration_creates_an_account_and_logs_in(client):
    response = register(client)
    assert response.status_code == 200
    user = User.query.filter_by(username="newbie").first()
    assert user is not None
    assert user.password_hash != "python123"
    assert b"Dashboard" in response.data


def test_under_13_must_supply_a_guardian_email(client):
    year = date.today().year
    response = register(client, birth_year=str(year - 11), guardian_email="")
    assert b"parent or guardian email is required" in response.data
    assert User.query.filter_by(username="newbie").first() is None


def test_under_13_succeeds_with_a_guardian_email(client):
    year = date.today().year
    register(client, birth_year=str(year - 11), guardian_email="parent@example.com")
    user = User.query.filter_by(username="newbie").first()
    assert user is not None
    assert user.guardian_email == "parent@example.com"


def test_too_young_is_refused(client):
    year = date.today().year
    register(client, birth_year=str(year - 6))
    assert User.query.filter_by(username="newbie").first() is None


def test_too_old_is_refused(client):
    year = date.today().year
    register(client, birth_year=str(year - 30))
    assert User.query.filter_by(username="newbie").first() is None


def test_duplicate_username_is_refused(client, user):
    response = register(client, username=user.username)
    assert b"taken" in response.data


def test_duplicate_username_is_case_insensitive(client, user):
    register(client, username=user.username.upper(), email="other@example.com")
    assert User.query.filter(User.username == user.username.upper()).first() is None


def test_weak_passwords_are_refused(client):
    for weak in ["password", "12345678", "aaaaaaaa"]:
        response = register(client, password=weak, confirm=weak)
        assert User.query.filter_by(username="newbie").first() is None, weak
        assert response.status_code == 200


def test_password_may_not_contain_the_username(client):
    register(client, username="rocket", password="rocket12345", confirm="rocket12345")
    assert User.query.filter_by(username="rocket").first() is None


def test_login_accepts_username_or_email(client, user):
    for identifier in [user.username, user.email, user.username.upper()]:
        client.get("/logout")
        response = client.post(
            "/login", data={"identifier": identifier, "password": "python123"},
            follow_redirects=True,
        )
        assert b"Dashboard" in response.data, identifier


def test_login_with_a_bad_password_is_refused(client, user):
    response = client.post("/login", data={"identifier": user.username, "password": "wrong"})
    assert response.status_code == 401


def test_login_error_does_not_reveal_whether_a_user_exists(client, user):
    """A wrong password and an unknown account must give the same message."""
    known = client.post("/login", data={"identifier": user.username, "password": "wrong"})
    unknown = client.post("/login", data={"identifier": "ghost", "password": "wrong"})
    message = b"That username or password was not right."
    assert known.status_code == unknown.status_code == 401
    assert message in known.data and message in unknown.data


def test_protected_pages_require_login(client):
    for path in ["/dashboard", "/tracks", "/profile", "/playground", "/badges"]:
        response = client.get(path)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


def test_logout_requires_a_post(auth_client):
    assert auth_client.get("/logout").status_code == 405


def test_next_redirect_cannot_leave_the_site(client, user):
    response = client.post(
        "/login?next=https://evil.example.com/steal",
        data={"identifier": user.username, "password": "python123"},
    )
    assert "evil.example.com" not in response.headers["Location"]


def test_account_deletion_removes_everything(auth_client, user, db):
    from app.models import LessonProgress

    db.session.add(LessonProgress(user_id=user.id, lesson_slug="hello-world", track_slug="foundations"))
    db.session.commit()

    auth_client.post("/profile/delete", data={"confirm_username": user.username}, follow_redirects=True)
    assert User.query.filter_by(username=user.username).first() is None
    assert LessonProgress.query.count() == 0


def test_account_deletion_needs_the_exact_username(auth_client, user):
    auth_client.post("/profile/delete", data={"confirm_username": "wrong"}, follow_redirects=True)
    assert User.query.filter_by(username=user.username).first() is not None


def test_password_change_requires_the_current_password(auth_client, user):
    auth_client.post(
        "/profile",
        data={"current_password": "nope", "password": "newpass123", "confirm": "newpass123", "submit": "y"},
        follow_redirects=True,
    )
    assert User.query.filter_by(username=user.username).first().check_password("python123")


def test_suggested_track_follows_age(app):
    year = date.today().year
    assert make_user("young", birth_year=year - 11).suggested_track == "foundations"
    assert make_user("mid", birth_year=year - 14).suggested_track == "builders"
    assert make_user("older", birth_year=year - 17).suggested_track == "creators"
