# Learn Python With Claude

A self-hosted, account-based web app that teaches Python to learners aged 10-18.
Thirty-four hands-on lessons across three tracks, an in-browser editor, automatic
grading with plain-English error messages, an optional AI tutor sidebar, and
per-account progress, XP, streaks and badges.

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')" .venv/bin/python wsgi.py
# open http://127.0.0.1:5000
```

## What it does

**Accounts.** Sign-up asks for a username, email, birth year and password.
Passwords are hashed with Werkzeug's PBKDF2 and never stored in the clear.
Learners can rename themselves, change their password, and permanently delete
their account along with every row that belongs to it.

**Three tracks**, ordered by difficulty and suggested by age. Every lesson is
gated behind the one before it, so nobody lands in the middle of a topic:

| Track | Suggested age | Lessons | Covers |
|---|---|---|---|
| Foundations | 10-12 | 13 | print, variables, maths, strings, input, if/elif, and/or/not, for, lists, while, functions, random |
| Builders | 13-15 | 11 | default arguments, slicing, sets, dictionaries, string methods, number formatting, nested loops, try/except, modules, comprehensions |
| Creators | 16-18 | 10 | classes, inheritance, recursion, higher-order functions, decorators, generators, binary search, data modelling, testing |

**The lesson player.** Each lesson has teaching copy - including a "why this
matters" explanation of where the idea is actually used, and a "common
mistakes" list of the errors learners hit most - a worked example, a brief,
starter code, three progressive hints, a "key terms" box, and a set of checks.
Learners can *run* their code to see its output, or *check* it to be graded.
Failing checks say what was expected and what the code actually did. The
reference solution unlocks after four attempts, or immediately on passing.

**Glossary.** Every term taught across all three tracks - `variable`,
`f-string`, `decorator`, `binary search`, and around 80 more - is indexed on
one searchable `/glossary` page (`app/curriculum/schema.py`'s `GlossaryTerm`,
aggregated by `curriculum.glossary_entries()`). Each entry links back to the
lesson that first taught it, and each lesson's own "key terms" box links
forward to its entry, so a learner who has forgotten what a `set` is can look
it up and jump straight back to the lesson to revise it.

**Progress.** Passing a lesson for the first time awards its XP; resubmitting
awards none. Levels get progressively longer (100 XP for level 2, then +50 each).
A day streak increments once per calendar day and resets after a missed day, but
never erases the recorded best. Ten badges cover first steps, persistence,
streaks, levels, per-track completion and finishing the course.

**Playground.** A free scratchpad with no grading, under the same safety limits.

**AI tutor sidebar.** A retractable chat panel on every lesson page, powered by
Google's Gemini API. It is entirely optional - the app runs normally without it,
and the panel simply explains that it is turned off until a `GEMINI_API_KEY` is
configured. See [AI tutor](#ai-tutor) below for how it is kept from handing out
answers.

## Running learner code safely

This is the part that matters most, so it is worth reading before you deploy.
`app/sandbox/` runs submitted Python in a child process with four layers of
containment:

1. **A source pre-scan** (`prescan`) rejects imports like `os`, `socket` and
   `subprocess`, plus `eval`/`exec`/`open`, with a friendly explanation. This is a
   *teaching aid, not a security control* — it is trivially bypassable and the
   code treats it that way.
2. **Isolation**: a throw-away working directory, a stripped environment, and
   CPython's isolated mode (`-I`), so nothing from the host leaks in.
3. **POSIX resource limits** applied in the child before `exec`: CPU time,
   address space, file size, process count, open files, and no core dumps.
4. **A wall-clock timeout** enforced by the parent, which kills the entire
   process group.

Layers 2-4 hold even when layer 1 is bypassed. Output is capped inside the child
and again in the parent, so a runaway `print` loop cannot exhaust memory.
Requests to the run/check endpoints are rate limited per account.

**For a public deployment this is not sufficient on its own.** Put the whole
application inside an OS-level sandbox — a container with no network namespace,
a seccomp profile, or gVisor — and treat the process as untrusted. The in-process
limits above raise the cost of an attack; they are not a substitute for kernel
isolation.

## AI tutor

`app/services/tutor.py` calls the Gemini API to give a stuck learner a nudge,
from a chat sidebar on the lesson page (`app/static/js/tutor.js`,
`app/templates/learn/lesson.html`). It is designed so it cannot become an
answer key, with two independent safeguards:

1. **The model is never shown the reference solution.** The prompt built by
   `build_contents()` includes only the lesson's goal, concept, brief, the
   hints already unlocked on the page, the learner's current code, and what
   happened the last time they ran or checked it. There is nothing to leak,
   however the conversation is steered.
2. **Every reply is filtered before it reaches the learner.** `sanitize_reply()`
   strips any multi-line fenced code block out of the response, replacing it
   with a short note. A one-line generic reminder (`if x > 0:`) survives; a
   pasted-in solution does not, regardless of the wording used to ask for it.

The system prompt also instructs the model to teach with questions and small
nudges rather than write code, but the two safeguards above hold even if a
learner talks the model out of following it.

The tutor endpoint (`POST /api/tutor/<lesson_slug>`) is rate limited per
account like the sandbox endpoints, requires login, and returns `503` with a
plain explanation if no `GEMINI_API_KEY` is configured - nothing about the
rest of the app depends on it. No chat history is stored server-side; the
last few turns are kept in the browser tab only and are gone on reload.

## Privacy and younger learners

Only the birth *year* is collected, never a full date of birth. Under-13 sign-ups
require a parent or guardian email on the account, enforced as a cross-field rule
in `RegistrationForm.validate`. There is no chat or profile visible to other
learners, no file uploads, no adverts and no third-party scripts loaded in the
browser — the Content-Security-Policy is `'self'` only, which is why the app
contains no inline styles or scripts. The one exception is the optional AI
tutor: when enabled, a learner's lesson brief, code and last output are sent
server-side to the Gemini API to generate a reply (never their account details,
and never to any other learner). It is off unless an operator sets a
`GEMINI_API_KEY`, and Google's own data-handling terms apply to that traffic -
review them before enabling it for real learners.

Note that a guardian email field is a design commitment, not legal compliance.
If you deploy this publicly, COPPA (US), the UK Age Appropriate Design Code, and
GDPR/GDPR-K (EU) may require verifiable parental consent and a published privacy
notice. That responsibility sits with the operator.

## Layout

```
app/
  __init__.py        application factory, error handlers, security headers, CLI
  config.py          per-environment configuration
  models.py          User, LessonProgress, Submission, BadgeAward
  forms.py           WTForms with the age and password rules
  ratelimit.py       per-user limiter for the sandbox endpoints
  blueprints/        main (landing, dashboard, glossary), auth, learn (player + API)
  curriculum/        schema.py (Lesson, GlossaryTerm) plus one module per track
  sandbox/           runner.py (parent, limits) and driver.py (in-sandbox harness)
  services/          progress.py (XP, streaks), badges.py, tutor.py (Gemini)
  templates/, static/
tests/               sandbox, curriculum, auth, learning flow, app-level
wsgi.py              entry point
```

Adding a lesson means appending a `Lesson` to a track module, with at least one
`GlossaryTerm` in its `glossary` list. The test suite then runs its reference
solution against its own checks, asserts the starter code does *not* already
pass, and asserts the concept copy actually explains why the idea matters and
where learners tend to trip up — so a broken, free, or thin lesson fails CI
rather than reaching a learner.

## Commands

```
.venv/bin/python -m pytest              # 280+ tests
FLASK_APP=wsgi flask init-db            # create tables
FLASK_APP=wsgi flask create-demo-user   # demo / demo-pass-1
FLASK_APP=wsgi flask check-curriculum   # solve every lesson, report failures
FLASK_APP=wsgi flask reset-db           # drop and recreate (destructive)
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | dev placeholder | Session signing. **Set this in production.** |
| `DATABASE_URL` | SQLite in `instance/` | Any SQLAlchemy URL |
| `FLASK_CONFIG` | `development` | `development`, `testing` or `production` |
| `SANDBOX_TIMEOUT_SECONDS` | `5` | Wall-clock limit per run |
| `SANDBOX_MEMORY_MB` | `128` | Address-space limit per run |
| `SESSION_COOKIE_SECURE` | off | Set to `1` behind HTTPS (forced in production config) |
| `GEMINI_API_KEY` | unset | Turns the AI tutor sidebar on. Leave unset to disable it entirely |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model used for tutor replies |
| `GEMINI_API_BASE` | Google's public endpoint | Override for testing or a proxy |
| `GEMINI_TIMEOUT_SECONDS` | `12` | How long to wait for a tutor reply before giving up |

The app logs a warning at startup if `SECRET_KEY` is still the built-in default.

## Deployment notes

Serve with a real WSGI server (`gunicorn wsgi:app`) behind HTTPS, and set
`FLASK_CONFIG=production` so secure cookies are enforced. The rate limiter keeps
its counters in process memory; behind multiple workers, move them to Redis.
Sandbox execution is CPU-bound and synchronous, so size the worker count against
the CPU available rather than the request count.

The sandbox relies on POSIX `resource` limits, `os.setsid` and process groups, so
it requires Linux or another Unix. It does not work on Windows.
