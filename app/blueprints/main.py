"""Landing page, dashboard and static-ish pages."""
from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..curriculum import TRACKS, total_lessons
from ..models import Submission
from ..services import badges, progress

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return dashboard()
    return render_template("index.html", tracks=TRACKS, lesson_count=total_lessons())


@bp.route("/dashboard")
@login_required
def dashboard():
    summaries = progress.all_track_summaries(current_user)
    track, lesson = progress.recommended_lesson(current_user)
    done = sum(summary["done"] for summary in summaries)
    earned = [badge for badge, award in badges.awarded(current_user) if award]
    into_level, needed = current_user.xp_into_level

    return render_template(
        "dashboard.html",
        summaries=summaries,
        next_track=track,
        next_lesson=lesson,
        completed_count=done,
        lesson_count=total_lessons(),
        earned_badges=earned,
        xp_into_level=into_level,
        xp_for_level=needed,
        level_percent=round(into_level / needed * 100) if needed else 0,
        recent=(
            Submission.query.filter_by(user_id=current_user.id)
            .order_by(Submission.created_at.desc(), Submission.id.desc())
            .limit(5)
            .all()
        ),
    )


@bp.route("/badges")
@login_required
def badge_list():
    return render_template("badges.html", badge_rows=badges.awarded(current_user))


@bp.route("/safety")
def safety():
    return render_template("safety.html")
