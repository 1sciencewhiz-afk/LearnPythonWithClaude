"""Lesson data structures.

A track is an ordered list of lessons.  A lesson carries everything the
player needs: the teaching copy, a worked example, starter code, hints,
the checks that grade a submission, and a reference solution used both to
unblock a stuck learner and to self-test the curriculum (see
``tests/test_curriculum.py``).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GlossaryTerm:
    term: str
    definition: str

    @property
    def anchor(self) -> str:
        """A stable id for linking straight to this entry on the glossary page."""
        slug = "".join(ch if ch.isalnum() else "-" for ch in self.term.lower())
        while "--" in slug:
            slug = slug.replace("--", "-")
        return f"term-{slug.strip('-')}"


@dataclass(frozen=True)
class Lesson:
    slug: str
    title: str
    goal: str
    concept: str
    example: str
    brief: str
    starter: str
    solution: str
    checks: list[dict]
    hints: list[str] = field(default_factory=list)
    glossary: list[GlossaryTerm] = field(default_factory=list)
    xp: int = 20
    minutes: int = 10

    @property
    def check_labels(self) -> list[str]:
        return [c.get("label", "Check") for c in self.checks]


@dataclass(frozen=True)
class Track:
    slug: str
    title: str
    tagline: str
    ages: str
    emoji: str
    blurb: str
    lessons: list[Lesson]

    @property
    def total_xp(self) -> int:
        return sum(lesson.xp for lesson in self.lessons)
