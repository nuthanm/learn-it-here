"""Modal dialogs."""

from __future__ import annotations

import streamlit as st

from services.supabase_client import get_client, save_topic


@st.dialog("Add Your Suggested Topic")
def suggest_topic_dialog() -> None:
    """Modal that lets users propose a new learning-hub topic."""
    st.markdown(
        "Share your idea and we'll consider adding it to the learning hub.",
    )
    topic = st.text_area(
        "What topic would you like to learn about?",
        placeholder="e.g. Docker & Kubernetes, CI/CD Pipelines, Azure Services...",
        height=130,
    )

    db_available = get_client() is not None
    if db_available:
        note_text = (
            "<strong>Note:</strong> Suggested topics will be reviewed by our team. "
            "Topics with the most requests will be featured in the "
            "<strong>Topic Suggestions</strong> section of the learning hub "
            "with <strong>#hashtag details</strong> and the number of requests received."
        )
    else:
        note_text = (
            "<strong>Note:</strong> Suggested topics will be reviewed by our team. "
            "Persistence is currently unavailable (no database credentials configured)."
        )
    st.markdown(
        f'<div class="suggest-note">{note_text}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Submit Suggestion", type="primary", use_container_width=True):
        if topic.strip():
            result = save_topic(topic)
            if result.ok:
                st.success("Thank you! Your suggestion has been noted.")
                st.session_state["_topic_submitted"] = True
                st.rerun()
            else:
                st.warning(f"⚠️  Could not save your suggestion — {result.message}")
        else:
            st.warning("Please enter a topic before submitting.")


# Backwards-compatible alias.
_suggest_topic_dialog = suggest_topic_dialog
