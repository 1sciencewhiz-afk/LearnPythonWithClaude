"""Application factory for Learn Python With Claude."""
from __future__ import annotations

import os
from pathlib import Path

import click
from flask import Flask, render_template

from .config import get_config
from .extensions import csrf, db, login_manager

__all__ = ["create_app"]


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    _warn_about_default_secret(app)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .blueprints.auth import bp as auth_bp
    from .blueprints.learn import bp as learn_bp
    from .blueprints.main import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(learn_bp)

    _register_errors(app)
    _register_context(app)
    _register_cli(app)
    _register_headers(app)

    with app.app_context():
        db.create_all()

    return app


def _warn_about_default_secret(app: Flask) -> None:
    if app.config["SECRET_KEY"] == "dev-only-change-me" and not app.config.get("TESTING"):
        app.logger.warning(
            "SECRET_KEY is the built-in default. Set the SECRET_KEY environment "
            "variable before letting anyone else use this server."
        )


def _register_errors(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def server_error(_error):  # pragma: no cover - exercised only on real failures
        db.session.rollback()
        return render_template("errors/500.html"), 500


def _register_context(app: Flask) -> None:
    from .curriculum import TRACKS

    @app.context_processor
    def inject_globals():
        return {"all_tracks": TRACKS, "site_name": "Learn Python With Claude"}


def _register_headers(app: Flask) -> None:
    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        # No third-party scripts, styles or frames anywhere in the app.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; "
            "script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
        )
        return response


def _register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db() -> None:
        """Create the database tables."""
        db.create_all()
        click.echo("Database ready.")

    @app.cli.command("reset-db")
    @click.confirmation_option(prompt="This deletes every account. Continue?")
    def reset_db() -> None:
        """Drop and recreate every table."""
        db.drop_all()
        db.create_all()
        click.echo("Database reset.")

    @app.cli.command("create-demo-user")
    def create_demo_user() -> None:
        """Add a demo learner so you can click around immediately."""
        from .models import User

        if User.query.filter_by(username="demo").first():
            click.echo("Demo user already exists.")
            return
        user = User(
            username="demo",
            email="demo@example.com",
            display_name="Demo Learner",
            birth_year=int(os.environ.get("DEMO_BIRTH_YEAR", "2011")),
        )
        user.set_password("demo-pass-1")
        db.session.add(user)
        db.session.commit()
        click.echo("Created user 'demo' with password 'demo-pass-1'.")

    @app.cli.command("check-curriculum")
    def check_curriculum() -> None:
        """Run every reference solution against its own checks."""
        from .curriculum import TRACKS
        from .sandbox import execute

        failures = 0
        for track in TRACKS:
            for lesson in track.lessons:
                result = execute(lesson.solution, checks=lesson.checks, timeout=10)
                status = "ok" if result.passed else "FAILED"
                if not result.passed:
                    failures += 1
                click.echo(f"[{status}] {track.slug}/{lesson.slug}")
        click.echo(f"{failures} failing lesson(s).")
        raise SystemExit(1 if failures else 0)
