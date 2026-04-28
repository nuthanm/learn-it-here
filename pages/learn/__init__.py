import streamlit as st
import streamlit.components.v1 as components
from components.header import _site_header_html
from components.footer import _footer_html, _scroll_nav_html, _copy_buttons_html
from components.dialogs import _suggest_topic_dialog
from config import PAGE_LEARN, LEARN_MENU_ITEMS, LATEST_NEW_TOPIC
from pages.learn.git import render_git
from pages.learn.visual_studio import render_visual_studio
from pages.learn.vscode import render_vscode
from pages.learn.efcore import render_efcore
from pages.learn.dotnet import render_dotnet
from pages.learn.unit_testing import render_unit_testing
from pages.learn.linq import render_linq
from pages.learn.blazor import render_blazor
from pages.learn.csharp import render_csharp
from pages.learn.topic_suggestions import render_topic_suggestions
from pages.learn.sql_developer import render_sql_developer


def page_learn():
    """Learning hub: slim header + quiet left rail + content column."""
    # ── Handle topic-submitted refresh ───────────────────────────────────────
    if st.session_state.pop("_topic_submitted", False):
        st.toast("✅ Your suggestion has been noted — thank you!", icon="🎉")

    # ── Handle banner dismiss via query param ─────────────────────────────────
    if st.query_params.get("banner_dismissed") == "1":
        st.session_state.learn_banner_dismissed = True
        del st.query_params["banner_dismissed"]

    # ── Slim site header with text-link nav ──────────────────────────────────
    st.markdown(_site_header_html(active=PAGE_LEARN), unsafe_allow_html=True)

    # ── Optional thin "new topic" strip below the header ─────────────────────
    if not st.session_state.get("learn_banner_dismissed", False):
        st.markdown(
            f'<div class="new-topic-strip">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'<span><strong>New:</strong> {LATEST_NEW_TOPIC} has been added to the learning hub.</span>'
            f'<a class="dismiss" href="?page=learn&banner_dismissed=1" target="_self" '
            f'aria-label="Dismiss">Dismiss</a>'
            f"</div>",
            unsafe_allow_html=True,
        )

    section = st.session_state.get("learn_section", "GIT")

    # ── Two-column layout: sidebar (2) + content (8) ──────────────────────────
    nav_col, content_col = st.columns([2, 8], gap="medium")

    # ── Sidebar nav ───────────────────────────────────────────────────────────
    with nav_col:
        st.markdown(
            '<div class="topics-heading">Topics</div>',
            unsafe_allow_html=True,
        )
        st.radio(
            "Topics",
            options=LEARN_MENU_ITEMS,
            key="learn_section",
            label_visibility="collapsed",
        )
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        # Demoted: small link-style "+ Suggest a topic"
        st.markdown('<div class="suggest-topic-btn">', unsafe_allow_html=True)
        if st.button(
            "+ Suggest a topic",
            key="suggest_topic_btn",
        ):
            _suggest_topic_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Sync section to URL so the page is deep-linkable ─────────────────────
    st.query_params["section"] = st.session_state.learn_section

    # ── Main content area ─────────────────────────────────────────────────────
    with content_col:
        # Breadcrumb at the top of the content column
        st.markdown(
            f'<div class="breadcrumb">'
            f'<a href="?go=home" target="_self">Home</a>'
            f'<span class="breadcrumb-sep">/</span>'
            f'<a href="?page=learn" target="_self">Learning Hub</a>'
            f'<span class="breadcrumb-sep">/</span>'
            f'<span class="breadcrumb-current">{section}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        section = st.session_state.learn_section
        if section == "GIT":
            render_git()
        elif section == "Visual Studio IDE":
            render_visual_studio()
        elif section == "VS Code":
            render_vscode()
        elif section == "EF Core + Oracle":
            render_efcore()
        elif section == ".NET":
            render_dotnet()
        elif section == "Unit Testing":
            render_unit_testing()
        elif section == "LINQ":
            render_linq()
        elif section == "Blazor":
            render_blazor()
        elif section == "C#":
            render_csharp()
        elif section == "Topic Suggestions":
            render_topic_suggestions()
        elif section == "SQL Developer":
            render_sql_developer()

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)
