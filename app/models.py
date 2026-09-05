"""Database models."""
from __future__ import annotations

from datetime import date, datetime, timezone

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    display_name = db.Column(db.String(64), nullable=False, default="")
    birth_year = db.Column(db.Integer, nullable=False)
    guardian_email = db.Column(db.String(255), nullable=True)

    xp = db.Column(db.Integer, nullable=False, default=0)
    streak_days = db.Column(db.Integer, nullable=False, default=0)
    longest_streak = db.Column(db.Integer, nullable=False, default=0)
    last_active_on = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    progress = db.relationship(
        "LessonProgress", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    submissions = db.relationship(
        "Submission", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    badges = db.relationship(
        "BadgeAward", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )

    # -- password -------------------------------------------------------
    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    # -- age ------------------------------------------------------------
    @property
    def age(self) -> int:
        """Approximate age from birth year. We never collect a full birth date."""
        return date.today().year - self.birth_year

    @property
    def needs_guardian(self) -> bool:
        from flask import current_app

        return self.age < current_app.config["GUARDIAN_REQUIRED_UNDER_AGE"]

    @property
    def suggested_track(self) -> str:
        age = self.age
        if age <= 12:
            return "foundations"
        if age <= 15:
            return "builders"
        return "creators"

    @property
    def level(self) -> int:
        """Levels get gradually longer: 100 XP for L2, then +50 each level."""
        level, needed, remaining = 1, 100, self.xp
        while remaining >= needed:
            remaining -= needed
            level += 1
            needed += 50
        return level

    @property
    def xp_into_level(self) -> tuple[int, int]:
        """(xp earned inside current level, xp needed to finish it)."""
        needed, remaining = 100, self.xp
        while remaining >= needed:
            remaining -= needed
            needed += 50
        return remaining, needed

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User {self.username}>"


class LessonProgress(db.Model):
    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_slug", name="uq_progress_user_lesson"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_slug = db.Column(db.String(80), nullable=False, index=True)
    track_slug = db.Column(db.String(40), nullable=False)

    completed = db.Column(db.Boolean, nullable=False, default=False)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    saved_code = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    user = db.relationship("User", back_populates="progress")


class Submission(db.Model):
    """A single run of a learner's code against a lesson's checks."""

    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    lesson_slug = db.Column(db.String(80), nullable=False, index=True)
    code = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    user = db.relationship("User", back_populates="submissions")


class BadgeAward(db.Model):
    __tablename__ = "badge_awards"
    __table_args__ = (UniqueConstraint("user_id", "badge_slug", name="uq_badge_user_slug"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    badge_slug = db.Column(db.String(40), nullable=False)
    awarded_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    user = db.relationship("User", back_populates="badges")


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
