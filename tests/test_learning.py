"""The lesson player: gating, grading, XP, streaks and badges."""
from __future__ import annotations

import json
from datetime import date, timedelta

from app.curriculum import TRACKS, get_lesson
from app.models import LessonProgress, Submission
from app.services import badges, progress

FIRST = TRACKS[0].lessons[0]
SECOND = TRACKS[0].lessons[1]


def check(client, lesson, code):
    response = client.post(
        f"/api/check/{lesson.slug}",
        data=json.dumps({"code": code, "stdin": ""}),
        content_type="application/json",
    )
    return response, response.get_json()


def test_lesson_page_renders_for_the_first_lesson(auth_client):
    response = auth_client.get(f"/lesson/{FIRST.slug}")
    assert response.status_code == 200
    assert FIRST.title.encode() in response.data


def test_later_lessons_are_locked_until_the_previous_one_is_done(auth_client):
    response = auth_client.get(f"/lesson/{SECOND.slug}")
    assert response.status_code == 302
    assert f"/track/{TRACKS[0].slug}" in response.headers["Location"]


def test_passing_a_lesson_unlocks_the_next_one(auth_client):
    check(auth_client, FIRST, FIRST.solution)
    assert auth_client.get(f"/lesson/{SECOND.slug}").status_code == 200


def test_correct_answer_awards_xp_once(auth_client, user):
    _, first = check(auth_client, FIRST, FIRST.solution)
    assert first["passed"] is True
    assert first["xp_gained"] == FIRST.xp
    assert first["first_time"] is True

    _, again = check(auth_client, FIRST, FIRST.solution)
    assert again["passed"] is True
    assert again["xp_gained"] == 0, "XP must not be farmed by resubmitting"
    assert again["first_time"] is False
    assert user.xp == FIRST.xp


def test_wrong_answer_reports_each_failing_check(auth_client):
    _, data = check(auth_client, FIRST, 'print("something else")')
    assert data["passed"] is False
    assert any(not result["passed"] for result in data["results"])
    assert all("label" in result for result in data["results"])


def test_wrong_answer_does_not_complete_the_lesson(auth_client, user):
    check(auth_client, FIRST, 'print("nope")')
    row = LessonProgress.query.filter_by(user_id=user.id, lesson_slug=FIRST.slug).first()
    assert row.completed is False
    assert user.xp == 0


def test_attempts_are_counted_and_code_is_saved(auth_client, user):
    check(auth_client, FIRST, 'print("try one")')
    check(auth_client, FIRST, 'print("try two")')
    row = LessonProgress.query.filter_by(user_id=user.id, lesson_slug=FIRST.slug).first()
    assert row.attempts == 2
    assert row.saved_code == 'print("try two")'

    page = auth_client.get(f"/lesson/{FIRST.slug}")
    assert b"try two" in page.data, "saved code should reappear in the editor"


def test_run_endpoint_shows_output_without_grading(auth_client, user):
    response = auth_client.post(
        f"/api/run/{FIRST.slug}",
        data=json.dumps({"code": 'print("just looking")', "stdin": ""}),
        content_type="application/json",
    )
    data = response.get_json()
    assert data["graded"] is False
    assert "just looking" in data["stdout"]
    assert LessonProgress.query.filter_by(user_id=user.id).first().attempts == 0


def test_dangerous_code_is_refused_by_the_endpoint(auth_client):
    _, data = check(auth_client, FIRST, "import os\nprint(os.listdir('/'))")
    assert data["passed"] is False
    assert data["error"]["type"] == "NotAllowed"


def test_solution_is_locked_until_enough_attempts(auth_client):
    assert auth_client.get(f"/api/solution/{FIRST.slug}").status_code == 403
    for _ in range(4):
        check(auth_client, FIRST, 'print("wrong")')
    response = auth_client.get(f"/api/solution/{FIRST.slug}")
    assert response.status_code == 200
    assert response.get_json()["solution"] == FIRST.solution


def test_solution_unlocks_immediately_after_passing(auth_client):
    check(auth_client, FIRST, FIRST.solution)
    assert auth_client.get(f"/api/solution/{FIRST.slug}").status_code == 200


def test_submission_history_is_capped(auth_client, user):
    for i in range(progress.SUBMISSION_HISTORY + 5):
        check(auth_client, FIRST, f'print("attempt {i}")')
    stored = Submission.query.filter_by(user_id=user.id, lesson_slug=FIRST.slug).count()
    assert stored <= progress.SUBMISSION_HISTORY


def test_unknown_lesson_is_a_404(auth_client):
    assert auth_client.get("/lesson/not-a-lesson").status_code == 404
    assert auth_client.get("/track/not-a-track").status_code == 404


def test_streak_increments_once_per_day(app, user):
    progress.touch_streak(user)
    assert user.streak_days == 1
    progress.touch_streak(user)
    assert user.streak_days == 1, "practising twice in a day is still one day"

    user.last_active_on = date.today() - timedelta(days=1)
    progress.touch_streak(user)
    assert user.streak_days == 2


def test_streak_resets_after_a_missed_day(app, user):
    """Build a real six-day run, miss a day, and keep the personal best."""
    for _ in range(6):
        # Pretend the last visit was yesterday, so each call is a new day.
        user.last_active_on = date.today() - timedelta(days=1)
        progress.touch_streak(user)
    assert user.streak_days == 6
    assert user.longest_streak == 6

    user.last_active_on = date.today() - timedelta(days=3)
    progress.touch_streak(user)
    assert user.streak_days == 1
    assert user.longest_streak == 6, "a broken streak must not erase the best"


def test_first_lesson_awards_the_first_steps_badge(auth_client, user):
    _, data = check(auth_client, FIRST, FIRST.solution)
    names = [badge["name"] for badge in data["new_badges"]]
    assert "First Steps" in names
    assert any(award for _, award in badges.awarded(user))


def test_badges_are_not_awarded_twice(auth_client, user):
    check(auth_client, FIRST, FIRST.solution)
    before = user.badges.count()
    badges.evaluate(user)
    assert user.badges.count() == before


def test_persistence_badge_needs_five_attempts(auth_client, user):
    for _ in range(5):
        check(auth_client, FIRST, 'print("nope")')
    _, data = check(auth_client, FIRST, FIRST.solution)
    assert "Persistent" in [badge["name"] for badge in data["new_badges"]]


def test_completing_a_track_awards_its_badge(app, user):
    for lesson in TRACKS[0].lessons:
        progress.complete_lesson(user, lesson.slug, lesson.solution)
    fresh = badges.evaluate(user)
    assert "track-foundations" in [badge.slug for badge in fresh]


def test_levels_rise_with_xp(app, user):
    assert user.level == 1
    user.xp = 99
    assert user.level == 1
    user.xp = 100
    assert user.level == 2
    user.xp = 250
    assert user.level == 3
    earned, needed = user.xp_into_level
    assert earned == 0 and needed == 200


def test_recommended_lesson_follows_the_learners_age(app, user):
    track, lesson = progress.recommended_lesson(user)
    assert track.slug == user.suggested_track
    assert lesson is track.lessons[0]

    progress.complete_lesson(user, track.lessons[0].slug, "x = 1")
    _, following = progress.recommended_lesson(user)
    assert following is track.lessons[1]


def test_dashboard_shows_progress(auth_client):
    check(auth_client, FIRST, FIRST.solution)
    response = auth_client.get("/dashboard")
    assert response.status_code == 200
    assert b"Total XP" in response.data


def test_dashboard_links_to_the_glossary(auth_client):
    from app.curriculum import glossary_entries

    response = auth_client.get("/dashboard")
    body = response.data.decode()
    assert 'href="/glossary"' in body
    assert f"{len(glossary_entries())} terms" in body


def test_playground_runs_free_code(auth_client):
    response = auth_client.post(
        "/api/playground",
        data=json.dumps({"code": "print(2 ** 10)", "stdin": ""}),
        content_type="application/json",
    )
    assert response.get_json()["stdout"].strip() == "1024"


def test_track_pages_render(auth_client):
    assert auth_client.get("/tracks").status_code == 200
    for track in TRACKS:
        assert auth_client.get(f"/track/{track.slug}").status_code == 200


def test_progress_is_private_to_each_account(app, client):
    from conftest import make_user

    alice = make_user("alice")
    bob = make_user("bob")
    progress.complete_lesson(alice, FIRST.slug, "print('hi')")

    assert progress.completed_map(bob) == {}
    assert len(progress.completed_map(alice)) == 1
