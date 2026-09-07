"""Every lesson must be solvable, and not solvable by accident."""
from __future__ import annotations

import pytest

from app import curriculum
from app.sandbox import execute

ALL_LESSONS = [
    pytest.param(track, lesson, id=f"{track.slug}-{lesson.slug}")
    for track in curriculum.TRACKS
    for lesson in track.lessons
]


@pytest.mark.parametrize("track,lesson", ALL_LESSONS)
def test_reference_solution_passes_its_own_checks(track, lesson):
    result = execute(lesson.solution, checks=lesson.checks, timeout=10)
    failed = [r["label"] for r in result.results if not r["passed"]]
    assert result.passed, f"{lesson.slug} failed: {failed} error={result.error}"


@pytest.mark.parametrize("track,lesson", ALL_LESSONS)
def test_starter_code_does_not_already_pass(track, lesson):
    """A starter that passes would hand out free XP."""
    result = execute(lesson.starter, checks=lesson.checks, timeout=10)
    assert not result.passed, f"{lesson.slug} is solved by its own starter code"


@pytest.mark.parametrize("track,lesson", ALL_LESSONS)
def test_lesson_content_is_complete(track, lesson):
    assert lesson.title and lesson.goal and lesson.brief
    assert lesson.concept.strip().startswith("<")
    assert lesson.checks, "a lesson with no checks can never be completed"
    assert len(lesson.hints) >= 3, "learners get stuck; give them three hints"
    assert lesson.xp > 0 and lesson.minutes > 0
    assert all(check.get("label") for check in lesson.checks)


@pytest.mark.parametrize("track,lesson", ALL_LESSONS)
def test_lesson_teaches_at_least_one_glossary_term(track, lesson):
    assert lesson.glossary, f"{lesson.slug} has no glossary terms for the index"
    for entry in lesson.glossary:
        assert entry.term.strip()
        assert entry.definition.strip()


@pytest.mark.parametrize("track,lesson", ALL_LESSONS)
def test_lesson_concept_has_teaching_depth(track, lesson):
    """Every lesson should explain why the idea matters, not just the syntax."""
    assert "Why this matters" in lesson.concept
    assert "Common mistakes" in lesson.concept
    assert "Try it yourself" in lesson.concept, (
        f"{lesson.slug} has no self-directed experiment beyond the graded brief"
    )


def test_lesson_slugs_are_unique_across_tracks():
    slugs = [lesson.slug for track in curriculum.TRACKS for lesson in track.lessons]
    assert len(slugs) == len(set(slugs))


def test_navigation_helpers():
    first = curriculum.TRACKS[0].lessons[0]
    second = curriculum.TRACKS[0].lessons[1]
    assert curriculum.neighbours(first.slug) == (None, second)
    assert curriculum.lesson_position(second.slug)[0] == 2
    assert curriculum.track_for_lesson(first.slug) is curriculum.TRACKS[0]
    assert curriculum.get_lesson("does-not-exist") is None


def test_tracks_are_ordered_by_difficulty():
    assert [t.slug for t in curriculum.TRACKS] == ["foundations", "builders", "creators"]
