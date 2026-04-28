"""Reusable Streamlit form widgets.

The "select X, or pick Other and type something custom" pattern repeats
five times in the requirements form. Centralising it here gives every
caller identical behaviour and shrinks the form file by ~40 %.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import streamlit as st


def select_with_other(
    label: str,
    options: Sequence[str],
    *,
    key: str,
    help: str = "",
    on_change: Callable[[], None] | None = None,
    other_label: str | None = None,
) -> str:
    """A selectbox that reveals a free-text input when the user picks "Other".

    Returns the chosen string. If "Other" was selected, returns the typed
    value (or the literal ``"Other"`` if the user left it blank).
    """
    choice = st.selectbox(
        label,
        options,
        index=None,
        placeholder="Choose an option",
        key=key,
        help=help,
        on_change=on_change,
    )
    if choice == "Other":
        custom = st.text_input(
            other_label or f"Specify {label.lower()}",
            key=f"{key}_other",
            on_change=on_change,
        )
        return custom or "Other"
    return choice or ""


def multiselect_with_other(
    label: str,
    options: Sequence[str],
    *,
    key: str,
    help: str = "",
    on_change: Callable[[], None] | None = None,
    other_label: str | None = None,
    join: str = ", ",
) -> str:
    """A multiselect that reveals a free-text input when "Other" is chosen.

    Returns the selections joined by ``join``. If "Other" was selected, the
    typed value replaces the literal "Other" in the output (or the literal
    is kept when the user left the input blank).
    """
    selections = st.multiselect(
        label,
        options,
        placeholder="Choose options",
        key=key,
        help=help,
        on_change=on_change,
    )
    items = list(selections)
    if "Other" in items:
        custom = st.text_input(
            other_label or f"Specify {label.lower()}",
            key=f"{key}_other",
            on_change=on_change,
        )
        if custom:
            items = [custom if x == "Other" else x for x in items]
    return join.join(items)
