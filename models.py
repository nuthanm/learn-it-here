"""Domain models — the typed shapes used across the app.

Centralising these here means the form (`pages/requirements.py`), the
persistence layer (`services/supabase_client.py`), and the PDF generator
(`services/pdf_service.py`) all agree on what a "requirements record" is.
"""

from dataclasses import dataclass
from typing import TypedDict


class RequirementsRecord(TypedDict, total=False):
    """The shape of a project-requirements submission.

    `total=False` because the form is built incrementally and some fields
    may legitimately be empty strings rather than missing keys.
    """

    submitted_at: str
    version_control: str
    ide: str
    code_push: str
    deployment: str
    architecture: str
    design_patterns: str
    orm: str
    additional_requirements: str


@dataclass(frozen=True)
class SaveResult:
    """Outcome of a persistence call.

    `ok` reports success; `message` is always populated with something the
    UI can show the user (success confirmation or human-readable failure).
    """

    ok: bool
    message: str
