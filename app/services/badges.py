"""Badge catalogue and the rules that award them."""
from __future__ import annotations

from dataclasses import dataclass

from ..curriculum import TRACKS, total_lessons
from ..extensions import db
from ..models import BadgeAward, LessonProgress, User


@dataclass(frozen=True)
class Badge:
    slug: str
    name: str
    description: str
    emoji: str


CATALOGUE: list[Badge] = [
    Badge("first-steps", "First Steps", "Finish your very first lesson.", "\N{FOOTPRINTS}"),
    Badge("persistent", "Persistent", "Finish a lesson after five or more attempts.", "\N{MOUNTAIN}"),
    Badge("streak-3", "Three in a Row", "Practise three days running.", "\N{FIRE}"),
    Badge("streak-7", "Week Strong", "Practise seven days running.", "\N{COLLISION SYMBOL}"),
    Badge("level-5", "Level Five", "Reach level 5.", "\N{GLOWING STAR}"),
    Badge("halfway", "Halfway There", "Complete half of every lesson in the course.", "\N{CHEQUERED FLAG}"),
    Badge("track-foundations", "Foundations Complete", "Finish the whole Foundations track.", "\N{SEEDLING}"),
    Badge("track-builders", "Builders Complete", "Finish the whole Builders track.", "\N{HAMMER AND WRENCH}"),
    Badge("track-creators", "Creators Complete", "Finish the whole Creators track.", "\N{ROCKET}"),
    Badge("graduate", "Python Graduate", "Complete every lesson in the course.", "\N{GRADUATION CAP}"),
]
BADGES_BY_SLUG = {badge.slug: badge for badge in CATALOGUE}


def _completed_slugs(user: User) -> set[str]:
    rows = LessonProgress.query.filter_by(user_id=user.id, completed=True).all()
    return {row.lesson_slug for row in rows}


def evaluate(user: User, *, attempts: int = 0) -> list[Badge]:
    """Award any badges the user has newly earned. Returns the new ones."""
    already = {award.badge_slug for award in user.badges}
    completed = _completed_slugs(user)
    earned: set[str] = set()

    if completed:
        earned.add("first-steps")
    if attempts >= 5:
        earned.add("persistent")
    if user.streak_days >= 3:
        earned.add("streak-3")
    if user.streak_days >= 7:
        earned.add("streak-7")
    if user.level >= 5:
        earned.add("level-5")

    everything = total_lessons()
    if everything and len(completed) * 2 >= everything:
        earned.add("halfway")
    if everything and len(completed) >= everything:
        earned.add("graduate")

    for track in TRACKS:
        slugs = {lesson.slug for lesson in track.lessons}
        if slugs and slugs <= completed:
            earned.add(f"track-{track.slug}")

    fresh = [BADGES_BY_SLUG[slug] for slug in sorted(earned - already) if slug in BADGES_BY_SLUG]
    for badge in fresh:
        db.session.add(BadgeAward(user_id=user.id, badge_slug=badge.slug))
    if fresh:
        db.session.commit()
    return fresh


def awarded(user: User) -> list[tuple[Badge, object]]:
    """Every badge in the catalogue with its award row, or None if unearned."""
    rows = {award.badge_slug: award for award in user.badges}
    return [(badge, rows.get(badge.slug)) for badge in CATALOGUE]
