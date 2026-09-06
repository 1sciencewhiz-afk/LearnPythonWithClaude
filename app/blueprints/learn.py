"""Track listings, the lesson player, and the code-running endpoints."""
from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from ..curriculum import TRACKS, get_lesson, get_track, lesson_position, neighbours, track_for_lesson
from ..extensions import db
from ..ratelimit import limit
from ..sandbox import execute
from ..services import badges, progress, tutor

bp = Blueprint("learn", __name__)

# Attempts before the reference solution is offered, so a stuck learner is
# never permanently blocked but is not handed the answer straight away.
ATTEMPTS_BEFORE_SOLUTION = 4


@bp.route("/tracks")
@login_required
def tracks():
    return render_template(
        "learn/tracks.html",
        summaries=progress.all_track_summaries(current_user),
        suggested=current_user.suggested_track,
    )


@bp.route("/track/<track_slug>")
@login_required
def track_detail(track_slug: str):
    track = get_track(track_slug)
    if track is None:
        abort(404)

    rows = progress.completed_map(current_user)
    lessons = []
    unlocked = True
    for lesson in track.lessons:
        row = rows.get(lesson.slug)
        done = bool(row and row.completed)
        lessons.append({"lesson": lesson, "row": row, "done": done, "unlocked": unlocked})
        # The next lesson unlocks once this one is finished; the first is
        # always open so nobody is stuck at a locked front door.
        unlocked = done

    return render_template(
        "learn/track.html",
        track=track,
        lessons=lessons,
        summary=progress.track_summary(current_user, track),
    )


def _lesson_or_404(lesson_slug: str):
    lesson = get_lesson(lesson_slug)
    if lesson is None:
        abort(404)
    return lesson


def _is_unlocked(lesson_slug: str) -> bool:
    """A lesson opens when the one before it in the track is complete."""
    track = track_for_lesson(lesson_slug)
    if track is None:
        return False
    previous, _ = neighbours(lesson_slug)
    if previous is None:
        return True
    rows = progress.completed_map(current_user)
    row = rows.get(previous.slug)
    return bool(row and row.completed)


@bp.route("/lesson/<lesson_slug>")
@login_required
def lesson(lesson_slug: str):
    lesson = _lesson_or_404(lesson_slug)
    track = track_for_lesson(lesson_slug)

    if not _is_unlocked(lesson_slug):
        return redirect(url_for("learn.track_detail", track_slug=track.slug))

    row = progress.get_or_create(current_user, lesson_slug)
    index, total = lesson_position(lesson_slug)
    previous, following = neighbours(lesson_slug)

    return render_template(
        "learn/lesson.html",
        lesson=lesson,
        track=track,
        row=row,
        code=row.saved_code or lesson.starter,
        index=index,
        total=total,
        previous=previous,
        following=following,
        show_solution=row.completed or row.attempts >= ATTEMPTS_BEFORE_SOLUTION,
        attempts_before_solution=ATTEMPTS_BEFORE_SOLUTION,
        tutor_enabled=bool(current_app.config.get("GEMINI_API_KEY")),
    )


def _sandbox_kwargs() -> dict:
    config = current_app.config
    return {
        "timeout": config["SANDBOX_TIMEOUT_SECONDS"],
        "memory_mb": config["SANDBOX_MEMORY_MB"],
        "max_output": config["SANDBOX_MAX_OUTPUT_BYTES"],
        "max_source": config["SANDBOX_MAX_SOURCE_BYTES"],
    }


@bp.post("/api/run/<lesson_slug>")
@login_required
@limit(40, 60)
def run_code(lesson_slug: str):
    """Run the learner's code and show the output, without grading it."""
    _lesson_or_404(lesson_slug)
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")

    result = execute(code, stdin=payload.get("stdin", ""), **_sandbox_kwargs())

    row = progress.get_or_create(current_user, lesson_slug)
    row.saved_code = code
    db.session.commit()

    return jsonify({"graded": False, **result.to_dict()})


@bp.post("/api/check/<lesson_slug>")
@login_required
@limit(40, 60)
def check_code(lesson_slug: str):
    """Grade the learner's code against the lesson's checks."""
    lesson = _lesson_or_404(lesson_slug)
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")

    result = execute(
        code, checks=lesson.checks, stdin=payload.get("stdin", ""), **_sandbox_kwargs()
    )

    row = progress.record_attempt(current_user, lesson_slug, code, result.passed)
    response = {"graded": True, **result.to_dict(), "attempts": row.attempts}

    if result.passed:
        was_complete = row.completed
        row, gained = progress.complete_lesson(current_user, lesson_slug, code)
        fresh = badges.evaluate(current_user, attempts=row.attempts)
        _, following = neighbours(lesson_slug)
        response.update(
            {
                "xp_gained": gained,
                "first_time": not was_complete,
                "total_xp": current_user.xp,
                "level": current_user.level,
                "streak": current_user.streak_days,
                "new_badges": [
                    {"name": badge.name, "emoji": badge.emoji, "description": badge.description}
                    for badge in fresh
                ],
                "next_url": url_for("learn.lesson", lesson_slug=following.slug) if following else None,
                "next_title": following.title if following else None,
            }
        )
    else:
        response["show_solution"] = row.attempts >= ATTEMPTS_BEFORE_SOLUTION

    return jsonify(response)


@bp.get("/api/solution/<lesson_slug>")
@login_required
def solution(lesson_slug: str):
    """The reference solution, once it has been unlocked."""
    lesson = _lesson_or_404(lesson_slug)
    row = progress.get_or_create(current_user, lesson_slug)
    if not (row.completed or row.attempts >= ATTEMPTS_BEFORE_SOLUTION):
        return jsonify({"available": False, "attempts_needed": ATTEMPTS_BEFORE_SOLUTION - row.attempts}), 403
    return jsonify({"available": True, "solution": lesson.solution})


@bp.post("/api/tutor/<lesson_slug>")
@login_required
@limit(12, 60)
def tutor_help(lesson_slug: str):
    """Ask the AI tutor sidebar for a nudge. It never sees the reference solution."""
    lesson = _lesson_or_404(lesson_slug)

    if not current_app.config.get("GEMINI_API_KEY"):
        return jsonify({"ok": False, "error": "The AI tutor is not turned on for this server."}), 503

    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"ok": False, "error": "Type a question first."}), 400
    if len(message) > 2000:
        return jsonify({"ok": False, "error": "That message is a bit long - try shortening it."}), 400

    history = payload.get("history")
    if not isinstance(history, list):
        history = []

    last_result = payload.get("last_result")
    if not isinstance(last_result, dict):
        last_result = {}
    last_error = last_result.get("error")
    failed_checks = [
        str(item.get("label", "")).strip()
        for item in (last_result.get("results") or [])
        if isinstance(item, dict) and not item.get("passed") and item.get("label")
    ]

    context = tutor.TutorContext(
        lesson=lesson,
        code=str(payload.get("code", "")),
        stdout=str(last_result.get("stdout", "")),
        stderr=str(last_result.get("stderr", "")),
        error=last_error if isinstance(last_error, dict) else None,
        failed_checks=failed_checks,
    )

    try:
        reply = tutor.ask_tutor(current_app.config, context, history, message)
    except tutor.TutorError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502

    return jsonify({"ok": True, "reply": reply})


@bp.route("/playground")
@login_required
def playground():
    return render_template("learn/playground.html", tracks=TRACKS)


@bp.post("/api/playground")
@login_required
@limit(40, 60)
def playground_run():
    payload = request.get_json(silent=True) or {}
    result = execute(payload.get("code", ""), stdin=payload.get("stdin", ""), **_sandbox_kwargs())
    return jsonify(result.to_dict())
