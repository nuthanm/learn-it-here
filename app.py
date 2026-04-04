"""Learn It Here
A Streamlit learning hub for developers – project requirements capture + tech-stack guides.
Stores responses in Supabase (PostgreSQL) and allows PDF export.
"""

import os
import streamlit as st
from datetime import datetime

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

  /* ─ Global background (parchment / bamboo paper) ─ */
  [data-testid="stAppViewContainer"] { background: #F5F0E8; }
  [data-testid="stHeader"]           { background: transparent; }
  .block-container {
    padding-top: 1.2rem !important;
    max-width: 1280px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }

  /* ─ Top nav bar ─ */
  .kfp-nav {
    display: flex; align-items: center; gap: 1.2rem;
    padding: 0.7rem 1.6rem; margin-bottom: 1.6rem;
    background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
    border-radius: 16px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.28);
  }
  .kfp-nav-logo  { font-size: 2.1rem; }
  .kfp-nav-title {
    font-size: 1.45rem; font-weight: 800;
    background: linear-gradient(135deg, #D4AC0D, #F4D03F);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.3px;
  }
  .kfp-nav-sub { font-size: 0.78rem; color: #94A3B8; margin-left: auto; }

  /* ─ Landing hero ─ */
  .hero-title {
    font-size: 2.9rem; font-weight: 900; line-height: 1.15;
    color: #1A1A1A; margin-bottom: 0;
  }
  .hero-title span { color: #C4541A; }
  .hero-sub {
    font-size: 1.05rem; color: #475569;
    margin: 0.9rem 0 1.8rem; line-height: 1.75;
  }

  /* ─ Workflow steps on landing ─ */
  .wf-step {
    display: flex; align-items: flex-start; gap: 0.9rem;
    background: white; border-radius: 14px; padding: 0.85rem 1.3rem;
    border-left: 4px solid #2D6A4F;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 0.75rem;
  }
  .wf-step-icon { font-size: 1.5rem; flex-shrink: 0; }
  .wf-step-text strong { color: #1A1A1A; font-size: 0.9rem; display: block; }
  .wf-step-text p { color: #64748B; font-size: 0.8rem; margin: 0.1rem 0 0; }

  /* ─ CTA buttons ─ */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #C4541A 0%, #E07040 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-size: 1rem !important;
    font-weight: 700 !important; padding: 0.7rem 0 !important;
    box-shadow: 0 6px 20px rgba(196,84,26,0.38) !important;
    transition: opacity 0.2s !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.88 !important; }

  div[data-testid="stButton"] > button[kind="secondary"] {
    background: linear-gradient(135deg, #2D6A4F 0%, #40916C 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-size: 1rem !important;
    font-weight: 700 !important; padding: 0.7rem 0 !important;
    box-shadow: 0 6px 20px rgba(45,106,79,0.38) !important;
    transition: opacity 0.2s !important;
  }
  div[data-testid="stButton"] > button[kind="secondary"]:hover { opacity: 0.88 !important; }

  /* ─ Download button ─ */
  div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(16,185,129,0.35) !important;
  }

  /* ─ Tabs ─ */
  [data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: white !important; border-radius: 14px !important;
    padding: 0.3rem 0.5rem !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07) !important;
    margin-bottom: 1.2rem !important;
  }
  [data-testid="stTabs"] button {
    font-size: 0.97rem !important; font-weight: 600 !important;
    color: #475569 !important; border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
  }
  [data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #C4541A, #E07040) !important;
    color: white !important;
  }

  /* ─ Content cards ─ */
  .content-card {
    background: white; border-radius: 18px;
    padding: 2rem 2.4rem; margin-bottom: 1.5rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  }
  .card-title {
    font-size: 1.2rem; font-weight: 700; color: #1A1A1A;
    margin-bottom: 0.9rem;
  }
  .card-body { color: #475569; line-height: 1.8; font-size: 0.95rem; }
  .card-section-title {
    font-size: 0.8rem; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 1.1px;
    margin: 1.6rem 0 0.6rem;
  }

  /* ─ Workflow diagram nodes ─ */
  .wf-diagram {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 0.4rem; margin: 1rem 0;
  }
  .wf-node {
    background: linear-gradient(135deg, #1A1A1A, #333);
    color: white; padding: 0.45rem 1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18);
  }
  .wf-node-green {
    background: linear-gradient(135deg, #2D6A4F, #40916C);
    color: white; padding: 0.45rem 1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600;
  }
  .wf-arrow { color: #C4541A; font-size: 1.1rem; font-weight: 700; }

  /* ─ Feature grid pills ─ */
  .feature-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 0.85rem; margin: 1rem 0;
  }
  .feature-pill {
    background: #F0FDF4; border: 1px solid #BBF7D0;
    border-radius: 12px; padding: 0.85rem 1.1rem;
  }
  .feature-pill strong { color: #166534; font-size: 0.88rem; display: block; }
  .feature-pill p { color: #4B5563; font-size: 0.78rem; margin: 0.25rem 0 0; }

  /* ─ Platform badges ─ */
  .platform-row { display: flex; flex-wrap: wrap; gap: 0.9rem; margin: 1rem 0; }
  .platform-badge {
    display: flex; align-items: center; gap: 0.55rem;
    background: white; border: 2px solid #E2E8F0;
    border-radius: 12px; padding: 0.65rem 1.3rem;
    font-weight: 700; color: #1E3A5F; font-size: 0.88rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }

  /* ─ Command blocks ─ */
  .cmd-block {
    background: #1A1A1A; color: #A3E635;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto;
  }
  .cmd-comment { color: #6B7280; font-style: italic; }

  /* ─ Settings / JSON blocks ─ */
  .json-block {
    background: #0F172A; color: #7DD3FC;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto;
  }

  /* ─ Requirements form card ─ */
  .form-card {
    background: #ffffff; border-radius: 18px;
    padding: 2rem 2.2rem; border: 1px solid #E2E8F0;
    box-shadow: 0 4px 24px rgba(30,58,95,0.07);
  }
  .app-title   { font-size: 1.9rem; font-weight: 700; color: #1A1A1A; margin-bottom: 0.2rem; }
  .app-subtitle { font-size: 0.92rem; color: #64748B; margin-bottom: 1.8rem; }
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

  /* ─ Success card ─ */
  .success-card {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1px solid #BBF7D0; border-radius: 18px;
    padding: 2.5rem 3rem; text-align: center;
  }
  .success-title { font-size: 1.6rem; font-weight: 700; color: #166534; margin-bottom: 0.4rem; }
  .success-sub   { font-size: 0.95rem; color: #22C55E; margin-bottom: 1.8rem; }

  /* ─ Shortcut table ─ */
  .shortcut-table { width: 100%; border-collapse: collapse; margin: 0.6rem 0; }
  .shortcut-table th {
    background: #1A1A1A; color: #D4AC0D;
    padding: 0.55rem 1rem; text-align: left; font-size: 0.83rem;
    border-radius: 0;
  }
  .shortcut-table td {
    padding: 0.5rem 1rem; font-size: 0.85rem; color: #374151;
    border-bottom: 1px solid #F1F5F9;
  }
  .shortcut-table tr:last-child td { border-bottom: none; }
  .shortcut-table tr:nth-child(even) td { background: #FAFAFA; }

  /* ─ KFP footer ─ */
  .kfp-footer {
    margin-top: 3rem; padding: 0.5rem 0 1rem;
    text-align: center; font-size: 0.8rem; color: #94A3B8;
  }
</style>
""",
    unsafe_allow_html=True,
)


# ── Kung Fu Panda — Landing Animation ────────────────────────────────────────
def _panda_landing_html() -> str:
    """Return an animated Kung Fu Panda (Po) HTML component for the landing page.
    Po drops from the top, dust clouds puff out, a 'Welcome' bubble appears,
    then his right arm swings to point towards the left-side content.
    """
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    background:transparent;
    display:flex;flex-direction:column;align-items:center;
    justify-content:flex-start;padding-top:8px;
    font-family:'Segoe UI',system-ui,sans-serif;
    min-height:500px;overflow:hidden;
  }

  /* ─ Drop-in entrance ─ */
  @keyframes poLand{
    0%  {transform:translateY(-420px) rotate(-6deg);opacity:0}
    65% {transform:translateY(18px)  rotate( 2deg);opacity:1}
    78% {transform:translateY(-12px) rotate( 0deg)}
    100%{transform:translateY(0)     rotate( 0deg);opacity:1}
  }
  /* ─ Dust puffs ─ */
  @keyframes dustPuff{
    0%  {width:0;height:0;opacity:.85;transform:translateX(-50%) scaleY(1)}
    100%{width:240px;height:70px;opacity:0;transform:translateX(-50%) scaleY(.7)}
  }
  @keyframes dustPuff2{
    0%  {width:0;height:0;opacity:.65}
    100%{width:150px;height:55px;opacity:0}
  }
  /* ─ Bubble & pointer ─ */
  @keyframes bubbleIn{
    from{opacity:0;transform:scale(.88) translateY(8px)}
    to  {opacity:1;transform:scale(1)   translateY(0)}
  }
  @keyframes pointLeft{
    0%,55%{transform:rotate(12deg)}
    100%  {transform:rotate(-80deg) translateX(-4px)}
  }
  /* ─ Idle breathe ─ */
  @keyframes breathe{
    0%,100%{transform:scaleY(1)}
    50%    {transform:scaleY(1.04)}
  }
  /* ─ Eye blink ─ */
  @keyframes blink{
    0%,86%,100%{transform:scaleY(1)}
    90%         {transform:scaleY(.08)}
  }

  /* Scene */
  .scene{position:relative;width:270px;height:490px;display:flex;flex-direction:column;align-items:center}

  /* Dust */
  .dust1{
    position:absolute;bottom:115px;left:50%;border-radius:50%;
    background:radial-gradient(ellipse,rgba(180,140,65,.6),transparent 70%);
    animation:dustPuff 1s ease-out .6s both;pointer-events:none;
  }
  .dust2{
    position:absolute;bottom:112px;left:42%;border-radius:50%;
    background:radial-gradient(ellipse,rgba(160,115,50,.45),transparent 70%);
    animation:dustPuff2 1.1s ease-out .7s both;width:0;height:0;pointer-events:none;
  }

  /* Po wrapper */
  .po-wrap{
    animation:poLand .8s cubic-bezier(.22,1,.36,1) .1s both;
    display:flex;flex-direction:column;align-items:center;
    position:relative;margin-top:20px;
  }

  /* Speech bubble */
  .bubble{
    background:#fff;border:2.5px solid #C4541A;border-radius:18px;
    padding:11px 18px;font-size:13.5px;color:#C4541A;font-weight:700;
    max-width:210px;text-align:center;line-height:1.55;
    box-shadow:0 4px 18px rgba(196,84,26,.18);
    animation:bubbleIn .5s ease .95s both;
    margin-bottom:14px;position:relative;
  }
  .bubble::after{
    content:'';position:absolute;bottom:-13px;left:50%;transform:translateX(-50%);
    border:10px solid transparent;border-top-color:#C4541A;
  }
  .bubble::before{
    content:'';position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);
    border:9px solid transparent;border-top-color:#fff;z-index:1;
  }

  /* Panda body */
  .panda{
    position:relative;display:flex;flex-direction:column;align-items:center;
    animation:breathe 3.2s ease-in-out 1.3s infinite;
  }

  /* Head */
  .p-head{
    width:112px;height:104px;background:#fff;border-radius:50%;
    border:3px solid #1A1A1A;position:relative;z-index:2;
    box-shadow:3px 4px 14px rgba(0,0,0,.14);
  }
  /* Ears via pseudo-elements */
  .p-head::before,.p-head::after{
    content:'';position:absolute;
    width:32px;height:32px;border-radius:50%;background:#1A1A1A;
  }
  .p-head::before{top:-10px;left:8px}
  .p-head::after {top:-10px;right:8px}

  /* Eye patches */
  .ep-l,.ep-r{
    position:absolute;top:28px;
    width:34px;height:30px;background:#1A1A1A;border-radius:50%;
  }
  .ep-l{left:13px;transform:rotate(-10deg)}
  .ep-r{right:13px;transform:rotate( 10deg)}

  /* Eyes */
  .eye-l,.eye-r{
    position:absolute;top:35px;
    width:19px;height:19px;background:#fff;border-radius:50%;
    animation:blink 5.5s infinite;
  }
  .eye-l{left:19px}.eye-r{right:19px}
  .eye-l::after,.eye-r::after{
    content:'';position:absolute;width:9px;height:9px;
    border-radius:50%;background:#1A1A1A;top:50%;left:50%;
    transform:translate(-50%,-50%);
  }
  .eye-l::before,.eye-r::before{
    content:'';position:absolute;width:4px;height:4px;
    border-radius:50%;background:#fff;z-index:2;top:3px;right:3px;
  }

  /* Nose & mouth */
  .p-nose{
    position:absolute;top:62px;left:50%;transform:translateX(-50%);
    width:20px;height:14px;background:#1A1A1A;border-radius:50% 50% 40% 40%;
  }
  .p-mouth{
    position:absolute;top:76px;left:50%;transform:translateX(-50%);
    width:34px;height:12px;
    border-bottom:3px solid #4A2020;border-radius:0 0 17px 17px;
  }

  /* Torso row */
  .torso-row{display:flex;align-items:flex-start;gap:5px;margin-top:-3px}

  /* Body */
  .p-body{
    width:104px;height:115px;
    background:#1A1A1A;border-radius:24px 24px 30px 30px;
    position:relative;z-index:1;
    box-shadow:0 6px 16px rgba(0,0,0,.22);
  }
  .p-belly{
    position:absolute;bottom:10px;left:50%;transform:translateX(-50%);
    width:66px;height:78px;background:#fff;
    border-radius:50%;border:2px solid #E0E0E0;
  }

  /* Arms */
  .arm-l,.arm-r{
    width:28px;height:78px;
    background:#1A1A1A;border-radius:14px;
    transform-origin:top center;
  }
  .arm-l{transform:rotate(14deg)}
  .arm-r{animation:pointLeft 1.3s cubic-bezier(.22,1,.36,1) 1.15s both}

  /* Legs + feet */
  .legs{display:flex;gap:8px;margin-top:0}
  .leg-l,.leg-r{
    width:36px;height:55px;
    background:#1A1A1A;border-radius:0 0 18px 18px;
    box-shadow:0 4px 8px rgba(0,0,0,.18);position:relative;
  }
  .leg-l::after,.leg-r::after{
    content:'';display:block;
    width:42px;height:18px;
    background:#1A1A1A;border-radius:0 0 22px 22px;
    position:absolute;bottom:-10px;left:-3px;
  }
</style></head>
<body>
<div class="scene">
  <div class="dust1"></div>
  <div class="dust2"></div>
  <div class="po-wrap">
    <div class="bubble">Hey there! 🐼<br>Check the left — that's where<br>the magic happens! 👈</div>
    <div class="panda">
      <div class="p-head">
        <div class="ep-l"></div><div class="ep-r"></div>
        <div class="eye-l"></div><div class="eye-r"></div>
        <div class="p-nose"></div><div class="p-mouth"></div>
      </div>
      <div class="torso-row">
        <div class="arm-l"></div>
        <div class="p-body"><div class="p-belly"></div></div>
        <div class="arm-r"></div>
      </div>
      <div class="legs">
        <div class="leg-l"></div><div class="leg-r"></div>
      </div>
    </div>
  </div>
</div>
</body></html>"""


# ── Kung Fu Panda — Form-page Robot (thinking/bye states kept) ────────────────
def _robot_html(state: str) -> str:
    """Return the animated panda helper for the requirements form page."""
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
    arm_l = "arm arm-left" + (" wave-left" if state == "bye" else "")
    arm_r = "arm arm-right" + (" wave-right" if state in ("welcome", "bye") else "")
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
  .bubble{{
    background:#fff;border:2px solid #C4541A;border-radius:18px;
    padding:14px 20px;font-size:13.5px;color:#C4541A;
    max-width:240px;text-align:center;line-height:1.6;
    box-shadow:0 4px 20px rgba(196,84,26,.15);
    animation:fadeUp .45s ease forwards;position:relative;
    margin-bottom:20px;font-weight:600;
  }}
  .bubble::after{{
    content:'';position:absolute;bottom:-13px;left:50%;
    transform:translateX(-50%);
    border:10px solid transparent;border-top-color:#C4541A;
  }}
  .{body_cls.split()[0]}{{display:flex;flex-direction:column;align-items:center;gap:0}}
  {'.' + body_cls.split()[1] + '{{animation:thinkBob 2s ease-in-out infinite}}' if 'think-bob' in body_cls else ''}
  .antenna-stem{{width:4px;height:22px;background:#D4AC0D;border-radius:2px;position:relative}}
  .antenna-ball{{
    width:14px;height:14px;
    background:radial-gradient(circle at 35% 35%,#F4D03F,#D4AC0D);
    border-radius:50%;position:absolute;top:-16px;left:50%;
    transform:translateX(-50%);animation:antPulse 2s infinite;
  }}
  @keyframes antPulse{{0%,100%{{box-shadow:0 0 8px rgba(212,172,13,.5)}}50%{{box-shadow:0 0 20px rgba(212,172,13,.9)}}}}
  .head{{
    width:82px;height:70px;
    background:linear-gradient(145deg,#1A1A1A,#333);
    border-radius:18px;
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;
    box-shadow:0 6px 22px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.08);
  }}
  .eyes{{display:flex;gap:17px}}
  .eye{{width:15px;height:15px;background:#fff;border-radius:50%;position:relative;animation:blink 5s infinite}}
  .eye::after{{content:'';position:absolute;width:7px;height:7px;background:#1A1A1A;border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%)}}
  @keyframes blink{{0%,88%,100%{{transform:scaleY(1)}}90%{{transform:scaleY(.1)}}}}
  .mouth{{width:28px;height:10px;border-bottom:3px solid #D4AC0D;border-radius:0 0 14px 14px;opacity:.9}}
  .mouth-bye{{width:32px;height:14px;border-bottom:3px solid #D4AC0D;border-radius:50%}}
  .torso{{display:flex;align-items:flex-start;gap:5px;margin-top:4px}}
  .body-main{{
    width:72px;height:76px;
    background:linear-gradient(145deg,#2D2D2D,#1A1A1A);
    border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 4px 16px rgba(0,0,0,.2),inset 0 1px 0 rgba(255,255,255,.06);
  }}
  .chest-led{{
    width:22px;height:22px;
    background:radial-gradient(circle at 35% 35%,#F4D03F,#D4AC0D);
    border-radius:50%;border:2.5px solid rgba(255,255,255,.4);
    animation:ledPulse 1.8s infinite;
  }}
  @keyframes ledPulse{{0%,100%{{box-shadow:0 0 0 0 rgba(212,172,13,.6)}}50%{{box-shadow:0 0 0 9px rgba(212,172,13,0)}}}}
  .arm{{width:18px;height:60px;background:linear-gradient(145deg,#2D2D2D,#1A1A1A);border-radius:9px}}
  .arm-left{{transform-origin:top center}}
  .arm-right{{transform-origin:top center}}
  .wave-right{{animation:waveR .65s ease-in-out infinite}}
  .wave-left{{animation:waveL .65s ease-in-out infinite;animation-delay:.15s}}
  @keyframes waveR{{0%,100%{{transform:rotate(-15deg)}}50%{{transform:rotate(45deg)}}}}
  @keyframes waveL{{0%,100%{{transform:rotate(15deg)}}50%{{transform:rotate(-45deg)}}}}
  .legs{{display:flex;gap:12px;margin-top:4px}}
  .leg{{width:22px;height:32px;background:linear-gradient(145deg,#2D2D2D,#1A1A1A);border-radius:0 0 10px 10px}}
  .dots span{{display:inline-block;animation:dotBounce 1.2s infinite;font-size:16px;font-weight:700;color:#C4541A}}
  .dots span:nth-child(2){{animation-delay:.2s}}
  .dots span:nth-child(3){{animation-delay:.4s}}
  @keyframes dotBounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
  @keyframes thinkBob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
  @keyframes fadeUp{{from{{opacity:0;transform:translateY(-12px)}}to{{opacity:1;transform:translateY(0)}}}}
</style></head>
<body>
  <div class="bubble">{msg}</div>
  <div class="{body_cls}">
    <div style="position:relative;display:flex;flex-direction:column;align-items:center">
      <div class="antenna-stem"><div class="antenna-ball"></div></div>
      <div class="head">
        <div class="eyes"><div class="eye"></div><div class="eye"></div></div>
        <div class="{mouth_cls}"></div>
      </div>
      <div class="torso">
        <div class="{arm_l}"></div>
        <div class="body-main"><div class="chest-led"></div></div>
        <div class="{arm_r}"></div>
      </div>
      <div class="legs"><div class="leg"></div><div class="leg"></div></div>
    </div>
  </div>
</body></html>"""


# ── KFP Footer ────────────────────────────────────────────────────────────────
def _footer_html() -> str:
    """Kung Fu Panda themed footer — lazy panda on left, active on right."""
    return """
<div style="
  display:flex;align-items:center;justify-content:center;gap:2.5rem;
  padding:1.2rem 1rem 0.6rem;margin-top:2.8rem;
  border-top:2px dashed #D4AC0D;
  font-family:'Segoe UI',system-ui,sans-serif;
">
  <!-- Lazy / sleeping panda (left) -->
  <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
    <div style="font-size:2.8rem;animation:snoozeBob 3s ease-in-out infinite">🐼</div>
    <div style="font-size:0.72rem;color:#94A3B8;font-style:italic">Yesterday…</div>
  </div>

  <!-- Centre text -->
  <div style="text-align:center;">
    <div style="font-size:0.95rem;font-weight:800;
      background:linear-gradient(135deg,#D4AC0D,#C4541A);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      🐼 Learn It Here
    </div>
    <div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">
      From lazy scrolling to legendary skills ✨
    </div>
  </div>

  <!-- Active / kung-fu panda (right) -->
  <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
    <div style="font-size:2.8rem;animation:kungFuKick 1.4s ease-in-out infinite">🥋</div>
    <div style="font-size:0.72rem;color:#C4541A;font-weight:700">Today! 💪</div>
  </div>
</div>

<style>
  @keyframes snoozeBob{0%,100%{transform:rotate(-8deg) translateY(0)}50%{transform:rotate(8deg) translateY(-4px)}}
  @keyframes kungFuKick{0%,100%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-15deg) scale(1.1)}75%{transform:rotate(15deg) scale(1.1)}}
</style>
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
  <div>
    <div class="kfp-nav-title">Learn It Here</div>
    <div style="font-size:0.72rem;color:#94A3B8;">Your developer learning hub</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([55, 45], gap="large")

    with col_left:
        st.markdown(
            """
<div class="hero-title">
  Your <span>one-stop guide</span><br>for project developers
</div>
<div class="hero-sub">
  Whether you're kicking off a new project or want to sharpen your skills —
  this is the place. Fill your project requirements to get a reference PDF,
  or jump straight into our tech guides.
</div>
""",
            unsafe_allow_html=True,
        )

        # Workflow steps
        steps = [
            ("📋", "Fill Project Requirements",
             "Answer 12 quick questions about your tech stack and download a shareable PDF reference document."),
            ("🔧", "Learn GIT",
             "Understand version control workflows, supported platforms (GitHub, Azure DevOps, Bitbucket, GitLab) and daily commands with VS IDE."),
            ("💻", "Master Visual Studio IDE",
             "Unlock productivity features: Paste JSON as Classes, Quick Actions, IntelliSense, and the best settings."),
            ("📝", "Level up with VS Code",
             "Lightweight but powerful — extensions, multi-cursor editing, integrated terminal and the shortcuts that save hours."),
        ]
        for icon, title, desc in steps:
            st.markdown(
                f"""<div class="wf-step">
  <div class="wf-step-icon">{icon}</div>
  <div class="wf-step-text"><strong>{title}</strong><p>{desc}</p></div>
</div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        btn_col1, btn_col2 = st.columns(2, gap="medium")
        with btn_col1:
            if st.button(
                "📋 Fill Project Requirements",
                type="primary",
                use_container_width=True,
            ):
                _nav_to("requirements")
        with btn_col2:
            if st.button(
                "🎓 Learn It Here →",
                type="secondary",
                use_container_width=True,
            ):
                _nav_to("learn")

    with col_right:
        st.html(_panda_landing_html())

    st.html(_footer_html())


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
  <div>
    <div class="kfp-nav-title">Learn It Here</div>
    <div style="font-size:0.72rem;color:#94A3B8;">Project Requirements</div>
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
                    file_name=f"project_requirements_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
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
        st.html(_footer_html())
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
                "submitted_at":    datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
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

    st.html(_footer_html())


# ── Learning Hub Page ─────────────────────────────────────────────────────────
def page_learn():
    """Tabbed learning hub: GIT | Visual Studio IDE | VS Code."""
    # Nav bar
    st.markdown(
        """
<div class="kfp-nav">
  <span class="kfp-nav-logo">🐼</span>
  <div>
    <div class="kfp-nav-title">Learn It Here</div>
    <div style="font-size:0.72rem;color:#94A3B8;">Developer Learning Hub</div>
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

    st.html(_footer_html())


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
