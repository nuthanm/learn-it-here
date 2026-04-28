"""App-wide configuration: page constants, learning-hub menu, routing helpers.

Public API:
    PAGE_LANDING, PAGE_REQUIREMENTS, PAGE_LEARN
    LEARN_SECTIONS                      Hierarchical learning-hub menu data
    LEARN_MENU_ITEMS                    Flat list of display titles (legacy)
    LATEST_NEW_TOPIC                    Most recently added topic — drives banner
    register_pages(pages)               Wire StreamlitPage objects to constants
    init_session_state()                Seed defaults onto st.session_state
    on_interact()                       Animation-state side-effect callback
    nav_to(page, section, sub)          st.switch_page wrapper that syncs URL
    url_for(page, section, sub)         Build a stable shareable URL
    find_section(identifier)            Resolve a section by slug or title
    find_subsection(section, ident)     Resolve a sub-section
    default_section_slug()              Fallback section for the learning hub

The leading-underscore names (``_nav_to``, ``_url_for``, ``_on_interact``)
are kept as aliases at the bottom of this module for backwards compatibility
with code that hasn't migrated yet.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

# ── Page name constants ────────────────────────────────────────────────────────
PAGE_LANDING = "landing"
PAGE_REQUIREMENTS = "requirements"
PAGE_LEARN = "learn"

_DEFAULTS = {
    "page": PAGE_LANDING,              # "landing" | "requirements" | "learn"
    "animation_state": "welcome",
    "submitted": False,
    "pdf_bytes": None,
    "interacted": False,
    "learn_section": "git",            # active learn-hub section (slug)
    "learn_sub": None,                 # active sub-section slug (or None)
    "learn_banner_dismissed": False,   # new-topic banner dismissed this session
}


# ── Learn-hub menu (hierarchical, data-driven) ────────────────────────────────
# Each section: {slug, title, renderer, subsections?}
# `slug` is the URL-stable id and MUST NOT change once published — that's what
# makes shared links durable. `title` is display-only and can be edited freely.
# `renderer` is the dotted "module:function" path to render the section
# landing. Sub-sections follow the same shape but without further nesting.
#
# To add a new top-level topic: append a dict here. To add a sub-page: append
# to the parent's "subsections" list. Nothing else needs to change.
LEARN_SECTIONS = [
    {
        "slug": "git",
        "title": "GIT",
        "renderer": "pages.learn.git:render_git",
        "subsections": [
            {
                "slug": "basics",
                "title": "Basics",
                "renderer": "pages.learn.git.basics:render",
            },
            {
                "slug": "branching",
                "title": "Branching",
                "renderer": "pages.learn.git.branching:render",
            },
        ],
    },
    {
        "slug": "visual-studio",
        "title": "Visual Studio IDE",
        "renderer": "pages.learn.visual_studio:render_visual_studio",
    },
    {
        "slug": "vscode",
        "title": "VS Code",
        "renderer": "pages.learn.vscode:render_vscode",
    },
    {
        "slug": "efcore-oracle",
        "title": "EF Core + Oracle",
        "renderer": "pages.learn.efcore:render_efcore",
    },
    {
        "slug": "dotnet",
        "title": ".NET",
        "renderer": "pages.learn.dotnet:render_dotnet",
    },
    {
        "slug": "unit-testing",
        "title": "Unit Testing",
        "renderer": "pages.learn.unit_testing:render_unit_testing",
    },
    {
        "slug": "linq",
        "title": "LINQ",
        "renderer": "pages.learn.linq:render_linq",
    },
    {
        "slug": "blazor",
        "title": "Blazor",
        "renderer": "pages.learn.blazor:render_blazor",
    },
    {
        "slug": "csharp",
        "title": "C#",
        "renderer": "pages.learn.csharp:render_csharp",
    },
    {
        "slug": "topic-suggestions",
        "title": "Topic Suggestions",
        "renderer": "pages.learn.topic_suggestions:render_topic_suggestions",
    },
    {
        "slug": "sql-developer",
        "title": "SQL Developer",
        "renderer": "pages.learn.sql_developer:render_sql_developer",
    },
]

# Backwards-compatible flat list of display titles (used by older code paths).
LEARN_MENU_ITEMS = [s["title"] for s in LEARN_SECTIONS]

# LATEST_NEW_TOPIC is the item that triggers the "new menu" banner.
# Update this string whenever a brand-new item is added.
LATEST_NEW_TOPIC = "SQL Developer"


# ── Lookup helpers ─────────────────────────────────────────────────────────────
def find_section(identifier):
    """Return the section dict matching `identifier`, or None.

    Accepts either a slug (canonical) or a display title (legacy URLs).
    """
    if not identifier:
        return None
    for s in LEARN_SECTIONS:
        if s["slug"] == identifier or s["title"] == identifier:
            return s
    return None


def find_subsection(section, identifier):
    """Return the subsection dict matching `identifier` within `section`, or None."""
    if not section or not identifier:
        return None
    for sub in section.get("subsections") or []:
        if sub["slug"] == identifier or sub["title"] == identifier:
            return sub
    return None


def default_section_slug():
    return LEARN_SECTIONS[0]["slug"] if LEARN_SECTIONS else None


# ── Sharable URL builder ──────────────────────────────────────────────────────
def _url_for(page=None, section=None, sub=None):
    """Build a stable, shareable in-app URL using path-based routing.

    Top-level pages are mapped to a single URL path segment (the maximum
    Streamlit Cloud supports — see README). Section / sub-section selection
    inside the Learning Hub stays in the query string because Streamlit does
    not support nested path segments or path segments containing spaces.

    Examples:
      _url_for()                                      -> '/'
      _url_for(page='requirements')                   -> '/projectrequirements'
      _url_for(page='learn', section='git')           -> '/learning-hub?section=git'
      _url_for(page='learn', section='git',
               sub='basics')                          -> '/learning-hub?section=git&sub=basics'
    """
    if page in (None, PAGE_LANDING):
        return "/"
    if page == PAGE_REQUIREMENTS:
        return "/projectrequirements"
    if page == PAGE_LEARN:
        url = "/learning-hub"
        params = []
        if section:
            params.append(f"section={section}")
            if sub:
                params.append(f"sub={sub}")
        if params:
            url += "?" + "&".join(params)
        return url
    return "/"


# ── Page registry (populated by app.py once st.Page objects exist) ────────────
# `_nav_to` needs the StreamlitPage objects so it can call st.switch_page on
# them. app.py constructs the pages and registers them here on every rerun.
_PAGES: dict = {}


def register_pages(pages: dict) -> None:
    """Register the StreamlitPage objects keyed by PAGE_* constants."""
    _PAGES.clear()
    _PAGES.update(pages)


# ── Lookup helpers ───────────────────────────────────────────────────────────
def find_section(identifier: str | None) -> dict[str, Any] | None:
    """Return the section dict matching ``identifier``, or ``None``.

    Accepts either a slug (canonical) or a display title (legacy URLs).
    """
    if not identifier:
        return None
    for section in LEARN_SECTIONS:
        if section["slug"] == identifier or section["title"] == identifier:
            return section
    return None


def find_subsection(
    section: dict[str, Any] | None,
    identifier: str | None,
) -> dict[str, Any] | None:
    """Return the subsection dict matching ``identifier`` within ``section``."""
    if not section or not identifier:
        return None
    for sub in section.get("subsections") or []:
        if sub["slug"] == identifier or sub["title"] == identifier:
            return sub
    return None


def default_section_slug() -> str | None:
    """Slug of the first section, used as the learning-hub default."""
    return LEARN_SECTIONS[0]["slug"] if LEARN_SECTIONS else None


# ── Sharable URL builder ─────────────────────────────────────────────────────
def url_for(
    page: str | None = None,
    section: str | None = None,
    sub: str | None = None,
) -> str:
    """Build a stable, shareable in-app URL using path-based routing.

    Top-level pages map to a single URL path segment (the maximum Streamlit
    Cloud supports — see README). Section / sub-section selection inside the
    Learning Hub stays in the query string because Streamlit does not
    support nested path segments or path segments containing spaces.

    Examples::

        url_for()                                      -> '/'
        url_for(page='requirements')                   -> '/projectrequirements'
        url_for(page='learn', section='git')           -> '/learning-hub?section=git'
        url_for(page='learn', section='git',
                sub='basics')                          -> '/learning-hub?section=git&sub=basics'
    """
    if page in (None, PAGE_LANDING):
        return "/"
    if page == PAGE_REQUIREMENTS:
        return "/projectrequirements"
    if page == PAGE_LEARN:
        url = "/learning-hub"
        params: list[str] = []
        if section:
            params.append(f"section={section}")
            if sub:
                params.append(f"sub={sub}")
        if params:
            url += "?" + "&".join(params)
        return url
    return "/"


# ── Page registry (populated by app.py once st.Page objects exist) ───────────
# `nav_to` needs the StreamlitPage objects so it can call st.switch_page on
# them. app.py constructs the pages and registers them here on every rerun.
_PAGES: dict[str, Any] = {}


def register_pages(pages: dict[str, Any]) -> None:
    """Register the StreamlitPage objects keyed by ``PAGE_*`` constants."""
    _PAGES.clear()
    _PAGES.update(pages)


def init_session_state() -> None:
    """Seed the default session-state values without overwriting existing ones."""
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def on_interact() -> None:
    """Switch the panda from 'welcome' to 'thinking' on first form interaction."""
    if not st.session_state.interacted:
        st.session_state.interacted = True
        st.session_state.animation_state = "thinking"


def _nav_to(page: str, section: str = None, sub: str = None):
    """Navigate to a page via st.switch_page, keeping the URL in sync.

    `st.switch_page` preserves the current query string across the rerun, so
    we update `st.query_params` to the canonical state for the destination
    page *before* switching.
    """
    if page == PAGE_LEARN:
        if section:
            st.query_params["section"] = section
        elif "section" in st.query_params:
            del st.query_params["section"]
        if sub:
            st.query_params["sub"] = sub
        elif "sub" in st.query_params:
            del st.query_params["sub"]
    else:
        for k in ("section", "sub"):
            if k in st.query_params:
                del st.query_params[k]
    # Strip any legacy keys that should never appear in the new URL scheme.
    for k in ("page", "go"):
        if k in st.query_params:
            del st.query_params[k]

    target = _PAGES.get(page) or _PAGES.get(PAGE_LANDING)
    if target is not None:
        st.switch_page(target)
    else:
        # Fallback if registry isn't populated (shouldn't happen at runtime).
        st.rerun()


# ── Backwards-compatible aliases ─────────────────────────────────────────────
# Older modules import the leading-underscore names; keep them working until
# every caller is migrated to the public names documented at the top.
_on_interact = on_interact
