"""The sandbox is the security boundary, so it gets the most attention."""
from __future__ import annotations

import pytest

from app.sandbox import execute, prescan


def test_runs_simple_program():
    result = execute('print("hello")')
    assert result.ok
    assert result.stdout.strip() == "hello"
    assert result.error is None


def test_reports_syntax_error_with_line_number():
    result = execute('print("unclosed\n')
    assert result.error["type"] == "SyntaxError"
    assert result.error["line"] == 1
    assert result.error["hint"]


def test_reports_runtime_error_with_friendly_hint():
    result = execute("print(missing_name)")
    assert result.error["type"] == "NameError"
    assert "spell" in result.error["hint"].lower()


@pytest.mark.parametrize(
    "source",
    [
        "import os",
        "import   subprocess",
        "from socket import socket",
        "import shutil as s",
        "open('/etc/passwd')",
        "eval('1+1')",
        "__import__('os')",
    ],
)
def test_blocks_dangerous_source(source):
    assert prescan(source) is not None
    assert execute(source).error["type"] == "NotAllowed"


@pytest.mark.parametrize("source", ["import math", "import random", "from datetime import date"])
def test_allows_safe_modules(source):
    assert prescan(source) is None


def test_infinite_loop_is_stopped():
    result = execute("while True:\n    pass", timeout=2)
    assert result.timed_out
    assert result.error["type"] == "Timeout"


def test_memory_bomb_is_stopped():
    result = execute("x = [0] * 10 ** 9", timeout=5, memory_mb=64)
    assert not result.passed
    assert result.error is not None


def test_runaway_printing_is_stopped():
    result = execute('while True:\n    print("x" * 100)', timeout=5)
    assert result.error is not None
    assert result.error["type"] in {"OutputTooLong", "Timeout", "RunnerError"}


def test_empty_source_is_rejected():
    assert execute("   \n  ").error["type"] == "NotAllowed"


def test_oversized_source_is_rejected():
    assert execute("x = 1\n" * 20000, max_source=100).error["type"] == "NotAllowed"


def test_stdin_is_delivered():
    result = execute("print(input().upper())", stdin="quiet\n")
    assert result.stdout.strip() == "QUIET"


def test_call_check_passes_and_fails():
    checks = [{"kind": "call", "func": "double", "args": [3], "expect": 6, "label": "double(3)"}]
    assert execute("def double(n):\n    return n * 2", checks=checks).passed
    assert not execute("def double(n):\n    return n + 2", checks=checks).passed


def test_call_check_reports_missing_function():
    checks = [{"kind": "call", "func": "nope", "args": [], "expect": 1, "label": "nope()"}]
    result = execute("x = 1", checks=checks)
    assert not result.passed
    assert result.results[0]["error"]["type"] == "MissingFunction"


def test_stdout_match_modes():
    assert execute('print("a")\nprint("b")', checks=[
        {"kind": "stdout", "expect": ["a", "b"], "match": "lines", "label": "lines"}
    ]).passed
    assert execute('print("Total: 42")', checks=[
        {"kind": "stdout", "expect": "total", "match": "contains", "label": "contains"}
    ]).passed
    assert execute('print("x=7")', checks=[
        {"kind": "stdout", "expect": r"x=\d+", "match": "regex", "label": "regex"}
    ]).passed


def test_source_check_enforces_technique():
    checks = [{
        "kind": "source",
        "must_contain": [r"\bfor\b"],
        "describe": "uses a for loop",
        "label": "loop",
    }]
    assert execute("for i in range(2):\n    print(i)", checks=checks).passed
    assert not execute("print(0)\nprint(1)", checks=checks).passed


def test_trailing_whitespace_does_not_fail_a_learner():
    checks = [{"kind": "stdout", "expect": "hi", "label": "hi"}]
    assert execute('print("hi   ")', checks=checks).passed
    assert execute('print("hi")\nprint()', checks=checks).passed


def test_each_run_gets_a_fresh_namespace():
    """State must not leak between the checks of one submission."""
    source = "counter = counter + 1 if 'counter' in dir() else 1\nprint(counter)"
    checks = [
        {"kind": "stdout", "expect": "1", "label": "first"},
        {"kind": "stdout", "expect": "1", "label": "second"},
    ]
    assert execute(source, checks=checks).passed
