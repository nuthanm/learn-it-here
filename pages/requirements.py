import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone
from components.header import _site_header_html
from components.footer import _footer_html, _scroll_nav_html, _copy_buttons_html
from config import PAGE_REQUIREMENTS, _on_interact, _nav_to
from services.supabase_client import save_to_supabase
from services.pdf_service import generate_pdf


def page_requirements():
    """Project requirements questionnaire — minimalist layout."""
    cb = _on_interact

    # Keep the URL in sync with the active page so the address bar always shows
    # `?page=requirements` (this is what makes the page sharable / bookmarkable
    # and prevents the URL from collapsing to "/" on subsequent reruns).
    if st.query_params.get("page") != PAGE_REQUIREMENTS:
        st.query_params["page"] = PAGE_REQUIREMENTS

    # Slim site header with text-link nav
    st.markdown(_site_header_html(active=PAGE_REQUIREMENTS), unsafe_allow_html=True)

    # Breadcrumb + title
    st.markdown(
        '<div class="breadcrumb">'
        '<a href="?go=home" target="_self">Home</a>'
        '<span class="breadcrumb-sep">/</span>'
        '<span class="breadcrumb-current">Requirements</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Post-submission view ─────────────────────────────────────────────────
    if st.session_state.submitted:
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
            st.download_button(
                label="Download requirements as PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"project_requirements_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.pdf",
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
            '<a class="text-link" href="?page=learn" target="_self">'
            "Browse the learning hub →</a>"
            '<a class="text-link" href="?page=requirements" target="_self" '
            'onclick="window.location.reload();">Submit another response</a>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(_footer_html(), unsafe_allow_html=True)
        components.html(_scroll_nav_html(), height=0)
        return

    # ── Page heading ─────────────────────────────────────────────────────────
    st.markdown('<h1 class="page-title">Project Requirements</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-lead">'
        "Capture your project's tech-stack details. "
        "Fill in the questions and download a shareable PDF."
        "</p>",
        unsafe_allow_html=True,
    )

    # ── Form ────────────────────────────────────────────────────────────────
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # ── Section 1: Version Management ──────────────────────────────
    st.markdown('<div class="section-label">Version Management</div>', unsafe_allow_html=True)
    vc = st.selectbox(
        "Version control",
        ["Git", "SVN (Subversion)", "TFS (Team Foundation)", "Mercurial", "Perforce", "None", "Other"],
        index=None, placeholder="Choose an option",
        key="version_control",
        help="Which version control system does your team use?",
        on_change=cb,
    )
    vc_other = ""
    if vc == "Other":
        vc_other = st.text_input("Specify version control", key="vc_other", on_change=cb)

    code_push = st.selectbox(
        "How do you push the code?",
        [
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
        ],
        index=None, placeholder="Choose an option",
        key="code_push",
        help="Which tool or method do you use to push code to the remote repository?",
        on_change=cb,
    )
    code_push_other = ""
    if code_push == "Other":
        code_push_other = st.text_input("Specify code push method", key="code_push_other", on_change=cb)

    # ── Section 2: Development Environment ─────────────────────────
    st.markdown('<div class="section-label">Development Environment</div>', unsafe_allow_html=True)
    ide = st.selectbox(
        "IDE or editor",
        [
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
        ],
        index=None, placeholder="Choose an option",
        key="ide",
        help="Select the IDE / editor your team primarily uses.",
        on_change=cb,
    )
    ide_other = ""
    if ide == "Other":
        ide_other = st.text_input("Specify IDE / Editor", key="ide_other", on_change=cb)

    deployment = st.multiselect(
        "Deployment approaches",
        [
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
        ],
        placeholder="Choose options",
        key="deployment",
        help="Select all deployment strategies that apply to your project.",
        on_change=cb,
    )
    deployment_other = ""
    if "Other" in deployment:
        deployment_other = st.text_input("Specify deployment approach", key="deployment_other", on_change=cb)

    # ── Section 3: Architecture ────────────────────────────────────
    st.markdown('<div class="section-label">Architecture</div>', unsafe_allow_html=True)
    architecture = st.multiselect(
        "Architecture patterns",
        [
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
        ],
        placeholder="Choose options",
        key="architecture",
        help="Select the architecture patterns followed in your project.",
        on_change=cb,
    )
    arch_other = ""
    if "Other" in architecture:
        arch_other = st.text_input("Specify architecture pattern", key="arch_other", on_change=cb)

    design_patterns = st.multiselect(
        "Design patterns",
        [
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
        ],
        placeholder="Choose options",
        key="design_patterns",
        help="Select the design patterns commonly used in your codebase.",
        on_change=cb,
    )
    dp_other = ""
    if "Other" in design_patterns:
        dp_other = st.text_input("Specify design pattern", key="dp_other", on_change=cb)

    orm = st.selectbox(
        "ORM",
        [
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
        ],
        index=None, placeholder="Choose an option",
        key="orm",
        help="Which ORM framework does your project use?",
        on_change=cb,
    )
    orm_other = ""
    if orm == "Other":
        orm_other = st.text_input("Specify ORM", key="orm_other", on_change=cb)

    # ── Section 4: Other ───────────────────────────────────────────
    st.markdown('<div class="section-label">Other</div>', unsafe_allow_html=True)
    additional_requirements = st.text_area(
        "Additional notes",
        placeholder="e.g. We use Docker for containerization, Redis for caching, CI/CD with GitHub Actions…",
        height=120,
        key="additional_requirements",
        help="Any other tools, frameworks, or notes you'd like to mention?",
        on_change=cb,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close .form-card

    # ── Action row: right-aligned Submit + text-link Cancel ─────────
    st.markdown('<div class="form-actions">', unsafe_allow_html=True)
    spacer, cancel_col, submit_col = st.columns([6, 2, 3])
    with cancel_col:
        st.markdown(
            '<a class="text-link" href="?go=home" target="_self" '
            'style="display:inline-block;padding-top:10px;">Cancel</a>',
            unsafe_allow_html=True,
        )
    with submit_col:
        submit_clicked = st.button(
            "Submit requirements", type="primary", use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Handle Submission ─────────────────────────────────────────────
    if submit_clicked:
        vc_val = vc if vc != "Other" else (vc_other or "Other")
        ide_val = ide if ide != "Other" else (ide_other or "Other")
        cp_val = code_push if code_push != "Other" else (code_push_other or "Other")

        deploy_list = list(deployment)
        if "Other" in deploy_list and deployment_other:
            deploy_list = [deployment_other if x == "Other" else x for x in deploy_list]
        deploy_val = ", ".join(deploy_list)

        arch_list = list(architecture)
        if "Other" in arch_list and arch_other:
            arch_list = [arch_other if x == "Other" else x for x in arch_list]
        arch_val = ", ".join(arch_list)

        dp_list = list(design_patterns)
        if "Other" in dp_list and dp_other:
            dp_list = [dp_other if x == "Other" else x for x in dp_list]
        dp_val = ", ".join(dp_list)

        orm_val = orm if orm != "Other" else (orm_other or "Other")

        record = {
            "submitted_at":      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version_control":   vc_val,
            "ide":               ide_val,
            "code_push":         cp_val,
            "deployment":        deploy_val,
            "architecture":      arch_val,
            "design_patterns":   dp_val,
            "orm":               orm_val,
            "additional_requirements": additional_requirements.strip(),
        }

        ok, db_msg = save_to_supabase(record)
        if ok:
            st.success(db_msg)
        else:
            st.info(f"ℹ️  {db_msg}")

        try:
            st.session_state.pdf_bytes = generate_pdf(record)
            st.session_state.pdf_error = None
        except Exception as exc:
            st.session_state.pdf_bytes = None
            st.session_state.pdf_error = str(exc)

        st.session_state.animation_state = "bye"
        st.session_state.submitted = True
        st.rerun()

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)
