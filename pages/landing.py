"""Landing page — minimalist hero with the panda mascot."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from components.footer import footer_html, scroll_nav_html
from components.header import site_header_html
from components.panda import panda_landing_html
from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    PAGE_REQUIREMENTS,
    default_section_slug,
    nav_to,
    url_for,
)


def page_landing() -> None:
    """Minimalist hero landing: slim header + two-column hero + feature row."""
    # Strip any stale query params left over from legacy URLs (e.g.
    # ?go=home, ?page=…, or section/sub from a previous Learning Hub view).
    for key in ("page", "go", "section", "sub"):
        if key in st.query_params:
            del st.query_params[key]

    st.markdown(site_header_html(active=PAGE_LANDING), unsafe_allow_html=True)

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

        if st.button(
            "Start a project brief",
            type="primary",
            use_container_width=True,
            key="cta_start",
        ):
            nav_to(PAGE_REQUIREMENTS)

        # target="_self" is required inside Streamlit Community Cloud's
        # sandboxed iframe (target="_top" is blocked there).
        st.markdown(
            f'<div class="hero-secondary">'
            f'<a class="text-link" '
            f'href="{url_for(page=PAGE_LEARN, section=default_section_slug())}" '
            f'target="_self">or browse the learning hub →</a></div>',
            unsafe_allow_html=True,
        )

    with hero_right:
        # Give the iframe enough room to fit the SVG (~292 px) plus the label
        # row and quote box (~130 px) without clipping or overlapping.
        components.html(panda_landing_html(), height=460, scrolling=False)

    # ── Feature row ──────────────────────────────────────────────────────────
    st.markdown(
        """
<div class="feature-row">
  <div class="feature-cell">
    <span class="feat-icon">📋</span>
    <strong>Capture requirements</strong>
    <span>Eight targeted questions that define your project context and tech stack.</span>
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

    st.markdown(footer_html(), unsafe_allow_html=True)
    components.html(scroll_nav_html(), height=0)
