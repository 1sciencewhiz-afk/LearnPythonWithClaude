"""The course content and the helpers used to navigate it."""
from __future__ import annotations

from .builders import TRACK as BUILDERS
from .creators import TRACK as CREATORS
from .foundations import TRACK as FOUNDATIONS
from .schema import Lesson, Track

TRACKS: list[Track] = [FOUNDATIONS, BUILDERS, CREATORS]
TRACKS_BY_SLUG: dict[str, Track] = {track.slug: track for track in TRACKS}

# Lesson slugs are unique across the whole course, which keeps progress rows
# simple and lets a lesson be linked to without knowing its track.
LESSONS_BY_SLUG: dict[str, Lesson] = {
    lesson.slug: lesson for track in TRACKS for lesson in track.lessons
}
TRACK_OF_LESSON: dict[str, str] = {
    lesson.slug: track.slug for track in TRACKS for lesson in track.lessons
}


def get_track(slug: str) -> Track | None:
    return TRACKS_BY_SLUG.get(slug)


def get_lesson(slug: str) -> Lesson | None:
    return LESSONS_BY_SLUG.get(slug)


def track_for_lesson(slug: str) -> Track | None:
    track_slug = TRACK_OF_LESSON.get(slug)
    return TRACKS_BY_SLUG.get(track_slug) if track_slug else None


def lesson_position(lesson_slug: str) -> tuple[int, int]:
    """(1-based index, total) of a lesson inside its track."""
    track = track_for_lesson(lesson_slug)
    if track is None:
        return (0, 0)
    for index, lesson in enumerate(track.lessons, start=1):
        if lesson.slug == lesson_slug:
            return (index, len(track.lessons))
    return (0, len(track.lessons))


def neighbours(lesson_slug: str) -> tuple[Lesson | None, Lesson | None]:
    """The lessons before and after this one within its track."""
    track = track_for_lesson(lesson_slug)
    if track is None:
        return (None, None)
    slugs = [lesson.slug for lesson in track.lessons]
    index = slugs.index(lesson_slug)
    previous = track.lessons[index - 1] if index > 0 else None
    following = track.lessons[index + 1] if index + 1 < len(track.lessons) else None
    return (previous, following)


def total_lessons() -> int:
    return len(LESSONS_BY_SLUG)


__all__ = [
    "Lesson",
    "Track",
    "TRACKS",
    "TRACKS_BY_SLUG",
    "LESSONS_BY_SLUG",
    "get_track",
    "get_lesson",
    "track_for_lesson",
    "lesson_position",
    "neighbours",
    "total_lessons",
]
