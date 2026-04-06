import os
import streamlit as st


def save_to_supabase(data: dict) -> tuple:
    """Insert data into Supabase. Returns (success: bool, message: str)."""
    try:
        url = st.secrets.get("SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    except Exception:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")

    if not url or not key:
        return (
            False,
            "Supabase credentials not configured — data was not saved to the database. "
            "Your PDF download is still available.",
        )
    try:
        from supabase import create_client
        client = create_client(url, key)
        client.table("project_requirements").insert(data).execute()
        return True, "Responses saved to Supabase successfully."
    except Exception as exc:
        return False, f"Database error: {exc}"


def _get_supabase_client():
    """Return a Supabase client or None if credentials are not configured."""
    try:
        url = st.secrets.get("SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    except Exception:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None
    from supabase import create_client
    return create_client(url, key)


def save_topic_suggestion(topic: str) -> tuple:
    """Insert a topic suggestion into Supabase. Returns (success: bool, message: str)."""
    client = _get_supabase_client()
    if client is None:
        return (
            False,
            "Supabase credentials not configured — suggestion was not saved to the database.",
        )
    try:
        client.table("topic_suggestions").insert({"topic": topic.strip()}).execute()
        return True, "Suggestion saved successfully."
    except Exception as exc:
        return False, f"Database error: {exc}"


def fetch_topic_suggestions() -> list:
    """Fetch all topic suggestions from Supabase. Returns a list of dicts."""
    client = _get_supabase_client()
    if client is None:
        return []
    try:
        response = client.table("topic_suggestions").select("topic").execute()
        return response.data or []
    except Exception:
        return []


# ── Landing Page ──────────────────────────────────────────────────────────────

