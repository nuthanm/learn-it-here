import streamlit as st
import streamlit.components.v1 as components
from components.panda import _panda_landing_html
from components.footer import _footer_html, _scroll_nav_html
from config import _nav_to


def page_landing():
    """Full-width hero landing page with Po animation and two CTAs."""
    # Disable scroll on desktop only (≥1024 px); allow scroll on mobile/tablet
    st.markdown(
        """
<style>
  @media (min-width: 1024px) {
    html, body { overflow: hidden !important; }
    .stApp,
    .st-emotion-cache-1nryt4l,
    [data-testid="stAppViewContainer"],
    .stMain,
    [data-testid="stMain"] { overflow: hidden !important; }
  }
  @media (max-width: 1023px) {
    html, body { overflow-y: auto !important; height: auto !important; min-height: 100% !important; }
    .stApp,
    [data-testid="stAppViewContainer"],
    .stMain,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] { overflow-y: auto !important; height: auto !important; }
  }
</style>
""",
        unsafe_allow_html=True,
    )
    # Top nav bar
    st.markdown(
        """
<div class="kfp-nav">
  <a href="?go=home" target="_self" class="kfp-nav-brand">
    <span class="kfp-nav-logo">🐼</span>
    <div class="kfp-nav-text">
      <div class="kfp-nav-title">Learn It Here</div>
      <div class="kfp-nav-tagline">Hub to learn most important topics</div>
    </div>
  </a>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Centered hero: equal left/right columns ─────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown(
            """
<h1 class="hero-headline">Know Before You Go!</h1>
<div class="hero-bar"></div>
<p class="hero-sub">
  Don't start blind — know your stack upfront, capture what your project truly needs,
  then learn <em>exactly</em> what moves it forward. No generic tutorials, no wasted time.
</p>
<div class="hero-features">
  <div class="hero-feat">
    <span class="feat-icon">📋</span>
    <div class="feat-text">
      <strong>Capture Requirements</strong>
      <span>7 targeted questions that define your exact project context and tech stack</span>
    </div>
  </div>
  <div class="hero-feat">
    <span class="feat-icon">🎓</span>
    <div class="feat-text">
      <strong>Stack-Matched Guides</strong>
      <span>Curated learning built around your specific versions, tools, and architecture</span>
    </div>
  </div>
  <div class="hero-feat">
    <span class="feat-icon">⚡</span>
    <div class="feat-text">
      <strong>Learn &amp; Ship Fast</strong>
      <span>Hands-on, zero fluff — only the knowledge your project actually needs</span>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        bc1, bc2 = st.columns(2, gap="medium")
        with bc1:
            if st.button(
                "📋 Fill Project Requirements",
                type="primary",
                use_container_width=True,
            ):
                _nav_to("requirements")
        with bc2:
            if st.button(
                "🎓 Learn It Here →",
                type="secondary",
                use_container_width=True,
            ):
                _nav_to("learn")

    with col_right:
        # Center the panda both horizontally and vertically within its column
        st.markdown(
            '<div style="display:flex;justify-content:center;align-items:center;height:100%;">',
            unsafe_allow_html=True,
        )
        components.html(_panda_landing_html(), height=510, scrolling=False)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)


# ── Requirements Page ─────────────────────────────────────────────────────────

