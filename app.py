"""Project Requirements Questionnaire
A single-page Streamlit app to capture project tech-stack requirements.
Stores responses in Supabase (PostgreSQL) and allows PDF export.
"""

import os
import streamlit as st
from datetime import datetime

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Project Requirements Questionnaire",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session State Initialization ──────────────────────────────────────────────
_DEFAULTS = {
    "animation_state": "welcome",
    "submitted": False,
    "pdf_bytes": None,
    "interacted": False,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


def _on_interact():
    """Switch robot from 'welcome' to 'thinking' on first form interaction."""
    if not st.session_state.interacted:
        st.session_state.interacted = True
        st.session_state.animation_state = "thinking"


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
  /* Global background */
  [data-testid="stAppViewContainer"] { background: #F0F5FF; }
  [data-testid="stHeader"] { background: transparent; }
  .block-container { padding-top: 2rem; max-width: 1200px; }

  /* Title */
  .app-title {
    font-size: 1.9rem; font-weight: 700; color: #1E3A5F;
    letter-spacing: -0.5px; margin-bottom: 0.2rem;
  }
  .app-subtitle {
    font-size: 0.92rem; color: #64748B; margin-bottom: 1.8rem;
  }

  /* Form card */
  .form-card {
    background: #ffffff; border-radius: 18px;
    padding: 2rem 2.2rem; border: 1px solid #E2E8F0;
    box-shadow: 0 4px 24px rgba(30,58,95,0.07);
  }

  /* Question labels */
  .q-label {
    font-size: 0.93rem; font-weight: 600; color: #1E3A5F; margin-bottom: 2px;
  }
  .q-hint {
    font-size: 0.76rem; color: #94A3B8; margin-bottom: 4px; font-style: italic;
  }
  .section-label {
    font-size: 0.7rem; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-top: 1.4rem; margin-bottom: 2px;
  }

  /* Submit button */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-size: 1rem !important;
    font-weight: 600 !important; width: 100% !important;
    padding: 0.65rem 0 !important;
    box-shadow: 0 4px 16px rgba(59,130,246,0.35) !important;
    transition: opacity 0.2s !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover {
    opacity: 0.88 !important;
  }

  /* Download button */
  div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.35) !important;
  }

  /* Success card */
  .success-card {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid #BFDBFE; border-radius: 18px;
    padding: 2.5rem 3rem; text-align: center;
  }
  .success-title { font-size: 1.6rem; font-weight: 700; color: #1E40AF; margin-bottom: 0.4rem; }
  .success-sub   { font-size: 0.95rem; color: #3B82F6; margin-bottom: 1.8rem; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Animated Robot HTML ───────────────────────────────────────────────────────
def _robot_html(state: str) -> str:
    """Return an animated robot HTML component for the given state."""
    _messages = {
        "welcome": (
            "Welcome! 👋<br>I'm here to help you capture your project "
            "requirements.<br>Fill in the form to get started!"
        ),
        "thinking": (
            "Hmm, thinking along<br>with you… 🤔"
            "<br><span class='dots'><span>.</span><span>.</span><span>.</span></span>"
        ),
        "bye": (
            "Thank you! 🎉<br>Your requirements have been saved.<br>"
            "Download your PDF below!<br>See you soon 👋"
        ),
    }
    msg = _messages.get(state, _messages["welcome"])

    arm_left_cls = "arm arm-left" + (" wave-left" if state == "bye" else "")
    arm_right_cls = "arm arm-right" + (
        " wave-right" if state in ("welcome", "bye") else ""
    )
    body_cls = "robot-wrap" + (" think-bob" if state == "thinking" else "")
    mouth_cls = "mouth" + (" mouth-bye" if state == "bye" else "")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    background:transparent;
    display:flex;flex-direction:column;align-items:center;
    justify-content:flex-start;padding-top:24px;
    font-family:'Segoe UI',system-ui,sans-serif;min-height:460px;
  }}

  /* ─ Speech Bubble ─ */
  .bubble{{
    background:#fff;border:2px solid #BFDBFE;border-radius:18px;
    padding:14px 20px;font-size:13.5px;color:#1E40AF;
    max-width:240px;text-align:center;line-height:1.6;
    box-shadow:0 4px 20px rgba(59,130,246,.13);
    animation:fadeUp .45s ease forwards;position:relative;
    margin-bottom:20px;
  }}
  .bubble::after{{
    content:'';position:absolute;bottom:-13px;left:50%;
    transform:translateX(-50%);
    border:10px solid transparent;border-top-color:#BFDBFE;
  }}

  /* ─ Robot ─ */
  .{body_cls.split()[0]}{{
    display:flex;flex-direction:column;align-items:center;gap:0;
  }}
  {'.' + body_cls.split()[1] + '{animation:thinkBob 2s ease-in-out infinite;}' if 'think-bob' in body_cls else ''}

  /* Antenna */
  .antenna-stem{{
    width:4px;height:22px;background:#93C5FD;border-radius:2px;position:relative;
  }}
  .antenna-ball{{
    width:14px;height:14px;
    background:radial-gradient(circle at 35% 35%,#93C5FD,#3B82F6);
    border-radius:50%;position:absolute;top:-16px;left:50%;
    transform:translateX(-50%);
    animation:antPulse 2s infinite;
  }}
  @keyframes antPulse{{
    0%,100%{{box-shadow:0 0 8px rgba(59,130,246,.5)}}
    50%{{box-shadow:0 0 20px rgba(59,130,246,.9)}}
  }}

  /* Head */
  .head{{
    width:82px;height:70px;
    background:linear-gradient(145deg,#60A5FA,#2563EB);
    border-radius:18px;
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;
    box-shadow:0 6px 22px rgba(37,99,235,.35),inset 0 1px 0 rgba(255,255,255,.2);
  }}
  .eyes{{display:flex;gap:17px;}}
  .eye{{
    width:15px;height:15px;background:#fff;border-radius:50%;position:relative;
    animation:blink 5s infinite;
  }}
  .eye::after{{
    content:'';position:absolute;width:7px;height:7px;
    background:#1E40AF;border-radius:50%;
    top:50%;left:50%;transform:translate(-50%,-50%);
  }}
  @keyframes blink{{0%,88%,100%{{transform:scaleY(1)}}90%{{transform:scaleY(.1)}}}}

  .mouth{{width:28px;height:10px;border-bottom:3px solid #fff;border-radius:0 0 14px 14px;opacity:.85;}}
  .mouth-bye{{width:32px;height:14px;border-bottom:3px solid #fff;border-radius:50%;}}

  /* Torso row */
  .torso{{display:flex;align-items:flex-start;gap:5px;margin-top:4px;}}
  .body-main{{
    width:72px;height:76px;
    background:linear-gradient(145deg,#93C5FD,#3B82F6);
    border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 4px 16px rgba(59,130,246,.25),inset 0 1px 0 rgba(255,255,255,.2);
  }}
  .chest-led{{
    width:22px;height:22px;
    background:radial-gradient(circle at 35% 35%,#BFDBFE,#60A5FA);
    border-radius:50%;border:2.5px solid rgba(255,255,255,.7);
    animation:ledPulse 1.8s infinite;
  }}
  @keyframes ledPulse{{
    0%,100%{{box-shadow:0 0 0 0 rgba(191,219,254,.7)}}
    50%{{box-shadow:0 0 0 9px rgba(191,219,254,0)}}
  }}

  .arm{{width:18px;height:60px;background:linear-gradient(145deg,#93C5FD,#3B82F6);border-radius:9px;box-shadow:0 2px 8px rgba(59,130,246,.2);}}
  .arm-left{{transform-origin:top center;}}
  .arm-right{{transform-origin:top center;}}
  .wave-right{{animation:waveR .65s ease-in-out infinite;}}
  .wave-left{{animation:waveL .65s ease-in-out infinite;animation-delay:.15s;}}
  @keyframes waveR{{0%,100%{{transform:rotate(-15deg)}}50%{{transform:rotate(45deg)}}}}
  @keyframes waveL{{0%,100%{{transform:rotate(15deg)}}50%{{transform:rotate(-45deg)}}}}

  /* Legs */
  .legs{{display:flex;gap:12px;margin-top:4px;}}
  .leg{{width:22px;height:32px;background:linear-gradient(145deg,#60A5FA,#2563EB);border-radius:0 0 10px 10px;box-shadow:0 3px 8px rgba(37,99,235,.2);}}

  /* Thinking dots */
  .dots span{{display:inline-block;animation:dotBounce 1.2s infinite;font-size:16px;font-weight:700;color:#3B82F6;}}
  .dots span:nth-child(2){{animation-delay:.2s}}
  .dots span:nth-child(3){{animation-delay:.4s}}
  @keyframes dotBounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}

  @keyframes thinkBob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
  @keyframes fadeUp{{from{{opacity:0;transform:translateY(-12px)}}to{{opacity:1;transform:translateY(0)}}}}
</style></head>
<body>
  <div class="bubble">{msg}</div>
  <div class="{body_cls}">
    <div style="position:relative;display:flex;flex-direction:column;align-items:center;">
      <div class="antenna-stem"><div class="antenna-ball"></div></div>
      <div class="head">
        <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
        <div class="{mouth_cls}"></div>
      </div>
      <div class="torso">
        <div class="{arm_left_cls}"></div>
        <div class="body-main"><div class="chest-led"></div></div>
        <div class="{arm_right_cls}"></div>
      </div>
      <div class="legs"><div class="leg"></div><div class="leg"></div></div>
    </div>
  </div>
</body></html>"""


# ── PDF Generation ────────────────────────────────────────────────────────────
def _safe(text) -> str:
    """Strip characters outside Latin-1 for built-in PDF fonts."""
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


def generate_pdf(data: dict) -> bytes:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos

    FIELDS = [
        ("version_control",  "1. Version Control"),
        ("ide",              "2. IDE / Editor"),
        ("dotnet_csharp",    "3. .NET / C# Version"),
        ("ef_core",          "4. EF Core Version"),
        ("architecture",     "5. Architecture & Design Patterns"),
        ("deployment",       "6. Deployment Process"),
        ("crystal_report",   "7. Crystal Reports Requirement"),
        ("local_testing",    "8. Local Testing Feasibility"),
        ("logging_tools",    "9. Logging / Tracing Tools"),
        ("project_mgmt",     "10. Project Management Tool"),
        ("unit_testing",     "11. Unit Testing Framework"),
        ("code_quality",     "12. Code Quality / Static Analysis"),
        ("additional_notes", "Additional Notes"),
    ]

    pdf = FPDF()
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # ── Header bar ──────────────────────────────────────────────────────────
    pdf.set_fill_color(30, 58, 95)
    pdf.rect(0, 0, 210, 36, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_xy(20, 9)
    pdf.cell(0, 10, "Project Requirements Questionnaire", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(180, 205, 230)
    ts = data.get("submitted_at", datetime.utcnow().isoformat())
    # Make ISO timestamp human-readable for PDF display
    ts_display = ts.replace("T", " ").replace("Z", " UTC") if "T" in ts else ts
    pdf.set_x(20)
    pdf.cell(0, 7, f"Submitted: {ts_display}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ── Body ─────────────────────────────────────────────────────────────────
    pdf.set_y(46)
    for field, label in FIELDS:
        answer = data.get(field, "")
        if not answer:
            continue
        # Question label
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 58, 95)
        pdf.multi_cell(0, 7, _safe(label))
        # Answer text
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(71, 85, 105)
        pdf.set_x(26)
        pdf.multi_cell(0, 6, _safe(answer))
        pdf.ln(2)
        # Divider
        pdf.set_draw_color(226, 232, 240)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)

    # ── Footer ───────────────────────────────────────────────────────────────
    pdf.set_y(-18)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(
        0, 8,
        "Generated by Project Requirements Questionnaire  |  Powered by Streamlit & Supabase",
        align="C",
    )

    return bytes(pdf.output())


# ── Supabase Storage ──────────────────────────────────────────────────────────
def save_to_supabase(data: dict) -> tuple:
    """Insert data into Supabase. Returns (success: bool, message: str)."""
    try:
        url = st.secrets.get("SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    except Exception:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")

    if not url or not key:
        return (
            False,
            "Supabase credentials not configured — data was not saved to the database. "
            "Your PDF download is still available.",
        )
    try:
        from supabase import create_client
        client = create_client(url, key)
        client.table("project_requirements").insert(data).execute()
        return True, "Responses saved to Supabase successfully."
    except Exception as exc:
        return False, f"Database error: {exc}"


# ── Main Application ──────────────────────────────────────────────────────────
def main():
    cb = _on_interact  # shorthand for on_change callback

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="app-title">📋 Project Requirements Questionnaire</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-subtitle">'
        "Capture essential tech-stack details before kicking off your project. "
        "Fill in all 12 questions and download a shareable PDF."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Post-submission view ──────────────────────────────────────────────────
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
            st.html(_robot_html("bye"))
            if st.session_state.pdf_bytes:
                st.download_button(
                    label="⬇️  Download Requirements as PDF",
                    data=st.session_state.pdf_bytes,
                    file_name=f"project_requirements_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝  Submit Another Response", use_container_width=True):
                # Clear state and widget keys
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
        return

    # ── Two-column layout ─────────────────────────────────────────────────────
    col_form, col_anim = st.columns([3, 2], gap="large")

    # ── Right: Animation ──────────────────────────────────────────────────────
    with col_anim:
        st.html(_robot_html(st.session_state.animation_state))

    # ── Left: Form ────────────────────────────────────────────────────────────
    with col_form:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)

        # ── Q1: Version Control ───────────────────────────────────────────────
        st.markdown('<div class="section-label">Source Control</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">1. Version Control Platform</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">Which platform hosts your source code? (Git is used locally for all of them.)</div>',
            unsafe_allow_html=True,
        )
        vc = st.radio(
            "vc_radio", ["GitHub", "Azure DevOps", "Bitbucket", "GitLab", "Other"],
            horizontal=True, key="version_control",
            label_visibility="collapsed", on_change=cb,
        )
        vc_other = ""
        if vc == "Other":
            vc_other = st.text_input("Specify platform", key="vc_other", on_change=cb)

        # ── Q2: IDE ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Development Environment</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">2. IDE / Editor</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">Always use the latest version to leverage all features.</div>',
            unsafe_allow_html=True,
        )
        ide = st.radio(
            "ide_radio",
            ["Visual Studio (Full IDE)", "Visual Studio Code", "Both", "Other"],
            horizontal=True, key="ide",
            label_visibility="collapsed", on_change=cb,
        )
        ide_other = ""
        if ide == "Other":
            ide_other = st.text_input("Specify IDE", key="ide_other", on_change=cb)

        # ── Q3: .NET / C# ─────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Technology Stack</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">3. .NET / C# Version</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">'
            ".NET 9 → C# 13 &nbsp;|&nbsp; .NET 8 → C# 12 (LTS) &nbsp;|&nbsp; .NET 6/7 → C# 10/11 &nbsp;"
            '— <a href="https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning" '
            'target="_blank">Official reference ↗</a>'
            "</div>",
            unsafe_allow_html=True,
        )
        dotnet = st.selectbox(
            "dotnet_select",
            [".NET 9 / C# 13 (Latest)", ".NET 8 / C# 12 (LTS)", ".NET 7 / C# 11",
             ".NET 6 / C# 10 (LTS)", "Other / Not sure"],
            key="dotnet_csharp", label_visibility="collapsed", on_change=cb,
        )

        # ── Q4: EF Core ───────────────────────────────────────────────────────
        st.markdown('<div class="q-label">4. Entity Framework Core Version</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">'
            '<a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/" target="_blank">'
            "EF Core release notes ↗</a>"
            "</div>",
            unsafe_allow_html=True,
        )
        ef = st.selectbox(
            "ef_select",
            ["EF Core 9.0", "EF Core 8.0 (LTS)", "EF Core 7.0",
             "EF Core 6.0 (LTS)", "Not using EF Core", "Other"],
            key="ef_core", label_visibility="collapsed", on_change=cb,
        )

        # ── Q5: Architecture ──────────────────────────────────────────────────
        st.markdown('<div class="section-label">Architecture</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">5. Application Architecture &amp; Design Patterns</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">e.g., Clean Architecture, CQRS, DDD, MVC, Repository Pattern, SOLID…</div>',
            unsafe_allow_html=True,
        )
        arch = st.text_area(
            "arch_input",
            placeholder="Describe your architecture and key design patterns…",
            key="architecture", label_visibility="collapsed",
            on_change=cb, height=85,
        )

        # ── Q6: Deployment ────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Deployment &amp; DevOps</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">6. Deployment Process</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">How does code move from local validation → staging → production?</div>',
            unsafe_allow_html=True,
        )
        deploy = st.radio(
            "deploy_radio",
            ["Azure DevOps Pipelines", "GitHub Actions", "Manual / FTP", "Other CI/CD"],
            horizontal=True, key="deployment",
            label_visibility="collapsed", on_change=cb,
        )
        deploy_notes = st.text_input(
            "Deployment notes",
            placeholder="e.g., staging → UAT → prod, Azure App Service, Docker…",
            key="deploy_notes", on_change=cb,
        )

        # ── Q7: Crystal Reports ───────────────────────────────────────────────
        st.markdown('<div class="section-label">Reporting</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">7. Crystal Reports Requirement</div>', unsafe_allow_html=True)
        crystal = st.radio(
            "crystal_radio",
            ["Yes — required", "No — not needed", "Under consideration"],
            horizontal=True, key="crystal_report",
            label_visibility="collapsed", on_change=cb,
        )

        # ── Q8: Local Testing ─────────────────────────────────────────────────
        st.markdown('<div class="section-label">Testing &amp; Quality</div>', unsafe_allow_html=True)
        st.markdown('<div class="q-label">8. Local Testing Feasibility</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">Can changes be fully tested locally, or is deployment required?</div>',
            unsafe_allow_html=True,
        )
        local_test = st.radio(
            "local_test_radio",
            [
                "Full local testing possible",
                "Partial — some services need deployment",
                "Deployment required for all testing",
            ],
            key="local_testing", label_visibility="collapsed", on_change=cb,
        )

        # ── Q9: Logging Tools ─────────────────────────────────────────────────
        st.markdown('<div class="q-label">9. Logging / Tracing / Monitoring</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">Critical for debugging defects and analysing exceptions in production.</div>',
            unsafe_allow_html=True,
        )
        logging_opts = st.multiselect(
            "logging_select",
            ["Application Insights", "Serilog", "NLog", "ELK Stack",
             "Splunk", "Dynatrace", "Datadog", "Other"],
            key="logging_tools", label_visibility="collapsed", on_change=cb,
        )
        logging_other = ""
        if "Other" in logging_opts:
            logging_other = st.text_input("Specify logging tool", key="logging_other", on_change=cb)

        # ── Q10: Project Management ───────────────────────────────────────────
        st.markdown('<div class="q-label">10. Project Management Tool</div>', unsafe_allow_html=True)
        proj_mgmt = st.radio(
            "proj_mgmt_radio",
            ["Azure DevOps (Boards)", "JIRA", "Both", "Other"],
            horizontal=True, key="project_mgmt",
            label_visibility="collapsed", on_change=cb,
        )

        # ── Q11: Unit Testing ─────────────────────────────────────────────────
        st.markdown('<div class="q-label">11. Unit Testing Framework</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">Select all that apply. xUnit is most popular for .NET.</div>',
            unsafe_allow_html=True,
        )
        unit_test = st.multiselect(
            "unit_test_select",
            ["xUnit", "NUnit", "MSTest", "None currently", "Other"],
            key="unit_testing", label_visibility="collapsed", on_change=cb,
        )

        # ── Q12: Code Quality ─────────────────────────────────────────────────
        st.markdown('<div class="q-label">12. Code Quality / Static Analysis</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="q-hint">e.g., SonarQube detects code smells, bugs, and security vulnerabilities.</div>',
            unsafe_allow_html=True,
        )
        code_quality = st.radio(
            "cq_radio",
            ["SonarQube — mandatory", "SonarQube — optional", "Other tool", "Not currently used"],
            horizontal=True, key="code_quality",
            label_visibility="collapsed", on_change=cb,
        )
        cq_other = ""
        if code_quality == "Other tool":
            cq_other = st.text_input("Specify code quality tool", key="cq_other", on_change=cb)

        # ── Additional Notes ──────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="q-label">Additional Notes / Context</div>', unsafe_allow_html=True)
        notes = st.text_area(
            "notes_input",
            placeholder="Any other constraints, context, or information to share…",
            key="additional_notes", label_visibility="collapsed",
            on_change=cb, height=80,
        )

        # ── Submit Button ─────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        submit_clicked = st.button(
            "Submit Requirements →", type="primary", use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)  # close .form-card

        # ── Handle Submission ─────────────────────────────────────────────────
        if submit_clicked:
            # Build the record
            vc_val = vc if vc != "Other" else (vc_other or "Other")
            ide_val = ide if ide != "Other" else (ide_other or "Other")

            logging_list = list(logging_opts)
            if "Other" in logging_list and logging_other:
                logging_list = [logging_other if x == "Other" else x for x in logging_list]
            logging_val = ", ".join(logging_list)

            unit_val = ", ".join(unit_test)
            cq_val = code_quality if code_quality != "Other tool" else (cq_other or "Other tool")

            deploy_val = deploy
            if deploy_notes.strip():
                deploy_val = f"{deploy} — {deploy_notes.strip()}"

            record = {
                "submitted_at":   datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "version_control": vc_val,
                "ide":             ide_val,
                "dotnet_csharp":   dotnet,
                "ef_core":         ef,
                "architecture":    arch,
                "deployment":      deploy_val,
                "crystal_report":  crystal,
                "local_testing":   local_test,
                "logging_tools":   logging_val,
                "project_mgmt":    proj_mgmt,
                "unit_testing":    unit_val,
                "code_quality":    cq_val,
                "additional_notes": notes,
            }

            # Persist to Supabase
            ok, db_msg = save_to_supabase(record)
            if ok:
                st.success(db_msg)
            else:
                st.info(f"ℹ️  {db_msg}")

            # Generate PDF
            try:
                st.session_state.pdf_bytes = generate_pdf(record)
            except Exception as exc:
                st.warning(f"PDF generation failed: {exc}")
                st.session_state.pdf_bytes = None

            # Transition to bye state
            st.session_state.animation_state = "bye"
            st.session_state.submitted = True
            st.rerun()


main()
