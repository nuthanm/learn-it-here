import streamlit as st

# ── Page name constants ────────────────────────────────────────────────────────
PAGE_LANDING = "landing"
PAGE_REQUIREMENTS = "requirements"
PAGE_LEARN = "learn"

_DEFAULTS = {
    "page": PAGE_LANDING,              # "landing" | "requirements" | "learn"
    "animation_state": "welcome",
    "submitted": False,
    "pdf_bytes": None,
    "interacted": False,
    "learn_section": "GIT",         # active learn-hub section
    "learn_banner_dismissed": False, # new-topic banner dismissed this session
}

# ── Learn-hub menu definitions ─────────────────────────────────────────────────
# To add a new menu item, append to this list and update LATEST_NEW_TOPIC.
LEARN_MENU_ITEMS = ["GIT", "Visual Studio IDE", "VS Code", "EF Core + Oracle", ".NET", "Unit Testing", "LINQ", "Blazor", "C#", "Topic Suggestions", "SQL Developer"]
# LATEST_NEW_TOPIC is the item that triggers the "new menu" banner.
# Update this string whenever a brand-new item is added to LEARN_MENU_ITEMS.
LATEST_NEW_TOPIC = "SQL Developer"


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
    """Navigate to a page and rerun, keeping the URL in sync."""
    st.session_state.page = page
    if page in (PAGE_REQUIREMENTS, PAGE_LEARN):
        st.query_params["page"] = page
    else:
        if "page" in st.query_params:
            del st.query_params["page"]
    st.rerun()
