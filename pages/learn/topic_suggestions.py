"""Topic Suggestions — animated tag cloud + inline suggestion form (mockup 06)."""

from __future__ import annotations

from collections import Counter, defaultdict
from html import escape

import streamlit as st

from components.content import section_intro, section_title
from services.supabase_client import (
    fetch_topics,
    get_client,
    save_topic,
)

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


def _render_inline_form() -> None:
    """Inline 'Suggest your own' form (mockup 06)."""
    db_available = get_client() is not None
    st.markdown(
        '<div class="suggest-form-card">'
        '<h3>Suggest your own</h3>',
        unsafe_allow_html=True,
    )
    topic = st.text_input(
        "Topic name",
        key="ts_inline_topic",
        placeholder="Topic name (e.g. Docker for .NET devs)",
        label_visibility="collapsed",
    )
    why = st.text_area(  # noqa: F841 — captured but not yet persisted
        "Why it matters (optional)",
        key="ts_inline_why",
        placeholder="Why it matters (optional)",
        height=88,
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="legend">Suggestions are public. Be kind. 🐼</div>',
        unsafe_allow_html=True,
    )
    if st.button(
        "Submit suggestion",
        type="primary",
        key="ts_inline_submit",
        disabled=not topic.strip(),
    ):
        if not db_available:
            st.warning(
                "Persistence is currently unavailable "
                "(no database credentials configured)."
            )
        else:
            result = save_topic(topic)
            if result.ok:
                st.success("Thank you! Your suggestion has been noted.")
                st.session_state["_topic_submitted"] = True
                # Clear the input fields for next submission.
                st.session_state.pop("ts_inline_topic", None)
                st.session_state.pop("ts_inline_why", None)
                st.rerun()
            else:
                st.warning(f"⚠️  Could not save your suggestion — {result.message}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_topic_suggestions():
    section_title("What others want to learn", "Community-requested topics.")
    section_intro(
        "Tag size reflects how many people have requested it. "
        "The most-requested topics get added to the learning hub first."
    )

    if get_client() is None:
        st.info(
            "ℹ️  No database credentials configured. "
            "Connect Supabase to persist and display community topic suggestions."
        )
        _render_inline_form()
        return

    rows = fetch_topics()
    if not rows:
        st.info("No topic suggestions yet. Be the first to suggest one!")
    else:
        _render_tag_cloud(_build_case_insensitive_counts(rows))

    _render_inline_form()
