"""Tests for the domain models."""

from __future__ import annotations

from models import RequirementsRecord, SaveResult


def test_save_result_is_immutable():
    """``frozen=True`` — once created, fields cannot be reassigned."""
    result = SaveResult(ok=True, message="saved")
    assert result.ok is True
    assert result.message == "saved"

    raised = False
    try:
        result.ok = False  # type: ignore[misc]
    except Exception:
        raised = True
    assert raised, "SaveResult should be frozen"


def test_save_result_equality():
    a = SaveResult(ok=True, message="x")
    b = SaveResult(ok=True, message="x")
    c = SaveResult(ok=False, message="x")
    assert a == b
    assert a != c


def test_requirements_record_accepts_partial_data():
    """``total=False`` — records can be built incrementally."""
    record: RequirementsRecord = {"version_control": "Git"}
    assert record["version_control"] == "Git"
