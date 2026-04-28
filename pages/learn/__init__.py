"""Learn hub: slim header + data-driven left rail + content column."""

from __future__ import annotations

import importlib
import logging
from collections.abc import Callable
from html import escape
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from components.dialogs import suggest_topic_dialog
from components.footer import copy_buttons_html, footer_html, scroll_nav_html
from components.header import site_header_html
from config import (
    LATEST_NEW_TOPIC,
    LEARN_SECTIONS,
    PAGE_LANDING,
    PAGE_LEARN,
    default_section_slug,
    find_section,
    find_subsection,
    url_for,
)

logger = logging.getLogger(__name__)

# Query-string keys that pages other than the canonical section/sub may
# transiently set and consume themselves (e.g. the dismiss banner). They are
# preserved by the URL canonicalization step at the top of `page_learn`.
_PRESERVE_KEYS: set[str] = {"banner_dismissed"}


def _resolve_renderer(dotted: str) -> Callable[[], None]:
    """Resolve a "module:function" string into the actual callable."""
    module_path, _, fn_name = dotted.partition(":")
    module = importlib.import_module(module_path)
    return getattr(module, fn_name)


def _render_sidebar(
    active_section_slug: str | None,
    active_sub_slug: str | None,
) -> None:
    """Render the data-driven left rail with anchor links (sharable)."""
    items_html: list[str] = ['<nav class="topics-nav" aria-label="Learning topics">']
    for sec in LEARN_SECTIONS:
        is_active = sec["slug"] == active_section_slug
        cls = "topic-link active" if is_active else "topic-link"
        href = escape(url_for(page=PAGE_LEARN, section=sec["slug"]), quote=True)
        items_html.append(
            f'<a class="{cls}" href="{href}" target="_self">{escape(sec["title"])}</a>'
        )
        # Render second-level submenu only under the active section.
        if is_active and sec.get("subsections"):
            items_html.append('<div class="sub-nav">')
            # "Overview" link goes back to the section landing (no sub).
            overview_cls = "sub-link active" if not active_sub_slug else "sub-link"
            items_html.append(
                f'<a class="{overview_cls}" href="{href}" target="_self">Overview</a>'
            )
            for sub in sec["subsections"]:
                sub_cls = "sub-link active" if sub["slug"] == active_sub_slug else "sub-link"
                sub_href = escape(
                    url_for(page=PAGE_LEARN, section=sec["slug"], sub=sub["slug"]),
                    quote=True,
                )
                items_html.append(
                    f'<a class="{sub_cls}" href="{sub_href}" target="_self">'
                    f"{escape(sub['title'])}</a>"
                )
            items_html.append("</div>")
    items_html.append("</nav>")
    st.markdown(
        '<div class="topics-heading">Topics</div>' + "".join(items_html),
        unsafe_allow_html=True,
    )


def _render_breadcrumb(
    section: dict[str, Any] | None,
    sub: dict[str, Any] | None,
) -> None:
    """Render the breadcrumb path for the current section/sub."""
    parts: list[str] = [
        '<div class="breadcrumb">',
        f'<a href="{escape(url_for(PAGE_LANDING), quote=True)}" target="_self">Home</a>',
        '<span class="breadcrumb-sep">/</span>',
        f'<a href="{escape(url_for(PAGE_LEARN), quote=True)}" target="_self">Learning Hub</a>',
    ]
    if section:
        parts.append('<span class="breadcrumb-sep">/</span>')
        section_title = escape(section["title"])
        if sub:
            section_url = escape(url_for(page=PAGE_LEARN, section=section["slug"]), quote=True)
            parts.append(f'<a href="{section_url}" target="_self">{section_title}</a>')
            parts.append('<span class="breadcrumb-sep">/</span>')
            parts.append(f'<span class="breadcrumb-current">{escape(sub["title"])}</span>')
        else:
            parts.append(f'<span class="breadcrumb-current">{section_title}</span>')
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def _canonicalize_query_params(
    section: dict[str, Any] | None,
    sub: dict[str, Any] | None,
) -> None:
    """Rewrite ``st.query_params`` so the URL exactly matches the active state."""
    canonical: dict[str, str] = {}
    if section:
        canonical["section"] = section["slug"]
    if sub:
        canonical["sub"] = sub["slug"]
    for key in list(st.query_params.keys()):
        if key in _PRESERVE_KEYS or key in canonical:
            continue
        del st.query_params[key]
    for key, value in canonical.items():
        if st.query_params.get(key) != value:
            st.query_params[key] = value


def _render_new_topic_banner(
    section: dict[str, Any] | None,
    sub: dict[str, Any] | None,
) -> None:
    """Render the dismissable strip that announces the most recent topic."""
    if st.session_state.get("learn_banner_dismissed", False):
        return
    dismiss_url = url_for(
        PAGE_LEARN,
        section=section["slug"] if section else None,
        sub=sub["slug"] if sub else None,
    )
    dismiss_url += ("&" if "?" in dismiss_url else "?") + "banner_dismissed=1"
    dismiss_url = escape(dismiss_url, quote=True)
    new_topic = escape(LATEST_NEW_TOPIC)
    st.markdown(
        f'<div class="new-topic-strip">'
        f'<span class="dot" aria-hidden="true"></span>'
        f"<span><strong>New:</strong> {new_topic} has been added to the learning hub.</span>"
        f'<a class="dismiss" href="{dismiss_url}" target="_self" '
        f'aria-label="Dismiss">Dismiss</a>'
        f"</div>",
        unsafe_allow_html=True,
    )


def page_learn() -> None:
    """Learning hub: slim header + quiet left rail + content column."""
    # ── Handle topic-submitted refresh ──────────────────────────────
    if st.session_state.pop("_topic_submitted", False):
        st.toast("✅ Your suggestion has been noted — thank you!", icon="🎉")

    # ── Handle banner dismiss via query param ───────────────────────
    if st.query_params.get("banner_dismissed") == "1":
        st.session_state.learn_banner_dismissed = True
        del st.query_params["banner_dismissed"]

    # ── Resolve section / sub from the URL, then canonicalize ───────
    section = find_section(st.query_params.get("section")) or find_section(default_section_slug())
    sub_param = st.query_params.get("sub")
    sub = find_subsection(section, sub_param) if section else None

    st.session_state.learn_section = section["slug"] if section else None
    st.session_state.learn_sub = sub["slug"] if sub else None

    _canonicalize_query_params(section, sub)

    # ── Header ─────────────────────────────────────────────────────
    st.markdown(site_header_html(active=PAGE_LEARN), unsafe_allow_html=True)
    _render_new_topic_banner(section, sub)

    # ── Two-column layout: sidebar (2) + content (8) ────────────────
    nav_col, content_col = st.columns([2, 8], gap="medium")

    with nav_col:
        _render_sidebar(
            section["slug"] if section else None,
            st.session_state.learn_sub,
        )
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<div class="suggest-topic-btn">', unsafe_allow_html=True)
        if st.button("+ Suggest a topic", key="suggest_topic_btn"):
            suggest_topic_dialog()
        st.markdown("</div>", unsafe_allow_html=True)

    with content_col:
        _render_breadcrumb(section, sub)

        target = sub if sub else section
        if target and target.get("renderer"):
            try:
                renderer = _resolve_renderer(target["renderer"])
            except (ImportError, AttributeError) as exc:
                logger.exception("Failed to load renderer for %s", target.get("slug"))
                st.error(f"Failed to load page: {exc}")
            else:
                renderer()
        else:
            st.info("Select a topic from the sidebar.")

    st.markdown(footer_html(), unsafe_allow_html=True)
    components.html(scroll_nav_html(), height=0)
    components.html(copy_buttons_html(), height=0)
