"""Registration, login, profile and account deletion."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from urllib.parse import urlparse

from ..extensions import db
from ..forms import DeleteAccountForm, LoginForm, PasswordChangeForm, ProfileForm, RegistrationForm
from ..models import User
from ..services import badges

bp = Blueprint("auth", __name__)


def _safe_next(target: str | None) -> str:
    """Only follow a ?next= that points back at this site."""
    if not target:
        return url_for("main.dashboard")
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or not target.startswith("/"):
        return url_for("main.dashboard")
    return target


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            display_name=form.username.data.strip(),
            birth_year=int(form.birth_year.data),
            guardian_email=(form.guardian_email.data or "").strip().lower() or None,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome aboard, {user.display_name}! Pick a track to begin.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = (form.identifier.data or "").strip().lower()
        user = User.query.filter(
            (func.lower(User.username) == identifier) | (func.lower(User.email) == identifier)
        ).first()

        # One message for both failure modes, so the form cannot be used to
        # discover which usernames exist.
        if user is None or not user.check_password(form.password.data):
            flash("That username or password was not right. Try again.", "error")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=form.remember.data)
        badges.evaluate(user)
        return redirect(_safe_next(request.args.get("next")))

    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You are logged out. See you next time!", "info")
    return redirect(url_for("main.index"))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    password_form = PasswordChangeForm()
    delete_form = DeleteAccountForm()

    if form.submit.data and form.validate_on_submit():
        current_user.display_name = (form.display_name.data or current_user.username).strip()
        current_user.guardian_email = (form.guardian_email.data or "").strip().lower() or None
        if current_user.needs_guardian and not current_user.guardian_email:
            flash("A guardian email is required while you are under 13.", "error")
        else:
            db.session.commit()
            flash("Profile saved.", "success")
            return redirect(url_for("auth.profile"))

    if password_form.submit.data and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash("Your current password was not right.", "error")
        else:
            current_user.set_password(password_form.password.data)
            db.session.commit()
            flash("Password changed.", "success")
            return redirect(url_for("auth.profile"))

    return render_template(
        "auth/profile.html",
        form=form,
        password_form=password_form,
        delete_form=delete_form,
        badge_rows=badges.awarded(current_user),
    )


@bp.route("/profile/delete", methods=["POST"])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit() and form.confirm_username.data.strip() == current_user.username:
        user = current_user._get_current_object()
        logout_user()
        db.session.delete(user)  # progress, submissions and badges cascade
        db.session.commit()
        flash("Your account and all its data have been deleted.", "info")
        return redirect(url_for("main.index"))

    flash("Type your username exactly to confirm deletion.", "error")
    return redirect(url_for("auth.profile"))
