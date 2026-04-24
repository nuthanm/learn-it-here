import streamlit as st
import streamlit.components.v1 as components
from components.footer import _footer_html, _scroll_nav_html, _copy_buttons_html
from components.dialogs import _suggest_topic_dialog
from config import _nav_to, LEARN_MENU_ITEMS, LATEST_NEW_TOPIC
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
    """Sidebar learning hub: GIT | Visual Studio IDE | VS Code | EF Core + Oracle."""
    # ── Handle topic-submitted refresh ───────────────────────────────────────
    if st.session_state.pop("_topic_submitted", False):
        st.toast("✅ Your suggestion has been noted — thank you!", icon="🎉")

    # ── Handle banner dismiss via query param ─────────────────────────────────
    if st.query_params.get("banner_dismissed") == "1":
        st.session_state.learn_banner_dismissed = True
        del st.query_params["banner_dismissed"]

    # ── Nav bar (logo + banner/breadcrumbs) ───────────────────────────────────
    section = st.session_state.get("learn_section", "GIT")

    _LOGO_HTML = """
<div class="kfp-nav">
  <a href="?go=home" target="_self" class="kfp-nav-brand">
    <span class="kfp-nav-logo">🐼</span>
    <div class="kfp-nav-text">
      <div class="kfp-nav-title">Learn It Here</div>
      <div class="kfp-nav-tagline">Developer Learning Hub</div>
    </div>
  </a>
</div>
"""
    _BC_HTML = (
        f'<div class="breadcrumb">'
        f'<span>Home</span><span class="breadcrumb-sep">›</span>'
        f'<span>Developer Learning Hub</span><span class="breadcrumb-sep">›</span>'
        f'<span class="breadcrumb-current">{section}</span>'
        f"</div>"
    )

    if not st.session_state.get("learn_banner_dismissed", False):
        # Logo + Banner on same row
        st.markdown(
            f'<div class="kfp-nav">'
            f'<a href="?go=home" target="_self" class="kfp-nav-brand">'
            f'<span class="kfp-nav-logo">🐼</span>'
            f'<div class="kfp-nav-text">'
            f'<div class="kfp-nav-title">Learn It Here</div>'
            f'<div class="kfp-nav-tagline">Developer Learning Hub</div>'
            f'</div></a>'
            f'<div class="new-topic-banner">'
            f'<span><span class="new-topic-badge">NEW</span>'
            f'<strong>{LATEST_NEW_TOPIC}</strong> has been added to the learning hub — check it out!</span>'
            f'<a href="?banner_dismissed=1" class="banner-dismiss-btn" aria-label="Dismiss banner">✕ Dismiss</a>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        # Logo only
        st.markdown(_LOGO_HTML, unsafe_allow_html=True)

    st.divider()

    # Row 2: Breadcrumb (right-aligned with content column)
    _, bc_col = st.columns([2, 8], gap="medium")
    with bc_col:
        st.markdown(_BC_HTML, unsafe_allow_html=True)

    # ── Two-column layout: sidebar (2) + content (8) ──────────────────────────
    nav_col, content_col = st.columns([2, 8], gap="medium")

    # ── Sidebar nav ───────────────────────────────────────────────────────────
    with nav_col:
        st.markdown(
            '<div class="learn-sidebar"></div>',
            unsafe_allow_html=True,
        )
        st.radio(
            "Topics",
            options=LEARN_MENU_ITEMS,
            key="learn_section",
            label_visibility="collapsed",
        )
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        if st.button(
            "Add your suggested topic",
            key="suggest_topic_btn",
            use_container_width=True,
        ):
            _suggest_topic_dialog()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Home", key="learn_back", use_container_width=True):
            _nav_to("landing")

    # ── Main content area ─────────────────────────────────────────────────────
    with content_col:
        section = st.session_state.learn_section

    # ══════════════════════════════════════════════════════════════════════════
    # GIT SECTION
    # ══════════════════════════════════════════════════════════════════════════
    with content_col:
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
