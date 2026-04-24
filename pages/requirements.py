import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone
from components.panda import _robot_html
from components.footer import _footer_html, _scroll_nav_html, _copy_buttons_html
from config import _on_interact, _nav_to
from services.supabase_client import save_to_supabase
from services.pdf_service import generate_pdf


def page_requirements():
    """Project requirements questionnaire — professional layout, no sidebar."""
    cb = _on_interact

    # Nav bar (logo only, no back button at top)
    st.markdown(
        """
<div class="kfp-nav">
  <a href="?go=home" target="_self" class="kfp-nav-brand">
    <span class="kfp-nav-logo">🐼</span>
    <div class="kfp-nav-text">
      <div class="kfp-nav-title">Learn It Here</div>
      <div class="kfp-nav-tagline">Project Requirements</div>
    </div>
  </a>
</div>
""",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="app-title">📋 Project Requirements</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-subtitle">'
        "Capture your project's tech-stack details. "
        "Fill in the questions and download a shareable PDF."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Post-submission view ─────────────────────────────────────────────────
    if st.session_state.submitted:
        _, c2, _ = st.columns([1, 2, 1])
        with c2:
            st.markdown(
                """<div class="success-card">
  <div class="success-title">🎉 All done — great work!</div>
  <div class="success-sub">Your project requirements have been captured successfully.</div>
</div>""",
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.get("pdf_bytes"):
                st.download_button(
                    label="⬇️  Download Requirements as PDF",
                    data=st.session_state.pdf_bytes,
                    file_name=f"project_requirements_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                pdf_err = st.session_state.get("pdf_error", "")
                if pdf_err:
                    st.warning(f"PDF generation failed: {pdf_err}")
                else:
                    st.info("PDF could not be generated. Your requirements were still saved.")
            st.markdown("<br>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2, gap="medium")
            with sc1:
                if st.button("🎓 Go to Learning Hub →", type="primary", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    _nav_to("learn")
            with sc2:
                if st.button("📝 Submit Another Response", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()
        st.markdown(_footer_html(), unsafe_allow_html=True)
        components.html(_scroll_nav_html(), height=0)
        return

    # ── Full-width form layout ─────────────────────────────────────────────
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # ── Q1: Version Control ───────────────────────────────────────────
    st.markdown('<div class="section-label">Version Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-label">1. Version Control</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Which version control system does your team use?</div>',
        unsafe_allow_html=True,
    )
    vc = st.selectbox(
        "vc_select",
        ["Git", "SVN (Subversion)", "TFS (Team Foundation)", "Mercurial", "Perforce", "None", "Other"],
        index=None, placeholder="Choose an option",
        key="version_control", label_visibility="collapsed", on_change=cb,
    )
    vc_other = ""
    if vc == "Other":
        vc_other = st.text_input("Specify version control", key="vc_other", on_change=cb)

    # ── Q2: IDE or Editor ─────────────────────────────────────────────
    st.markdown('<div class="section-label">Development Environment</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-label">2. IDE or Editor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Select the IDE / editor your team primarily uses.</div>',
        unsafe_allow_html=True,
    )
    ide = st.selectbox(
        "ide_select",
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
        key="ide", label_visibility="collapsed", on_change=cb,
    )
    ide_other = ""
    if ide == "Other":
        ide_other = st.text_input("Specify IDE / Editor", key="ide_other", on_change=cb)

    # ── Q3: How do you push the code ──────────────────────────────────
    st.markdown('<div class="section-label">Code Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-label">3. How do you push the code?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Which tool or method do you use to push code to the remote repository?</div>',
        unsafe_allow_html=True,
    )
    code_push = st.selectbox(
        "code_push_select",
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
        key="code_push", label_visibility="collapsed", on_change=cb,
    )
    code_push_other = ""
    if code_push == "Other":
        code_push_other = st.text_input("Specify code push method", key="code_push_other", on_change=cb)

    # ── Q4: Deployment Approaches ─────────────────────────────────────
    st.markdown('<div class="section-label">Deployment &amp; DevOps</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-label">4. Which deployment approaches are you following?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Select all deployment strategies that apply to your project.</div>',
        unsafe_allow_html=True,
    )
    deployment = st.multiselect(
        "deployment_select",
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
        key="deployment", label_visibility="collapsed", on_change=cb,
    )
    deployment_other = ""
    if "Other" in deployment:
        deployment_other = st.text_input("Specify deployment approach", key="deployment_other", on_change=cb)

    # ── Q5: Architecture Patterns ─────────────────────────────────────
    st.markdown('<div class="section-label">Architecture &amp; Design</div>', unsafe_allow_html=True)
    st.markdown('<div class="q-label">5. Architecture Patterns</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Select the architecture patterns followed in your project.</div>',
        unsafe_allow_html=True,
    )
    architecture = st.multiselect(
        "arch_select",
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
        key="architecture", label_visibility="collapsed", on_change=cb,
    )
    arch_other = ""
    if "Other" in architecture:
        arch_other = st.text_input("Specify architecture pattern", key="arch_other", on_change=cb)

    # ── Q6: Design Patterns ───────────────────────────────────────────
    st.markdown('<div class="q-label">6. Design Patterns</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Select the design patterns commonly used in your codebase.</div>',
        unsafe_allow_html=True,
    )
    design_patterns = st.multiselect(
        "dp_select",
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
        key="design_patterns", label_visibility="collapsed", on_change=cb,
    )
    dp_other = ""
    if "Other" in design_patterns:
        dp_other = st.text_input("Specify design pattern", key="dp_other", on_change=cb)

    # ── Q7: ORM ───────────────────────────────────────────────────────
    st.markdown('<div class="q-label">7. ORM (Object-Relational Mapping)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Which ORM framework does your project use?</div>',
        unsafe_allow_html=True,
    )
    orm = st.selectbox(
        "orm_select",
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
        key="orm", label_visibility="collapsed", on_change=cb,
    )
    orm_other = ""
    if orm == "Other":
        orm_other = st.text_input("Specify ORM", key="orm_other", on_change=cb)

    # ── Additional Requirements ─────────────────────────────────────
    st.markdown('<div class="q-label">8. Additional Requirements</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="q-hint">Any other tools, frameworks, or notes you\'d like to mention?</div>',
        unsafe_allow_html=True,
    )
    additional_requirements = st.text_area(
        "additional_requirements",
        placeholder="e.g. We use Docker for containerization, Redis for caching, CI/CD with GitHub Actions…",
        height=120,
        key="additional_requirements", label_visibility="collapsed", on_change=cb,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close .form-card

    # ── Action Buttons: Submit | Back to Home ─────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    btn1, btn2 = st.columns(2, gap="medium")
    with btn1:
        submit_clicked = st.button(
            "Submit Requirements →", type="primary", use_container_width=True
        )
    with btn2:
        back_clicked = st.button(
            "← Back to Home", use_container_width=True
        )

    if back_clicked:
        _nav_to("landing")

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


# ── Suggest-topic dialog (module-level so the decorator is stable) ────────────

