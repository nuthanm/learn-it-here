"""Project requirements questionnaire — single-page form.

All questions live on one page (no wizard / progress bar). The list of
questions in ``STEPS`` remains the single source of truth: the landing
page reads ``len(STEPS)`` for the trust-strip counter, and adding or
removing a question here automatically updates that count.
"""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components

from components.footer import _copy_buttons_html, _footer_html, _scroll_nav_html
from components.header import _site_header_html
from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    PAGE_REQUIREMENTS,
    _on_interact,
    _url_for,
)
from services.pdf_service import generate_pdf
from services.supabase_client import save_to_supabase

# ── Question option lists ────────────────────────────────────────────────────
VC_OPTIONS = [
    "Git", "SVN (Subversion)", "TFS (Team Foundation)", "Mercurial",
    "Perforce", "None", "Other",
]
CODE_PUSH_OPTIONS = [
    "GIT CLI (Command Line)", "GitHub Desktop", "Visual Studio Built-in Git",
    "VS Code Built-in Git", "SourceTree", "GitKraken", "TortoiseGit",
    "Azure DevOps (Web Push)", "Fork (Git Client)", "Other",
]
IDE_OPTIONS = [
    "Visual Studio (Full IDE)", "Visual Studio Code", "IntelliJ IDEA",
    "Eclipse", "Rider (JetBrains)", "PyCharm", "WebStorm", "Sublime Text",
    "Atom", "Notepad++", "Vim / Neovim", "Other",
]
DEPLOYMENT_OPTIONS = [
    "Azure DevOps Pipelines (CI/CD)", "GitHub Actions", "Jenkins",
    "AWS CodePipeline", "Docker / Containers", "Kubernetes (K8s)",
    "Manual / FTP Deploy", "Azure App Service", "IIS Direct Deploy", "Other",
]
ARCHITECTURE_OPTIONS = [
    "Clean Architecture", "Microservices", "Monolithic", "Layered (N-Tier)",
    "Event-Driven", "Serverless", "CQRS", "DDD (Domain-Driven Design)",
    "Hexagonal (Ports & Adapters)", "MVC", "Other",
]
DESIGN_PATTERN_OPTIONS = [
    "Repository Pattern", "Unit of Work", "Singleton", "Factory", "Strategy",
    "Observer", "Mediator (MediatR)", "Dependency Injection",
    "SOLID Principles", "Builder", "Decorator", "Other",
]
ORM_OPTIONS = [
    "Entity Framework Core", "Entity Framework 6", "Dapper", "NHibernate",
    "ADO.NET (Raw)", "Hibernate (Java)", "SQLAlchemy (Python)",
    "Django ORM (Python)", "Sequelize (Node.js)", "Prisma (Node.js)",
    "None / Not applicable", "Other",
]


# ── Question definitions ─────────────────────────────────────────────────────
# Single source of truth for the questionnaire. The landing page reads
# ``len(STEPS)`` to render the dynamic question count, and the form below
# iterates this list, so adding / removing / reordering a question here is
# the *only* place you need to change.
STEPS = [
    {"key": "version_control", "title": "Version control",
     "help": "Which version control system does your team use?",
     "kind": "select", "options": VC_OPTIONS, "section": "Version Management"},
    {"key": "code_push", "title": "How do you push the code?",
     "help": "Which tool or method do you use to push code to the remote repository?",
     "kind": "select", "options": CODE_PUSH_OPTIONS, "section": "Version Management"},
    {"key": "ide", "title": "IDE or editor",
     "help": "Select the IDE / editor your team primarily uses.",
     "kind": "select", "options": IDE_OPTIONS, "section": "Development Environment"},
    {"key": "deployment", "title": "Deployment approaches",
     "help": "Select all deployment strategies that apply to your project.",
     "kind": "multi", "options": DEPLOYMENT_OPTIONS, "section": "Development Environment"},
    {"key": "architecture", "title": "Architecture patterns",
     "help": "Select the architecture patterns followed in your project.",
     "kind": "multi", "options": ARCHITECTURE_OPTIONS, "section": "Architecture"},
    {"key": "design_patterns", "title": "Design patterns",
     "help": "Select the design patterns commonly used in your codebase.",
     "kind": "multi", "options": DESIGN_PATTERN_OPTIONS, "section": "Architecture"},
    {"key": "orm", "title": "ORM",
     "help": "Which ORM framework does your project use?",
     "kind": "select", "options": ORM_OPTIONS, "section": "Architecture"},
    {"key": "additional_requirements", "title": "Additional notes",
     "help": "Any other tools, frameworks, or notes you'd like to mention?",
     "kind": "text", "section": "Other",
     "placeholder": (
         "e.g. We use Docker for containerization, Redis for caching, "
         "CI/CD with GitHub Actions…"
     )},
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def _render_widget(step: dict) -> object:
    """Render the widget for a question and return its current value."""
    cb = _on_interact
    key = step["key"]
    kind = step["kind"]
    label = step["title"]
    help_text = step.get("help")

    if kind == "select":
        value = st.selectbox(
            label, step["options"],
            index=None, placeholder="Choose an option",
            key=key, help=help_text, on_change=cb,
        )
        if value == "Other":
            st.text_input(
                f"Specify {label.lower()}",
                key=f"{key}_other", on_change=cb,
            )
        return value

    if kind == "multi":
        value = st.multiselect(
            label, step["options"],
            placeholder="Choose options",
            key=key, help=help_text, on_change=cb,
        )
        if "Other" in (value or []):
            st.text_input(
                f"Specify other {label.lower()}",
                key=f"{key}_other", on_change=cb,
            )
        return value

    # kind == "text"
    return st.text_area(
        label,
        placeholder=step.get("placeholder", ""),
        height=120,
        key=key, help=help_text, on_change=cb,
    )


def _resolve_select(key: str, value) -> str:
    if value is None:
        return ""
    if value == "Other":
        return (st.session_state.get(f"{key}_other") or "Other").strip()
    return value


def _resolve_multi(key: str, value) -> str:
    items = list(value or [])
    other = (st.session_state.get(f"{key}_other") or "").strip()
    if "Other" in items and other:
        items = [other if x == "Other" else x for x in items]
    return ", ".join(items)


def _build_record() -> dict:
    """Translate session_state answers into the persistence record shape."""
    out = {
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    for step in STEPS:
        key = step["key"]
        val = st.session_state.get(key)
        if step["kind"] == "select":
            out[key] = _resolve_select(key, val)
        elif step["kind"] == "multi":
            out[key] = _resolve_multi(key, val)
        else:  # text
            out[key] = (val or "").strip()
    return out


def _submit(record: dict) -> None:
    ok, db_msg = save_to_supabase(record)
    if ok:
        st.success(db_msg)
    else:
        st.info(f"ℹ️  {db_msg}")
    try:
        st.session_state.pdf_bytes = generate_pdf(record)
        st.session_state.pdf_error = None
    except Exception as exc:  # pragma: no cover — defensive
        st.session_state.pdf_bytes = None
        st.session_state.pdf_error = str(exc)
    st.session_state.animation_state = "bye"
    st.session_state.submitted = True
    st.rerun()


def _render_success() -> None:
    st.markdown('<div class="success-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<h1 class="page-title">All done — great work</h1>'
        '<p class="page-lead">Your project requirements have been captured.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="success-card">'
        '<div class="success-title">🎉 Submission saved</div>'
        '<div class="success-sub">Download a shareable PDF of your project '
        'brief below, or move on to the learning hub.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    pdf_bytes = st.session_state.get("pdf_bytes")
    pdf_err = st.session_state.get("pdf_error", "")

    # Two-button action row + onward link, all width-matched.
    st.markdown('<div class="success-actions">', unsafe_allow_html=True)
    dl_col, again_col = st.columns(2, gap="small")
    with dl_col:
        if pdf_bytes:
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📄  Download PDF",
                data=pdf_bytes,
                file_name=f"project_requirements_{ts}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            # Render a disabled-looking placeholder so the row stays balanced.
            st.button("📄  Download PDF", disabled=True, use_container_width=True)
    with again_col:
        if st.button(
            "Submit another response",
            key="reset_form",
            use_container_width=True,
        ):
            for step in STEPS:
                st.session_state.pop(step["key"], None)
                st.session_state.pop(f"{step['key']}_other", None)
            st.session_state.pop("pdf_bytes", None)
            st.session_state.pop("pdf_error", None)
            st.session_state.submitted = False
            st.session_state.animation_state = "welcome"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if not pdf_bytes:
        if pdf_err:
            st.warning(f"PDF generation failed: {pdf_err}")
        else:
            st.info("PDF could not be generated. Your requirements were still saved.")

    st.markdown(
        f'<div class="success-footnote">'
        f'<a class="text-link" href="{_url_for(PAGE_LEARN)}" target="_self">'
        "Browse the learning hub →</a></div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # close .success-wrap


# ── Public page entry point ──────────────────────────────────────────────────
def page_requirements():
    """Project requirements questionnaire — single-page form."""
    for _k in ("page", "go", "section", "sub"):
        if _k in st.query_params:
            del st.query_params[_k]

    st.markdown(_site_header_html(active=PAGE_REQUIREMENTS), unsafe_allow_html=True)

    st.markdown(
        '<div class="breadcrumb">'
        f'<a href="{_url_for(PAGE_LANDING)}" target="_self">Home</a>'
        '<span class="breadcrumb-sep">/</span>'
        '<span class="breadcrumb-current">Requirements</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("submitted"):
        _render_success()
        st.markdown(_footer_html(), unsafe_allow_html=True)
        components.html(_scroll_nav_html(), height=0)
        return

    # Page heading
    st.markdown(
        '<h1 class="page-title">Project Requirements</h1>'
        '<p class="page-lead">'
        f"Capture your project's tech-stack details across {len(STEPS)} questions, "
        "then download a shareable PDF."
        "</p>",
        unsafe_allow_html=True,
    )

    # Form card — group questions by their declared "section" header.
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    last_section = None
    for step in STEPS:
        if step.get("section") and step["section"] != last_section:
            st.markdown(
                f'<div class="section-label">{step["section"]}</div>',
                unsafe_allow_html=True,
            )
            last_section = step["section"]
        _render_widget(step)

    st.markdown("</div>", unsafe_allow_html=True)  # close .form-card

    # Action row — Cancel rendered as a ghost-button anchor so it visually
    # balances the primary Submit button. The previous `.form-actions` flex
    # wrapper was a no-op (Streamlit flushes raw `st.markdown` divs into
    # their own container, so the wrapper never actually contained the
    # columns below it) — we use the column layout directly instead.
    _spacer, cancel_col, submit_col = st.columns([6, 2, 3])
    with cancel_col:
        st.markdown(
            f'<a class="btn-link-secondary" '
            f'href="{_url_for(PAGE_LANDING)}" target="_self">Cancel</a>',
            unsafe_allow_html=True,
        )
    with submit_col:
        submit_clicked = st.button(
            "Submit requirements", type="primary", use_container_width=True,
        )

    if submit_clicked:
        _submit(_build_record())

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)
