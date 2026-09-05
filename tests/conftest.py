from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402
from app.models import User  # noqa: E402
from app.ratelimit import reset as reset_limits  # noqa: E402


@pytest.fixture()
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()
    reset_limits()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


def make_user(username="learner", birth_year=2012, password="python123") -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        display_name=username,
        birth_year=birth_year,
    )
    user.set_password(password)
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture()
def user(app):
    return make_user()


@pytest.fixture()
def auth_client(client, user):
    client.post(
        "/login",
        data={"identifier": user.username, "password": "python123"},
        follow_redirects=True,
    )
    return client
