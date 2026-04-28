"""Shared minimal-layout primitives for content pages.

Use these helpers from any `pages/learn/<topic>/<sub>.py` so every section
renders with the same minimalist visual language as the rest of the site.
Avoid bespoke HTML / coloured cards — keep the page chrome quiet so the
content reads first.
"""

from html import escape
from typing import Iterable, Optional, Sequence, Tuple, Union

import streamlit as st


def section_title(title: str, subtitle: Optional[str] = None) -> None:
    """Render the page-level title + optional lead paragraph."""
    st.markdown(
        f'<h1 class="page-title">{escape(title)}</h1>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<p class="page-lead">{escape(subtitle)}</p>',
            unsafe_allow_html=True,
        )


def section_intro(text: str) -> None:
    """Short muted-ink paragraph used for one-liner intros."""
    st.markdown(
        f'<p class="section-intro">{escape(text)}</p>',
        unsafe_allow_html=True,
    )


def subsection(heading: str) -> None:
    """Render an H2 heading with a subtle bottom border."""
    st.markdown(
        f'<h2 class="sub-heading">{escape(heading)}</h2>',
        unsafe_allow_html=True,
    )


def paragraph(text: str) -> None:
    """Render a plain body paragraph."""
    st.markdown(
        f'<p class="body-text">{escape(text)}</p>',
        unsafe_allow_html=True,
    )


def code_block(code: str, language: str = "", label: Optional[str] = None) -> None:
    """Render a minimal labelled code block.

    Uses Streamlit's native `st.code` for syntax highlighting and copy button.
    """
    if label:
        st.markdown(
            f'<div class="code-label">{escape(label)}</div>',
            unsafe_allow_html=True,
        )
    st.code(code, language=language or None)


LinkItem = Union[str, Tuple[str, str], Tuple[str, str, str]]


def link_list(items: Iterable[LinkItem]) -> None:
    """Render a simple bulleted list of links.

    Each item may be:
      - a string (rendered as a plain bullet)
      - a (label, href) tuple
      - a (label, href, description) tuple
    """
    parts = ['<ul class="link-list">']
    for item in items:
        if isinstance(item, str):
            parts.append(f"<li>{escape(item)}</li>")
            continue
        if not isinstance(item, Sequence) or len(item) < 2:
            continue
        label = escape(str(item[0]))
        href = escape(str(item[1]), quote=True)
        desc = escape(str(item[2])) if len(item) >= 3 and item[2] else ""
        desc_html = f' <span class="link-desc">— {desc}</span>' if desc else ""
        parts.append(
            f'<li><a href="{href}" target="_blank" rel="noopener">{label}</a>{desc_html}</li>'
        )
    parts.append("</ul>")
    st.markdown("".join(parts), unsafe_allow_html=True)
