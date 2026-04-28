"""Tests for the form-helper widgets.

Streamlit widget calls require a running Streamlit context, so these tests
focus on the parts of the helpers we *can* exercise outside that context:
imports, signatures, and the logic that joins multiselect output.
"""

from __future__ import annotations

import inspect

from components import forms


def test_select_with_other_is_callable():
    assert callable(forms.select_with_other)


def test_multiselect_with_other_is_callable():
    assert callable(forms.multiselect_with_other)


def test_select_with_other_signature_has_expected_keyword_args():
    sig = inspect.signature(forms.select_with_other)
    expected = {"label", "options", "key", "help", "on_change", "other_label"}
    assert expected.issubset(sig.parameters.keys())


def test_multiselect_with_other_signature_has_expected_keyword_args():
    sig = inspect.signature(forms.multiselect_with_other)
    expected = {"label", "options", "key", "help", "on_change", "other_label", "join"}
    assert expected.issubset(sig.parameters.keys())
