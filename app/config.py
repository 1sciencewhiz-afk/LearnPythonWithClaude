"""Application configuration objects."""
from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Defaults shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'learnpython.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sessions: young learners often share devices, so keep logins short-lived.
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    # Sandbox limits for learner-submitted code.
    SANDBOX_TIMEOUT_SECONDS = float(os.environ.get("SANDBOX_TIMEOUT_SECONDS", "5"))
    SANDBOX_MEMORY_MB = int(os.environ.get("SANDBOX_MEMORY_MB", "128"))
    SANDBOX_MAX_OUTPUT_BYTES = int(os.environ.get("SANDBOX_MAX_OUTPUT_BYTES", "20000"))
    SANDBOX_MAX_SOURCE_BYTES = int(os.environ.get("SANDBOX_MAX_SOURCE_BYTES", "40000"))

    # Minimum age we will create an account for at all.
    MIN_SIGNUP_AGE = 10
    MAX_SIGNUP_AGE = 18
    # Under this age we require a guardian email on the account.
    GUARDIAN_REQUIRED_UNDER_AGE = 13


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    SANDBOX_TIMEOUT_SECONDS = 5.0


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str | None = None):
    name = name or os.environ.get("FLASK_CONFIG", "development")
    return CONFIGS.get(name, DevelopmentConfig)
