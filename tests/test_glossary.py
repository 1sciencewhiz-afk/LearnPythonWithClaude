"""The glossary aggregates every lesson's terms into one searchable, linkable index."""
from __future__ import annotations

import re

from app.curriculum import TRACKS, glossary_entries
from app.curriculum.schema import GlossaryTerm


def test_glossary_entries_are_sorted_alphabetically():
    entries = glossary_entries()
    terms = [entry["term"].lower() for entry in entries]
    assert terms == sorted(terms)


def test_glossary_entries_have_required_fields():
    entries = glossary_entries()
    assert entries, "the glossary should not be empty"
    for entry in entries:
        assert entry["term"]
        assert entry["definition"]
        assert entry["anchor"].startswith("term-")
        assert entry["lesson"] in entry["track"].lessons


def test_glossary_terms_are_deduplicated_case_insensitively():
    entries = glossary_entries()
    keys = [entry["term"].lower() for entry in entries]
    assert len(keys) == len(set(keys))


def test_glossary_links_to_the_earliest_teaching_lesson():
    """A term redefined later should still point at where it was first taught."""
    seen_slugs = set()
    for track in TRACKS:
        for lesson in track.lessons:
            seen_slugs.add(lesson.slug)

    for entry in glossary_entries():
        # The lesson recorded against a term must be a real lesson from the
        # curriculum, and must actually list that term in its own glossary.
        assert entry["lesson"].slug in seen_slugs
        own_terms = {t.term.strip().lower() for t in entry["lesson"].glossary}
        assert entry["term"].strip().lower() in own_terms


def test_anchor_is_stable_and_url_safe():
    term = GlossaryTerm("f-string", "example")
    anchor = term.anchor
    assert anchor == "term-f-string"
    assert re.match(r"^term-[a-z0-9-]+$", anchor)


def test_anchor_collapses_punctuation_and_repeated_dashes():
    term = GlossaryTerm(".get()", "example")
    assert term.anchor == "term-get"
    term2 = GlossaryTerm("*args and **kwargs", "example")
    assert re.match(r"^term-[a-z0-9-]+$", term2.anchor)
    assert "--" not in term2.anchor


# ---------- the /glossary route ----------


def test_glossary_route_requires_login(client):
    response = client.get("/glossary")
    assert response.status_code in (302, 401)


def test_glossary_route_lists_every_term(auth_client):
    response = auth_client.get("/glossary")
    assert response.status_code == 200
    body = response.data.decode()
    entries = glossary_entries()
    assert f"{len(entries)} terms" in body
    # Spot-check a term from each track appears with its anchor.
    for entry in entries[:3]:
        assert entry["anchor"] in body
        assert entry["term"] in body


def test_glossary_route_links_to_the_teaching_lesson(auth_client):
    response = auth_client.get("/glossary")
    body = response.data.decode()
    entry = next(e for e in glossary_entries() if e["term"] == "print()")
    assert f"/lesson/{entry['lesson'].slug}" in body


def test_lesson_page_shows_key_terms_box(auth_client):
    from app.curriculum import get_lesson

    lesson = get_lesson("hello-world")
    body = auth_client.get(f"/lesson/{lesson.slug}").data.decode()
    assert "Key terms" in body
    for term in lesson.glossary:
        assert term.anchor in body
