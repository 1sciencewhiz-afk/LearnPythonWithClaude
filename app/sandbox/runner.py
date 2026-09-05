"""Runs learner-submitted Python in an isolated child process.

Layers of containment, weakest to strongest:

1.  A source pre-scan that rejects obviously off-limits imports with a
    friendly message.  This is a teaching aid, *not* a security control -
    it is trivially bypassable and is treated as such.
2.  A throw-away working directory, a stripped environment, and CPython's
    isolated mode (``-I``) so nothing from the host leaks in.
3.  POSIX resource limits (CPU, address space, file size, process count)
    applied in the child before ``exec``.
4.  A wall-clock timeout enforced by the parent, which kills the whole
    process group.

Layers 2-4 hold even when 1 is bypassed.  For a public deployment you
should still put the whole app behind an OS-level sandbox (a container
with no network namespace, seccomp, or gVisor) - see README.md.
"""
from __future__ import annotations

import json
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

DRIVER_PATH = Path(__file__).with_name("driver.py")

# Modules that let code reach outside the lesson. Blocked with a friendly
# message so learners get an explanation rather than a mystery failure.
BLOCKED_MODULES = {
    "os", "sys", "subprocess", "socket", "shutil", "pathlib", "ctypes",
    "multiprocessing", "threading", "importlib", "urllib", "http", "requests",
    "pickle", "marshal", "tempfile", "glob", "webbrowser", "signal", "resource",
    "builtins", "gc", "inspect", "code", "codeop", "pty", "fcntl", "mmap",
}
BLOCKED_NAMES = {"__import__", "eval", "exec", "compile", "open", "globals", "vars"}

_IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_][\w.]*)", re.MULTILINE)


@dataclass
class SandboxResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    error: dict | None = None
    results: list[dict] = field(default_factory=list)
    passed: bool = False
    timed_out: bool = False

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error": self.error,
            "results": self.results,
            "passed": self.passed,
            "timed_out": self.timed_out,
        }


def _blocked_error(message: str, hint: str) -> SandboxResult:
    return SandboxResult(
        ok=False,
        error={"type": "NotAllowed", "message": message, "line": None, "hint": hint},
    )


def prescan(source: str) -> SandboxResult | None:
    """Reject imports and builtins that lessons never need. Returns None if clean."""
    for module in _IMPORT_RE.findall(source):
        root = module.split(".")[0]
        if root in BLOCKED_MODULES:
            return _blocked_error(
                f"The '{root}' module is switched off in the lesson player.",
                "Lessons only need plain Python plus math, random, string, json and datetime.",
            )
    for name in BLOCKED_NAMES:
        if re.search(rf"\b{re.escape(name)}\s*\(", source):
            return _blocked_error(
                f"'{name}()' is switched off in the lesson player.",
                "Solve the exercise with ordinary Python statements instead.",
            )
    if "__" in source and re.search(r"__[a-z_]+__\s*(?:\[|\.)", source):
        return _blocked_error(
            "Dunder attribute tricks are switched off in the lesson player.",
            "Stick to the Python you are learning in the lesson.",
        )
    return None


def _apply_limits(memory_mb: int, cpu_seconds: int):
    """Returned closure runs in the child, between fork and exec."""

    def _limit() -> None:
        os.setsid()  # own process group, so a timeout can kill every descendant
        nofile = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
        limits = [
            (resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds)),
            (resource.RLIMIT_AS, (memory_mb * 1024 * 1024,) * 2),
            (resource.RLIMIT_FSIZE, (1024 * 1024,) * 2),
            (resource.RLIMIT_NPROC, (64, 64)),
            (resource.RLIMIT_NOFILE, (min(64, nofile),) * 2),
            (resource.RLIMIT_CORE, (0, 0)),
        ]
        for which, values in limits:
            try:
                resource.setrlimit(which, values)
            except (ValueError, OSError):
                pass  # limit unavailable on this platform; others still apply

    return _limit


def _run_child(workdir: Path, timeout: float, memory_mb: int, max_output: int) -> tuple[str, str, bool]:
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(workdir),
        "TMPDIR": str(workdir),
        "LC_ALL": "C.UTF-8",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
    }
    cpu_seconds = max(1, int(timeout) + 1)
    proc = subprocess.Popen(
        [sys.executable, "-I", "-B", "driver.py"],
        cwd=str(workdir),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=_apply_limits(memory_mb, cpu_seconds),  # noqa: PLW1509 - POSIX only
    )
    timed_out = False
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_group(proc)
        stdout, stderr = proc.communicate()
    return stdout[:max_output], stderr[:max_output], timed_out


def _kill_group(proc: subprocess.Popen) -> None:
    for sig in (signal.SIGKILL,):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass


def execute(
    source: str,
    *,
    checks: list[dict] | None = None,
    stdin: str = "",
    timeout: float = 5.0,
    memory_mb: int = 128,
    max_output: int = 20_000,
    max_source: int = 40_000,
) -> SandboxResult:
    """Run ``source``; with ``checks`` it grades, without it just runs."""
    if not source.strip():
        return _blocked_error("There is no code to run yet.", "Write some Python, then press Run.")
    if len(source.encode("utf-8")) > max_source:
        return _blocked_error("That program is too long for the lesson player.", "Try a shorter solution.")

    blocked = prescan(source)
    if blocked is not None:
        return blocked

    spec = {
        "mode": "check" if checks else "run",
        "checks": checks or [],
        "stdin": stdin,
    }

    workdir = Path(tempfile.mkdtemp(prefix="lpwc-"))
    try:
        (workdir / "solution.py").write_text(source, encoding="utf-8")
        (workdir / "spec.json").write_text(json.dumps(spec), encoding="utf-8")
        shutil.copyfile(DRIVER_PATH, workdir / "driver.py")
        os.chmod(workdir, 0o700)

        stdout, stderr, timed_out = _run_child(workdir, timeout, memory_mb, max_output)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    if timed_out:
        return SandboxResult(
            ok=False,
            timed_out=True,
            error={
                "type": "Timeout",
                "message": f"Your code ran for more than {timeout:g} seconds and was stopped.",
                "line": None,
                "hint": "Look for a loop whose condition never becomes False.",
            },
        )

    try:
        payload = json.loads(stdout)
    except (json.JSONDecodeError, ValueError):
        detail = (stderr or "").strip().splitlines()
        message = detail[-1] if detail else "The lesson player could not run that code."
        if "MemoryError" in (stderr or "") or "Cannot allocate" in (stderr or ""):
            message = "Your code tried to use too much memory and was stopped."
        return SandboxResult(ok=False, stderr=stderr, error={
            "type": "RunnerError", "message": message, "line": None,
            "hint": "Check for very large lists or a loop that never ends.",
        })

    return SandboxResult(
        ok=True,
        stdout=payload.get("stdout", ""),
        stderr=payload.get("stderr", ""),
        error=payload.get("error"),
        results=payload.get("results", []),
        passed=bool(payload.get("passed", False)),
    )
