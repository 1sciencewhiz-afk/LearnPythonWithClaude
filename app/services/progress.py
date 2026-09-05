"""Progress, XP and streak bookkeeping."""
from __future__ import annotations

from datetime import date, timedelta

from ..curriculum import TRACKS, Track, get_lesson, track_for_lesson
from ..extensions import db
from ..models import LessonProgress, Submission, User, utcnow

# Only the most recent submissions per lesson are kept - this is a teaching
# tool, not an archive, and learners run their code a great many times.
SUBMISSION_HISTORY = 10


def get_or_create(user: User, lesson_slug: str) -> LessonProgress:
    row = LessonProgress.query.filter_by(user_id=user.id, lesson_slug=lesson_slug).first()
    if row is None:
        track = track_for_lesson(lesson_slug)
        row = LessonProgress(
            user_id=user.id,
            lesson_slug=lesson_slug,
            track_slug=track.slug if track else "",
        )
        db.session.add(row)
        db.session.commit()
    return row


def touch_streak(user: User) -> None:
    """Bump the daily streak. Same day is a no-op; a missed day resets to 1."""
    today = date.today()
    last = user.last_active_on
    if last == today:
        return

    # Bank the run that is ending before it is reset, so a broken streak
    # never erases the learner's personal best.
    user.longest_streak = max(user.longest_streak, user.streak_days)

    if last == today - timedelta(days=1):
        user.streak_days += 1
    else:
        user.streak_days = 1

    user.last_active_on = today
    user.longest_streak = max(user.longest_streak, user.streak_days)


def record_submission(user: User, lesson_slug: str, code: str, passed: bool) -> None:
    db.session.add(
        Submission(user_id=user.id, lesson_slug=lesson_slug, code=code, passed=passed)
    )
    db.session.flush()
    stale = (
        Submission.query.filter_by(user_id=user.id, lesson_slug=lesson_slug)
        .order_by(Submission.created_at.desc(), Submission.id.desc())
        .offset(SUBMISSION_HISTORY)
        .all()
    )
    for row in stale:
        db.session.delete(row)


def complete_lesson(user: User, lesson_slug: str, code: str) -> tuple[LessonProgress, int]:
    """Mark a lesson complete. Returns the row and the XP newly awarded."""
    lesson = get_lesson(lesson_slug)
    row = get_or_create(user, lesson_slug)
    row.saved_code = code

    gained = 0
    if not row.completed:
        row.completed = True
        row.completed_at = utcnow()
        gained = lesson.xp if lesson else 0
        user.xp += gained

    touch_streak(user)
    db.session.commit()
    return row, gained


def record_attempt(user: User, lesson_slug: str, code: str, passed: bool) -> LessonProgress:
    row = get_or_create(user, lesson_slug)
    row.attempts += 1
    row.saved_code = code
    record_submission(user, lesson_slug, code, passed)
    db.session.commit()
    return row


def completed_map(user: User) -> dict[str, LessonProgress]:
    return {row.lesson_slug: row for row in user.progress}


def track_summary(user: User, track: Track) -> dict:
    rows = completed_map(user)
    done = sum(1 for lesson in track.lessons if rows.get(lesson.slug) and rows[lesson.slug].completed)
    total = len(track.lessons)
    return {
        "track": track,
        "done": done,
        "total": total,
        "percent": round(done / total * 100) if total else 0,
        "started": any(lesson.slug in rows for lesson in track.lessons),
    }


def all_track_summaries(user: User) -> list[dict]:
    return [track_summary(user, track) for track in TRACKS]


def next_lesson_for(user: User, track: Track):
    """The first unfinished lesson in a track, or None if the track is done."""
    rows = completed_map(user)
    for lesson in track.lessons:
        row = rows.get(lesson.slug)
        if row is None or not row.completed:
            return lesson
    return None


def recommended_lesson(user: User):
    """Where to send the learner next: their suggested track first, then any."""
    preferred = [t for t in TRACKS if t.slug == user.suggested_track]
    for track in preferred + [t for t in TRACKS if t.slug != user.suggested_track]:
        lesson = next_lesson_for(user, track)
        if lesson is not None:
            return track, lesson
    return TRACKS[0], TRACKS[0].lessons[0]
