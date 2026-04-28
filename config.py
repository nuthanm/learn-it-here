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
    for sub in section.get("subsections", []) or []:
        if sub["slug"] == identifier or sub["title"] == identifier:
            return sub
    return None


def default_section_slug():
    return LEARN_SECTIONS[0]["slug"] if LEARN_SECTIONS else None


# ── Sharable URL builder ──────────────────────────────────────────────────────
def _url_for(page=None, section=None, sub=None):
    """Build a stable, shareable in-app URL.

    Examples:
      _url_for()                                 -> '?go=home'
      _url_for(page='requirements')              -> '?page=requirements'
      _url_for(page='learn', section='git')      -> '?page=learn&section=git'
      _url_for(page='learn', section='git',
               sub='basics')                     -> '?page=learn&section=git&sub=basics'
    """
    if page in (None, PAGE_LANDING):
        return "?go=home"
    parts = [f"page={page}"]
    if page == PAGE_LEARN and section:
        parts.append(f"section={section}")
        if sub:
            parts.append(f"sub={sub}")
    return "?" + "&".join(parts)


def init_session_state():
    for _k, _v in _DEFAULTS.items():
        if _k not in st.session_state:
            st.session_state[_k] = _v


def _on_interact():
    """Switch robot from 'welcome' to 'thinking' on first form interaction."""
    if not st.session_state.interacted:
        st.session_state.interacted = True
        st.session_state.animation_state = "thinking"


def _nav_to(page: str, section: str = None, sub: str = None):
    """Navigate to a page and rerun, keeping the URL in sync."""
    st.session_state.page = page
    if page in (PAGE_REQUIREMENTS, PAGE_LEARN):
        st.query_params["page"] = page
        if page == PAGE_LEARN and section:
            st.query_params["section"] = section
            if sub:
                st.query_params["sub"] = sub
            elif "sub" in st.query_params:
                del st.query_params["sub"]
        else:
            for k in ("section", "sub"):
                if k in st.query_params:
                    del st.query_params[k]
    else:
        for k in ("page", "section", "sub"):
            if k in st.query_params:
                del st.query_params[k]
    st.rerun()
