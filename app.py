import streamlit as st
from config import (
    PAGE_LANDING,
    PAGE_REQUIREMENTS,
    PAGE_LEARN,
    LEARN_SECTIONS,
    init_session_state,
    find_section,
    find_subsection,
    default_section_slug,
)
from components.css import inject_css
from pages.landing import page_landing
from pages.requirements import page_requirements
from pages.learn import page_learn

st.set_page_config(
    page_title="Learn It Here 🐼",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()

# ── URL-driven routing ────────────────────────────────────────────────────────
# The URL is the single source of truth for which page is active. On every
# rerun we:
#   1) Handle the brand-click "?go=home" sentinel by clearing the URL.
#   2) Read the canonical (page, section, sub) from the URL.
#   3) Re-write st.query_params so that ONLY the canonical keys remain — this
#      guarantees the address bar matches the active page (e.g. navigating
#      Learn → Requirements never leaves a stale "section=git" behind), so
#      every URL is bookmarkable / shareable.
#
# Keys that are read transiently by individual pages (e.g. banner_dismissed)
# are preserved here so those pages can consume + delete them.
_PRESERVE_KEYS = {"banner_dismissed"}

# 1) Logo / brand click — reset to a clean landing URL.
if st.query_params.get("go") == "home":
    for _k in list(st.query_params.keys()):
        if _k not in _PRESERVE_KEYS:
            del st.query_params[_k]
    st.session_state.page = PAGE_LANDING

# 2) Resolve the canonical state purely from the URL.
_url_page = st.query_params.get("page")
if _url_page == PAGE_REQUIREMENTS:
    _target_page = PAGE_REQUIREMENTS
    _canonical = {"page": PAGE_REQUIREMENTS}
elif _url_page == PAGE_LEARN:
    _target_page = PAGE_LEARN
    # Accept slug (canonical) or legacy display title; fall back to default.
    _section = (
        find_section(st.query_params.get("section"))
        or find_section(default_section_slug())
    )
    _sub = (
        find_subsection(_section, st.query_params.get("sub")) if _section else None
    )
    st.session_state.learn_section = _section["slug"] if _section else None
    st.session_state.learn_sub = _sub["slug"] if _sub else None
    _canonical = {"page": PAGE_LEARN}
    if _section:
        _canonical["section"] = _section["slug"]
    if _sub:
        _canonical["sub"] = _sub["slug"]
else:
    _target_page = PAGE_LANDING
    _canonical = {}

st.session_state.page = _target_page

# 3) Normalize the URL to exactly match canonical state.
#    Remove anything that shouldn't be there, then set / update the rest.
for _k in list(st.query_params.keys()):
    if _k in _PRESERVE_KEYS or _k in _canonical:
        continue
    del st.query_params[_k]
for _k, _v in _canonical.items():
    if st.query_params.get(_k) != _v:
        st.query_params[_k] = _v

inject_css()

page = st.session_state.page
if page == PAGE_REQUIREMENTS:
    page_requirements()
elif page == PAGE_LEARN:
    page_learn()
else:
    page_landing()
