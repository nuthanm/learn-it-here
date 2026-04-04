"""Learn It Here
A Streamlit learning hub for developers – project requirements capture + tech-stack guides.
Stores responses in Supabase (PostgreSQL) and allows PDF export.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Learn It Here 🐼",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session State Initialization ──────────────────────────────────────────────
_DEFAULTS = {
    "page": "landing",        # "landing" | "requirements" | "learn"
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


def _nav_to(page: str):
    """Navigate to a page and rerun."""
    st.session_state.page = page
    st.rerun()


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
  /* ─ Always hide the sidebar & its toggle ─ */
  [data-testid="stSidebar"]        { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }

  /* ─ Global — panda fur white/gray palette, fills full viewport ─ */
  html, body { width: 100% !important; height: 100% !important; overflow-x: hidden !important; }
  /* Override Streamlit's default blue theme root fully */
  .stApp,
  .st-emotion-cache-1nryt4l,
  [data-testid="stAppViewContainer"],
  .stMain,
  [data-testid="stMain"] {
    background: #F8F8F8 !important;
    color: #1A1A1A !important;
  }
  [data-testid="stHeader"] { background: transparent !important; }
  .block-container {
    padding-top: 0.2rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }

  /* ─ Top nav bar ─ */
  .kfp-nav {
    display: flex; align-items: center; gap: 1.2rem;
    padding: 0.3rem 0; margin-bottom: 0.4rem;
    background: transparent;
    justify-content: flex-start;
  }
  .kfp-nav-logo  {
    font-size: 1.85rem; line-height: 1; align-self: center;
    background: #1A1A1A; border-radius: 50%;
    width: 2.6rem; height: 2.6rem;
    display: flex; align-items: center; justify-content: center;
  }
  .kfp-nav-text  { display: flex; flex-direction: column; gap: 0; line-height: 1; }
  .kfp-nav-title {
    font-size: 1.45rem; font-weight: 800;
    background: linear-gradient(135deg, #1A1A1A, #2D2D2D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.3px; line-height: 1.2; margin: 0; padding: 0;
  }
  .kfp-nav-tagline { font-size: 0.72rem; color: #40916C; margin: 0; padding: 0; line-height: 1.3; }
  .kfp-nav-sub { font-size: 0.78rem; color: #40916C; margin-left: auto; }

  /* ─ Landing hero section ─ */
  .hero-eyebrow {
    display: inline-block;
    font-size: 0.7rem; font-weight: 800; letter-spacing: 2px;
    text-transform: uppercase; color: #2D6A4F;
    background: #E8F5EE; border-radius: 20px;
    padding: 3px 14px; margin-bottom: 6px;
    animation: eyebrowPop .55s cubic-bezier(.34,1.56,.64,1) .1s both;
  }
  @keyframes eyebrowPop{
    from{opacity:0;transform:translateY(-8px) scale(.88)}
    to  {opacity:1;transform:translateY(0) scale(1)}
  }
  .hero-headline {
    font-size: 2.1rem; font-weight: 900; color: #1A1A1A;
    line-height: 1.15; margin: 0 0 10px;
    animation: headlineIn .65s cubic-bezier(.34,1.56,.64,1) .22s both;
  }
  @keyframes headlineIn{
    from{opacity:0;transform:translateY(16px)}
    to  {opacity:1;transform:translateY(0)}
  }
  .hero-sub {
    font-size: 0.9rem; color: #555555; line-height: 1.65;
    margin-bottom: 14px;
    animation: headlineIn .65s ease .38s both;
  }
  /* ─ animated accent divider ─ */
  .hero-bar {
    height: 4px; border-radius: 4px; margin-bottom: 14px;
    background: linear-gradient(90deg, #1A1A1A 0%, #2D6A4F 50%, #FFB3BA 100%);
    background-size: 200% 100%;
    animation: barSlide 3.5s ease-in-out infinite;
  }
  @keyframes barSlide{
    0%  {background-position: 0%   50%}
    50% {background-position: 100% 50%}
    100%{background-position: 0%   50%}
  }
  /* ─ hero feature highlights ─ */
  .hero-features {
    display: flex; flex-direction: column; gap: 0.5rem;
    margin-bottom: 14px;
    animation: headlineIn .65s ease .50s both;
  }
  .hero-feat {
    display: flex; align-items: flex-start; gap: 0.7rem;
    background: #FFFFFF; border-radius: 9px; padding: 0.5rem 0.9rem;
    border-left: 3px solid #2D6A4F;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
  }
  .feat-icon { font-size: 1.15rem; flex-shrink: 0; margin-top: 2px; }
  .feat-text { display: flex; flex-direction: column; gap: 1px; }
  .feat-text strong { font-size: 0.85rem; color: #1A1A1A; font-weight: 700; line-height: 1.3; }
  .feat-text span { font-size: 0.76rem; color: #666666; line-height: 1.4; }

  /* ─ Workflow steps on landing ─ */
  .wf-step {
    display: flex; align-items: flex-start; gap: 0.9rem;
    background: #FFFFFF; border-radius: 14px; padding: 0.85rem 1.3rem;
    border-left: 4px solid #1A1A1A;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 0.75rem;
  }
  .wf-step-icon { font-size: 1.5rem; flex-shrink: 0; }
  .wf-step-text strong { color: #1A1A1A; font-size: 0.9rem; display: block; }
  .wf-step-text p { color: #555555; font-size: 0.8rem; margin: 0.1rem 0 0; }

  /* ─ CTA buttons — primary: panda black, secondary: bamboo green ─ */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%) !important;
    color: #FFFFFF !important; border: none !important;
    border-radius: 12px !important; font-size: 1rem !important;
    font-weight: 700 !important; padding: 0.7rem 0 !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.32) !important;
    transition: opacity 0.2s !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.85 !important; }

  div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(135deg, #2D6A4F 0%, #40916C 100%) !important;
    color: #FFFFFF !important; border: none !important;
    border-radius: 12px !important; font-size: 1rem !important;
    font-weight: 700 !important; padding: 0.7rem 0 !important;
    box-shadow: 0 6px 20px rgba(45,106,79,0.38) !important;
    transition: opacity 0.2s !important;
  }
  div[data-testid="stButton"] > button[kind="secondary"]:hover { opacity: 0.88 !important; }

  /* ─ Download button — bamboo green ─ */
  div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #2D6A4F 0%, #40916C 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(45,106,79,0.38) !important;
  }

  /* ─ Tabs — panda black active ─ */
  [data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #FFFFFF !important; border-radius: 14px !important;
    padding: 0.3rem 0.5rem !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
    margin-bottom: 1.2rem !important;
  }
  [data-testid="stTabs"] button {
    font-size: 0.97rem !important; font-weight: 600 !important;
    color: #555555 !important; border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
  }
  [data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #1A1A1A, #2D2D2D) !important;
    color: #FFFFFF !important;
  }

  /* ─ Content cards — panda white ─ */
  .content-card {
    background: #FFFFFF; border-radius: 18px;
    padding: 2rem 2.4rem; margin-bottom: 1.5rem;
    border: 1px solid #D0D0D0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }
  .card-title {
    font-size: 1.2rem; font-weight: 700; color: #1A1A1A;
    margin-bottom: 0.9rem;
  }
  .card-body { color: #444444; line-height: 1.8; font-size: 0.95rem; }
  .card-section-title {
    font-size: 0.8rem; font-weight: 700; color: #40916C;
    text-transform: uppercase; letter-spacing: 1.1px;
    margin: 1.6rem 0 0.6rem;
  }

  /* ─ Workflow diagram nodes — panda black + bamboo ─ */
  .wf-diagram {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 0.4rem; margin: 1rem 0;
  }
  .wf-node {
    background: linear-gradient(135deg, #1A1A1A, #2D2D2D);
    color: #FFFFFF; padding: 0.45rem 1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600;
    box-shadow: 0 2px 8px rgba(0,0,0,0.22);
  }
  .wf-node-green {
    background: linear-gradient(135deg, #2D6A4F, #40916C);
    color: #FFFFFF; padding: 0.45rem 1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600;
  }
  .wf-arrow { color: #1A1A1A; font-size: 1.1rem; font-weight: 700; }

  /* ─ Feature grid pills — panda off-white with dark border ─ */
  .feature-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 0.85rem; margin: 1rem 0;
  }
  .feature-pill {
    background: #F5F5F5; border: 1px solid #CCCCCC;
    border-radius: 12px; padding: 0.85rem 1.1rem;
  }
  .feature-pill strong { color: #1A1A1A; font-size: 0.88rem; display: block; }
  .feature-pill p { color: #555555; font-size: 0.78rem; margin: 0.25rem 0 0; }

  /* ─ Platform badges — panda black border ─ */
  .platform-row { display: flex; flex-wrap: wrap; gap: 0.9rem; margin: 1rem 0; }
  .platform-badge {
    display: flex; align-items: center; gap: 0.55rem;
    background: #FFFFFF; border: 2px solid #1A1A1A;
    border-radius: 12px; padding: 0.65rem 1.3rem;
    font-weight: 700; color: #1A1A1A; font-size: 0.88rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  /* ─ Command blocks — panda black bg, bamboo text ─ */
  .cmd-block {
    background: #1A1A1A; color: #74C69D;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto;
  }
  .cmd-comment { color: #888888; font-style: italic; }

  /* ─ Settings / JSON blocks — deep panda black ─ */
  .json-block {
    background: #0D0D0D; color: #B7E4C7;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto;
  }

  /* ─ Requirements form card ─ */
  .form-card {
    background: #FFFFFF; border-radius: 18px;
    padding: 2rem 2.2rem; border: 1px solid #D0D0D0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }
  .app-title   { font-size: 1.9rem; font-weight: 700; color: #1A1A1A; margin-bottom: 0.2rem; }
  .app-subtitle { font-size: 0.92rem; color: #555555; margin-bottom: 1.8rem; }
  .q-label {
    font-size: 0.93rem; font-weight: 600; color: #1A1A1A; margin-bottom: 2px;
  }
  .q-hint {
    font-size: 0.76rem; color: #888888; margin-bottom: 4px; font-style: italic;
  }
  .section-label {
    font-size: 0.7rem; font-weight: 700; color: #40916C;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-top: 1.4rem; margin-bottom: 2px;
  }

  /* ─ Success card — panda white + bamboo accent ─ */
  .success-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 100%);
    border: 1.5px solid #1A1A1A; border-radius: 18px;
    padding: 2.5rem 3rem; text-align: center;
  }
  .success-title { font-size: 1.6rem; font-weight: 700; color: #1A1A1A; margin-bottom: 0.4rem; }
  .success-sub   { font-size: 0.95rem; color: #2D6A4F; margin-bottom: 1.8rem; }

  /* ─ Shortcut table — panda black header ─ */
  .shortcut-table { width: 100%; border-collapse: collapse; margin: 0.6rem 0; }
  .shortcut-table th {
    background: #1A1A1A; color: #74C69D;
    padding: 0.55rem 1rem; text-align: left; font-size: 0.83rem;
    border-radius: 0;
  }
  .shortcut-table td {
    padding: 0.5rem 1rem; font-size: 0.85rem; color: #333333;
    border-bottom: 1px solid #E8E8E8;
  }
  .shortcut-table tr:last-child td { border-bottom: none; }
  .shortcut-table tr:nth-child(even) td { background: #F5F5F5; }

  /* ─ Footer fixed at bottom ─ */
  .kfp-footer {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
    display: flex; align-items: center; justify-content: space-between;
    padding: 6px 1.5rem;
    background: #1A1A1A;
    border-top: 2px solid #2D6A4F;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }
  .kfp-footer-text {
    font-size: 0.78rem; color: #74C69D; font-weight: 700; margin-right: 12px;
  }
  .kfp-footer-copy { font-size: 0.75rem; color: #888888; }
  /* push content above footer */
  .stMain section, [data-testid="stMainBlockContainer"] {
    padding-bottom: 50px !important;
  }
  /* ─ Tighter global spacing ─ */
  .stVerticalBlock { gap: 0.25rem !important; }
  /* ─ Reduce motion for accessibility ─ */
  @media (prefers-reduced-motion: reduce) {
    .wf-step, .content-card, .kfp-nav { transition: none !important; }
    .hero-bar { animation: none !important; }
    .hero-eyebrow, .hero-headline, .hero-sub, .hero-stats { animation: none !important; opacity: 1 !important; }
  }

  /* ─ Mobile responsive styles ─ */
  @media (max-width: 768px) {
    .block-container {
      padding-left: 1rem !important;
      padding-right: 1rem !important;
    }

    /* Center nav logo and text on mobile */
    .kfp-nav {
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      gap: 0.5rem !important;
      padding: 0.6rem 0 !important;
    }
    .kfp-nav-text { align-items: center !important; }
    .kfp-nav-sub {
      margin-left: 0 !important;
      text-align: center !important;
    }

    /* Hero headline smaller on mobile */
    .hero-headline { font-size: 1.5rem !important; }
    .hero-sub { font-size: 0.85rem !important; }

    /* Content cards padding */
    .content-card {
      padding: 1.2rem 1rem !important;
      border-radius: 12px !important;
    }
    .form-card {
      padding: 1.2rem 1rem !important;
      border-radius: 12px !important;
    }
    .success-card {
      padding: 1.5rem 1rem !important;
    }

    /* Feature grid single column */
    .feature-grid {
      grid-template-columns: 1fr !important;
    }

    /* Platform badges stack */
    .platform-row {
      flex-direction: column !important;
      gap: 0.6rem !important;
    }
    .platform-badge {
      width: 100% !important;
      box-sizing: border-box !important;
    }

    /* Code blocks smaller font on mobile */
    .cmd-block, .json-block {
      font-size: 0.76rem !important;
      padding: 0.8rem 0.9rem !important;
    }

    /* Footer stacks vertically on mobile */
    .kfp-footer {
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 2px !important;
      padding: 8px 1rem !important;
      text-align: center !important;
    }

    /* Shortcut table scroll on mobile */
    .shortcut-table { font-size: 0.78rem !important; }
    .shortcut-table th, .shortcut-table td { padding: 0.4rem 0.6rem !important; }

    /* App title smaller */
    .app-title { font-size: 1.4rem !important; }
  }
</style>
""",
    unsafe_allow_html=True,
)


# ── Kung Fu Panda — Landing Animation ────────────────────────────────────────
def _panda_landing_html() -> str:
    """Full KFP Po face — SVG with 5 cycling expressions + per-emotion orbital dots."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }
  /* ── Entrance bounce ── */
  @keyframes entrance{
    0%  {opacity:0;transform:scale(.25)translateY(-80px)rotate(-18deg)}
    60% {transform:scale(1.06)translateY(8px)rotate(2deg);opacity:1}
    78% {transform:scale(.97)translateY(-4px)rotate(-.4deg)}
    100%{transform:scale(1)translateY(0)rotate(0);opacity:1}
  }
  /* ── Gentle float ── */
  @keyframes float{
    0%,100%{transform:translateY(0)}
    50%    {transform:translateY(-10px)}
  }
  /* ── Pupils wander ── */
  @keyframes pupilL{
    0%,12%{transform:translate(0,0)}20%,35%{transform:translate(4px,3px)}
    45%,60%{transform:translate(-4px,-3px)}70%,84%{transform:translate(3px,-4px)}
    92%,100%{transform:translate(0,0)}
  }
  @keyframes pupilR{
    0%,12%{transform:translate(0,0)}20%,35%{transform:translate(-4px,3px)}
    45%,60%{transform:translate(4px,-3px)}70%,84%{transform:translate(-2px,-4px)}
    92%,100%{transform:translate(0,0)}
  }
  /* ── Blink ── */
  @keyframes blink{
    0%,84%,100%{transform:scaleY(1)}
    88%        {transform:scaleY(.06)}
  }
  /* ── 50s expression loop: 8s on, 2s crossfade ── */
  @keyframes eHappy  {0%,2%{opacity:1}16%{opacity:1}20%{opacity:0}99%{opacity:0}100%{opacity:1}}
  @keyframes eExcited{0%,18%{opacity:0}22%{opacity:1}36%{opacity:1}40%{opacity:0}100%{opacity:0}}
  @keyframes eThink  {0%,38%{opacity:0}42%{opacity:1}56%{opacity:1}60%{opacity:0}100%{opacity:0}}
  @keyframes eWink   {0%,58%{opacity:0}62%{opacity:1}76%{opacity:1}80%{opacity:0}100%{opacity:0}}
  @keyframes eDeter  {0%,78%{opacity:0}82%{opacity:1}95%{opacity:1}99%{opacity:0}100%{opacity:0}}
  /* same keyframes reused for labels / quotes */
  @keyframes lblHappy  {0%,2%{opacity:.9}16%{opacity:.9}20%{opacity:0}99%{opacity:0}100%{opacity:.9}}
  @keyframes lblExcited{0%,18%{opacity:0}22%{opacity:.9}36%{opacity:.9}40%{opacity:0}100%{opacity:0}}
  @keyframes lblThink  {0%,38%{opacity:0}42%{opacity:.9}56%{opacity:.9}60%{opacity:0}100%{opacity:0}}
  @keyframes lblWink   {0%,58%{opacity:0}62%{opacity:.9}76%{opacity:.9}80%{opacity:0}100%{opacity:0}}
  @keyframes lblDeter  {0%,78%{opacity:0}82%{opacity:.9}95%{opacity:.9}99%{opacity:0}100%{opacity:0}}
  /* ── Dot orbit spin ── */
  @keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
  @keyframes spinRev{from{transform:rotate(0deg)}to{transform:rotate(-360deg)}}
  /* ── Dot pulse ── */
  @keyframes dotPulse{0%,100%{r:4;opacity:.7}50%{r:6;opacity:1}}
  /* ── Thought bubble pop ── */
  @keyframes bubblePop{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}
  /* ── Speed-line flicker ── */
  @keyframes speedFlicker{0%,100%{opacity:.5}50%{opacity:1}}

  .wrap{animation:entrance 1s cubic-bezier(.34,1.56,.64,1) .2s both;
        display:flex;flex-direction:column;align-items:center;gap:8px}
  .floater{animation:float 4s ease-in-out 1.4s infinite}
  .pupil-l{transform-box:fill-box;transform-origin:center;animation:pupilL 11s ease-in-out 2s infinite}
  .pupil-r{transform-box:fill-box;transform-origin:center;animation:pupilR 11s ease-in-out 2.6s infinite}
  .lid-l{transform-box:fill-box;transform-origin:50% 40%;animation:blink 6.5s ease-in-out 3s infinite}
  .lid-r{transform-box:fill-box;transform-origin:50% 40%;animation:blink 6.5s ease-in-out 3.3s infinite}

  .e-happy  {animation:eHappy   50s ease-in-out 2.2s infinite}
  .e-excited{animation:eExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .e-think  {animation:eThink   50s ease-in-out 2.2s infinite;opacity:0}
  .e-wink   {animation:eWink    50s ease-in-out 2.2s infinite;opacity:0}
  .e-deter  {animation:eDeter   50s ease-in-out 2.2s infinite;opacity:0}

  /* orbital container must be centred on the face */
  .orbit-happy  {animation:eHappy   50s ease-in-out 2.2s infinite}
  .orbit-excited{animation:eExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-think  {animation:eThink   50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-wink   {animation:eWink    50s ease-in-out 2.2s infinite;opacity:0}
  .orbit-deter  {animation:eDeter   50s ease-in-out 2.2s infinite;opacity:0}

  .spin    {transform-box:fill-box;transform-origin:center;animation:spin 4s linear infinite}
  .spin-rev{transform-box:fill-box;transform-origin:center;animation:spinRev 6s linear infinite}
  .dp{animation:dotPulse 1.6s ease-in-out infinite}
  .bp{animation:bubblePop 1.2s ease-in-out infinite}
  .sf{animation:speedFlicker .8s ease-in-out infinite}
  /* right base arm hides whilst thinking arm is shown */
  @keyframes hideForThink{0%,38%{opacity:1}42%{opacity:0}56%{opacity:0}60%{opacity:1}100%{opacity:1}}
  .base-arm-right{animation:hideForThink 50s ease-in-out 2.2s infinite}

  /* label pill */
  .lbl{
    font-size:12px;font-weight:800;letter-spacing:.9px;text-transform:uppercase;
    color:#2D6A4F;background:#fff;border:2px solid #2D6A4F;
    border-radius:20px;padding:4px 16px;position:absolute;
    box-shadow:0 2px 8px rgba(45,106,79,.15);
  }
  .lbl-happy  {animation:lblHappy   50s ease-in-out 2.2s infinite}
  .lbl-excited{animation:lblExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-think  {animation:lblThink   50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-wink   {animation:lblWink    50s ease-in-out 2.2s infinite;opacity:0}
  .lbl-deter  {animation:lblDeter   50s ease-in-out 2.2s infinite;opacity:0}
  .labels{position:relative;height:28px;width:160px;display:flex;align-items:center;justify-content:center}

  /* quote */
  .quotebox{position:relative;height:100px;width:275px;display:flex;align-items:flex-start;justify-content:center;margin-top:4px}
  .q{position:absolute;top:0;text-align:center;padding:0 6px;width:100%}
  .qtext{display:block;font-size:13px;color:#444;line-height:1.6;font-style:italic}
  .qattr{display:block;font-size:11.5px;color:#2D6A4F;margin-top:5px;font-weight:800;letter-spacing:.3px}
  .q-happy  {animation:lblHappy   50s ease-in-out 2.2s infinite}
  .q-excited{animation:lblExcited 50s ease-in-out 2.2s infinite;opacity:0}
  .q-think  {animation:lblThink   50s ease-in-out 2.2s infinite;opacity:0}
  .q-wink   {animation:lblWink    50s ease-in-out 2.2s infinite;opacity:0}
  .q-deter  {animation:lblDeter   50s ease-in-out 2.2s infinite;opacity:0}

  @media(prefers-reduced-motion:reduce){
    .wrap,.floater,.spin,.spin-rev{animation:none!important;opacity:1!important;transform:none!important}
    .e-happy,.orbit-happy,.lbl-happy,.q-happy{animation:none;opacity:1}
    .e-excited,.e-think,.e-wink,.e-deter{display:none}
    .orbit-excited,.orbit-think,.orbit-wink,.orbit-deter{display:none}
    .pupil-l,.pupil-r,.lid-l,.lid-r,.dp,.bp,.sf{animation:none}
    .base-arm-right{animation:none;opacity:1}
    .lbl-excited,.lbl-think,.lbl-wink,.lbl-deter{display:none}
    .q-excited,.q-think,.q-wink,.q-deter{display:none}
  }
</style>
</head>
<body>
<div class="wrap">

  <!-- ── SVG: panda + arms + per-emotion orbital decorations ── -->
  <div class="floater">
  <svg viewBox="-90 0 460 310" width="330" height="292" xmlns="http://www.w3.org/2000/svg">

    <!-- ═══ ORBITAL DECORATIONS (rendered behind the face) ═══ -->

    <!-- 1. HAPPY orbit — soft pink hearts / sparkle ring -->
    <g class="orbit-happy" opacity="1">
      <g class="spin" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="155" fill="none" stroke="#FFB3BA" stroke-width="1.5"
                stroke-dasharray="8 10" opacity=".55"/>
        <circle cx="295" cy="170" r="5" fill="#FFB3BA" opacity=".8" class="dp"/>
        <circle cx="140" cy="15"  r="4" fill="#FFB3BA" opacity=".7" class="dp" style="animation-delay:.4s"/>
        <circle cx="-15" cy="170" r="5" fill="#FFB3BA" opacity=".8" class="dp" style="animation-delay:.8s"/>
        <circle cx="140" cy="325" r="4" fill="#FFB3BA" opacity=".7" class="dp" style="animation-delay:1.2s"/>
        <!-- sparkle stars -->
        <text x="33"  y="55"  font-size="16" opacity=".7">✨</text>
        <text x="232" y="55"  font-size="16" opacity=".7">✨</text>
        <text x="33"  y="305" font-size="16" opacity=".6">✨</text>
        <text x="232" y="305" font-size="16" opacity=".6">✨</text>
      </g>
    </g>

    <!-- 2. EXCITED orbit — fast dual rings + energy circles -->
    <g class="orbit-excited" opacity="0">
      <g class="spin" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="148" fill="none" stroke="#FFB3BA" stroke-width="2"
                stroke-dasharray="12 8" opacity=".6"/>
        <circle cx="288" cy="170" r="6" fill="#FFB3BA" opacity=".9" class="dp"/>
        <circle cx="140" cy="22"  r="6" fill="#FFB3BA" opacity=".9" class="dp" style="animation-delay:.3s"/>
      </g>
      <g class="spin-rev" style="transform-origin:140px 170px">
        <circle cx="140" cy="170" r="162" fill="none" stroke="#FFD6A5" stroke-width="1.5"
                stroke-dasharray="6 14" opacity=".5"/>
        <circle cx="302" cy="170" r="5" fill="#FFD6A5" opacity=".8" class="dp" style="animation-delay:.5s"/>
        <circle cx="140" cy="8"   r="5" fill="#FFD6A5" opacity=".7" class="dp" style="animation-delay:.9s"/>
      </g>
      <!-- energy burst lines -->
      <line x1="-55" y1="80"  x2="-30" y2="95"  stroke="#FFB3BA" stroke-width="2.5" stroke-linecap="round" class="sf"/>
      <line x1="-65" y1="110" x2="-38" y2="112" stroke="#FFD6A5" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.2s"/>
      <line x1="-55" y1="140" x2="-30" y2="128" stroke="#FFB3BA" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.4s"/>
      <line x1="335" y1="80"  x2="310" y2="95"  stroke="#FFB3BA" stroke-width="2.5" stroke-linecap="round" class="sf"/>
      <line x1="345" y1="110" x2="318" y2="112" stroke="#FFD6A5" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.3s"/>
      <line x1="335" y1="140" x2="310" y2="128" stroke="#FFB3BA" stroke-width="2"   stroke-linecap="round" class="sf" style="animation-delay:.6s"/>
    </g>

    <!-- 3. THINK orbit — slow dashed ring + floating thought bubbles -->
    <g class="orbit-think" opacity="0">
      <g class="spin-rev" style="transform-origin:140px 170px;animation-duration:10s">
        <circle cx="140" cy="170" r="152" fill="none" stroke="#A8DADC" stroke-width="1.5"
                stroke-dasharray="4 12" opacity=".55"/>
        <circle cx="292" cy="170" r="5" fill="#A8DADC" opacity=".8" class="dp"/>
        <circle cx="140" cy="18"  r="4" fill="#A8DADC" opacity=".7" class="dp" style="animation-delay:.6s"/>
        <circle cx="-12" cy="170" r="5" fill="#A8DADC" opacity=".8" class="dp" style="animation-delay:1.1s"/>
        <circle cx="140" cy="322" r="4" fill="#A8DADC" opacity=".6" class="dp" style="animation-delay:1.6s"/>
      </g>
      <!-- rising thought bubbles left side -->
      <circle cx="-42" cy="200" r="4.5" fill="#CCCCCC" opacity=".6" class="bp"/>
      <circle cx="-55" cy="175" r="6.5" fill="#BBBBBB" opacity=".6" class="bp" style="animation-delay:.4s"/>
      <circle cx="-45" cy="148" r="9"   fill="#AAAAAA" opacity=".6" class="bp" style="animation-delay:.8s"/>
      <text x="-52" y="152" font-size="11" text-anchor="middle" fill="#555">💡</text>
    </g>

    <!-- 4. WINK orbit — cheeky arc + sparkles one side -->
    <g class="orbit-wink" opacity="0">
      <g class="spin" style="transform-origin:140px 170px;animation-duration:7s">
        <circle cx="140" cy="170" r="150" fill="none" stroke="#B7E4C7" stroke-width="1.5"
                stroke-dasharray="10 7" opacity=".55"/>
        <circle cx="290" cy="170" r="5"  fill="#B7E4C7" opacity=".8" class="dp"/>
        <circle cx="140" cy="20"  r="4"  fill="#B7E4C7" opacity=".7" class="dp" style="animation-delay:.5s"/>
      </g>
      <!-- cheeky wink stars right side -->
      <text x="305" y="120" font-size="18" opacity=".75" class="bp">★</text>
      <text x="320" y="155" font-size="13" opacity=".6"  class="bp" style="animation-delay:.3s">✦</text>
      <text x="308" y="195" font-size="15" opacity=".65" class="bp" style="animation-delay:.6s">✨</text>
    </g>

    <!-- 5. DETERMINED orbit — heavy dashes + speed lines -->
    <g class="orbit-deter" opacity="0">
      <g class="spin" style="transform-origin:140px 170px;animation-duration:3s">
        <circle cx="140" cy="170" r="150" fill="none" stroke="#1A1A1A" stroke-width="2"
                stroke-dasharray="16 6" opacity=".2"/>
        <circle cx="290" cy="170" r="6" fill="#1A1A1A" opacity=".35" class="dp"/>
        <circle cx="140" cy="20"  r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:.4s"/>
        <circle cx="-10" cy="170" r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:.8s"/>
        <circle cx="140" cy="320" r="6" fill="#1A1A1A" opacity=".3"  class="dp" style="animation-delay:1.2s"/>
      </g>
      <!-- speed lines left -->
      <line x1="-68" y1="140" x2="-30" y2="140" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" opacity=".35" class="sf"/>
      <line x1="-72" y1="160" x2="-34" y2="157" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".25" class="sf" style="animation-delay:.15s"/>
      <line x1="-70" y1="178" x2="-32" y2="172" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".2"  class="sf" style="animation-delay:.3s"/>
      <!-- speed lines right -->
      <line x1="348" y1="140" x2="310" y2="140" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" opacity=".35" class="sf"/>
      <line x1="352" y1="160" x2="314" y2="157" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".25" class="sf" style="animation-delay:.2s"/>
      <line x1="350" y1="178" x2="312" y2="172" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" opacity=".2"  class="sf" style="animation-delay:.4s"/>
    </g>

    <!-- ═══ PANDA ARMS (inside SVG, arching out left & right) ═══ -->
    <!-- Left arm — rounded rect rotated to arch left-down -->
    <rect x="14" y="188" width="24" height="72" rx="12"
          fill="#1A1A1A" transform="rotate(-28 26 188)"/>
    <!-- Left paw -->
    <ellipse cx="5" cy="246" rx="14" ry="10" fill="#1A1A1A" transform="rotate(-28 5 246)"/>
    <g class="base-arm-right">
    <!-- Right arm -->
    <rect x="242" y="188" width="24" height="72" rx="12"
          fill="#1A1A1A" transform="rotate(28 254 188)"/>
    <!-- Right paw -->
    <ellipse cx="275" cy="246" rx="14" ry="10" fill="#1A1A1A" transform="rotate(28 275 246)"/>
    </g>

    <!-- ═══ DROP SHADOW ═══ -->
    <ellipse cx="140" cy="292" rx="56" ry="6" fill="#1A1A1A" opacity=".06">
      <animate attributeName="rx" values="56;44;56" dur="4s" begin="1.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".06;.03;.06" dur="4s" begin="1.4s" repeatCount="indefinite"/>
    </ellipse>

    <!-- ═══ PANDA HEAD ═══ -->
    <!-- Ears -->
    <circle cx="52"  cy="64" r="46" fill="#1A1A1A"/>
    <circle cx="228" cy="64" r="46" fill="#1A1A1A"/>
    <circle cx="52"  cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
    <circle cx="228" cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
    <!-- Face -->
    <ellipse cx="140" cy="172" rx="118" ry="116" fill="#EFEFED"/>
    <ellipse cx="140" cy="170" rx="114" ry="112" fill="#FFFFFF"/>
    <!-- cheek shading -->
    <ellipse cx="30"  cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
    <ellipse cx="250" cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
    <!-- Eye patches -->
    <ellipse cx="88"  cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(-10 88 138)"/>
    <ellipse cx="192" cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(10 192 138)"/>
    <!-- Sclera + blink -->
    <g class="lid-l"><ellipse cx="90"  cy="133" rx="27" ry="26" fill="#FFFFFF"/></g>
    <g class="lid-r"><ellipse cx="190" cy="133" rx="27" ry="26" fill="#FFFFFF"/></g>
    <!-- Pupils -->
    <g class="pupil-l">
      <circle cx="92"  cy="133" r="14" fill="#1A1A1A"/>
      <circle cx="98"  cy="126" r="6"  fill="#FFFFFF"/>
      <circle cx="87"  cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
    </g>
    <g class="pupil-r">
      <circle cx="188" cy="133" r="14" fill="#1A1A1A"/>
      <circle cx="194" cy="126" r="6"  fill="#FFFFFF"/>
      <circle cx="183" cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
    </g>
    <!-- Nose -->
    <ellipse cx="140" cy="164" rx="6" ry="8" fill="#E8E8E8"/>
    <ellipse cx="140" cy="178" rx="17" ry="13" fill="#1A1A1A"/>
    <ellipse cx="133" cy="174" rx="6"  ry="4"  fill="#3A3A3A" opacity=".4"/>
    <line x1="128" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="152" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>

    <!-- ═══ EXPRESSIONS ═══ -->
    <!-- 1. HAPPY -->
    <g class="e-happy">
      <path d="M 96 210 Q 140 248 184 210" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="54"  cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
      <ellipse cx="226" cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
    </g>
    <!-- 2. EXCITED -->
    <g class="e-excited">
      <path d="M 88 208 Q 140 256 192 208" stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M 89 209 Q 140 252 191 209 L 188 224 Q 140 252 92 224 Z" fill="#FFFFFF" stroke="#D4D4D4" stroke-width="1.2"/>
      <line x1="115" y1="210" x2="115" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
      <line x1="140" y1="210" x2="140" y2="224" stroke="#D4D4D4" stroke-width="1.5"/>
      <line x1="165" y1="210" x2="165" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
      <path d="M 54  108 Q 76  94  100 100" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <path d="M 180 100 Q 204 94  226 108" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="42"  cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
      <ellipse cx="238" cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
    </g>
    <!-- 3. THINKING — matches 🤔: RIGHT brow raised, right paw touching chin -->
    <g class="e-think">
      <!-- smirk mouth -->
      <path d="M 100 214 Q 128 230 158 212" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
      <!-- LEFT brow: flat / slightly lowered -->
      <path d="M 52  112 Q 72  106 96 110"  stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- RIGHT brow: raised HIGH — key 🤔 feature -->
      <path d="M 184  96 Q 206  84 228  96" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- Right arm curving from shoulder (lower-right) up to chin -->
      <path d="M 238 292 Q 232 268 215 256 Q 200 254 178 268"
            stroke="#1A1A1A" stroke-width="24" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Paw / fist resting at chin -->
      <ellipse cx="168" cy="270" rx="22" ry="17" fill="#1A1A1A"/>
      <!-- Knuckle highlights -->
      <circle cx="160" cy="265" r="5" fill="#2D2D2D" opacity=".4"/>
      <circle cx="171" cy="261" r="5" fill="#2D2D2D" opacity=".4"/>
    </g>
    <!-- 4. WINK -->
    <g class="e-wink">
      <ellipse cx="190" cy="133" rx="27" ry="26" fill="#1A1A1A"/>
      <path d="M 165 133 Q 190 120 215 133" stroke="#FFFFFF" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <path d="M 165 128 Q 190 117 215 128" stroke="#1A1A1A" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M 100 212 Q 140 242 174 218" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="230" cy="196" rx="21" ry="13" fill="#FFB3BA" opacity=".62"/>
    </g>
    <!-- 5. DETERMINED -->
    <g class="e-deter">
      <line x1="102" y1="218" x2="178" y2="218" stroke="#1A1A1A" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 52  102 Q 72  95  96 104"  stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M 184 104 Q 208 95 228 102"  stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
      <line x1="96"  y1="104" x2="104" y2="112" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
      <line x1="184" y1="104" x2="176" y2="112" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
    </g>

  </svg>
  </div>

  <!-- Label pill -->
  <div class="labels">
    <span class="lbl lbl-happy"  >😊 Happy</span>
    <span class="lbl lbl-excited">🎉 Excited!</span>
    <span class="lbl lbl-think"  >🤔 Thinking…</span>
    <span class="lbl lbl-wink"   >😉 Wink</span>
    <span class="lbl lbl-deter"  >💪 Determined</span>
  </div>

  <!-- Quote -->
  <div class="quotebox">
    <div class="q q-happy">
      <span class="qtext">"Happiness is not something ready-made.<br>It comes from your own actions."</span>
      <span class="qattr">— Dalai Lama XIV</span>
    </div>
    <div class="q q-excited">
      <span class="qtext">"Nothing great in the world was accomplished without passion."</span>
      <span class="qattr">— G. W. F. Hegel</span>
    </div>
    <div class="q q-think">
      <span class="qtext">"The measure of intelligence is the ability to change."</span>
      <span class="qattr">— Albert Einstein</span>
    </div>
    <div class="q q-wink">
      <span class="qtext">"Life is too important to be taken seriously."</span>
      <span class="qattr">— Oscar Wilde</span>
    </div>
    <div class="q q-deter">
      <span class="qtext">"It does not matter how slowly you go as long as you do not stop."</span>
      <span class="qattr">— Confucius</span>
    </div>
  </div>

</div>
</body>
</html>"""


# ── Panda Helper — Requirements Form (welcome / thinking / bye states) ────────
def _robot_html(state: str) -> str:
    """Animated panda face helper for the requirements form page — matches landing panda style."""
    _messages = {
        "welcome": (
            "Hey! 🐼 Let's capture your<br>project requirements.<br>Fill in the form!"
        ),
        "thinking": (
            "Hmm, thinking along<br>with you… 🤔"
            "<br><span class='dots'><span>.</span><span>.</span><span>.</span></span>"
        ),
        "bye": (
            "Awesome! 🎉<br>Requirements saved!<br>"
            "Download your PDF below!<br>Time to learn! 🐼"
        ),
    }
    msg = _messages.get(state, _messages["welcome"])
    # Expression visibility per state
    s_happy   = "1" if state == "welcome"  else "0"
    s_think   = "1" if state == "thinking" else "0"
    s_excited = "1" if state == "bye"      else "0"

    wave_l     = "waveL .7s ease-in-out infinite" if state in ("welcome", "bye") else "none"
    wave_r     = "waveR .7s ease-in-out infinite" if state in ("welcome", "bye") else "none"
    body_anim  = "thinkBob 2s ease-in-out infinite" if state == "thinking" else "float 4s ease-in-out 1.2s infinite"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:flex-start;padding-top:18px;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }}
  @keyframes fadeUp{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:translateY(0)}}}}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
  @keyframes thinkBob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
  @keyframes waveR{{0%,100%{{transform:rotate(-15deg)}}50%{{transform:rotate(45deg)}}}}
  @keyframes waveL{{0%,100%{{transform:rotate(15deg)}}50%{{transform:rotate(-45deg)}}}}
  @keyframes blink{{0%,85%,100%{{transform:scaleY(1)}}89%{{transform:scaleY(.06)}}}}
  @keyframes pupilW{{0%,100%{{transform:translate(0,0)}}40%{{transform:translate(3px,2px)}}80%{{transform:translate(-3px,-2px)}}}}
  .dots span{{display:inline-block;animation:dotBounce 1.2s infinite;font-size:15px;font-weight:700;color:#2D6A4F}}
  .dots span:nth-child(2){{animation-delay:.2s}}
  .dots span:nth-child(3){{animation-delay:.4s}}
  @keyframes dotBounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
  @media(prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important;transform:none!important}}}}
</style></head>
<body>
  <!-- Speech bubble — bamboo green to match panda theme -->
  <div style="
    background:#fff;border:2.5px solid #2D6A4F;border-radius:20px;
    padding:13px 20px;font-size:13.5px;color:#2D6A4F;
    max-width:230px;text-align:center;line-height:1.6;
    box-shadow:0 4px 18px rgba(45,106,79,.18);
    position:relative;margin-bottom:16px;font-weight:600;
    animation:fadeUp .45s ease forwards;
  ">{msg}
    <span style="position:absolute;bottom:-13px;left:50%;transform:translateX(-50%);
      border:10px solid transparent;border-top-color:#2D6A4F;"></span>
  </div>
  <!-- Panda face + arms -->
  <div style="animation:{body_anim};display:flex;align-items:flex-end;">
    <!-- Left arm -->
    <div style="
      width:22px;height:62px;background:#1A1A1A;border-radius:11px;
      transform-origin:top center;animation:{wave_l};
      align-self:flex-end;margin-bottom:14px;margin-right:-5px;
    "></div>
    <!-- Panda SVG (same palette as landing page) -->
    <svg viewBox="0 0 280 290" width="195" height="203" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="140" cy="285" rx="58" ry="6.5" fill="#1A1A1A" opacity=".06"/>
      <!-- Ears -->
      <circle cx="52"  cy="64" r="46" fill="#1A1A1A"/>
      <circle cx="228" cy="64" r="46" fill="#1A1A1A"/>
      <circle cx="52"  cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
      <circle cx="228" cy="64" r="28" fill="#2D2D2D" opacity=".45"/>
      <!-- Head -->
      <ellipse cx="140" cy="172" rx="118" ry="116" fill="#EFEFED"/>
      <ellipse cx="140" cy="170" rx="114" ry="112" fill="#FFFFFF"/>
      <ellipse cx="30"  cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
      <ellipse cx="250" cy="188" rx="22" ry="16" fill="#E8E8E6" opacity=".8"/>
      <!-- Eye patches -->
      <ellipse cx="88"  cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(-10 88 138)"/>
      <ellipse cx="192" cy="138" rx="46" ry="42" fill="#1A1A1A" transform="rotate(10 192 138)"/>
      <!-- Sclera (blink) -->
      <ellipse cx="90"  cy="133" rx="27" ry="26" fill="#FFFFFF"
        style="transform-box:fill-box;transform-origin:50% 40%;animation:blink 5.5s ease-in-out 2s infinite"/>
      <ellipse cx="190" cy="133" rx="27" ry="26" fill="#FFFFFF"
        style="transform-box:fill-box;transform-origin:50% 40%;animation:blink 5.5s ease-in-out 2.5s infinite"/>
      <!-- Pupils (wander) -->
      <g style="transform-box:fill-box;transform-origin:center;animation:pupilW 8s ease-in-out 1s infinite">
        <circle cx="92"  cy="133" r="14" fill="#1A1A1A"/>
        <circle cx="98"  cy="126" r="6"  fill="#FFFFFF"/>
        <circle cx="87"  cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
      </g>
      <g style="transform-box:fill-box;transform-origin:center;animation:pupilW 8s ease-in-out 2s infinite">
        <circle cx="188" cy="133" r="14" fill="#1A1A1A"/>
        <circle cx="194" cy="126" r="6"  fill="#FFFFFF"/>
        <circle cx="183" cy="138" r="3"  fill="#FFFFFF" opacity=".5"/>
      </g>
      <!-- Nose bridge + nose -->
      <ellipse cx="140" cy="164" rx="6" ry="8" fill="#E8E8E8"/>
      <ellipse cx="140" cy="178" rx="17" ry="13" fill="#1A1A1A"/>
      <ellipse cx="133" cy="174" rx="6"  ry="4"  fill="#3A3A3A" opacity=".4"/>
      <line x1="128" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="152" y1="186" x2="140" y2="193" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>
      <!-- WELCOME: happy smile + blush -->
      <g opacity="{s_happy}">
        <path d="M 96 210 Q 140 248 184 210" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="54"  cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
        <ellipse cx="226" cy="204" rx="18" ry="11" fill="#FFB3BA" opacity=".45"/>
      </g>
      <!-- THINKING: smirk + raised brow + thought bubbles -->
      <g opacity="{s_think}">
        <path d="M 100 214 Q 128 228 158 212" stroke="#1A1A1A" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M 52  110 Q 72  94  96 102"  stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path d="M 184 104 Q 206 100 228 112" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <circle cx="218" cy="92"  r="5.5" fill="#CCCCCC" opacity=".75"/>
        <circle cx="232" cy="74"  r="8"   fill="#CCCCCC" opacity=".75"/>
        <circle cx="250" cy="52"  r="12"  fill="#CCCCCC" opacity=".75"/>
        <text x="250" y="57" font-size="13" text-anchor="middle" font-family="'Segoe UI',sans-serif" fill="#555">💡</text>
      </g>
      <!-- BYE: excited grin + raised brows + big blush -->
      <g opacity="{s_excited}">
        <path d="M 88 208 Q 140 256 192 208" stroke="#1A1A1A" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M 89 209 Q 140 252 191 209 L 188 224 Q 140 252 92 224 Z" fill="#FFFFFF" stroke="#D4D4D4" stroke-width="1.2"/>
        <line x1="115" y1="210" x2="115" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
        <line x1="140" y1="210" x2="140" y2="224" stroke="#D4D4D4" stroke-width="1.5"/>
        <line x1="165" y1="210" x2="165" y2="223" stroke="#D4D4D4" stroke-width="1.5"/>
        <path d="M 54  108 Q 76  94  100 100" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path d="M 180 100 Q 204 94  226 108" stroke="#1A1A1A" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="42"  cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
        <ellipse cx="238" cy="196" rx="24" ry="15" fill="#FFB3BA" opacity=".55"/>
      </g>
    </svg>
    <!-- Right arm -->
    <div style="
      width:22px;height:62px;background:#1A1A1A;border-radius:11px;
      transform-origin:top center;animation:{wave_r};
      align-self:flex-end;margin-bottom:14px;margin-left:-5px;
    "></div>
  </div>
</body></html>"""


# ── KFP Footer ────────────────────────────────────────────────────────────────
def _footer_html() -> str:
    """Fixed bottom footer — panda palette."""
    return """
<div class="kfp-footer">
  <span style="font-size:0.9rem;font-weight:800;
    background:linear-gradient(135deg,#74C69D,#FFB3BA);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    🐼 Learn It Here &mdash; Developed in 2026
  </span>
  <span style="font-size:0.75rem;color:#888888;">
    Powered by Streamlit &amp; Supabase
  </span>
</div>
"""


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
    pdf.cell(0, 10, "Learn It Here — Project Requirements", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(180, 205, 230)
    ts = data.get("submitted_at", datetime.now(timezone.utc).isoformat())
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
        "Generated by Learn It Here  |  Powered by Streamlit & Supabase  |  learnit.here",
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


# ── Landing Page ──────────────────────────────────────────────────────────────
def page_landing():
    """Full-width hero landing page with Po animation and two CTAs."""
    # Top nav bar
    st.markdown(
        """
<div class="kfp-nav">
  <span class="kfp-nav-logo">🐼</span>
  <div class="kfp-nav-text">
    <div class="kfp-nav-title">Learn It Here</div>
    <div class="kfp-nav-tagline">Hub to learn most important topics</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Centered hero: equal left/right columns ─────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown(
            """
<h1 class="hero-headline">Know Before You Go!</h1>
<div class="hero-bar"></div>
<p class="hero-sub">
  Don't start blind — know your stack upfront, capture what your project truly needs,
  then learn <em>exactly</em> what moves it forward. No generic tutorials, no wasted time.
</p>
<div class="hero-features">
  <div class="hero-feat">
    <span class="feat-icon">📋</span>
    <div class="feat-text">
      <strong>Capture Requirements</strong>
      <span>12 targeted questions that define your exact project context and tech stack</span>
    </div>
  </div>
  <div class="hero-feat">
    <span class="feat-icon">🎓</span>
    <div class="feat-text">
      <strong>Stack-Matched Guides</strong>
      <span>Curated learning built around your specific versions, tools, and architecture</span>
    </div>
  </div>
  <div class="hero-feat">
    <span class="feat-icon">⚡</span>
    <div class="feat-text">
      <strong>Learn &amp; Ship Fast</strong>
      <span>Hands-on, zero fluff — only the knowledge your project actually needs</span>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        bc1, bc2 = st.columns(2, gap="small")
        with bc1:
            if st.button(
                "📋 Fill Project Requirements",
                type="primary",
                use_container_width=True,
            ):
                _nav_to("requirements")
        with bc2:
            if st.button(
                "🎓 Learn It Here →",
                type="secondary",
                use_container_width=True,
            ):
                _nav_to("learn")

    with col_right:
        # Center the panda both horizontally and vertically within its column
        st.markdown(
            '<div style="display:flex;justify-content:center;align-items:center;height:100%;">',
            unsafe_allow_html=True,
        )
        components.html(_panda_landing_html(), height=510, scrolling=False)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(_footer_html(), unsafe_allow_html=True)


# ── Requirements Page ─────────────────────────────────────────────────────────
def page_requirements():
    """Project requirements questionnaire — same form, KFP branding."""
    cb = _on_interact

    # Nav bar with back button
    nav_col, _ = st.columns([6, 1])
    with nav_col:
        st.markdown(
            """
<div class="kfp-nav">
  <span class="kfp-nav-logo">🐼</span>
  <div class="kfp-nav-text">
    <div class="kfp-nav-title">Learn It Here</div>
    <div class="kfp-nav-tagline">Project Requirements</div>
  </div>
  <div class="kfp-nav-sub">📋 Step 1 of your journey</div>
</div>
""",
            unsafe_allow_html=True,
        )

    if st.button("← Back to Home", key="req_back"):
        _nav_to("landing")

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="app-title">📋 Project Requirements</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-subtitle">'
        "Capture your project's tech-stack details. "
        "Fill in all 12 questions and download a shareable PDF."
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
            st.html(_robot_html("bye"))
            if st.session_state.pdf_bytes:
                st.download_button(
                    label="⬇️  Download Requirements as PDF",
                    data=st.session_state.pdf_bytes,
                    file_name=f"project_requirements_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.markdown("<br>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2, gap="medium")
            with sc1:
                if st.button("🎓 Go to Learning Hub →", type="primary", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.session_state.page = "learn"
                    st.rerun()
            with sc2:
                if st.button("📝 Submit Another Response", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()
        st.markdown(_footer_html(), unsafe_allow_html=True)
        return

    # ── Two-column layout ─────────────────────────────────────────────────────
    col_form, col_anim = st.columns([3, 2], gap="large")

    with col_anim:
        st.html(_robot_html(st.session_state.animation_state))

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
                "submitted_at":    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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

            ok, db_msg = save_to_supabase(record)
            if ok:
                st.success(db_msg)
            else:
                st.info(f"ℹ️  {db_msg}")

            try:
                st.session_state.pdf_bytes = generate_pdf(record)
            except Exception as exc:
                st.warning(f"PDF generation failed: {exc}")
                st.session_state.pdf_bytes = None

            st.session_state.animation_state = "bye"
            st.session_state.submitted = True
            st.rerun()

    st.markdown(_footer_html(), unsafe_allow_html=True)


# ── Learning Hub Page ─────────────────────────────────────────────────────────
def page_learn():
    """Tabbed learning hub: GIT | Visual Studio IDE | VS Code."""
    # Nav bar
    st.markdown(
        """
<div class="kfp-nav">
  <span class="kfp-nav-logo">🐼</span>
  <div class="kfp-nav-text">
    <div class="kfp-nav-title">Learn It Here</div>
    <div class="kfp-nav-tagline">Developer Learning Hub</div>
  </div>
  <div class="kfp-nav-sub">🎓 Knowledge is your best weapon</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("← Back to Home", key="learn_back"):
        _nav_to("landing")

    tab_git, tab_vsIDE, tab_vsCode = st.tabs(
        ["🔧  GIT", "💻  Visual Studio IDE", "📝  VS Code"]
    )

    # ══════════════════════════════════════════════════════════════════════════
    # GIT TAB
    # ══════════════════════════════════════════════════════════════════════════
    with tab_git:
        # Overview
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔧 What is GIT?</div>
  <div class="card-body">
    <b>Git</b> is a <em>distributed version control system</em> that tracks changes in source code
    during software development. It lets multiple developers collaborate simultaneously,
    maintains a complete history of every change, and supports powerful branching and merging
    workflows — all without needing a constant connection to a central server.
    <br><br>
    Git lives on your machine. The platforms below are <em>cloud hosting services</em> that store
    your Git repositories and add collaboration features like pull requests, pipelines, and boards.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Supported platforms
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🌐 Supported Platforms</div>
  <div class="card-body">
    Git works the same way locally regardless of which platform hosts your remote repository.
    Each platform adds its own collaboration and CI/CD features on top.
  </div>
  <div class="platform-row">
    <div class="platform-badge">🐙 <span>GitHub<br><small style="font-weight:400;color:#64748B">Open-source leader, GitHub Actions CI/CD, GitHub Copilot</small></span></div>
    <div class="platform-badge">🔷 <span>Azure DevOps<br><small style="font-weight:400;color:#64748B">Microsoft ecosystem, Boards + Pipelines + Repos</small></span></div>
    <div class="platform-badge">🪣 <span>Bitbucket<br><small style="font-weight:400;color:#64748B">Atlassian ecosystem, integrates with JIRA natively</small></span></div>
    <div class="platform-badge">🦊 <span>GitLab<br><small style="font-weight:400;color:#64748B">All-in-one DevOps platform, built-in CI/CD pipelines</small></span></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Workflow diagram
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🗺️ Workflow Diagram — Clone to Push</div>
  <div class="card-body">
    This is the standard day-to-day workflow every developer follows, from getting the
    codebase to your machine all the way to merging your changes back.
  </div>
  <div class="wf-diagram">
    <div class="wf-node">📥 Clone / Pull</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node">🌿 Create Branch</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node">✏️ Write Code</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node">📦 Stage Changes</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node">💾 Commit</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node">🚀 Push</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node-green">🔍 Pull Request</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node-green">✅ Code Review</div>
    <div class="wf-arrow">→</div>
    <div class="wf-node-green">🔀 Merge</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Commands
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⌨️ Commands We Use Regularly</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="card-body">These are the commands you\'ll run day-to-day — '
            "from getting the repo to pushing your work back up.</div>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card-section-title">Starting Out</div>', unsafe_allow_html=True)
        st.markdown(
            """<div class="cmd-block">
<span class="cmd-comment"># Clone the repository to your local machine</span>
git clone https://github.com/your-org/your-repo.git

<span class="cmd-comment"># Navigate into the project folder</span>
cd your-repo

<span class="cmd-comment"># Check current branch and status</span>
git status
git branch
</div>""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card-section-title">Daily Workflow</div>', unsafe_allow_html=True)
        st.markdown(
            """<div class="cmd-block">
<span class="cmd-comment"># Always pull latest changes before starting work</span>
git fetch origin
git pull origin main

<span class="cmd-comment"># Create and switch to a new feature branch</span>
git checkout -b feature/my-feature-name

<span class="cmd-comment"># See what has changed</span>
git status
git diff

<span class="cmd-comment"># Stage your changes (all files, or a specific file)</span>
git add .
git add src/MyFile.cs

<span class="cmd-comment"># Commit with a clear message</span>
git commit -m "feat: add user login endpoint"

<span class="cmd-comment"># Push your branch to the remote</span>
git push origin feature/my-feature-name
</div>""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card-section-title">Keeping Your Branch Up to Date</div>', unsafe_allow_html=True)
        st.markdown(
            """<div class="cmd-block">
<span class="cmd-comment"># Option 1: Rebase on main (keeps history clean — preferred)</span>
git fetch origin
git rebase origin/main

<span class="cmd-comment"># Option 2: Merge main into your branch</span>
git merge origin/main

<span class="cmd-comment"># Undo staged changes (before commit)</span>
git reset HEAD src/MyFile.cs

<span class="cmd-comment"># Temporarily stash unfinished work and come back later</span>
git stash
git stash pop
</div>""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card-section-title">Useful Inspection Commands</div>', unsafe_allow_html=True)
        st.markdown(
            """<div class="cmd-block">
<span class="cmd-comment"># Last 10 commits on current branch</span>
git log --oneline -10

<span class="cmd-comment"># See changes between your branch and main</span>
git diff main..HEAD

<span class="cmd-comment"># Show all local and remote branches</span>
git branch -a

<span class="cmd-comment"># Delete a local branch after merging</span>
git branch -d feature/my-feature-name
</div>""",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)  # close content-card

        # VS IDE Integration
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">💻 Using GIT inside Visual Studio IDE</div>
  <div class="card-body">
    You don't need to use the terminal at all — Visual Studio has a full Git UI built in.
  </div>
  <div class="feature-grid">
    <div class="feature-pill">
      <strong>Open Git Changes</strong>
      <p>View &rarr; Git Changes (Ctrl+0, Ctrl+G) — stage, unstage, and commit files visually.</p>
    </div>
    <div class="feature-pill">
      <strong>Git Repository Window</strong>
      <p>View &rarr; Git Repository — see branch history, compare commits, create branches.</p>
    </div>
    <div class="feature-pill">
      <strong>Create Branch</strong>
      <p>Click the branch name in the status bar (bottom-right) and select "New Branch".</p>
    </div>
    <div class="feature-pill">
      <strong>Pull / Push / Fetch</strong>
      <p>Git menu at the top &rarr; Pull, Push, Fetch — or use the sync icon in the status bar.</p>
    </div>
    <div class="feature-pill">
      <strong>Resolve Merge Conflicts</strong>
      <p>VS opens a 3-way merge editor — accept incoming, current, or both, side by side.</p>
    </div>
    <div class="feature-pill">
      <strong>Create Pull Request</strong>
      <p>Git menu &rarr; "Create Pull Request" — opens your platform (Azure DevOps / GitHub) in the browser pre-filled.</p>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # VISUAL STUDIO IDE TAB
    # ══════════════════════════════════════════════════════════════════════════
    with tab_vsIDE:
        # Overview
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">💻 What is Visual Studio (Full IDE)?</div>
  <div class="card-body">
    <b>Visual Studio</b> is Microsoft's flagship integrated development environment —
    the most powerful tooling available for .NET, C#, ASP.NET, Azure, and enterprise applications.
    It goes far beyond a text editor: it's a complete development workbench with debuggers,
    profilers, designers, test runners, and deep Git integration built in.
    <br><br>
    Always install the <b>latest stable version</b> and keep it updated to access new C# language
    features, improved IntelliSense, and the most recent .NET SDK tooling.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Key features
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⚡ Key Productivity Features</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="feature-grid">
  <div class="feature-pill">
    <strong>🪄 Paste JSON as Classes</strong>
    <p>Edit &rarr; Paste Special &rarr; <b>Paste JSON as Classes</b>.
       Copies JSON from clipboard and auto-generates matching C# model classes. Huge time-saver!</p>
  </div>
  <div class="feature-pill">
    <strong>🪄 Paste XML as Classes</strong>
    <p>Edit &rarr; Paste Special &rarr; <b>Paste XML as Classes</b>.
       Same idea for XML data — instant model generation.</p>
  </div>
  <div class="feature-pill">
    <strong>💡 Quick Actions (Lightbulb)</strong>
    <p>Press <b>Ctrl+.</b> anywhere to get context-aware suggestions:
       generate constructors, implement interfaces, extract methods, rename symbols.</p>
  </div>
  <div class="feature-pill">
    <strong>🏗️ Generate from Usage</strong>
    <p>Type a class or method that doesn't exist yet, press Ctrl+. and choose
       "Generate class / method" — VS creates the skeleton automatically.</p>
  </div>
  <div class="feature-pill">
    <strong>🔬 Live Code Analysis</strong>
    <p>Roslyn analysers flag issues, suggest improvements, and enforce code style in real time —
       no need to build first.</p>
  </div>
  <div class="feature-pill">
    <strong>🧪 Test Explorer</strong>
    <p>View &rarr; Test Explorer. Run, debug, and profile all xUnit / NUnit / MSTest tests
       directly from the IDE with green/red indicators per test.</p>
  </div>
  <div class="feature-pill">
    <strong>📦 NuGet Package Manager</strong>
    <p>Tools &rarr; NuGet Package Manager &rarr; Manage NuGet Packages for Solution —
       search, install, and update packages across all projects at once.</p>
  </div>
  <div class="feature-pill">
    <strong>🗂️ Solution Explorer</strong>
    <p>The backbone of VS — browse files, projects, and dependencies.
       Right-click a project for <b>Add &rarr; New Item</b>, scaffolding, and class diagrams.</p>
  </div>
  <div class="feature-pill">
    <strong>📐 Class Diagram</strong>
    <p>Right-click a project &rarr; Add &rarr; New Item &rarr; Class Diagram.
       Visual representation of all classes, interfaces, and their relationships.</p>
  </div>
  <div class="feature-pill">
    <strong>🔍 Object Browser</strong>
    <p>View &rarr; Object Browser — explore all types, members, and assemblies in your solution
       and referenced NuGet packages.</p>
  </div>
  <div class="feature-pill">
    <strong>📊 Performance Profiler</strong>
    <p>Debug &rarr; Performance Profiler — analyse CPU usage, memory allocations,
       and database query times without leaving VS.</p>
  </div>
  <div class="feature-pill">
    <strong>🔄 Refactor Menu</strong>
    <p>Right-click any symbol &rarr; Refactor: rename everywhere, extract interface,
       extract method, inline temporary variable, and more — safely across the whole solution.</p>
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Productivity settings
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⚙️ Productivity Settings Worth Configuring</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="feature-grid">
  <div class="feature-pill">
    <strong>Font &amp; Editor Size</strong>
    <p>Tools &rarr; Options &rarr; Environment &rarr; Fonts and Colors.
       Set font to <em>Cascadia Code</em> or <em>JetBrains Mono</em> at size 14–15 for ligatures.</p>
  </div>
  <div class="feature-pill">
    <strong>IntelliSense Completion</strong>
    <p>Tools &rarr; Options &rarr; Text Editor &rarr; C# &rarr; IntelliSense.
       Enable "Show completion list after character is deleted" and "Highlight matching portions".</p>
  </div>
  <div class="feature-pill">
    <strong>Code Style &amp; Formatting</strong>
    <p>Tools &rarr; Options &rarr; Text Editor &rarr; C# &rarr; Code Style.
       Configure naming conventions, prefer var vs explicit types, expression-bodied members.</p>
  </div>
  <div class="feature-pill">
    <strong>Format on Save</strong>
    <p>Use a <b>.editorconfig</b> file in the solution root to enforce formatting rules
       across the whole team automatically on save.</p>
  </div>
  <div class="feature-pill">
    <strong>Word Wrap</strong>
    <p>Edit &rarr; Advanced &rarr; Word Wrap (Ctrl+E, W). Prevents horizontal scrolling
       on long lines — great for wide monitors.</p>
  </div>
  <div class="feature-pill">
    <strong>Column Guides</strong>
    <p>Add <code>guidelines</code> extension or set column guides in .editorconfig
       to keep lines under 120 characters.</p>
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Recommended extensions
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔌 Extensions Worth Installing</div>
  <div class="feature-grid">
    <div class="feature-pill">
      <strong>GitHub Copilot</strong>
      <p>AI pair programmer — suggests whole lines, methods, and even entire classes as you type.</p>
    </div>
    <div class="feature-pill">
      <strong>ReSharper / Rider</strong>
      <p>JetBrains' powerful refactoring and analysis tools. Deep code inspections, rename across solutions.</p>
    </div>
    <div class="feature-pill">
      <strong>CodeMaid</strong>
      <p>Cleans up code — removes unused usings, reorganises members, formats on save.</p>
    </div>
    <div class="feature-pill">
      <strong>Visual Studio IntelliCode</strong>
      <p>AI-assisted IntelliCode completions trained on open-source .NET code patterns.</p>
    </div>
    <div class="feature-pill">
      <strong>Web Essentials</strong>
      <p>Browser sync, BundlerMinifier, and CSS / JavaScript helpers for web projects.</p>
    </div>
    <div class="feature-pill">
      <strong>Productivity Power Tools</strong>
      <p>Double-click to select word, middle-click to close tabs, enhanced scrollbar — quality-of-life pack.</p>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Key shortcuts
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<table class="shortcut-table">
<tr><th>Shortcut</th><th>Action</th></tr>
<tr><td>Ctrl+.</td><td>Quick Actions / Lightbulb fixes</td></tr>
<tr><td>Ctrl+R, R</td><td>Rename symbol everywhere</td></tr>
<tr><td>F12</td><td>Go to Definition</td></tr>
<tr><td>Alt+F12</td><td>Peek Definition (inline preview)</td></tr>
<tr><td>Shift+F12</td><td>Find All References</td></tr>
<tr><td>Ctrl+K, D</td><td>Format document</td></tr>
<tr><td>Ctrl+K, C / U</td><td>Comment / Uncomment selection</td></tr>
<tr><td>Ctrl+Shift+B</td><td>Build solution</td></tr>
<tr><td>F5 / Ctrl+F5</td><td>Debug / Run without debug</td></tr>
<tr><td>Ctrl+0, Ctrl+G</td><td>Open Git Changes window</td></tr>
<tr><td>Ctrl+T</td><td>Go to file / type / member</td></tr>
<tr><td>Ctrl+Q</td><td>Quick Launch — search VS menus</td></tr>
</table>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # VS CODE TAB
    # ══════════════════════════════════════════════════════════════════════════
    with tab_vsCode:
        # Overview
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📝 What is VS Code?</div>
  <div class="card-body">
    <b>Visual Studio Code</b> is a lightweight but extremely powerful source-code editor from
    Microsoft. It runs on Windows, macOS, and Linux and is ideal for front-end development,
    scripting, PowerShell, Python, Docker files, and quick code edits.
    <br><br>
    With the right extensions it becomes a fully capable environment for C#/.NET development too.
    Its extension marketplace has over 50,000 extensions — there's almost nothing you can't do in it.
    Unlike the full Visual Studio IDE, VS Code starts in under a second and never feels heavy.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Key features
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⚡ Key Features</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="feature-grid">
  <div class="feature-pill">
    <strong>🖱️ Multi-Cursor Editing</strong>
    <p><b>Alt+Click</b> to add cursors. <b>Ctrl+D</b> selects the next occurrence.
       <b>Ctrl+Shift+L</b> selects all occurrences. Edit many places at once!</p>
  </div>
  <div class="feature-pill">
    <strong>🎨 Command Palette</strong>
    <p><b>Ctrl+Shift+P</b> opens every command VS Code can run — format, lint, git, settings, extensions.</p>
  </div>
  <div class="feature-pill">
    <strong>🖥️ Integrated Terminal</strong>
    <p><b>Ctrl+`</b> opens a full terminal right in the editor. Run builds, git commands,
       npm scripts without switching windows.</p>
  </div>
  <div class="feature-pill">
    <strong>🌐 Live Share</strong>
    <p>Real-time collaborative editing with teammates — they see your cursor, you see theirs.
       Great for pair programming and code reviews.</p>
  </div>
  <div class="feature-pill">
    <strong>🔌 Remote Development</strong>
    <p>Edit code running on a remote SSH server, inside WSL (Linux on Windows),
       or inside Docker containers — seamlessly.</p>
  </div>
  <div class="feature-pill">
    <strong>✂️ Code Snippets</strong>
    <p>Type a prefix (e.g., <em>prop</em>, <em>ctor</em>, <em>for</em>) and press Tab to
       expand full code templates. You can create custom snippets too.</p>
  </div>
  <div class="feature-pill">
    <strong>🧘 Zen Mode</strong>
    <p><b>Ctrl+K Z</b> hides all UI — just your code on a clean background.
       Perfect for focused writing or presentations.</p>
  </div>
  <div class="feature-pill">
    <strong>🔍 IntelliSense</strong>
    <p>Powered by language servers (LSP). C# Dev Kit, Pylance, ESLint etc.
       give you completions, signatures, and hover docs just like the full IDE.</p>
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Recommended extensions
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">🔌 Recommended Extensions</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="feature-grid">
  <div class="feature-pill">
    <strong>C# Dev Kit (Microsoft)</strong>
    <p>Full .NET / C# support — IntelliSense, refactoring, Test Explorer, and Solution Explorer inside VS Code.</p>
  </div>
  <div class="feature-pill">
    <strong>GitLens</strong>
    <p>Supercharges VS Code's built-in Git — inline blame, rich history, branch comparison, PR integration.</p>
  </div>
  <div class="feature-pill">
    <strong>REST Client / Thunder Client</strong>
    <p>Test HTTP APIs by writing <code>.http</code> files or using a GUI — no need to leave the editor.</p>
  </div>
  <div class="feature-pill">
    <strong>Prettier</strong>
    <p>Opinionated code formatter for JS/TS/CSS/JSON/Markdown. Format on save with zero configuration.</p>
  </div>
  <div class="feature-pill">
    <strong>GitHub Copilot</strong>
    <p>AI pair programmer — completes functions, writes tests, and explains code from comments.</p>
  </div>
  <div class="feature-pill">
    <strong>ESLint / Pylint</strong>
    <p>Language-specific linting with inline highlights for JavaScript/TypeScript and Python respectively.</p>
  </div>
  <div class="feature-pill">
    <strong>Todo Tree</strong>
    <p>Scans all files for TODO / FIXME / HACK comments and lists them in a sidebar panel.</p>
  </div>
  <div class="feature-pill">
    <strong>Bracket Pair Colorizer</strong>
    <p>Matching brackets are coloured the same — makes nested code much easier to read at a glance.</p>
  </div>
  <div class="feature-pill">
    <strong>Path Intellisense</strong>
    <p>Autocompletes file paths as you type <code>import</code> or reference statements.</p>
  </div>
  <div class="feature-pill">
    <strong>Docker</strong>
    <p>Browse containers, images, and registries. Build and run Dockerfiles from the explorer panel.</p>
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Settings
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⚙️ Recommended settings.json</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="card-body">Open with <b>Ctrl+Shift+P</b> &rarr; "Open User Settings (JSON)"</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="json-block">{
  "editor.fontSize": 14,
  "editor.fontFamily": "'Cascadia Code', 'JetBrains Mono', Consolas, monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 4,
  "editor.formatOnSave": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.suggestSelection": "first",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "git.autofetch": true,
  "git.confirmSync": false,
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}</div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Shortcuts
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<table class="shortcut-table">
<tr><th>Shortcut</th><th>Action</th></tr>
<tr><td>Ctrl+P</td><td>Quick file open (fuzzy search)</td></tr>
<tr><td>Ctrl+Shift+P</td><td>Command Palette — search all commands</td></tr>
<tr><td>Ctrl+`</td><td>Toggle integrated terminal</td></tr>
<tr><td>Ctrl+B</td><td>Toggle sidebar visibility</td></tr>
<tr><td>Ctrl+/</td><td>Toggle line comment</td></tr>
<tr><td>Alt+↑ / Alt+↓</td><td>Move current line up / down</td></tr>
<tr><td>Shift+Alt+↓</td><td>Duplicate current line below</td></tr>
<tr><td>Ctrl+D</td><td>Select next occurrence of current word</td></tr>
<tr><td>Ctrl+Shift+L</td><td>Select ALL occurrences of current word</td></tr>
<tr><td>F12</td><td>Go to Definition</td></tr>
<tr><td>Shift+F12</td><td>Find All References</td></tr>
<tr><td>F2</td><td>Rename symbol everywhere</td></tr>
<tr><td>Ctrl+K Z</td><td>Zen mode (distraction-free)</td></tr>
<tr><td>Ctrl+Shift+`</td><td>New terminal instance</td></tr>
</table>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(_footer_html(), unsafe_allow_html=True)


# ── Main Routing ──────────────────────────────────────────────────────────────
def main():
    page = st.session_state.page
    if page == "requirements":
        page_requirements()
    elif page == "learn":
        page_learn()
    else:
        page_landing()


main()

