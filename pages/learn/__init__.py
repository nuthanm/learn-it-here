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


# ── Topic metadata for the card-grid index page (mockup 03) ──────────────────
# slug → (icon, short description). Sections without entries fall back to a
# generic icon and a description derived from the title.
_TOPIC_META = {
    "git":               ("🌿", "Version control demystified — basics, branching, more."),
    "visual-studio":     ("🛠️", "IDE shortcuts and workflows that pay back daily."),
    "vscode":            ("📝", "Lightweight editor — extensions, debugging, tasks."),
    "efcore-oracle":     ("🗄️", "Entity Framework Core with Oracle — practical setup."),
    "dotnet":            ("🟣", "The unified runtime — versions, project types, workflow."),
    "unit-testing":      ("🧪", "xUnit, naming, AAA, mocks — keep it boring."),
    "linq":              ("🔗", "Query objects, collections, and DBs the C# way."),
    "blazor":            ("🔥", "Modern component model vs classic Web Forms."),
    "csharp":            ("#️⃣", "Language essentials, modern features worth knowing."),
    "topic-suggestions": ("💡", "What others want next — vote or suggest your own."),
    "sql-developer":     ("🗃️", "Oracle SQL Developer — the practical guide."),
}


def _render_index_page() -> None:
    """Mockup 03 — searchable card grid of every learning-hub topic."""
    st.markdown(
        '<div class="breadcrumb">'
        f'<a href="{_url_for(PAGE_LANDING)}" target="_self">Home</a>'
        '<span class="breadcrumb-sep">/</span>'
        '<span class="breadcrumb-current">Learning Hub</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h1 class="page-title">Learning Hub</h1>'
        '<p class="page-lead">Pick a topic. Each guide is short, opinionated, '
        'and copy-ready.</p>',
        unsafe_allow_html=True,
    )

    # Search box (client-side filter not possible without JS in Streamlit;
    # the input filters server-side via session_state on rerun).
    query = st.text_input(
        "Search topics",
        key="learn_index_query",
        placeholder="🔍  Search topics…",
        label_visibility="collapsed",
    ).strip().lower()

    cards = []
    for sec in LEARN_SECTIONS:
        title = sec["title"]
        desc_default = f"{title} — quick guide."
        icon, desc = _TOPIC_META.get(sec["slug"], ("📘", desc_default))
        if query and query not in title.lower() and query not in desc.lower():
            continue
        sub_count = len(sec.get("subsections") or [])
        meta_pill = (
            f'<span class="meta pill">{sub_count} sub-pages</span>'
            if sub_count else ""
        )
        href = _url_for(page=PAGE_LEARN, section=sec["slug"])
        cards.append(
            f'<a class="card topic-card" href="{href}" target="_self">'
            f'{meta_pill}'
            f'<div class="ico">{icon}</div>'
            f'<h3>{title}</h3>'
            f'<p>{desc}</p>'
            f'</a>'
        )

    if cards:
        st.markdown(
            f'<div class="topic-grid">{"".join(cards)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No topics match your search.")

    # Inline "Suggest a topic" strip (mirrors the mockup green block).
    st.markdown(
        '<div class="suggest-strip">'
        '<h3>💡 Suggest a topic</h3>'
        '<p>What would you like to learn next?</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    suggest_l, suggest_c, suggest_r = st.columns([1, 4, 1])
    with suggest_c:
        if st.button(
            "Open suggestion form", type="primary",
            use_container_width=True, key="open_suggest_dialog",
        ):
            _suggest_topic_dialog()


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


def _render_pill_tabs(section, active_sub) -> None:
    """Pill tabs for a section's sub-pages (mockup 05).

    Renders an "Overview" pill plus one pill per sub-page. The active pill
    has a filled (ink) background; the rest are quiet outlines.
    """
    subs = section.get("subsections") or []
    if not subs:
        return

    pills = []
    overview_cls = "active" if not active_sub else ""
    pills.append(
        f'<a class="{overview_cls}" '
        f'href="{_url_for(page=PAGE_LEARN, section=section["slug"])}" '
        f'target="_self">Overview</a>'
    )
    for sub in subs:
        cls = "active" if active_sub and sub["slug"] == active_sub["slug"] else ""
        pills.append(
            f'<a class="{cls}" '
            f'href="{_url_for(page=PAGE_LEARN, section=section["slug"], sub=sub["slug"])}" '
            f'target="_self">{sub["title"]}</a>'
        )
    st.markdown(
        f'<nav class="pill-tabs" aria-label="Sub-sections">{"".join(pills)}</nav>',
        unsafe_allow_html=True,
    )


def _render_topic_pager(section) -> None:
    """Previous / Next links between top-level learning-hub sections (mockup 04)."""
    slugs = [s["slug"] for s in LEARN_SECTIONS]
    try:
        i = slugs.index(section["slug"])
    except ValueError:
        return

    prev_sec = LEARN_SECTIONS[i - 1] if i > 0 else None
    next_sec = LEARN_SECTIONS[i + 1] if i + 1 < len(LEARN_SECTIONS) else None

    prev_html = (
        f'<a href="{_url_for(page=PAGE_LEARN, section=prev_sec["slug"])}" '
        f'target="_self">← {prev_sec["title"]}</a>'
        if prev_sec else '<span class="ph">·</span>'
    )
    next_html = (
        f'<a class="next" '
        f'href="{_url_for(page=PAGE_LEARN, section=next_sec["slug"])}" '
        f'target="_self">{next_sec["title"]} →</a>'
        if next_sec else '<span class="ph">·</span>'
    )
    st.markdown(
        f'<div class="topic-pager">{prev_html}{next_html}</div>',
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

    # ── Resolve section / sub from the URL ────────────────────────────────────
    # The URL is the source of truth. When NO section is in the URL we render
    # the card-grid index page (mockup 03). Selecting a section sets the
    # query param and the user enters the standard 2-column layout.
    section_param = st.query_params.get("section")
    show_index = not section_param

    section = find_section(section_param) if section_param else None
    sub_param = st.query_params.get("sub")
    sub = find_subsection(section, sub_param) if section else None

    st.session_state.learn_section = section["slug"] if section else None
    st.session_state.learn_sub = sub["slug"] if sub else None

    # Canonicalize the URL whenever a section is active (drops unknown keys).
    if not show_index:
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

    if show_index:
        _render_index_page()
        st.markdown(_footer_html(), unsafe_allow_html=True)
        components.html(_scroll_nav_html(), height=0)
        return

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

        # ── Pill tabs for sections that have sub-pages (mockup 05) ──────────
        if section and section.get("subsections"):
            _render_pill_tabs(section, sub)

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

        # ── Prev/next pager between top-level sections (mockup 04) ──────────
        if section and not sub:
            _render_topic_pager(section)

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)
