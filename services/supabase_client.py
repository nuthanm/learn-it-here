"""Supabase persistence layer.

Single cached client (via ``@st.cache_resource``) instead of building a new
one on every call. Functions are named after what they do (domain) rather
than where the data lives (infrastructure) — so swapping out the backend
later doesn't ripple through call sites.

Backwards-compatible aliases (``save_to_supabase``, ``save_topic_suggestion``,
``fetch_topic_suggestions``, ``_get_supabase_client``) are kept at the bottom
of this module so any existing imports keep working.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import streamlit as st

from models import RequirementsRecord, SaveResult

logger = logging.getLogger(__name__)


# ── Connection ────────────────────────────────────────────────────────────────
def _read_credentials() -> tuple[str, str]:
    """Pull Supabase URL + key from Streamlit secrets, falling back to env."""
    try:
        url = st.secrets.get("SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    except Exception:  # noqa: BLE001 - st.secrets may raise outside Streamlit
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
    return url, key


@st.cache_resource(show_spinner=False)
def get_client() -> Any | None:
    """Return a cached Supabase client, or ``None`` when credentials are missing.

    Cached with ``@st.cache_resource`` so the client is built once per
    Streamlit process and reused across reruns. Returns ``None`` (rather
    than raising) when secrets are absent, which lets the app degrade
    gracefully — the PDF download still works without a database.
    """
    url, key = _read_credentials()
    if not url or not key:
        return None
    try:
        from supabase import create_client

        return create_client(url, key)
    except Exception:
        logger.exception("Failed to construct Supabase client")
        return None


# ── Project requirements ──────────────────────────────────────────────────────
def save_requirements(record: RequirementsRecord) -> SaveResult:
    """Persist a requirements submission to the ``project_requirements`` table."""
    client = get_client()
    if client is None:
        return SaveResult(
            ok=False,
            message=(
                "Supabase credentials not configured — data was not saved to "
                "the database. Your PDF download is still available."
            ),
        )
    try:
        client.table("project_requirements").insert(dict(record)).execute()
    except Exception as exc:
        logger.exception("Failed to insert requirements record")
        return SaveResult(ok=False, message=f"Database error: {exc}")
    return SaveResult(ok=True, message="Responses saved to Supabase successfully.")


# ── Topic suggestions ────────────────────────────────────────────────────────
def save_topic(topic: str) -> SaveResult:
    """Persist a single topic suggestion."""
    client = get_client()
    if client is None:
        return SaveResult(
            ok=False,
            message=(
                "Supabase credentials not configured — suggestion was not saved to the database."
            ),
        )
    try:
        client.table("topic_suggestions").insert({"topic": topic.strip()}).execute()
    except Exception as exc:
        logger.exception("Failed to insert topic suggestion")
        return SaveResult(ok=False, message=f"Database error: {exc}")
    return SaveResult(ok=True, message="Suggestion saved successfully.")


@st.cache_data(ttl=60, show_spinner=False)
def fetch_topics() -> list[dict]:
    """Return all topic suggestions, cached for 60 s to spare the DB."""
    client = get_client()
    if client is None:
        return []
    try:
        response = client.table("topic_suggestions").select("topic").execute()
        return response.data or []
    except Exception:
        logger.exception("Failed to fetch topic suggestions")
        return []


# ── Backwards-compatible aliases ─────────────────────────────────────────────
# Older modules import these names directly. Keep them as thin wrappers that
# adapt the new SaveResult dataclass back to the legacy ``(ok, message)``
# tuple so nothing else has to change in lock-step.
def _get_supabase_client():
    """Deprecated: use ``get_client()`` instead."""
    return get_client()


def save_to_supabase(data: dict) -> tuple[bool, str]:
    """Deprecated: use ``save_requirements()`` instead."""
    result = save_requirements(data)  # type: ignore[arg-type]
    return result.ok, result.message


def save_topic_suggestion(topic: str) -> tuple[bool, str]:
    """Deprecated: use ``save_topic()`` instead."""
    result = save_topic(topic)
    return result.ok, result.message


def fetch_topic_suggestions() -> list[dict]:
    """Deprecated: use ``fetch_topics()`` instead."""
    return fetch_topics()
