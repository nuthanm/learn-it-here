"""Project requirements questionnaire page."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components

from components.footer import copy_buttons_html, footer_html, scroll_nav_html
from components.forms import multiselect_with_other, select_with_other
from components.header import site_header_html
from config import (
    PAGE_LANDING,
    PAGE_LEARN,
    PAGE_REQUIREMENTS,
    on_interact,
    url_for,
)
from models import RequirementsRecord
from services.pdf_service import generate_pdf
from services.supabase_client import save_requirements

# ── Question option lists ────────────────────────────────────────────────────
VC_OPTIONS = [
    "Git",
    "SVN (Subversion)",
    "TFS (Team Foundation)",
    "Mercurial",
    "Perforce",
    "None",
    "Other",
]
CODE_PUSH_OPTIONS = [
    "GIT CLI (Command Line)",
    "GitHub Desktop",
    "Visual Studio Built-in Git",
    "VS Code Built-in Git",
    "SourceTree",
    "GitKraken",
    "TortoiseGit",
    "Azure DevOps (Web Push)",
    "Fork (Git Client)",
    "Other",
]
IDE_OPTIONS = [
    "Visual Studio (Full IDE)",
    "Visual Studio Code",
    "IntelliJ IDEA",
    "Eclipse",
    "Rider (JetBrains)",
    "PyCharm",
    "WebStorm",
    "Sublime Text",
    "Atom",
    "Notepad++",
    "Vim / Neovim",
    "Other",
]
DEPLOYMENT_OPTIONS = [
    "Azure DevOps Pipelines (CI/CD)",
    "GitHub Actions",
    "Jenkins",
    "AWS CodePipeline",
    "Docker / Containers",
    "Kubernetes (K8s)",
    "Manual / FTP Deploy",
    "Azure App Service",
    "IIS Direct Deploy",
    "Other",
]
ARCHITECTURE_OPTIONS = [
    "Clean Architecture",
    "Microservices",
    "Monolithic",
    "Layered (N-Tier)",
    "Event-Driven",
    "Serverless",
    "CQRS",
    "DDD (Domain-Driven Design)",
    "Hexagonal (Ports & Adapters)",
    "MVC",
    "Other",
]
DESIGN_PATTERN_OPTIONS = [
    "Repository Pattern",
    "Unit of Work",
    "Singleton",
    "Factory",
    "Strategy",
    "Observer",
    "Mediator (MediatR)",
    "Dependency Injection",
    "SOLID Principles",
    "Builder",
    "Decorator",
    "Other",
]
ORM_OPTIONS = [
    "Entity Framework Core",
    "Entity Framework 6",
    "Dapper",
    "NHibernate",
    "ADO.NET (Raw)",
    "Hibernate (Java)",
    "SQLAlchemy (Python)",
    "Django ORM (Python)",
    "Sequelize (Node.js)",
    "Prisma (Node.js)",
    "None / Not applicable",
    "Other",
]


def _strip_legacy_query_params() -> None:
    """Drop any stale query keys left over from the legacy URL scheme."""
    for key in ("page", "go", "section", "sub"):
        if key in st.query_params:
            del st.query_params[key]


def _render_post_submission_view() -> None:
    """The thank-you screen with a PDF download and quick links."""
    st.markdown(
        '<h1 class="page-title">All done — great work</h1>'
        '<p class="page-lead">Your project requirements have been captured.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="success-card">'
        '<div class="success-title">🎉 Submission saved</div>'
        '<div class="success-sub">Download a shareable PDF of your project brief below.</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.get("pdf_bytes"):
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download requirements as PDF",
            data=st.session_state.pdf_bytes,
            file_name=f"project_requirements_{ts}.pdf",
            mime="application/pdf",
        )
    else:
        pdf_err = st.session_state.get("pdf_error", "")
        if pdf_err:
            st.warning(f"PDF generation failed: {pdf_err}")
        else:
            st.info("PDF could not be generated. Your requirements were still saved.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:16px;align-items:center;">'
        f'<a class="text-link" href="{url_for(PAGE_LEARN)}" target="_self">'
        "Browse the learning hub →</a>"
        f'<a class="text-link" href="{url_for(PAGE_REQUIREMENTS)}" target="_self" '
        'onclick="window.location.reload();">Submit another response</a>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(footer_html(), unsafe_allow_html=True)
    components.html(scroll_nav_html(), height=0)


def _render_form() -> RequirementsRecord | None:
    """Render the requirements form. Returns the record on submit, else ``None``."""
    cb = on_interact

    st.markdown('<h1 class="page-title">Project Requirements</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-lead">'
        "Capture your project's tech-stack details. "
        "Fill in the questions and download a shareable PDF."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # ── Section 1: Version Management ───────────────────────────────
    st.markdown('<div class="section-label">Version Management</div>', unsafe_allow_html=True)
    vc_val = select_with_other(
        "Version control",
        VC_OPTIONS,
        key="version_control",
        help="Which version control system does your team use?",
        on_change=cb,
        other_label="Specify version control",
    )
    code_push_val = select_with_other(
        "How do you push the code?",
        CODE_PUSH_OPTIONS,
        key="code_push",
        help="Which tool or method do you use to push code to the remote repository?",
        on_change=cb,
        other_label="Specify code push method",
    )

    # ── Section 2: Development Environment ──────────────────────────
    st.markdown(
        '<div class="section-label">Development Environment</div>',
        unsafe_allow_html=True,
    )
    ide_val = select_with_other(
        "IDE or editor",
        IDE_OPTIONS,
        key="ide",
        help="Select the IDE / editor your team primarily uses.",
        on_change=cb,
        other_label="Specify IDE / Editor",
    )
    deployment_val = multiselect_with_other(
        "Deployment approaches",
        DEPLOYMENT_OPTIONS,
        key="deployment",
        help="Select all deployment strategies that apply to your project.",
        on_change=cb,
        other_label="Specify deployment approach",
    )

    # ── Section 3: Architecture ─────────────────────────────────────
    st.markdown('<div class="section-label">Architecture</div>', unsafe_allow_html=True)
    arch_val = multiselect_with_other(
        "Architecture patterns",
        ARCHITECTURE_OPTIONS,
        key="architecture",
        help="Select the architecture patterns followed in your project.",
        on_change=cb,
        other_label="Specify architecture pattern",
    )
    dp_val = multiselect_with_other(
        "Design patterns",
        DESIGN_PATTERN_OPTIONS,
        key="design_patterns",
        help="Select the design patterns commonly used in your codebase.",
        on_change=cb,
        other_label="Specify design pattern",
    )
    orm_val = select_with_other(
        "ORM",
        ORM_OPTIONS,
        key="orm",
        help="Which ORM framework does your project use?",
        on_change=cb,
        other_label="Specify ORM",
    )

    # ── Section 4: Other ────────────────────────────────────────────
    st.markdown('<div class="section-label">Other</div>', unsafe_allow_html=True)
    additional = st.text_area(
        "Additional notes",
        placeholder=(
            "e.g. We use Docker for containerization, Redis for caching, CI/CD with GitHub Actions…"
        ),
        height=120,
        key="additional_requirements",
        help="Any other tools, frameworks, or notes you'd like to mention?",
        on_change=cb,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close .form-card

    # ── Action row ─────────────────────────────────────────────────
    st.markdown('<div class="form-actions">', unsafe_allow_html=True)
    _spacer, cancel_col, submit_col = st.columns([6, 2, 3])
    with cancel_col:
        st.markdown(
            f'<a class="text-link" href="{url_for(PAGE_LANDING)}" target="_self" '
            'style="display:inline-block;padding-top:10px;">Cancel</a>',
            unsafe_allow_html=True,
        )
    with submit_col:
        submit_clicked = st.button("Submit requirements", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not submit_clicked:
        return None

    record: RequirementsRecord = {
        "submitted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version_control": vc_val,
        "ide": ide_val,
        "code_push": code_push_val,
        "deployment": deployment_val,
        "architecture": arch_val,
        "design_patterns": dp_val,
        "orm": orm_val,
        "additional_requirements": additional.strip(),
    }
    return record


def page_requirements() -> None:
    """Project requirements questionnaire — minimalist layout."""
    st.markdown(site_header_html(active=PAGE_REQUIREMENTS), unsafe_allow_html=True)
    _strip_legacy_query_params()

    # Breadcrumb
    st.markdown(
        '<div class="breadcrumb">'
        f'<a href="{url_for(PAGE_LANDING)}" target="_self">Home</a>'
        '<span class="breadcrumb-sep">/</span>'
        '<span class="breadcrumb-current">Requirements</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    # Branch: post-submission thank-you screen vs the form itself.
    if st.session_state.submitted:
        _render_post_submission_view()
        return

    record = _render_form()
    if record is None:
        st.markdown(footer_html(), unsafe_allow_html=True)
        components.html(scroll_nav_html(), height=0)
        components.html(copy_buttons_html(), height=0)
        return

    # ── Submission handling ─────────────────────────────────────────
    save_result = save_requirements(record)
    if save_result.ok:
        st.success(save_result.message)
    else:
        st.info(f"ℹ️  {save_result.message}")

    try:
        st.session_state.pdf_bytes = generate_pdf(record)
        st.session_state.pdf_error = None
    except Exception as exc:  # noqa: BLE001 - PDF lib can raise many things
        st.session_state.pdf_bytes = None
        st.session_state.pdf_error = str(exc)

    st.session_state.animation_state = "bye"
    st.session_state.submitted = True
    st.rerun()
