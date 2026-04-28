"""Streamlit entry point — page config and routing only.

The actual page logic lives under ``pages/``; the routing helpers and
constants under ``config.py``; the persistence and PDF code under
``services/``. Keep this file thin.
"""

from __future__ import annotations

import logging

import streamlit as st

from components.css import inject_css
from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    PAGE_REQUIREMENTS,
    init_session_state,
    register_pages,
)
from pages.landing import page_landing
from pages.learn import page_learn
from pages.requirements import page_requirements

# ── Logging — visible in Streamlit Community Cloud's app logs ────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

st.set_page_config(
    page_title="Learn It Here 🐼",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()
inject_css()

# ── Path-based routing via st.navigation ─────────────────────────────────────
# Each top-level page is mapped to a single URL path segment. Streamlit Cloud
# does not support nested path segments or path segments containing spaces, so
# section / sub-section selection inside the Learning Hub stays in the query
# string (handled inside `page_learn`). See README for the full URL scheme.
_landing_page = st.Page(
    page_landing,
    title="Home",
    url_path="",
    default=True,
)
_requirements_page = st.Page(
    page_requirements,
    title="Requirements",
    url_path="projectrequirements",
)
_learn_page = st.Page(
    page_learn,
    title="Learning Hub",
    url_path="learning-hub",
)

# Make the StreamlitPage objects available to navigation helpers in config.py
# so `nav_to(...)` can call `st.switch_page(<page>)`.
register_pages(
    {
        PAGE_LANDING: _landing_page,
        PAGE_REQUIREMENTS: _requirements_page,
        PAGE_LEARN: _learn_page,
    }
)

# ── Backward-compatible legacy URL redirects ─────────────────────────────────
# Older shared links use `?page=<name>[&section=…&sub=…]` or the brand-click
# `?go=home` sentinel. Translate them to the new path-based URLs while
# preserving section / sub for the Learning Hub. `st.switch_page` preserves
# the (post-edit) query string across the rerun, so we strip the stale
# `page` / `go` keys *before* switching.
_legacy_go = st.query_params.get("go")
_legacy_page = st.query_params.get("page")


def _strip_query_keys(*keys: str) -> None:
    for key in keys:
        if key in st.query_params:
            del st.query_params[key]


if _legacy_go == "home" or _legacy_page == PAGE_LANDING:
    _strip_query_keys("go", "page", "section", "sub")
    st.switch_page(_landing_page)
elif _legacy_page == PAGE_REQUIREMENTS:
    _strip_query_keys("page", "go", "section", "sub")
    st.switch_page(_requirements_page)
elif _legacy_page == PAGE_LEARN:
    # Keep `section` / `sub` (Learning Hub will canonicalize them); drop the
    # legacy `page` / `go` keys.
    _strip_query_keys("page", "go")
    st.switch_page(_learn_page)

# ── Run the active page (the URL path determines which page runs) ────────────
st.navigation(
    [_landing_page, _requirements_page, _learn_page],
    position="hidden",
).run()
