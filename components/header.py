"""Shared site header — slim brand + horizontal text-link nav."""

from config import PAGE_LANDING, PAGE_REQUIREMENTS, PAGE_LEARN, _url_for


def _site_header_html(active: str = PAGE_LANDING) -> str:
    """Render the slim site header as an HTML string.

    `active` is one of PAGE_LANDING / PAGE_REQUIREMENTS / PAGE_LEARN and
    controls which nav link is rendered with the "active" underline.
    """

    def _cls(page: str) -> str:
        return "active" if page == active else ""

    # Use target="_self" on the nav links. On Streamlit Community Cloud the
    # app is served inside a sandboxed iframe without `allow-top-navigation`,
    # so target="_top" is blocked by the browser with:
    #   "Unsafe attempt to initiate navigation for frame ... The frame
    #    attempting navigation of the top-level window is sandboxed..."
    # which makes every header click do nothing. target="_self" navigates
    # within the Streamlit iframe; st.navigation in app.py then matches the
    # new URL path and runs the correct page.
    return f"""
<div class="site-header">
  <a class="brand" href="{_url_for(PAGE_LANDING)}" target="_self">
    <span class="brand-mark">🐼</span>
    <span>Learn It Here</span>
  </a>
  <nav class="site-nav" aria-label="Primary">
    <a class="{_cls(PAGE_LANDING)}" href="{_url_for(PAGE_LANDING)}" target="_self">Home</a>
    <a class="{_cls(PAGE_REQUIREMENTS)}" href="{_url_for(PAGE_REQUIREMENTS)}" target="_self">Requirements</a>
    <a class="{_cls(PAGE_LEARN)}" href="{_url_for(PAGE_LEARN)}" target="_self">Learn</a>
  </nav>
</div>
"""
