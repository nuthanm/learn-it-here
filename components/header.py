"""Shared site header — slim brand + horizontal text-link nav."""

from config import PAGE_LANDING, PAGE_REQUIREMENTS, PAGE_LEARN


def _site_header_html(active: str = PAGE_LANDING) -> str:
    """Render the slim site header as an HTML string.

    `active` is one of PAGE_LANDING / PAGE_REQUIREMENTS / PAGE_LEARN and
    controls which nav link is rendered with the "active" underline.
    """

    def _cls(page: str) -> str:
        return "active" if page == active else ""

    # Use target="_top" on the nav links so the browser performs a real
    # navigation that updates the URL bar. With target="_self", Streamlit's
    # anchor-click interception can swallow the new query string when
    # switching pages (e.g. Learn → Requirements), leaving the URL — and
    # the rendered page — stuck on the previous page.
    return f"""
<div class="site-header">
  <a class="brand" href="?go=home" target="_top">
    <span class="brand-mark">🐼</span>
    <span>Learn It Here</span>
  </a>
  <nav class="site-nav" aria-label="Primary">
    <a class="{_cls(PAGE_LANDING)}" href="?go=home" target="_top">Home</a>
    <a class="{_cls(PAGE_REQUIREMENTS)}" href="?page=requirements" target="_top">Requirements</a>
    <a class="{_cls(PAGE_LEARN)}" href="?page=learn" target="_top">Learn</a>
  </nav>
</div>
"""
