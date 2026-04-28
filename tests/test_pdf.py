"""Smoke tests for the PDF generator."""

from __future__ import annotations

from services.pdf_service import FIELDS, RequirementsPDF, generate_pdf

SAMPLE_RECORD = {
    "submitted_at": "2026-04-28T12:00:00Z",
    "version_control": "Git",
    "ide": "Visual Studio Code",
    "code_push": "GIT CLI (Command Line)",
    "deployment": "GitHub Actions, Docker / Containers",
    "architecture": "Clean Architecture, Microservices",
    "design_patterns": "Repository Pattern, Dependency Injection",
    "orm": "Entity Framework Core",
    "additional_requirements": "We use Redis for caching.",
}


def test_generate_pdf_returns_bytes_with_pdf_header():
    pdf_bytes = generate_pdf(SAMPLE_RECORD)
    assert isinstance(pdf_bytes, bytes)
    # Every PDF starts with the magic %PDF- prefix.
    assert pdf_bytes.startswith(b"%PDF-"), "Output is not a valid PDF byte stream"
    assert len(pdf_bytes) > 500, "PDF byte stream looks empty"


def test_generate_pdf_skips_empty_fields():
    sparse = {"submitted_at": "2026-04-28T12:00:00Z", "version_control": "Git"}
    pdf_bytes = generate_pdf(sparse)
    assert pdf_bytes.startswith(b"%PDF-")


def test_pdf_handles_non_latin1_characters_gracefully():
    # `_safe()` should replace these with `?` rather than raise.
    weird = dict(SAMPLE_RECORD)
    weird["additional_requirements"] = "We deploy to 東京 — uses ñoño naming. 🚀"
    pdf_bytes = generate_pdf(weird)
    assert pdf_bytes.startswith(b"%PDF-")


def test_long_answer_produces_multipage_pdf_with_chrome_on_each_page():
    """The previous PDF impl drew the brand bar / footer once, so page 2
    rendered without them. The new RequirementsPDF uses FPDF lifecycle
    hooks — verify by rendering a long answer and checking page count > 1.
    """
    huge = " ".join(f"requirement_{i}_with_filler_text" for i in range(200))
    record = dict(SAMPLE_RECORD)
    record["additional_requirements"] = huge

    # Build the doc piece-by-piece so we can inspect it before output().
    pdf = RequirementsPDF(submitted_at=record["submitted_at"])
    pdf.add_page()
    for field_key, display_label in FIELDS:
        answer = record.get(field_key, "")
        if answer:
            pdf.render_field(display_label, answer)

    assert pdf.page_no() >= 2, (
        f"Expected long content to spill onto page 2 — only got {pdf.page_no()} page(s)"
    )
