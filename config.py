import streamlit as st

_DEFAULTS = {
    "page": "landing",              # "landing" | "requirements" | "learn"
    "animation_state": "welcome",
    "submitted": False,
    "pdf_bytes": None,
    "interacted": False,
    "learn_section": "GIT",         # active learn-hub section
    "learn_banner_dismissed": False, # new-topic banner dismissed this session
}

# ── Learn-hub menu definitions ─────────────────────────────────────────────────
# To add a new menu item, append to this list and update LATEST_NEW_TOPIC.
LEARN_MENU_ITEMS = ["GIT", "Visual Studio IDE", "VS Code", "EF Core + Oracle", ".NET", "Unit Testing", "LINQ", "Blazor", "C#", "Topic Suggestions"]
# LATEST_NEW_TOPIC is the item that triggers the "new menu" banner.
# Update this string whenever a brand-new item is added to LEARN_MENU_ITEMS.
LATEST_NEW_TOPIC = "Topic Suggestions"


def init_session_state():
    for _k, _v in _DEFAULTS.items():
        if _k not in st.session_state:
            st.session_state[_k] = _v


def _on_interact():
    """Switch robot from 'welcome' to 'thinking' on first form interaction."""
    if not st.session_state.interacted:
        st.session_state.interacted = True
        st.session_state.animation_state = "thinking"


def _nav_to(page: str):
    """Navigate to a page and rerun."""
    st.session_state.page = page
    st.rerun()
