"""Tests for URL building and learn-hub menu lookups."""

from __future__ import annotations

from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    PAGE_REQUIREMENTS,
    default_section_slug,
    find_section,
    find_subsection,
    url_for,
)


# ── url_for ──────────────────────────────────────────────────────────────────
def test_url_for_landing_returns_root():
    assert url_for() == "/"
    assert url_for(PAGE_LANDING) == "/"


def test_url_for_requirements_returns_path():
    assert url_for(PAGE_REQUIREMENTS) == "/projectrequirements"


def test_url_for_learn_section_uses_query_string():
    assert url_for(PAGE_LEARN) == "/learning-hub"
    assert url_for(PAGE_LEARN, section="git") == "/learning-hub?section=git"


def test_url_for_learn_section_and_sub():
    assert (
        url_for(PAGE_LEARN, section="git", sub="basics") == "/learning-hub?section=git&sub=basics"
    )


def test_url_for_learn_sub_without_section_is_ignored():
    """``sub`` requires ``section`` — without it, sub is not appended."""
    assert url_for(PAGE_LEARN, sub="basics") == "/learning-hub"


def test_url_for_unknown_page_falls_back_to_root():
    assert url_for("not-a-real-page") == "/"


# ── find_section / find_subsection ───────────────────────────────────────────
def test_find_section_by_slug():
    section = find_section("git")
    assert section is not None
    assert section["title"] == "GIT"


def test_find_section_by_legacy_title():
    """Legacy URLs sometimes used the display title — keep that path working."""
    section = find_section("GIT")
    assert section is not None
    assert section["slug"] == "git"


def test_find_section_unknown_returns_none():
    assert find_section("does-not-exist") is None
    assert find_section(None) is None
    assert find_section("") is None


def test_find_subsection_by_slug():
    section = find_section("git")
    sub = find_subsection(section, "basics")
    assert sub is not None
    assert sub["title"] == "Basics"


def test_find_subsection_unknown_returns_none():
    section = find_section("git")
    assert find_subsection(section, "no-such-sub") is None
    assert find_subsection(None, "basics") is None
    assert find_subsection(section, None) is None


def test_default_section_slug_is_first_section():
    assert default_section_slug() == "git"
