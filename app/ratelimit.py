"""A small in-process rate limiter for the code-execution endpoints.

Each sandbox run costs real CPU, so a single learner (or a script pretending
to be one) should not be able to queue up an unbounded number of them.  This
is per-process and resets on restart, which is fine for a single-instance
deployment; behind multiple workers, move the counter to Redis.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from functools import wraps
from threading import Lock

from flask import jsonify
from flask_login import current_user

_hits: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def _allow(key: str, limit: int, window: float) -> tuple[bool, float]:
    now = time.monotonic()
    with _lock:
        bucket = _hits[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= limit:
            return False, window - (now - bucket[0])
        bucket.append(now)
        return True, 0.0


def limit(limit_count: int = 30, window_seconds: float = 60.0):
    """Allow ``limit_count`` calls per ``window_seconds`` per user and endpoint."""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            who = getattr(current_user, "id", None) or "anonymous"
            key = f"{view.__name__}:{who}"
            ok, wait = _allow(key, limit_count, window_seconds)
            if not ok:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "results": [],
                            "passed": False,
                            "error": {
                                "type": "TooManyRuns",
                                "message": "You are running code very quickly. Take a short breath.",
                                "line": None,
                                "hint": f"Try again in about {int(wait) + 1} seconds.",
                            },
                        }
                    ),
                    429,
                )
            return view(*args, **kwargs)

        return wrapper

    return decorator


def reset() -> None:
    """Clear all counters (used by the test suite)."""
    with _lock:
        _hits.clear()
