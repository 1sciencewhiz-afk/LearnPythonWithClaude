"""WSGI entry point: ``gunicorn wsgi:app`` or ``python wsgi.py``."""
from __future__ import annotations

import os

from dotenv import load_dotenv

# Load a .env file from the project root, if one exists, before app/config.py
# reads its settings from the environment. Real environment variables (set by
# your shell or host) always take precedence over values from .env.
load_dotenv()

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
