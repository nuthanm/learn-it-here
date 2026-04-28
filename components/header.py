"""Shared site header — slim brand + horizontal text-link nav."""

from config import PAGE_LANDING, PAGE_REQUIREMENTS, PAGE_LEARN


def _site_header_html(active: str = PAGE_LANDING) -> str:
    """Render the slim site header as an HTML string.

    `active` is one of PAGE_LANDING / PAGE_REQUIREMENTS / PAGE_LEARN and
    controls which nav link is rendered with the "active" underline.
    """

    def _cls(page: str) -> str:
        return "active" if page == active else ""

    return f"""
<div class="site-header">
  <a class="brand" href="?go=home" target="_self">
    <span class="brand-mark">🐼</span>
    <span>Learn It Here</span>
  </a>
  <nav class="site-nav" aria-label="Primary">
    <a class="{_cls(PAGE_LANDING)}" href="?go=home" target="_self">Home</a>
    <a class="{_cls(PAGE_REQUIREMENTS)}" href="?page=requirements" target="_self">Requirements</a>
    <a class="{_cls(PAGE_LEARN)}" href="?page=learn" target="_self">Learn</a>
  </nav>
</div>
"""
