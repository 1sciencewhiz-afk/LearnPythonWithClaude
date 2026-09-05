"""Web forms with validation."""
from __future__ import annotations

import re
from datetime import date

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    ValidationError,
)

from .models import User

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")


def birth_year_choices() -> list[tuple[str, str]]:
    """Years that put a learner inside the supported age range."""
    this_year = date.today().year
    oldest = this_year - current_app.config["MAX_SIGNUP_AGE"]
    youngest = this_year - current_app.config["MIN_SIGNUP_AGE"]
    return [("", "Choose your birth year")] + [
        (str(year), str(year)) for year in range(youngest, oldest - 1, -1)
    ]


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 32)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    birth_year = SelectField("Birth year", validators=[DataRequired()], choices=[])
    guardian_email = StringField(
        "Parent or guardian email", validators=[Optional(), Email(), Length(max=255)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    confirm = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password", "Both passwords must match.")]
    )
    accept = BooleanField("I have permission to create this account.", validators=[DataRequired()])
    submit = SubmitField("Create my account")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.birth_year.choices = birth_year_choices()

    # -- field validation ------------------------------------------------
    def validate_username(self, field) -> None:
        if not USERNAME_RE.match(field.data or ""):
            raise ValidationError("Use 3-32 letters, numbers or underscores only.")
        if User.query.filter(db_lower(User.username) == field.data.lower()).first():
            raise ValidationError("That username is taken. Try another.")

    def validate_email(self, field) -> None:
        if User.query.filter(db_lower(User.email) == field.data.lower()).first():
            raise ValidationError("There is already an account with that email.")

    def validate_birth_year(self, field) -> None:
        try:
            year = int(field.data)
        except (TypeError, ValueError):
            raise ValidationError("Please choose your birth year.") from None

        age = date.today().year - year
        low = current_app.config["MIN_SIGNUP_AGE"]
        high = current_app.config["MAX_SIGNUP_AGE"]
        if not low <= age <= high:
            raise ValidationError(f"This course is built for ages {low} to {high}.")

    def validate(self, extra_validators=None) -> bool:
        """Cross-field rule: under-13s need a guardian on the account.

        This lives here rather than in a ``validate_guardian_email`` method
        because ``Optional()`` raises StopValidation on an empty field, which
        would skip a per-field validator entirely.
        """
        valid = super().validate(extra_validators)

        try:
            age = date.today().year - int(self.birth_year.data)
        except (TypeError, ValueError):
            return valid

        if age < current_app.config["GUARDIAN_REQUIRED_UNDER_AGE"] and not self.guardian_email.data:
            self.guardian_email.errors = list(self.guardian_email.errors) + [
                "Because you are under 13, a parent or guardian email is required."
            ]
            valid = False

        return valid

    def validate_password(self, field) -> None:
        value = field.data or ""
        if value.lower() in {"password", "12345678", "letmein", "qwertyui"}:
            raise ValidationError("That password is far too easy to guess.")
        if value.isdigit() or value.isalpha():
            raise ValidationError("Mix letters and numbers to make it harder to guess.")
        if self.username.data and self.username.data.lower() in value.lower():
            raise ValidationError("Do not put your username in your password.")


class LoginForm(FlaskForm):
    identifier = StringField("Username or email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Keep me logged in on this device")
    submit = SubmitField("Log in")


class ProfileForm(FlaskForm):
    display_name = StringField("Display name", validators=[Optional(), Length(max=64)])
    guardian_email = StringField(
        "Parent or guardian email", validators=[Optional(), Email(), Length(max=255)]
    )
    submit = SubmitField("Save changes")


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    password = PasswordField("New password", validators=[DataRequired(), Length(8, 128)])
    confirm = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("password", "Both passwords must match.")],
    )
    submit = SubmitField("Change password")

    def validate_password(self, field) -> None:
        value = field.data or ""
        if value.isdigit() or value.isalpha():
            raise ValidationError("Mix letters and numbers to make it harder to guess.")


def db_lower(column):
    """Case-insensitive comparison helper (SQLite's LOWER works on ASCII)."""
    from sqlalchemy import func

    return func.lower(column)


class DeleteAccountForm(FlaskForm):
    confirm_username = StringField("Type your username to confirm", validators=[DataRequired()])
    submit = SubmitField("Delete my account permanently")
