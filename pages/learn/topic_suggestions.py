import re
import streamlit as st
from collections import Counter, defaultdict

from components.content import section_intro, section_title
from services.supabase_client import _get_supabase_client, fetch_topic_suggestions

_TAG_COLORS = [
    "#8B1A6B", "#C41E7A", "#4B1040", "#6B2D5E", "#A0256E",
    "#3D0F35", "#B5127A", "#7A1E5A", "#501048", "#D42085",
]


def _build_case_insensitive_counts(rows):
    """Group raw rows by lowercase topic; return {display_name: count} dict."""
    buckets = defaultdict(list)
    for r in rows:
        topic = (r.get("topic") or "").strip()
        if topic:
            buckets[topic.lower()].append(topic)
    result = {}
    for variants in buckets.values():
        display_name = Counter(variants).most_common(1)[0][0]
        result[display_name] = len(variants)
    return result


def _render_tag_cloud(counts):
    """Render an animated, centred tag cloud from a {topic: count} dict."""
    if not counts:
        return

    max_count = max(counts.values())
    min_count = min(counts.values())
    count_range = max(max_count - min_count, 1)

    min_em = 0.85
    max_em = 3.0

    tags_html = ""
    for i, (topic, count) in enumerate(sorted(counts.items(), key=lambda x: x[1], reverse=True)):
        size = min_em + (count - min_count) / count_range * (max_em - min_em)
        color = _TAG_COLORS[i % len(_TAG_COLORS)]
        delay = round(i * 0.08, 2)
        req_label = "request" if count == 1 else "requests"
        title = f"{count} {req_label}"
        tags_html += (
            f'<span class="tc-tag" '
            f'style="font-size:{size:.2f}em;color:{color};animation-delay:{delay}s;" '
            f'title="{title}">'
            f'{topic}<sup class="tc-count">{count}</sup>'
            f'</span>\n'
        )

    st.markdown(
        f'<div class="tc-cloud">{tags_html}</div>',
        unsafe_allow_html=True,
    )


def render_topic_suggestions():
    section_title("Topic Suggestions", "Community-requested topics.")
    section_intro(
        "See which topics the community is requesting most. Use the "
        "Add your suggested topic button in the sidebar to vote for a "
        "new topic — the most-requested ones will be added to the learning hub."
    )
    
    db_available = _get_supabase_client() is not None

    if not db_available:
        st.info(
            "ℹ️  No database credentials configured. "
            "Connect Supabase to persist and display community topic suggestions."
        )
    else:
        rows = fetch_topic_suggestions()
        if not rows:
            st.info("No topic suggestions yet. Be the first to suggest one!")
        else:
            counts = _build_case_insensitive_counts(rows)
            _render_tag_cloud(counts)

