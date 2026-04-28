"""Learn hub: slim header + data-driven left rail + content column."""

import importlib

import streamlit as st
import streamlit.components.v1 as components

from components.dialogs import _suggest_topic_dialog
from components.footer import _copy_buttons_html, _footer_html, _scroll_nav_html
from components.header import _site_header_html
from config import (
    LATEST_NEW_TOPIC,
    LEARN_SECTIONS,
    PAGE_LANDING,
    PAGE_LEARN,
    _url_for,
    default_section_slug,
    find_section,
    find_subsection,
)


# Query-string keys that pages other than the canonical section/sub may
# transiently set and consume themselves (e.g. the dismiss banner). They are
# preserved by the URL canonicalization step at the top of `page_learn`.
_PRESERVE_KEYS = {"banner_dismissed"}


def _resolve_renderer(dotted: str):
    """Resolve a "module:function" string into the actual callable."""
    module_path, _, fn_name = dotted.partition(":")
    module = importlib.import_module(module_path)
    return getattr(module, fn_name)


def _render_sidebar(active_section_slug, active_sub_slug):
    """Render the data-driven left rail with anchor links (sharable)."""
    items_html = ['<nav class="topics-nav" aria-label="Learning topics">']
    for sec in LEARN_SECTIONS:
        is_active = sec["slug"] == active_section_slug
        cls = "topic-link active" if is_active else "topic-link"
        items_html.append(
            f'<a class="{cls}" href="{_url_for(page=PAGE_LEARN, section=sec["slug"])}" '
            f'target="_self">{sec["title"]}</a>'
        )
        # Render second-level submenu only under the active section.
        if is_active and sec.get("subsections"):
            items_html.append('<div class="sub-nav">')
            # "Overview" link goes back to the section landing (no sub).
            overview_cls = "sub-link active" if not active_sub_slug else "sub-link"
            items_html.append(
                f'<a class="{overview_cls}" '
                f'href="{_url_for(page=PAGE_LEARN, section=sec["slug"])}" '
                f'target="_self">Overview</a>'
            )
            for sub in sec["subsections"]:
                sub_cls = (
                    "sub-link active"
                    if sub["slug"] == active_sub_slug
                    else "sub-link"
                )
                items_html.append(
                    f'<a class="{sub_cls}" '
                    f'href="{_url_for(page=PAGE_LEARN, section=sec["slug"], sub=sub["slug"])}" '
                    f'target="_self">{sub["title"]}</a>'
                )
            items_html.append("</div>")
    items_html.append("</nav>")
    st.markdown(
        '<div class="topics-heading">Topics</div>' + "".join(items_html),
        unsafe_allow_html=True,
    )


def _render_breadcrumb(section, sub):
    """Render the breadcrumb path for the current section/sub."""
    parts = [
        '<div class="breadcrumb">',
        f'<a href="{_url_for(PAGE_LANDING)}" target="_self">Home</a>',
        '<span class="breadcrumb-sep">/</span>',
        f'<a href="{_url_for(PAGE_LEARN)}" target="_self">Learning Hub</a>',
    ]
    if section:
        parts.append('<span class="breadcrumb-sep">/</span>')
        if sub:
            # Section becomes a link, sub is the current crumb.
            parts.append(
                f'<a href="{_url_for(page=PAGE_LEARN, section=section["slug"])}" '
                f'target="_self">{section["title"]}</a>'
            )
            parts.append('<span class="breadcrumb-sep">/</span>')
            parts.append(
                f'<span class="breadcrumb-current">{sub["title"]}</span>'
            )
        else:
            parts.append(
                f'<span class="breadcrumb-current">{section["title"]}</span>'
            )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def page_learn():
    """Learning hub: slim header + quiet left rail + content column."""
    # ── Handle topic-submitted refresh ───────────────────────────────────────
    if st.session_state.pop("_topic_submitted", False):
        st.toast("✅ Your suggestion has been noted — thank you!", icon="🎉")

    # ── Handle banner dismiss via query param ───────────────────────
    if st.query_params.get("banner_dismissed") == "1":
        st.session_state.learn_banner_dismissed = True
        del st.query_params["banner_dismissed"]

    # ── Resolve & canonicalize section / sub from the URL ─────────────────────
    # The URL is the source of truth for which section/sub is active. Accept
    # slug (canonical) or legacy display title; fall back to the default
    # section. Then rewrite query params so the address bar exactly matches
    # the active state (e.g. unknown / stale section names get dropped).
    section = (
        find_section(st.query_params.get("section"))
        or find_section(default_section_slug())
    )
    sub_param = st.query_params.get("sub")
    sub = find_subsection(section, sub_param) if section else None

    st.session_state.learn_section = section["slug"] if section else None
    st.session_state.learn_sub = sub["slug"] if sub else None

    _canonical = {}
    if section:
        _canonical["section"] = section["slug"]
    if sub:
        _canonical["sub"] = sub["slug"]
    for _k in list(st.query_params.keys()):
        if _k in _PRESERVE_KEYS or _k in _canonical:
            continue
        del st.query_params[_k]
    for _k, _v in _canonical.items():
        if st.query_params.get(_k) != _v:
            st.query_params[_k] = _v

    # ── Slim site header with text-link nav ──────────────────────────────────
    st.markdown(_site_header_html(active=PAGE_LEARN), unsafe_allow_html=True)

    # ── Optional thin "new topic" strip below the header ─────────────────────
    if not st.session_state.get("learn_banner_dismissed", False):
        # Build a dismiss URL that preserves the current section / sub so the
        # user lands back exactly where they were after dismissing the banner.
        _dismiss_url = _url_for(
            PAGE_LEARN,
            section=section["slug"] if section else None,
            sub=sub["slug"] if sub else None,
        )
        _dismiss_url += ("&" if "?" in _dismiss_url else "?") + "banner_dismissed=1"
        st.markdown(
            f'<div class="new-topic-strip">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'<span><strong>New:</strong> {LATEST_NEW_TOPIC} has been added to the learning hub.</span>'
            f'<a class="dismiss" href="{_dismiss_url}" target="_self" '
            f'aria-label="Dismiss">Dismiss</a>'
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Two-column layout: sidebar (2) + content (8) ──────────────────────────
    nav_col, content_col = st.columns([2, 8], gap="medium")

    # ── Sidebar nav (data-driven anchor links, sharable URLs) ────────────────
    with nav_col:
        _render_sidebar(section["slug"] if section else None, st.session_state.learn_sub)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        # Demoted: small link-style "+ Suggest a topic"
        st.markdown('<div class="suggest-topic-btn">', unsafe_allow_html=True)
        if st.button(
            "+ Suggest a topic",
            key="suggest_topic_btn",
        ):
            _suggest_topic_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

    with content_col:
        _render_breadcrumb(section, sub)

        target = sub if sub else section
        if target and target.get("renderer"):
            try:
                renderer = _resolve_renderer(target["renderer"])
            except (ImportError, AttributeError) as exc:
                st.error(f"Failed to load page: {exc}")
            else:
                renderer()
        else:
            st.info("Select a topic from the sidebar.")

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)
