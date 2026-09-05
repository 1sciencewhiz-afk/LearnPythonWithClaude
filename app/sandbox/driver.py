"""Harness executed *inside* the sandbox subprocess.

Reads ``spec.json`` from the working directory, runs the learner's code
against each check, and writes a JSON report to stdout.  Nothing in this
file is trusted with anything the parent process cares about: it is a
throw-away script in a throw-away directory.
"""
from __future__ import annotations

import io
import json
import re
import sys
import traceback
from pathlib import Path

# The parent process truncates our stdout, so the JSON report must stay
# comfortably under its cap or it becomes unparseable. Captured program
# output is clipped well before that point.
MAX_STREAM_BYTES = 16 * 1024
MAX_REPORTED_CHARS = 4000


class OutputTooLong(Exception):
    pass


class CappedWriter(io.StringIO):
    """StringIO that refuses to grow past a cap, so runaway prints fail fast."""

    def write(self, s: str) -> int:  # type: ignore[override]
        if self.tell() + len(s) > MAX_STREAM_BYTES:
            raise OutputTooLong("Your program printed too much text.")
        return super().write(s)


def clip(text: str, limit: int = MAX_REPORTED_CHARS) -> str:
    """Keep reported output small enough for the parent to read back."""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... output trimmed ..."


def friendly_error(exc: BaseException) -> dict:
    """Turn a traceback into something a 12-year-old can act on."""
    if isinstance(exc, SyntaxError):
        line = exc.lineno or 0
        return {
            "type": "SyntaxError",
            "message": f"Python could not read line {line}: {exc.msg}.",
            "line": line,
            "hint": "Check for a missing ':', quote, or bracket on that line.",
        }
    if isinstance(exc, OutputTooLong):
        return {
            "type": "OutputTooLong",
            "message": str(exc),
            "line": None,
            "hint": "Do you have a loop that never stops printing?",
        }

    # Find the deepest frame that belongs to the learner's own file.
    line = None
    for frame in traceback.extract_tb(exc.__traceback__):
        if frame.filename.endswith("solution.py"):
            line = frame.lineno

    name = type(exc).__name__
    hints = {
        "NameError": "Did you spell the name the same way everywhere, and create it before using it?",
        "TypeError": "Check the types you are combining - you may need int() or str().",
        "ValueError": "A value had the right type but the wrong content, e.g. int('hello').",
        "IndexError": "You asked for a position that does not exist in the list.",
        "KeyError": "That key is not in the dictionary.",
        "ZeroDivisionError": "Something divided by zero. Guard against it with an if.",
        "IndentationError": "Check that the lines inside a block are indented the same amount.",
        "RecursionError": "A function kept calling itself. Make sure it has a stopping case.",
        "AttributeError": "That object does not have the thing you asked for.",
        "EOFError": "The program asked for input() but there was none left.",
        "MemoryError": "Your code tried to build something far too big to fit in memory.",
    }
    detail = str(exc)
    return {
        "type": name,
        "message": f"{name}: {detail}" if detail else name,
        "line": line,
        "hint": hints.get(name, "Read the error name - it usually says what went wrong."),
    }


def run_source(source: str, stdin_text: str) -> tuple[dict, dict | None]:
    """Execute the learner's code in a fresh namespace.

    Returns ``(result, namespace)`` where namespace is None if it crashed.
    """
    out, err = CappedWriter(), CappedWriter()
    namespace: dict = {"__name__": "__main__", "__file__": "solution.py"}
    real_stdin, real_stdout, real_stderr = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = io.StringIO(stdin_text), out, err
    error = None
    try:
        compiled = compile(source, "solution.py", "exec")
        exec(compiled, namespace)  # noqa: S102 - this is the point of the sandbox
    except BaseException as exc:  # noqa: BLE001 - report everything to the learner
        error = friendly_error(exc)
        namespace = None  # type: ignore[assignment]
    finally:
        sys.stdin, sys.stdout, sys.stderr = real_stdin, real_stdout, real_stderr

    return {"stdout": clip(out.getvalue()), "stderr": clip(err.getvalue()), "error": error}, namespace


def normalise(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def values_match(actual, expected) -> bool:
    if isinstance(expected, float) or isinstance(actual, float):
        try:
            return abs(float(actual) - float(expected)) < 1e-6
        except (TypeError, ValueError):
            return False
    if isinstance(expected, list) and isinstance(actual, tuple):
        actual = list(actual)
    return actual == expected


def check_stdout(check: dict, source: str) -> dict:
    result, _ = run_source(source, check.get("stdin", ""))
    if result["error"]:
        return {"passed": False, "error": result["error"], "got": result["stdout"]}

    got = normalise(result["stdout"])
    mode = check.get("match", "exact")
    expected = check.get("expect", "")

    if mode == "exact":
        passed = got == normalise(str(expected))
    elif mode == "contains":
        needles = expected if isinstance(expected, list) else [expected]
        passed = all(str(n).lower() in got.lower() for n in needles)
    elif mode == "regex":
        passed = re.search(str(expected), got, re.MULTILINE) is not None
    elif mode == "lines":
        passed = [line.strip() for line in got.split("\n") if line.strip()] == [
            str(line).strip() for line in expected
        ]
    else:
        passed = got == normalise(str(expected))

    return {"passed": passed, "got": clip(got, 1200), "expected": expected, "match": mode}


def check_call(check: dict, source: str) -> dict:
    result, namespace = run_source(source, check.get("stdin", ""))
    if result["error"]:
        return {"passed": False, "error": result["error"], "got": None}

    func_name = check["func"]
    func = namespace.get(func_name)
    if func is None:
        return {
            "passed": False,
            "error": {
                "type": "MissingFunction",
                "message": f"No function called {func_name}() was found.",
                "line": None,
                "hint": f"Define it with: def {func_name}(...):",
            },
            "got": None,
        }
    if not callable(func):
        return {
            "passed": False,
            "error": {
                "type": "NotAFunction",
                "message": f"{func_name} exists but is not a function.",
                "line": None,
                "hint": f"Use 'def {func_name}(...):' to make it a function.",
            },
            "got": None,
        }

    args = check.get("args", [])
    kwargs = check.get("kwargs", {})
    out = CappedWriter()
    real_stdout, real_stdin = sys.stdout, sys.stdin
    sys.stdout, sys.stdin = out, io.StringIO(check.get("stdin", ""))
    try:
        value = func(*args, **kwargs)
    except BaseException as exc:  # noqa: BLE001
        return {"passed": False, "error": friendly_error(exc), "got": None}
    finally:
        sys.stdout, sys.stdin = real_stdout, real_stdin

    expected = check.get("expect")
    return {
        "passed": values_match(value, expected),
        "got": clip(repr(value), 1200),
        "expected": repr(expected),
        "call": f"{func_name}({', '.join(repr(a) for a in args)})",
    }


def check_source(check: dict, source: str) -> dict:
    for pattern in check.get("must_contain", []):
        if not re.search(pattern, source):
            return {"passed": False, "got": None, "expected": check.get("describe", pattern)}
    for pattern in check.get("must_not_contain", []):
        if re.search(pattern, source):
            return {"passed": False, "got": None, "expected": check.get("describe", pattern)}
    return {"passed": True, "got": None, "expected": check.get("describe", "")}


CHECKERS = {"stdout": check_stdout, "call": check_call, "source": check_source}


def main() -> None:
    spec = json.loads(Path("spec.json").read_text(encoding="utf-8"))
    source = Path("solution.py").read_text(encoding="utf-8")

    if spec.get("mode") == "run":
        result, _ = run_source(source, spec.get("stdin", ""))
        print(json.dumps({"mode": "run", **result}))
        return

    results = []
    for check in spec.get("checks", []):
        checker = CHECKERS.get(check.get("kind", "stdout"), check_stdout)
        try:
            outcome = checker(check, source)
        except BaseException as exc:  # noqa: BLE001
            outcome = {"passed": False, "error": friendly_error(exc), "got": None}
        outcome["label"] = check.get("label", "Check")
        results.append(outcome)

    preview, _ = run_source(source, spec.get("stdin", ""))
    print(
        json.dumps(
            {
                "mode": "check",
                "results": results,
                "passed": all(r["passed"] for r in results) and bool(results),
                "stdout": preview["stdout"],
                "stderr": preview["stderr"],
                "error": preview["error"],
            }
        )
    )


if __name__ == "__main__":
    main()
