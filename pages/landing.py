import streamlit as st
import streamlit.components.v1 as components
from components.panda import _panda_landing_html
from components.header import _site_header_html
from components.footer import _footer_html, _scroll_nav_html
from config import PAGE_LANDING, _nav_to


def page_landing():
    """Minimalist hero landing: slim header + centred hero + feature row."""
    # Slim site header with text-link nav
    st.markdown(_site_header_html(active=PAGE_LANDING), unsafe_allow_html=True)

    # ── Centred hero ─────────────────────────────────────────────────────────
    st.markdown(
        """
<div class="hero">
  <span class="page-eyebrow">Project briefs · Curated learning</span>
  <h1 class="hero-headline">Know before you go.</h1>
  <p class="hero-sub">
    Capture exactly what your project needs, then learn only what moves it forward.
    No generic tutorials, no wasted time.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Single primary CTA + secondary text link ─────────────────────────────
    cta_l, cta_c, cta_r = st.columns([3, 2, 3])
    with cta_c:
        if st.button(
            "Start a project brief",
            type="primary",
            use_container_width=True,
            key="cta_start",
        ):
            _nav_to("requirements")
    st.markdown(
        '<div style="text-align:center;margin-top:8px;">'
        '<a class="text-link" href="?page=learn" target="_self">'
        "or browse the learning hub →</a></div>",
        unsafe_allow_html=True,
    )

    # ── Small panda illustration, centred ────────────────────────────────────
    p_l, p_c, p_r = st.columns([2, 1, 2])
    with p_c:
        components.html(_panda_landing_html(), height=240, scrolling=False)

    # ── Feature row (3 columns, no card chrome, divided by a thin line) ──────
    st.markdown(
        """
<div class="feature-row">
  <div class="feature-cell">
    <span class="feat-icon">📋</span>
    <strong>Capture requirements</strong>
    <span>Seven targeted questions that define your project context and tech stack.</span>
  </div>
  <div class="feature-cell">
    <span class="feat-icon">🎓</span>
    <strong>Stack-matched guides</strong>
    <span>Curated learning built around your specific versions, tools, and architecture.</span>
  </div>
  <div class="feature-cell">
    <span class="feat-icon">⚡</span>
    <strong>Learn &amp; ship fast</strong>
    <span>Hands-on, zero fluff — only the knowledge your project actually needs.</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
