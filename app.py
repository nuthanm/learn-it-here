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
# The URL is the source of truth on every rerun, so the header text-link nav,
# breadcrumbs, sidebar links and shared deep-links all just work.
_url_page = st.query_params.get("page")
_target_page = (
    _url_page if _url_page in (PAGE_REQUIREMENTS, PAGE_LEARN) else PAGE_LANDING
)
if st.session_state.page != _target_page:
    st.session_state.page = _target_page

if _target_page == PAGE_LEARN:
    # Resolve section: accept slug (canonical) or legacy display title.
    _url_section = st.query_params.get("section")
    _section = find_section(_url_section) or find_section(default_section_slug())
    st.session_state.learn_section = _section["slug"] if _section else None

    # Resolve sub: must belong to the resolved section, else clear.
    _url_sub = st.query_params.get("sub")
    _sub = find_subsection(_section, _url_sub)
    st.session_state.learn_sub = _sub["slug"] if _sub else None

    # Mirror the canonical slug back to the URL so legacy/title-based links
    # get normalised on the next render.
    if _section and st.query_params.get("section") != _section["slug"]:
        st.query_params["section"] = _section["slug"]
    if _sub:
        if st.query_params.get("sub") != _sub["slug"]:
            st.query_params["sub"] = _sub["slug"]
    elif "sub" in st.query_params:
        del st.query_params["sub"]
else:
    # Outside the learn page, never carry section/sub in the URL.
    for _k in ("section", "sub"):
        if _k in st.query_params:
            del st.query_params[_k]

# ── Logo-click navigation (?go=home) ──────────────────────────────────────────
# Only act on this when the user is actually navigating away from the current
# page; otherwise repeated reruns would keep clearing the URL and could mask
# the active page (e.g. requirements) in the address bar.
if st.query_params.get("go") == "home":
    del st.query_params["go"]
    _was_elsewhere = st.session_state.get("page") != PAGE_LANDING
    for _k in ("page", "section", "sub"):
        if _k in st.query_params:
            del st.query_params[_k]
    if _was_elsewhere:
        st.session_state.page = PAGE_LANDING
        st.rerun()

inject_css()

page = st.session_state.page
if page == PAGE_REQUIREMENTS:
    page_requirements()
elif page == PAGE_LEARN:
    page_learn()
else:
    page_landing()
