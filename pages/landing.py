import streamlit as st
import streamlit.components.v1 as components
from components.panda import _panda_landing_html
from components.header import _site_header_html
from components.footer import _footer_html, _scroll_nav_html
from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    _nav_to,
    _url_for,
    default_section_slug,
)


def page_landing():
    """Minimalist hero landing: slim header + two-column hero + feature row."""
    # Slim site header with text-link nav
    st.markdown(_site_header_html(active=PAGE_LANDING), unsafe_allow_html=True)

    # ── Two-column hero: text + CTA on the left, panda animation on the right
    hero_left, hero_right = st.columns([6, 5], gap="large")

    with hero_left:
        st.markdown(
            """
<div class="hero hero--left">
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

        # Primary CTA + secondary text link, left-aligned to match the hero.
        if st.button(
            "Start a project brief",
            type="primary",
            use_container_width=True,
            key="cta_start",
        ):
            _nav_to("requirements")
        # Use target="_top" so the browser performs a real navigation that
        # updates the URL bar with the full query string (?page=learn&section=git).
        # With target="_self", Streamlit's anchor-click interception can swallow
        # the query params and leave the user on the landing page.
        st.markdown(
            f'<div class="hero-secondary">'
            f'<a class="text-link" '
            f'href="{_url_for(page=PAGE_LEARN, section=default_section_slug())}" '
            f'target="_top">or browse the learning hub →</a></div>',
            unsafe_allow_html=True,
        )

    with hero_right:
        # Give the iframe enough room to fit the SVG (≈292px) plus the label
        # row and quote box (≈130px) without clipping or overlapping.
        components.html(_panda_landing_html(), height=460, scrolling=False)

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

    # ── 3-tile showcase removed per design — keep landing focused on the
    # hero CTA and the feature row above. The same destinations remain
    # reachable via the header nav and the "or browse the learning hub →"
    # secondary link.

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
