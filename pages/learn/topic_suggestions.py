"""Topic Suggestions — animated tag cloud of community-requested topics."""

from __future__ import annotations

from collections import Counter, defaultdict
from html import escape

import streamlit as st

from components.content import section_intro, section_title
from services.supabase_client import fetch_topics, get_client

_TAG_COLORS = [
    "#8B1A6B",
    "#C41E7A",
    "#4B1040",
    "#6B2D5E",
    "#A0256E",
    "#3D0F35",
    "#B5127A",
    "#7A1E5A",
    "#501048",
    "#D42085",
]


def _build_case_insensitive_counts(rows: list[dict]) -> dict[str, int]:
    """Group raw rows by lowercase topic; return {display_name: count}."""
    buckets: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        topic = (row.get("topic") or "").strip()
        if topic:
            buckets[topic.lower()].append(topic)
    result: dict[str, int] = {}
    for variants in buckets.values():
        display_name = Counter(variants).most_common(1)[0][0]
        result[display_name] = len(variants)
    return result


def _render_tag_cloud(counts: dict[str, int]) -> None:
    """Render an animated, centred tag cloud from a ``{topic: count}`` dict.

    User-supplied topic strings are HTML-escaped before going into the
    markup — even though the dialog only writes plain strings today, the
    field is user-controlled and the page is public.
    """
    if not counts:
        return

    max_count = max(counts.values())
    min_count = min(counts.values())
    count_range = max(max_count - min_count, 1)

    min_em = 0.85
    max_em = 3.0

    parts: list[str] = []
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for i, (topic, count) in enumerate(items):
        size = min_em + (count - min_count) / count_range * (max_em - min_em)
        color = _TAG_COLORS[i % len(_TAG_COLORS)]
        delay = round(i * 0.08, 2)
        req_label = "request" if count == 1 else "requests"
        title = f"{count} {req_label}"
        safe_topic = escape(topic)
        parts.append(
            f'<span class="tc-tag" '
            f'style="font-size:{size:.2f}em;color:{color};animation-delay:{delay}s;" '
            f'title="{escape(title, quote=True)}">'
            f'{safe_topic}<sup class="tc-count">{count}</sup>'
            f"</span>\n"
        )

    st.markdown(
        f'<div class="tc-cloud">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )


def render_topic_suggestions() -> None:
    """Render the topic-suggestions tag-cloud page."""
    section_title("Topic Suggestions", "Community-requested topics.")
    section_intro(
        "See which topics the community is requesting most. Use the "
        "Add your suggested topic button in the sidebar to vote for a "
        "new topic — the most-requested ones will be added to the learning hub."
    )

    if get_client() is None:
        st.info(
            "ℹ️  No database credentials configured. "
            "Connect Supabase to persist and display community topic suggestions."
        )
        return

    rows = fetch_topics()
    if not rows:
        st.info("No topic suggestions yet. Be the first to suggest one!")
        return

    _render_tag_cloud(_build_case_insensitive_counts(rows))
