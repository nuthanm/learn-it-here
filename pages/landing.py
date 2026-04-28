"""Landing page — minimalist hero with the panda mascot."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
from components.header import _site_header_html
from components.footer import _footer_html, _scroll_nav_html
from config import (
    LEARN_SECTIONS,
    PAGE_LANDING,
    PAGE_LEARN,
    _nav_to,
    _url_for,
    default_section_slug,
)
from pages.requirements import STEPS as REQUIREMENT_STEPS


def page_landing():
    """Minimalist hero landing: slim header + two-column hero + feature row."""
    # Strip any stale query params left over from legacy URLs (e.g.
    # ?go=home, ?page=…, or section/sub from a previous Learning Hub view).
    for _k in ("page", "go", "section", "sub"):
        if _k in st.query_params:
            del st.query_params[_k]

    # Slim site header with text-link nav
    st.markdown(_site_header_html(active=PAGE_LANDING), unsafe_allow_html=True)

    # ── Centered hero (mockup 01-landing): bouncing emoji mascot + headline + CTA
    st.markdown(
        """
<div class="hero hero--center">
  <div class="hero-mascot" aria-hidden="true">🐼</div>
  <h1 class="hero-headline">Know your stack<br>before you build.</h1>
  <p class="hero-sub">
    A 2-minute questionnaire plus curated, opinionated guides for
    .NET, GIT, Blazor, EF Core and more — export your answers as a PDF.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    # CTA pair, centered
    st.markdown('<div class="hero-actions-wrap">', unsafe_allow_html=True)
    cta_l, cta_c, cta_r = st.columns([1, 2, 1])
    with cta_c:
        c1, c2 = st.columns(2, gap="small")
        with c1:
            if st.button(
                "Start questionnaire →",
                type="primary",
                use_container_width=True,
                key="cta_start",
            ):
                _nav_to("requirements")
        with c2:
            st.markdown(
                f'<a class="btn-link-secondary" '
                f'href="{_url_for(page=PAGE_LEARN, section=default_section_slug())}" '
                f'target="_self">Browse guides</a>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # Trust strip — counts derived from the single sources of truth so they
    # stay in sync as the wizard or learning hub grows / shrinks over time.
    question_count = len(REQUIREMENT_STEPS)
    topic_count = len(LEARN_SECTIONS)
    st.markdown(
        f"""
<div class="trust-strip">
  <span>⚡ {question_count} questions</span>
  <span>📄 PDF export</span>
  <span>🗂 {topic_count} topics</span>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Feature row (3 columns, no card chrome, divided by a thin line) ──────
    st.markdown(
        """
<div class="feature-row">
  <div class="feature-cell">
    <span class="feat-icon">📋</span>
    <strong>Capture requirements</strong>
    <span>Targeted questions that define your project context and tech stack.</span>
  </div>
  <div class="feature-cell">
    <span class="feat-icon">🎓</span>
    <strong>Stack-matched guides</strong>
    <span>Curated learning built around your specific versions and architecture.</span>
  </div>
  <div class="feature-cell">
    <span class="feat-icon">⚡</span>
    <strong>Learn &amp; ship fast</strong>
    <span>Hands-on, zero fluff — only what your project actually needs.</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
