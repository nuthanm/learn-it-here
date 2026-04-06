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
    "page": "landing",              # "landing" | "requirements" | "learn"
    "animation_state": "welcome",
    "submitted": False,
    "pdf_bytes": None,
    "interacted": False,
    "learn_section": "GIT",         # active learn-hub section
    "learn_banner_dismissed": False, # new-topic banner dismissed this session
}

# ── Learn-hub menu definitions ─────────────────────────────────────────────────
# To add a new menu item, append to this list and update LATEST_NEW_TOPIC.
LEARN_MENU_ITEMS = ["GIT", "Visual Studio IDE", "VS Code", "EF Core + Oracle", ".NET", "Unit Testing", "LINQ", "Blazor", "C#", "Topic Suggestions"]
# LATEST_NEW_TOPIC is the item that triggers the "new menu" banner.
# Update this string whenever a brand-new item is added to LEARN_MENU_ITEMS.
LATEST_NEW_TOPIC = "Topic Suggestions"
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Logo-click navigation (query param set by the clickable logo anchor) ──────
if st.query_params.get("go") == "home":
    del st.query_params["go"]
    if st.session_state.get("page") != "landing":
        st.session_state.page = "landing"
        st.rerun()


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
  html, body { width: 100% !important; min-height: 100% !important; overflow-y: auto !important; }
  /* Override Streamlit's default blue theme root fully */
  .stApp,
  .st-emotion-cache-1nryt4l,
  [data-testid="stAppViewContainer"],
  .stMain,
  [data-testid="stMain"] {
    background: #F8F8F8 !important;
    color: #1A1A1A !important;
    overflow-y: auto !important;
  }
  [data-testid="stHeader"] { background: transparent !important; pointer-events: none !important; }
  .block-container {
    padding-top: 0.2rem !important;
    padding-bottom: 0.2rem !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }

  .stAppToolbar { display: none !important; }
  [class*="terminalButton"] { display: none !important; }
  /* ─ Top nav bar ─ */
  .kfp-nav {
    display: flex; align-items: center; gap: 1.2rem;
    padding: 0.3rem 0; margin-bottom: 0;
    background: transparent;
    justify-content: flex-start;
    flex-wrap: wrap;
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
  .kfp-nav-brand {
    display: flex; align-items: center; gap: 1.2rem;
    text-decoration: none; cursor: pointer;
  }
  .kfp-nav-brand, .kfp-nav-brand * { text-decoration: none !important; }
  .kfp-nav-brand:hover .kfp-nav-title { opacity: 0.75; }
  .kfp-nav-brand:hover .kfp-nav-logo  { opacity: 0.88; }

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
    margin-bottom: 1.4rem;
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
    border-left: 4px solid rgb(64, 145, 108) !important;
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
    background: #1A1A1A !important; color: #74C69D;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto; white-space: pre-wrap;
    position: relative;
  }
  .cmd-comment { color: #888888; font-style: italic; }

  /* ─ Settings / JSON blocks — deep panda black ─ */
  .json-block {
    background: #0D0D0D !important; color: #B7E4C7;
    border-radius: 12px; padding: 1.1rem 1.5rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.86rem; margin: 0.6rem 0; line-height: 1.9;
    overflow-x: auto; white-space: pre-wrap;
    position: relative;
  }

  /* ─ Code block copy button ─ */
  .copy-code-btn {
    position: absolute; top: 0.5rem; right: 0.5rem;
    background: rgba(45,106,79,0.88); color: #FFFFFF;
    border: none; border-radius: 6px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem; font-weight: 700;
    cursor: pointer; transition: background 0.2s, opacity 0.2s;
    font-family: 'Segoe UI', system-ui, sans-serif;
    z-index: 10; opacity: 0.75;
  }
  .copy-code-btn:hover { background: rgba(45,106,79,1); opacity: 1; }
  .copy-code-btn.copied { background: rgba(26,26,26,0.9); opacity: 1; }

  /* ─ Requirements form card ─ */
  .form-card {
    background: #FFFFFF; border-radius: 18px;
    padding: 2rem 2.2rem; border: 1px solid #D0D0D0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }
  .app-title   { font-size: 1.9rem; font-weight: 700; color: #1A1A1A; margin-bottom: 0.2rem; }
  .app-subtitle { font-size: 0.92rem; color: #555555; margin-bottom: 1.8rem; }
  .q-label {
    font-size: 0.93rem; font-weight: 600; color: #1A1A1A;
    margin-top: 0.5rem; margin-bottom: 0.25rem;
  }
  .q-hint {
    font-size: 0.76rem; color: #888888; margin-bottom: 0.5rem; font-style: italic;
  }
  .section-label {
    font-size: 0.7rem; font-weight: 700; color: #40916C;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-top: 1.6rem; margin-bottom: 0.4rem;
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
    padding-bottom: 30px !important;
  }
  /* ─ Tighter global spacing ─ */
  .stVerticalBlock { gap: 0.25rem !important; }
  /* ─ Reduce motion for accessibility ─ */
  @media (prefers-reduced-motion: reduce) {
    .wf-step, .content-card, .kfp-nav { transition: none !important; }
    .hero-bar { animation: none !important; }
    .hero-eyebrow, .hero-headline, .hero-sub, .hero-stats { animation: none !important; opacity: 1 !important; }
  }

  /* ─ Learn-hub sidebar navigation ─ */
  .learn-sidebar {
    background: transparent;
    overflow: hidden;
  }
  /* "Topics" heading — visible on desktop, hidden on mobile */
  .topics-heading {
    font-size: 0.82rem; font-weight: 800; letter-spacing: 1.5px;
    text-transform: uppercase; color: #888888;
    background: transparent;
    padding: 0.25rem 1rem 0.25rem;
    border: none;
    margin: 0;
    line-height: 1.6;
  }
  /* Sidebar separator between topic list and action buttons */
  .sidebar-divider {
    border: none; border-top: 1px solid #E5E5E5;
    margin: 0.5rem 0 0.4rem;
  }
  /* Style st.radio inside the sidebar to look like a vertical nav list */
  div[data-testid="stRadio"] > label { display: none !important; }
  div[data-testid="stRadio"] > div {
    display: flex !important; flex-direction: column !important; gap: 0 !important;
  }
  div[data-testid="stRadio"] > div > label {
    width: 100% !important;
    padding: 0.58rem 1rem !important;
    border-left: 3px solid transparent !important;
    border-top: 1px solid #F5F5F5 !important;
    border-radius: 0 !important;
    margin: 0 !important;
    cursor: pointer !important;
    transition: background .15s, border-color .15s !important;
    font-size: 0.88rem !important; font-weight: 600 !important; color: #444444 !important;
    display: flex !important; align-items: center !important;
  }
  div[data-testid="stRadio"] > div > label:first-child { border-top: none !important; }
  div[data-testid="stRadio"] > div > label:hover {
    background: #F5FAF7 !important; color: #2D6A4F !important;
    border-left-color: #74C69D !important;
  }
  /* Hide the radio circle */
  div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
  }
  /* Selected radio item */
  div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: transparent !important; color: #1A1A1A !important;
    border-left-color: #1A1A1A !important; font-weight: 700 !important;
  }
  /* Suggest topic button in sidebar */
  div[data-testid="stButton"].suggest-topic-btn > button {
    background: linear-gradient(135deg, #2D6A4F, #40916C) !important;
    color: #FFFFFF !important; border: none !important; border-radius: 8px !important;
    font-size: 0.82rem !important; font-weight: 700 !important;
    box-shadow: 0 3px 10px rgba(45,106,79,0.28) !important;
    padding: 0.55rem 0 !important;
    transition: opacity .2s !important;
  }
  div[data-testid="stButton"].suggest-topic-btn > button:hover { opacity: 0.85 !important; }

  /* ─ Breadcrumb ─ */
  .breadcrumb {
    display: flex; align-items: center; gap: 0.4rem;
    font-size: 0.8rem; color: #888888;
    padding: 0.25rem 0 0.5rem;
    flex-wrap: wrap;
    line-height: 1.6;
    margin-bottom: 1.0rem;
  }
  .breadcrumb-sep { color: #CCCCCC; }
  .breadcrumb-link { color: #2D6A4F; font-weight: 600; cursor: pointer; }
  .breadcrumb-current { color: #1A1A1A; font-weight: 700; }

  /* ─ New-topic announcement banner ─ */
  .new-topic-banner {
    display: flex; align-items: center; gap: 1rem;
    background: linear-gradient(90deg, #1A1A1A 0%, #2D6A4F 100%);
    border-radius: 10px; padding: 0.45rem 0.85rem;
    margin: 0; margin-left: auto;
    color: #FFFFFF; font-size: 0.83rem; font-weight: 600;
    box-shadow: 0 3px 12px rgba(0,0,0,0.18);
    animation: headlineIn .5s ease both;
    flex: 1 1 0; min-width: 0;
  }
  .new-topic-badge {
    display: inline-block;
    background: #FFB3BA; color: #1A1A1A;
    font-size: 0.65rem; font-weight: 800; letter-spacing: 1px;
    text-transform: uppercase; border-radius: 20px;
    padding: 2px 9px; margin-right: 8px;
  }
  .banner-dismiss-btn {
    display: inline-flex; align-items: center;
    color: #FFFFFF !important; text-decoration: none !important;
    font-size: 0.75rem; font-weight: 700; white-space: nowrap;
    padding: 0.22rem 0.65rem;
    background: transparent; border: 1px solid rgba(255,255,255,0.5); border-radius: 6px;
    margin-left: auto; flex-shrink: 0;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
    cursor: pointer; position: relative; z-index: 10;
  }
  .banner-dismiss-btn:hover {
    background: #FFB3BA !important; color: #1A1A1A !important;
    border-color: #FFB3BA !important;
    text-decoration: none !important;
  }

  /* ─ Suggest-topic dialog note ─ */
  .suggest-note {
    font-size: 0.76rem; color: #888888; font-style: italic;
    border-left: 3px solid #2D6A4F; padding: 0.5rem 0.8rem;
    background: #F5FAF7; border-radius: 0 8px 8px 0;
    margin-top: 0.6rem; line-height: 1.6;
  }

  /* ─ Hide empty Streamlit containers created by split-div pattern ─ */
  [data-testid="stMarkdownContainer"]:empty { display: none !important; }
  [data-testid="stMarkdownContainer"] > .content-card:empty,
  [data-testid="stMarkdownContainer"] > .form-card:empty { display: none !important; }
  /* Prevent Streamlit markdown wrapper from adding a white background above code blocks */
  [data-testid="stMarkdownContainer"] { background: transparent !important; }

  /* ─ Scroll-to-top / scroll-to-bottom floating buttons ─ */
  .scroll-nav-btn {
    position: fixed;
    right: 1.2rem;
    width: 2.4rem; height: 2.4rem;
    border-radius: 50%;
    background: #1A1A1A;
    color: #74C69D;
    border: 2px solid #2D6A4F;
    cursor: pointer;
    font-size: 1.2rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 3px 14px rgba(0,0,0,0.35);
    z-index: 9997;
    transition: opacity 0.2s, transform 0.15s, background 0.15s;
    opacity: 0; pointer-events: none;
    font-family: system-ui, sans-serif;
    line-height: 1;
  }
  .scroll-nav-btn.snb-visible { opacity: 0.82; pointer-events: auto; }
  .scroll-nav-btn:hover {
    opacity: 1 !important; transform: scale(1.1);
    background: #2D6A4F; color: #FFFFFF;
  }
  #snb-top { bottom: 5.6rem; }
  #snb-bot { bottom: 3.1rem; }

  /* ─ Mobile responsive ─ */
  @media (max-width: 768px) {
    /* Allow vertical scrolling */
    html, body { overflow-y: auto !important; }
    .stApp,
    [data-testid="stAppViewContainer"],
    .stMain,
    [data-testid="stMain"] { overflow-y: auto !important; }

    /* Tighter side padding */
    .block-container {
      padding-left: 0.75rem !important;
      padding-right: 0.75rem !important;
      padding-bottom: 70px !important;
    }

    /* Stack all Streamlit columns vertically */
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="stColumn"],
    [data-testid="column"] {
      width: 100% !important;
      flex: 1 1 100% !important;
      min-width: 100% !important;
    }

    /* Shrink hero headline */
    .hero-headline { font-size: 1.5rem !important; }

    /* Nav text sizing */
    .kfp-nav-title { font-size: 1.15rem !important; }
    .kfp-nav-tagline { font-size: 0.68rem !important; }
    /* Hide Topics heading in sidebar on mobile */
    .topics-heading { display: none !important; }

    /* Reduce page title */
    .app-title { font-size: 1.4rem !important; }

    /* Tighter card padding */
    .content-card { padding: 1.1rem 0.9rem !important; }
    .form-card { padding: 1.1rem 0.9rem !important; }
    .success-card { padding: 1.5rem 1rem !important; }
    .success-title { font-size: 1.25rem !important; }

    /* Shrink tab bar labels so they don't overflow */
    [data-testid="stTabs"] button {
      font-size: 0.78rem !important;
      padding: 0.4rem 0.55rem !important;
    }

    /* Single-column feature grid */
    .feature-grid { grid-template-columns: 1fr !important; }

    /* Platform badges — stack to full width */
    .platform-row { flex-direction: column !important; gap: 0.5rem !important; }
    .platform-badge { width: 100% !important; box-sizing: border-box !important; }

    /* Smaller mono blocks */
    .cmd-block, .json-block {
      font-size: 0.75rem !important;
      padding: 0.8rem 0.8rem !important;
    }

    /* Banner — stack below logo on mobile */
    .kfp-nav { flex-direction: column !important; align-items: flex-start !important; gap: 0.5rem !important; }
    .new-topic-banner { margin-left: 0 !important; margin-right: 0 !important; width: 100% !important; }

    /* Shortcut table — tighter cells */
    .shortcut-table th, .shortcut-table td {
      padding: 0.4rem 0.6rem !important;
      font-size: 0.78rem !important;
    }

    /* Footer — wrap text on small screens */
    .kfp-footer {
      flex-wrap: wrap !important;
      gap: 0.5rem !important;
      padding: 5px 0.75rem !important;
    }
    .kfp-footer > span { font-size: 0.68rem !important; }

    /* Extra bottom padding so footer doesn't cover content */
    .stMain section,
    [data-testid="stMainBlockContainer"] { padding-bottom: 70px !important; }

    /* Panda iframe: allow enough height for animation + quotes on mobile */
    iframe { max-height: 520px !important; }

    /* Scroll nav buttons — closer to edge on mobile */
    #snb-top { bottom: 6.4rem; right: 0.65rem; }
    #snb-bot { bottom: 3.9rem; right: 0.65rem; }
    .scroll-nav-btn { width: 2rem; height: 2rem; font-size: 1rem; }

    /* Learn sidebar — horizontal scrollable tab strip on mobile */
    div[data-testid="stRadio"] > div {
      flex-direction: row !important;
      flex-wrap: nowrap !important;
      overflow-x: auto !important;
      -webkit-overflow-scrolling: touch !important;
      padding-bottom: 4px !important;
      scrollbar-width: none !important;
    }
    div[data-testid="stRadio"] > div::-webkit-scrollbar { display: none !important; }
    div[data-testid="stRadio"] > div > label {
      min-width: max-content !important;
      border-left: none !important;
      border-right: 1px solid #F0F0F0 !important;
      border-top: none !important;
      border-bottom: 3px solid transparent !important;
      white-space: nowrap !important;
    }
    div[data-testid="stRadio"] > div > label:first-child {
      border-top: none !important;
    }
    div[data-testid="stRadio"] > div > label:has(input:checked) {
      background: transparent !important;
      border-left: none !important;
      border-bottom: 3px solid #1A1A1A !important;
    }

    /* Mobile menu scroll arrows — match menu item height */
    .menu-scroll-arrow {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 28px;
      height: 100%;
      border-radius: 0;
      background: rgba(248,248,248,0.95);
      color: #1A1A1A;
      border: none;
      border-bottom: 3px solid transparent;
      cursor: pointer;
      font-size: 1.1rem;
      font-weight: 700;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: none;
      transition: opacity 0.2s, background 0.15s;
      line-height: 1;
      padding: 0;
    }
    .menu-scroll-left { left: 0; box-shadow: 4px 0 8px -2px rgba(0,0,0,0.08); }
    .menu-scroll-right { right: 0; box-shadow: -4px 0 8px -2px rgba(0,0,0,0.08); }
    .menu-scroll-arrow:hover { background: #F0F0F0; }

    /* Requirements page: show robot animation column on small screens */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child:has(iframe) {
      display: block !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child:has(iframe) iframe {
      max-height: 380px !important;
    }

    /* Content cards: reduce side padding further on very small screens */
    .content-card { padding: 1rem 0.75rem !important; }
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
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<meta name="viewport" content="width=device-width, initial-scale=1">
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


# ── Sitting Panda — Waiting State (Requirements Page Right Side) ──────────────
def _sitting_panda_html() -> str:
    """Static sitting panda — same face style as landing, no animations."""
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{
    background:transparent;width:100%;height:100%;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;overflow:hidden;
    font-family:'Segoe UI',system-ui,sans-serif;
  }
</style></head>
<body>
  <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
    <!-- Speech bubble -->
    <div style="
      background:#fff;border:2.5px solid #2D6A4F;border-radius:18px;
      padding:11px 18px;font-size:13px;color:#2D6A4F;
      max-width:210px;text-align:center;line-height:1.55;
      box-shadow:0 4px 16px rgba(45,106,79,.15);
      position:relative;font-weight:600;
    ">Fill in your project<br>requirements 🐼
      <span style="position:absolute;bottom:-11px;left:50%;transform:translateX(-50%);
        border:9px solid transparent;border-top-color:#2D6A4F;"></span>
    </div>
    <!-- Sitting panda body (static) -->
    <div>
      <svg viewBox="0 0 320 420" width="220" height="300" xmlns="http://www.w3.org/2000/svg">
        <!-- Shadow -->
        <ellipse cx="160" cy="405" rx="70" ry="10" fill="#1A1A1A" opacity=".06"/>
        <!-- Body (sitting torso) -->
        <ellipse cx="160" cy="320" rx="82" ry="90" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1"/>
        <!-- Belly patch -->
        <ellipse cx="160" cy="320" rx="52" ry="60" fill="#F5F5F5"/>
        <!-- Legs (sitting, spread forward) -->
        <ellipse cx="105" cy="380" rx="38" ry="22" fill="#1A1A1A"/>
        <ellipse cx="215" cy="380" rx="38" ry="22" fill="#1A1A1A"/>
        <!-- Feet pads -->
        <ellipse cx="80"  cy="385" rx="16" ry="12" fill="#2D2D2D"/>
        <ellipse cx="240" cy="385" rx="16" ry="12" fill="#2D2D2D"/>
        <circle cx="73" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="87" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="233" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <circle cx="247" cy="382" r="4" fill="#3A3A3A" opacity=".4"/>
        <!-- Arms (resting on lap) -->
        <ellipse cx="90"  cy="305" rx="22" ry="48" fill="#1A1A1A" transform="rotate(25 90 305)"/>
        <ellipse cx="230" cy="305" rx="22" ry="48" fill="#1A1A1A" transform="rotate(-25 230 305)"/>
        <!-- Hand/paw circles on lap -->
        <circle cx="118" cy="340" r="15" fill="#1A1A1A"/>
        <circle cx="202" cy="340" r="15" fill="#1A1A1A"/>
        <!-- Paw pads -->
        <circle cx="118" cy="340" r="8" fill="#2D2D2D"/>
        <circle cx="202" cy="340" r="8" fill="#2D2D2D"/>
        <!-- Tail (static) -->
        <circle cx="248" cy="360" r="16" fill="#1A1A1A"/>

        <!-- === HEAD (same panda face as landing) === -->
        <!-- Ears -->
        <circle cx="82"  cy="84" r="42" fill="#1A1A1A"/>
        <circle cx="238" cy="84" r="42" fill="#1A1A1A"/>
        <circle cx="82"  cy="84" r="25" fill="#2D2D2D" opacity=".45"/>
        <circle cx="238" cy="84" r="25" fill="#2D2D2D" opacity=".45"/>
        <!-- Head shape -->
        <ellipse cx="160" cy="170" rx="108" ry="106" fill="#EFEFED"/>
        <ellipse cx="160" cy="168" rx="104" ry="102" fill="#FFFFFF"/>
        <!-- Cheek shading -->
        <ellipse cx="58"  cy="186" rx="18" ry="13" fill="#E8E8E6" opacity=".7"/>
        <ellipse cx="262" cy="186" rx="18" ry="13" fill="#E8E8E6" opacity=".7"/>
        <!-- Eye patches -->
        <ellipse cx="110" cy="140" rx="42" ry="38" fill="#1A1A1A" transform="rotate(-10 110 140)"/>
        <ellipse cx="210" cy="140" rx="42" ry="38" fill="#1A1A1A" transform="rotate(10 210 140)"/>
        <!-- Sclera -->
        <ellipse cx="112" cy="136" rx="24" ry="23" fill="#FFFFFF"/>
        <ellipse cx="208" cy="136" rx="24" ry="23" fill="#FFFFFF"/>
        <!-- Pupils -->
        <g>
          <circle cx="114" cy="136" r="12" fill="#1A1A1A"/>
          <circle cx="119" cy="130" r="5" fill="#FFFFFF"/>
          <circle cx="109" cy="140" r="2.5" fill="#FFFFFF" opacity=".5"/>
        </g>
        <g>
          <circle cx="206" cy="136" r="12" fill="#1A1A1A"/>
          <circle cx="211" cy="130" r="5" fill="#FFFFFF"/>
          <circle cx="201" cy="140" r="2.5" fill="#FFFFFF" opacity=".5"/>
        </g>
        <!-- Nose bridge + nose -->
        <ellipse cx="160" cy="162" rx="5.5" ry="7" fill="#E8E8E8"/>
        <ellipse cx="160" cy="175" rx="15" ry="11" fill="#1A1A1A"/>
        <ellipse cx="154" cy="172" rx="5" ry="3.5" fill="#3A3A3A" opacity=".4"/>
        <line x1="150" y1="183" x2="160" y2="189" stroke="#1A1A1A" stroke-width="2.2" stroke-linecap="round"/>
        <line x1="170" y1="183" x2="160" y2="189" stroke="#1A1A1A" stroke-width="2.2" stroke-linecap="round"/>
        <!-- Gentle smile -->
        <path d="M 118 204 Q 160 236 202 204" stroke="#1A1A1A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
        <!-- Blush -->
        <ellipse cx="76"  cy="198" rx="16" ry="10" fill="#FFB3BA" opacity=".4"/>
        <ellipse cx="244" cy="198" rx="16" ry="10" fill="#FFB3BA" opacity=".4"/>
      </svg>
    </div>
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


def _scroll_nav_html() -> str:
    """Return a full HTML document for components.html(height=0).

    Creates scroll-to-top / scroll-to-bottom buttons directly in the parent
    Streamlit page via ``window.parent.document`` so that ``position:fixed``
    is anchored to the viewport and the panda-theme CSS classes apply.
    Also creates mobile menu scroll arrows for horizontal radio strips.
    """
    return """<!DOCTYPE html>
<html>
<head>
<style>html,body{margin:0;padding:0;height:0;overflow:hidden;background:transparent}</style>
</head>
<body>
<script>
(function(){
  var pdoc = window.parent ? window.parent.document : document;
  var pwin = window.parent ? window.parent : window;

  /* ── Scroll-to-top / scroll-to-bottom buttons ── */
  function getOrCreate(id, content, bottom) {
    var btn = pdoc.getElementById(id);
    if (!btn) {
      btn = pdoc.createElement('button');
      btn.id = id;
      btn.type = 'button';
      btn.className = 'scroll-nav-btn';
      btn.title = id === 'snb-top' ? 'Scroll to top' : 'Scroll to bottom';
      btn.setAttribute('aria-label', btn.title);
      btn.innerHTML = content;
      btn.style.bottom = bottom;
      pdoc.body.appendChild(btn);
    }
    return btn;
  }

  var topBtn = getOrCreate('snb-top', '&#8679;', '5.6rem');
  var botBtn = getOrCreate('snb-bot', '&#8681;', '3.1rem');

  function findScrollEl() {
    var candidates = [
      pdoc.querySelector('[data-testid="stMain"]'),
      pdoc.querySelector('section.stMain'),
      pdoc.querySelector('section.main')
    ];
    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      if (el && el.scrollHeight > el.clientHeight + 10) return el;
    }
    /* Return first existing candidate even if not yet scrollable */
    for (var j = 0; j < candidates.length; j++) {
      if (candidates[j]) return candidates[j];
    }
    return pdoc.documentElement;
  }

  function getScrollTop(el) {
    return el === pdoc.documentElement
      ? (pwin.pageYOffset || pwin.scrollY || el.scrollTop || 0)
      : (el.scrollTop || 0);
  }

  function getClientHeight(el) {
    return el === pdoc.documentElement
      ? (pwin.innerHeight || el.clientHeight || 0)
      : (el.clientHeight || 0);
  }

  function update() {
    var el = findScrollEl();
    var st = getScrollTop(el);
    var sh = el.scrollHeight || 0;
    var ch = getClientHeight(el);
    topBtn.classList.toggle('snb-visible', st > 80);
    botBtn.classList.toggle('snb-visible', st + ch < sh - 80);
  }

  function scrollPage(top) {
    var el = findScrollEl();
    var opts = {top: top, behavior: 'smooth'};
    if (el === pdoc.documentElement) {
      try { pwin.scrollTo(opts); } catch(e) { pdoc.documentElement.scrollTop = top; pdoc.body.scrollTop = top; }
    } else {
      try { el.scrollTo(opts); } catch(e) { el.scrollTop = top; }
    }
  }

  /* Replace buttons with fresh clones to clear any stale listeners */
  function refreshBtn(old) {
    var fresh = old.cloneNode(true);
    if (old.parentNode) {
      try { old.parentNode.replaceChild(fresh, old); } catch(e) { /* node removed by React re-render */ }
    }
    return fresh;
  }
  topBtn = refreshBtn(topBtn);
  botBtn = refreshBtn(botBtn);

  topBtn.addEventListener('click', function() { scrollPage(0); });
  botBtn.addEventListener('click', function() {
    var el = findScrollEl();
    scrollPage(el.scrollHeight - getClientHeight(el));
  });

  /* Attach scroll listeners broadly to catch all possible containers */
  var _listeningEls = {};
  function attachScrollListeners() {
    var el = findScrollEl();
    var elId = el.getAttribute('data-testid') || el.tagName || 'root';
    if (!_listeningEls[elId]) {
      el.addEventListener('scroll', update, {passive: true});
      _listeningEls[elId] = true;
    }
  }
  attachScrollListeners();
  pwin.addEventListener('scroll', update, {passive: true});
  update();

  /* Re-check periodically in case content loads late */
  var _retries = 0;
  var _interval = setInterval(function() {
    attachScrollListeners();
    update();
    _retries++;
    if (_retries > 15) clearInterval(_interval);
  }, 1000);

  /* Also watch for DOM changes */
  var _snbDebounce;
  var _snbObserver = new MutationObserver(function() {
    clearTimeout(_snbDebounce);
    _snbDebounce = setTimeout(function() {
      attachScrollListeners();
      update();
    }, 300);
  });
  _snbObserver.observe(pdoc.body, { childList: true, subtree: true });

  /* ── Mobile menu scroll arrows ── */
  function setupMenuArrows() {
    if (pwin.innerWidth > 768) return;
    var radioContainers = pdoc.querySelectorAll('div[data-testid="stRadio"]');
    radioContainers.forEach(function(radio) {
      var stripDiv = radio.querySelector(':scope > div:last-child');
      if (!stripDiv || stripDiv.dataset.arrowsSetup) return;
      stripDiv.dataset.arrowsSetup = '1';

      var wrapper = radio;
      wrapper.style.position = 'relative';

      function makeArrow(dir) {
        var a = pdoc.createElement('button');
        a.type = 'button';
        a.className = 'menu-scroll-arrow menu-scroll-' + dir;
        a.innerHTML = dir === 'left' ? '&#8249;' : '&#8250;';
        a.setAttribute('aria-label', 'Scroll menu ' + dir);
        a.style.display = 'none';
        wrapper.appendChild(a);
        return a;
      }

      var arrowL = makeArrow('left');
      var arrowR = makeArrow('right');

      function updateArrows() {
        var sl = stripDiv.scrollLeft;
        var sw = stripDiv.scrollWidth;
        var cw = stripDiv.clientWidth;
        if (sw <= cw + 5) {
          arrowL.style.display = 'none';
          arrowR.style.display = 'none';
          return;
        }
        arrowL.style.display = sl > 5 ? 'flex' : 'none';
        arrowR.style.display = sl + cw < sw - 5 ? 'flex' : 'none';
      }

      arrowL.addEventListener('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        stripDiv.scrollBy({ left: -140, behavior: 'smooth' });
      });
      arrowR.addEventListener('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        stripDiv.scrollBy({ left: 140, behavior: 'smooth' });
      });

      stripDiv.addEventListener('scroll', updateArrows, { passive: true });
      updateArrows();
      setTimeout(updateArrows, 500);
    });
  }

  setupMenuArrows();
  var _maDebounce;
  var _maObserver = new MutationObserver(function() {
    clearTimeout(_maDebounce);
    _maDebounce = setTimeout(setupMenuArrows, 300);
  });
  _maObserver.observe(pdoc.body, { childList: true, subtree: true });

  /* Re-run on resize so arrows appear when switching to mobile resolution */
  var _maResizeDebounce;
  pwin.addEventListener('resize', function() {
    clearTimeout(_maResizeDebounce);
    _maResizeDebounce = setTimeout(function() {
      /* Reset arrows setup flags so they can be re-created */
      var radios = pdoc.querySelectorAll('div[data-testid="stRadio"]');
      radios.forEach(function(radio) {
        var stripDiv = radio.querySelector(':scope > div:last-child');
        if (stripDiv) {
          /* Remove existing arrows if switching to desktop */
          if (pwin.innerWidth > 768) {
            radio.querySelectorAll('.menu-scroll-arrow').forEach(function(a) { a.remove(); });
            delete stripDiv.dataset.arrowsSetup;
          } else {
            /* If switching to mobile and not yet set up */
            if (!stripDiv.dataset.arrowsSetup) {
              setupMenuArrows();
            }
          }
        }
      });
      if (pwin.innerWidth <= 768) setupMenuArrows();
    }, 250);
  });

})();
</script>
</body>
</html>
"""


def _copy_buttons_html() -> str:
    """Return a full HTML document for components.html(height=0).

    Injects a 'Copy' button into every ``.cmd-block`` and ``.json-block``
    in the parent Streamlit page via ``window.parent.document``. A
    MutationObserver re-runs the injection whenever Streamlit re-renders.
    """
    return """<!DOCTYPE html>
<html>
<head>
<style>html,body{margin:0;padding:0;height:0;overflow:hidden;background:transparent}</style>
</head>
<body>
<script>
(function(){
  var pdoc = window.parent ? window.parent.document : document;

  /* Strip the leading blank line and trailing whitespace that appear when
     <div class="cmd-block"> content starts/ends on its own line in the HTML
     source. Only div elements need this — <pre> blocks are already clean. */
  function trimBlockContent(block) {
    if (block.dataset.contentTrimmed || block.tagName.toLowerCase() !== 'div') return;
    block.dataset.contentTrimmed = '1';
    var fc = block.firstChild;
    if (fc && fc.nodeType === 3 && fc.nodeValue.charAt(0) === '\\n') {
      fc.nodeValue = fc.nodeValue.slice(1);
      if (!fc.nodeValue) { block.removeChild(fc); }
    }
    var lc = block.lastChild;
    if (lc && lc.nodeType === 3) {
      lc.nodeValue = lc.nodeValue.trimEnd ? lc.nodeValue.trimEnd() : lc.nodeValue;
      if (!lc.nodeValue) { block.removeChild(lc); }
    }
  }

  function addCopyButtons() {
    pdoc.querySelectorAll('.cmd-block, .json-block').forEach(function(block) {
      trimBlockContent(block);
      /* Skip blocks that already have a copy button injected. */
      if (block.querySelector('.copy-code-btn')) return;
      var btn = pdoc.createElement('button');
      btn.className = 'copy-code-btn';
      btn.textContent = 'Copy';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Copy code');
      btn.addEventListener('click', function() {
        /* Clone the block and strip the injected button before reading text. */
        var clone = block.cloneNode(true);
        var btnClone = clone.querySelector('.copy-code-btn');
        if (btnClone) { btnClone.parentNode.removeChild(btnClone); }
        var text = clone.innerText || clone.textContent || '';
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function() {
            btn.textContent = 'Copied!';
            btn.classList.add('copied');
            setTimeout(function() { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
          }).catch(function() { fallbackCopy(text, btn); });
        } else {
          fallbackCopy(text, btn);
        }
      });
      /* Append the button directly inside the code block.
         The block already has position:relative via CSS so the button
         is positioned with position:absolute at top/right. This avoids
         rearranging React-managed DOM nodes (which caused NotFoundError). */
      block.appendChild(btn);
    });
  }

  function fallbackCopy(text, btn) {
    var ta = pdoc.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
    pdoc.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { pdoc.execCommand('copy'); } catch(e) {}
    pdoc.body.removeChild(ta);
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
  }

  addCopyButtons();

  var debounceTimer;
  var observer = new MutationObserver(function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(addCopyButtons, 300); /* 300ms gives React time to finish re-rendering */
  });
  observer.observe(pdoc.body, { childList: true, subtree: true });
})();
</script>
</body>
</html>
"""



def _safe(text) -> str:
    """Strip characters outside Latin-1 for built-in PDF fonts."""
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


def generate_pdf(data: dict) -> bytes:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos

    FIELDS = [
        ("version_control",   "1. Version Control"),
        ("ide",               "2. IDE / Editor"),
        ("code_push",         "3. How Do You Push the Code?"),
        ("deployment",        "4. Deployment Approaches"),
        ("architecture",      "5. Architecture Patterns"),
        ("design_patterns",   "6. Design Patterns"),
        ("orm",               "7. ORM"),
        ("additional_requirements", "8. Additional Requirements"),
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
    pdf.cell(0, 10, "Learn It Here - Project Requirements", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
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


def _get_supabase_client():
    """Return a Supabase client or None if credentials are not configured."""
    try:
        url = st.secrets.get("SUPABASE_URL", "") or os.getenv("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "") or os.getenv("SUPABASE_KEY", "")
    except Exception:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None
    from supabase import create_client
    return create_client(url, key)


def save_topic_suggestion(topic: str) -> tuple:
    """Insert a topic suggestion into Supabase. Returns (success: bool, message: str)."""
    client = _get_supabase_client()
    if client is None:
        return (
            False,
            "Supabase credentials not configured — suggestion was not saved to the database.",
        )
    try:
        client.table("topic_suggestions").insert({"topic": topic.strip()}).execute()
        return True, "Suggestion saved successfully."
    except Exception as exc:
        return False, f"Database error: {exc}"


def fetch_topic_suggestions() -> list:
    """Fetch all topic suggestions from Supabase. Returns a list of dicts."""
    client = _get_supabase_client()
    if client is None:
        return []
    try:
        response = client.table("topic_suggestions").select("topic").execute()
        return response.data or []
    except Exception:
        return []


# ── Landing Page ──────────────────────────────────────────────────────────────
def page_landing():
    """Full-width hero landing page with Po animation and two CTAs."""
    # Disable scroll on desktop only (≥1024 px); allow scroll on mobile/tablet
    st.markdown(
        """
<style>
  @media (min-width: 1024px) {
    html, body { overflow: hidden !important; }
    .stApp,
    .st-emotion-cache-1nryt4l,
    [data-testid="stAppViewContainer"],
    .stMain,
    [data-testid="stMain"] { overflow: hidden !important; }
  }
  @media (max-width: 1023px) {
    html, body { overflow-y: auto !important; height: auto !important; min-height: 100% !important; }
    .stApp,
    [data-testid="stAppViewContainer"],
    .stMain,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] { overflow-y: auto !important; height: auto !important; }
  }
</style>
""",
        unsafe_allow_html=True,
    )
    # Top nav bar
    st.markdown(
        """
<div class="kfp-nav">
  <a href="?go=home" target="_self" class="kfp-nav-brand">
    <span class="kfp-nav-logo">🐼</span>
    <div class="kfp-nav-text">
      <div class="kfp-nav-title">Learn It Here</div>
      <div class="kfp-nav-tagline">Hub to learn most important topics</div>
    </div>
  </a>
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
      <span>7 targeted questions that define your exact project context and tech stack</span>
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

        bc1, bc2 = st.columns(2, gap="medium")
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
    components.html(_scroll_nav_html(), height=0)


# ── Requirements Page ─────────────────────────────────────────────────────────
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
                    st.session_state.page = "learn"
                    st.rerun()
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
@st.dialog("Add Your Suggested Topic")
def _suggest_topic_dialog():
    st.markdown(
        "Share your idea and we'll consider adding it to the learning hub.",
    )
    topic = st.text_area(
        "What topic would you like to learn about?",
        placeholder="e.g. Docker & Kubernetes, CI/CD Pipelines, Azure Services...",
        height=130,
    )

    db_available = _get_supabase_client() is not None
    if db_available:
        note_text = (
            "<strong>Note:</strong> Suggested topics will be reviewed by our team. "
            "Topics with the most requests will be featured in the "
            "<strong>Topic Suggestions</strong> section of the learning hub "
            "with <strong>#hashtag details</strong> and the number of requests received."
        )
    else:
        note_text = (
            "<strong>Note:</strong> Suggested topics will be reviewed by our team. "
            "Persistence is currently unavailable (no database credentials configured)."
        )
    st.markdown(
        f'<div class="suggest-note">{note_text}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Submit Suggestion", type="primary", use_container_width=True):
        if topic.strip():
            ok, db_msg = save_topic_suggestion(topic)
            if ok:
                st.success("Thank you! Your suggestion has been noted.")
            else:
                st.warning(f"⚠️  Could not save your suggestion — {db_msg}")
        else:
            st.warning("Please enter a topic before submitting.")


# ── Learning Hub Page ─────────────────────────────────────────────────────────
def page_learn():
    """Sidebar learning hub: GIT | Visual Studio IDE | VS Code | EF Core + Oracle."""
    # ── Handle banner dismiss via query param ─────────────────────────────────
    if st.query_params.get("banner_dismissed") == "1":
        st.session_state.learn_banner_dismissed = True
        del st.query_params["banner_dismissed"]

    # ── Nav bar (logo + banner/breadcrumbs) ───────────────────────────────────
    section = st.session_state.get("learn_section", "GIT")

    _LOGO_HTML = """
<div class="kfp-nav">
  <a href="?go=home" target="_self" class="kfp-nav-brand">
    <span class="kfp-nav-logo">🐼</span>
    <div class="kfp-nav-text">
      <div class="kfp-nav-title">Learn It Here</div>
      <div class="kfp-nav-tagline">Developer Learning Hub</div>
    </div>
  </a>
</div>
"""
    _BC_HTML = (
        f'<div class="breadcrumb">'
        f'<span>Home</span><span class="breadcrumb-sep">›</span>'
        f'<span>Developer Learning Hub</span><span class="breadcrumb-sep">›</span>'
        f'<span class="breadcrumb-current">{section}</span>'
        f"</div>"
    )

    if not st.session_state.get("learn_banner_dismissed", False):
        # Logo + Banner on same row
        st.markdown(
            f'<div class="kfp-nav">'
            f'<a href="?go=home" target="_self" class="kfp-nav-brand">'
            f'<span class="kfp-nav-logo">🐼</span>'
            f'<div class="kfp-nav-text">'
            f'<div class="kfp-nav-title">Learn It Here</div>'
            f'<div class="kfp-nav-tagline">Developer Learning Hub</div>'
            f'</div></a>'
            f'<div class="new-topic-banner">'
            f'<span><span class="new-topic-badge">NEW</span>'
            f'<strong>{LATEST_NEW_TOPIC}</strong> has been added to the learning hub — check it out!</span>'
            f'<a href="?banner_dismissed=1" class="banner-dismiss-btn" aria-label="Dismiss banner">✕ Dismiss</a>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        # Logo only
        st.markdown(_LOGO_HTML, unsafe_allow_html=True)

    st.divider()

    # Row 2: Breadcrumb (right-aligned with content column)
    _, bc_col = st.columns([2, 8], gap="medium")
    with bc_col:
        st.markdown(_BC_HTML, unsafe_allow_html=True)

    # ── Two-column layout: sidebar (2) + content (8) ──────────────────────────
    nav_col, content_col = st.columns([2, 8], gap="medium")

    # ── Sidebar nav ───────────────────────────────────────────────────────────
    with nav_col:
        st.markdown(
            '<div class="learn-sidebar"></div>',
            unsafe_allow_html=True,
        )
        st.radio(
            "Topics",
            options=LEARN_MENU_ITEMS,
            key="learn_section",
            label_visibility="collapsed",
        )
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        if st.button(
            "Add your suggested topic",
            key="suggest_topic_btn",
            use_container_width=True,
        ):
            _suggest_topic_dialog()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Home", key="learn_back", use_container_width=True):
            _nav_to("landing")

    # ── Main content area ─────────────────────────────────────────────────────
    with content_col:
        section = st.session_state.learn_section

    # ══════════════════════════════════════════════════════════════════════════
    # GIT SECTION
    # ══════════════════════════════════════════════════════════════════════════
    with content_col:
      if section == "GIT":
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

        # Real-world example
        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Your First Day on a Team Project</div>
  <div class="card-body">
    <b>Scenario:</b> You just joined a company building an online shopping website.
    Five other developers are already working on it. Your task: <em>add a "Forgot Password" feature</em>.
    <br><br>
    Without Git, you would copy the entire project folder, make changes, and then try to manually
    merge your changes back — a nightmare when five people do this at once. Git solves this entirely.
    <br><br>
    <b>Here's exactly what you do:</b>
    <br><br>
    <b>Step 1 — Get the project onto your laptop:</b>
    <pre class="cmd-block">git clone https://github.com/mycompany/shopping-website.git
cd shopping-website</pre>
    Now you have a full copy of the project. Everyone else is working on their own copies too.
    <br><br>
    <b>Step 2 — Create your own workspace (branch) so you don't disturb others:</b>
    <pre class="cmd-block">git checkout -b feature/forgot-password</pre>
    Think of a branch like a personal notebook. Your changes go here without touching the main codebase.
    <br><br>
    <b>Step 3 — Write your code. Then save your progress:</b>
    <pre class="cmd-block">git add .
git commit -m "feat: add forgot password email flow"</pre>
    A commit is like a save point in a video game — you can always go back to it.
    <br><br>
    <b>Step 4 — Share your work with the team:</b>
    <pre class="cmd-block">git push origin feature/forgot-password</pre>
    Your branch is now on GitHub/Azure DevOps. You open a <b>Pull Request</b> and a teammate reviews it.
    After approval it gets merged into the main codebase — safely, with a full history of every change you made.
    <br><br>
    <b>Why this matters:</b> If your code breaks something, Git lets the team roll back to the last
    good state in seconds. No files are ever lost.
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
        st.markdown(
            """<div class="content-card">
<div class="card-title">⌨️ Commands We Use Regularly</div>
<div class="card-body">These are the commands you'll run day-to-day — from getting the repo to pushing your work back up.</div>
<div class="card-section-title">Starting Out</div>
<div class="cmd-block">
<span class="cmd-comment"># Clone the repository to your local machine</span>
git clone https://github.com/your-org/your-repo.git
&#8203;
<span class="cmd-comment"># Navigate into the project folder</span>
cd your-repo
&#8203;
<span class="cmd-comment"># Check current branch and status</span>
git status
git branch
</div>
<div class="card-section-title">Daily Workflow</div>
<div class="cmd-block">
<span class="cmd-comment"># Always pull latest changes before starting work</span>
git fetch origin
git pull origin main
&#8203;
<span class="cmd-comment"># Create and switch to a new feature branch</span>
git checkout -b feature/my-feature-name
&#8203;
<span class="cmd-comment"># See what has changed</span>
git status
git diff
&#8203;
<span class="cmd-comment"># Stage your changes (all files, or a specific file)</span>
git add .
git add src/MyFile.cs
&#8203;
<span class="cmd-comment"># Commit with a clear message</span>
git commit -m "feat: add user login endpoint"
&#8203;
<span class="cmd-comment"># Push your branch to the remote</span>
git push origin feature/my-feature-name
</div>
<div class="card-section-title">Keeping Your Branch Up to Date</div>
<div class="cmd-block">
<span class="cmd-comment"># Option 1: Rebase on main (keeps history clean — preferred)</span>
git fetch origin
git rebase origin/main
&#8203;
<span class="cmd-comment"># Option 2: Merge main into your branch</span>
git merge origin/main
&#8203;
<span class="cmd-comment"># Undo staged changes (before commit)</span>
git reset HEAD src/MyFile.cs
&#8203;
<span class="cmd-comment"># Temporarily stash unfinished work and come back later</span>
git stash
git stash pop
</div>
<div class="card-section-title">Useful Inspection Commands</div>
<div class="cmd-block">
<span class="cmd-comment"># Last 10 commits on current branch</span>
git log --oneline -10
&#8203;
<span class="cmd-comment"># See changes between your branch and main</span>
git diff main..HEAD
&#8203;
<span class="cmd-comment"># Show all local and remote branches</span>
git branch -a
&#8203;
<span class="cmd-comment"># Delete a local branch after merging</span>
git branch -d feature/my-feature-name
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Real-world Git scenario
        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Fixing a Bug While Someone Else Adds a Feature</div>
  <div class="card-body">
    <b>Scenario:</b> Your teammate Alice is adding a new payment page. At the same time,
    your manager calls and says "the login button is broken in production — fix it NOW!"
    <br><br>
    You don't want to disturb Alice's half-finished payment work. Here's how Git handles this perfectly:
    <br><br>
    <b>1. Get the very latest code:</b>
    <pre class="cmd-block">git fetch origin
git pull origin main</pre>
    <b>2. Create a hotfix branch — completely separate from Alice's work:</b>
    <pre class="cmd-block">git checkout -b hotfix/login-button-not-working</pre>
    <b>3. Fix the bug in LoginController.cs, then save and share:</b>
    <pre class="cmd-block">git add src/Controllers/LoginController.cs
git commit -m "fix: login button now submits form correctly"
git push origin hotfix/login-button-not-working</pre>
    <b>4. After your hotfix is merged, get Alice's latest changes too:</b>
    <pre class="cmd-block">git fetch origin
git rebase origin/main</pre>
    Both changes are now in the main codebase — no conflicts, no overwriting each other's work.
    Git tracked every line changed by everyone, independently.
    <br><br>
    <b>Stash — save unfinished work temporarily:</b> Suppose while you were mid-way through a new
    feature your boss asks you to quickly check something on another branch. Use:
    <pre class="cmd-block">git stash          # hides your unfinished changes safely
git checkout main  # switch to another branch
# ... do the check ...
git checkout feature/my-feature
git stash pop      # bring your unfinished changes back</pre>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

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
    # VISUAL STUDIO IDE SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "Visual Studio IDE":
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

        # Real-world example — VS IDE
        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — A Typical C# Developer's Morning</div>
  <div class="card-body">
    <b>Scenario:</b> You're building a REST API for a hospital patient management system.
    A third-party lab system emails you a JSON sample of the patient data they'll send you.
    You need to create C# model classes that match it — and you have a bug to fix too.
    <br><br>
    <b>1. Generate C# classes from JSON in 10 seconds (Paste JSON as Classes):</b><br>
    You receive this JSON from the lab:
    <pre class="cmd-block">{
  "patientId": "P-1042",
  "fullName": "Jane Smith",
  "dateOfBirth": "1985-04-15",
  "testResults": [
    { "testName": "Blood Sugar", "value": 5.4, "unit": "mmol/L" }
  ]
}</pre>
    Instead of writing the C# class by hand, copy the JSON, then in Visual Studio go to:
    <b>Edit → Paste Special → Paste JSON as Classes</b>.
    Visual Studio instantly generates:
    <pre class="cmd-block">public class PatientResult
{
    public string PatientId { get; set; }
    public string FullName { get; set; }
    public string DateOfBirth { get; set; }
    public TestResult[] TestResults { get; set; }
}
public class TestResult
{
    public string TestName { get; set; }
    public float Value { get; set; }
    public string Unit { get; set; }
}</pre>
    This saves 10–15 minutes of repetitive typing on every integration.
    <br><br>
    <b>2. Quick Actions (Ctrl+.) — fix errors without looking anything up:</b><br>
    You write <code>patientService.GetById(id)</code> but <code>GetById</code> doesn't exist yet.
    The red squiggle appears. Press <b>Ctrl+.</b> → "Generate method 'GetById'" — VS creates
    the method stub in <code>PatientService.cs</code> automatically.
    <br><br>
    <b>3. Debugger — understand what's going wrong:</b><br>
    A test patient record shows the wrong age. Instead of adding <code>Console.WriteLine</code>
    everywhere, click the grey margin next to the age calculation line to set a <b>breakpoint</b>.
    Press <b>F5</b>. When the code hits that line, execution pauses and you can hover over any
    variable to see its exact value — catching the off-by-one error instantly.
    <br><br>
    <b>4. Test Explorer — run all tests with one click:</b><br>
    After fixing the age bug, open <b>View → Test Explorer</b> and click "Run All".
    All 47 unit tests finish in 3 seconds. 3 tests go red — those are the areas your fix
    might have broken. You fix them before pushing anything.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Key features
        st.markdown(
            """<div class="content-card">
<div class="card-title">⚡ Key Productivity Features</div>
<div class="feature-grid">
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
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Productivity settings
        st.markdown(
            """<div class="content-card">
<div class="card-title">⚙️ Productivity Settings Worth Configuring</div>
<div class="feature-grid">
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
</div>
</div>""",
            unsafe_allow_html=True,
        )

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
        st.markdown(
            """<div class="content-card">
<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>
<table class="shortcut-table">
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
</table>
</div>""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # VS CODE SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "VS Code":
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

        # Real-world example — VS Code
        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Daily Tasks Made Faster in VS Code</div>
  <div class="card-body">
    <b>Scenario:</b> You're a junior developer maintaining a website's front-end.
    No heavy IDE needed — VS Code is all you need. Here's how its features help you every day:
    <br><br>
    <b>1. Multi-Cursor Editing — rename the same thing in 10 places at once:</b><br>
    Your team decides to rename the CSS class <code>btn-blue</code> to <code>btn-primary</code>
    across an HTML file. Instead of using Find &amp; Replace and carefully crafting a regex pattern,
    click on <code>btn-blue</code> and press <b>Ctrl+Shift+L</b>.
    Every single occurrence gets its own cursor. Type <code>btn-primary</code> — all 10 are changed
    simultaneously in one keystroke. Done in 3 seconds.
    <br><br>
    <b>2. Integrated Terminal — no window switching:</b><br>
    You're editing a Python script and want to run it. Press <b>Ctrl+`</b>.
    A terminal opens right inside VS Code, already in the same folder as your file.
    Type <code>python script.py</code> and see the output immediately — without switching to
    a separate terminal window or losing your place in the code.
    <br><br>
    <b>3. Live Share — pair programming with a teammate in another city:</b><br>
    Your colleague in London is stuck on a bug. Instead of screen-sharing (laggy, read-only),
    install the <b>Live Share</b> extension, click "Share", and send her the link.
    She now sees your file, can edit it, and you both see each other's cursors in real time —
    just like Google Docs, but for code. No files to email, no VPN needed.
    <br><br>
    <b>4. Remote Development — edit code running on a server, from your laptop:</b><br>
    Your company's Python data pipeline runs on a Linux server. Instead of SSH-ing in and
    using <code>nano</code>, install the <b>Remote - SSH</b> extension. Connect to the server
    with one click. VS Code opens the server's files as if they were local — with full
    IntelliSense, syntax highlighting, and Git support. You edit, save, and run everything
    without leaving your laptop's comfortable setup.
    <br><br>
    <b>5. Command Palette — find any command without memorising menus:</b><br>
    Forgot how to format a JSON file? Press <b>Ctrl+Shift+P</b>, type "format", and
    "Format Document" appears instantly. Press Enter. The entire file is formatted.
    The Command Palette gives you access to literally every VS Code feature by searching for it.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Key features
        st.markdown(
            """<div class="content-card">
<div class="card-title">⚡ Key Features</div>
<div class="feature-grid">
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
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Recommended extensions
        st.markdown(
            """<div class="content-card">
<div class="card-title">🔌 Recommended Extensions</div>
<div class="feature-grid">
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
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Settings
        st.markdown(
            """<div class="content-card">
<div class="card-title">⚙️ Recommended settings.json</div>
<div class="card-body">Open with <b>Ctrl+Shift+P</b> &rarr; "Open User Settings (JSON)"</div>
<div class="json-block">{
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
}</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Shortcuts
        st.markdown(
            """<div class="content-card">
<div class="card-title">⌨️ Essential Keyboard Shortcuts</div>
<table class="shortcut-table">
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
</table>
</div>""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # EF CORE + ORACLE SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "EF Core + Oracle":
        # Overview
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🗄️ EF Core with Oracle — Overview</div>
  <div class="card-body">
    <b>Entity Framework Core (EF Core)</b> is Microsoft's modern, open-source
    object-relational mapper (ORM) for .NET. When targeting an <b>Oracle Database</b>,
    you use the official <b>Oracle.EntityFrameworkCore</b> provider maintained by Oracle
    Corporation.<br><br>
    EF Core with Oracle supports Code-First migrations, LINQ queries, stored procedures,
    sequences, and most EF Core features — with some Oracle-specific conventions that
    every team member <em>must</em> follow to keep the codebase consistent and correct.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Real-world example — EF Core + Oracle
        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🌍 Real-World Example — Building a Customer Orders System</div>
  <div class="card-body">
    <b>Scenario:</b> You're building a .NET 8 web API for an e-commerce company.
    Their database is Oracle 19c. You need to store <b>customers</b> and their <b>orders</b>.
    Here's the complete journey from zero to working code — the way it's done on a real project.
    <br><br>
    <b>Step 1 — Install the Oracle EF Core package:</b>
    <pre class="cmd-block">dotnet add package Oracle.EntityFrameworkCore</pre>
    <b>Step 2 — Define your C# entity classes (plain objects — no Oracle knowledge needed here):</b>
    <pre class="cmd-block">public class Customer
{
    public long Id { get; set; }           // maps to Oracle COLUMN "ID"
    public string FullName { get; set; }   // maps to "FULL_NAME"
    public string Email { get; set; }      // maps to "EMAIL"
    public ICollection&lt;Order&gt; Orders { get; set; }
}

public class Order
{
    public long Id { get; set; }
    public long CustomerId { get; set; }
    public decimal TotalAmount { get; set; }
    public DateTime OrderDate { get; set; }
    public Customer Customer { get; set; }
}</pre>
    <b>Step 3 — Configure the DbContext (this is where Oracle rules are applied):</b>
    <pre class="cmd-block">public class AppDbContext : DbContext
{
    public DbSet&lt;Customer&gt; Customers { get; set; }
    public DbSet&lt;Order&gt; Orders { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity&lt;Customer&gt;(b =&gt;
        {
            b.ToTable("CUSTOMERS");                        // Oracle table name MUST be UPPERCASE
            b.HasKey(e =&gt; e.Id);
            b.Property(e =&gt; e.Id)
             .HasColumnName("ID")
             .HasColumnType("NUMBER(19)")
             .UseHiLo("SEQ_CUSTOMERS");                    // Oracle sequence for auto-increment IDs
            b.Property(e =&gt; e.FullName)
             .HasColumnName("FULL_NAME")
             .HasColumnType("VARCHAR2(200)")
             .IsRequired();
            b.Property(e =&gt; e.Email)
             .HasColumnName("EMAIL")
             .HasColumnType("VARCHAR2(300)")
             .IsRequired();
        });

        modelBuilder.Entity&lt;Order&gt;(b =&gt;
        {
            b.ToTable("ORDERS");
            b.HasKey(e =&gt; e.Id);
            b.Property(e =&gt; e.Id)
             .HasColumnName("ID")
             .HasColumnType("NUMBER(19)")
             .UseHiLo("SEQ_ORDERS");
            b.Property(e =&gt; e.TotalAmount)
             .HasColumnName("TOTAL_AMOUNT")
             .HasColumnType("NUMBER(18,4)");               // Always specify precision for decimals
            b.Property(e =&gt; e.OrderDate)
             .HasColumnName("ORDER_DATE")
             .HasColumnType("TIMESTAMP");
            b.Property(e =&gt; e.CustomerId)
             .HasColumnName("CUSTOMER_ID")
             .HasColumnType("NUMBER(19)");
            b.HasOne(e =&gt; e.Customer)
             .WithMany(c =&gt; c.Orders)
             .HasForeignKey(e =&gt; e.CustomerId);
        });
    }
}</pre>
    <b>Step 4 — Create and apply the migration (this creates the Oracle tables):</b>
    <pre class="cmd-block">dotnet ef migrations add CreateCustomersAndOrders
dotnet ef database update</pre>
    EF Core generates the Oracle-compatible SQL and runs it. The tables <code>CUSTOMERS</code>
    and <code>ORDERS</code> are created in Oracle — complete with sequences and foreign keys.
    <br><br>
    <b>Step 5 — Query data in your API controller (plain C# — EF handles the Oracle SQL):</b>
    <pre class="cmd-block">// Get all orders for customer ID 42, newest first
var orders = await _context.Orders
    .Where(o =&gt; o.CustomerId == 42)
    .OrderByDescending(o =&gt; o.OrderDate)
    .ToListAsync();   // In web APIs, always prefer async DB calls to avoid blocking request threads.

// Add a new customer
var newCustomer = new Customer { FullName = "Jane Smith", Email = "jane@shop.com" };
_context.Customers.Add(newCustomer);
await _context.SaveChangesAsync();  // EF uses SEQ_CUSTOMERS to generate the ID automatically</pre>
    <b>Why Oracle-specific rules matter:</b> If you used the default lowercase table name
    <code>customers</code> instead of <code>CUSTOMERS</code>, Oracle would throw
    <em>"ORA-00942: table or view does not exist"</em> because Oracle's default behavior
    is case-sensitive with uppercase names. Following the naming conventions above prevents
    this class of runtime errors entirely.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Installation
        st.markdown(
            """<div class="content-card">
<div class="card-title">📦 NuGet Package Setup</div>
<div class="card-body">
  Install the Oracle EF Core provider that matches your EF Core version:
  <br><br>
  <b>Package Manager Console</b>
  <pre class="cmd-block">Install-Package Oracle.EntityFrameworkCore</pre>
  <b>.NET CLI</b>
  <pre class="cmd-block">dotnet add package Oracle.EntityFrameworkCore</pre>
  <b>Version alignment (mandatory standard):</b>
  <table class="shortcut-table">
    <tr><th>EF Core Version</th><th>Oracle.EntityFrameworkCore</th></tr>
    <tr><td>EF Core 9.x</td><td>9.x.x</td></tr>
    <tr><td>EF Core 8.x (LTS)</td><td>8.x.x</td></tr>
    <tr><td>EF Core 7.x</td><td>7.x.x</td></tr>
    <tr><td>EF Core 6.x (LTS)</td><td>6.x.x</td></tr>
  </table>
  Always keep EF Core and the Oracle provider on the <b>same major version</b>.
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Connection string
        st.markdown(
            """<div class="content-card">
<div class="card-title">🔌 Connection String &amp; DbContext Registration</div>
<div class="card-body">
  <b>appsettings.json</b>
  <pre class="cmd-block">{
  "ConnectionStrings": {
    "OracleDb": "User Id=myuser;Password=mypass;Data Source=myhost:1521/myservice;"
  }
}</pre>
  <b>Program.cs / Startup.cs registration (standard)</b>
  <pre class="cmd-block">builder.Services.AddDbContext&lt;AppDbContext&gt;(options =&gt;
    options.UseOracle(
        builder.Configuration.GetConnectionString("OracleDb"),
        o =&gt; o.UseOracleSQLCompatibility(OracleSQLCompatibility.DatabaseVersion19)));
</pre>
  <ul>
    <li>Always call <code>UseOracleSQLCompatibility</code> and target the correct Oracle DB version.</li>
    <li>Store connection strings in <b>app secrets / environment variables</b>, never in source control.</li>
  </ul>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Naming conventions
        st.markdown(
            """<div class="content-card">
<div class="card-title">📐 Naming Conventions (Mandatory Standards)</div>
<div class="card-body">
  Oracle historically uses <b>UPPERCASE</b> object names. Failing to follow these conventions
  causes case-sensitivity errors or "ORA-00942: table or view does not exist" at runtime.
  <table class="shortcut-table">
    <tr><th>Object</th><th>Convention</th><th>Example</th></tr>
    <tr><td>Table names</td><td>SCREAMING_SNAKE_CASE</td><td><code>CUSTOMER_ORDERS</code></td></tr>
    <tr><td>Column names</td><td>SCREAMING_SNAKE_CASE</td><td><code>ORDER_DATE</code></td></tr>
    <tr><td>Primary key column</td><td><code>ID</code></td><td><code>ID NUMBER</code></td></tr>
    <tr><td>Sequence names</td><td><code>SEQ_&lt;TABLE&gt;</code></td><td><code>SEQ_CUSTOMER_ORDERS</code></td></tr>
    <tr><td>Index names</td><td><code>IX_&lt;TABLE&gt;_&lt;COLS&gt;</code></td><td><code>IX_ORDERS_DATE</code></td></tr>
    <tr><td>Foreign key names</td><td><code>FK_&lt;TABLE&gt;_&lt;REF&gt;</code></td><td><code>FK_ORDERS_CUSTOMER</code></td></tr>
    <tr><td>Schema (owner)</td><td>UPPERCASE</td><td><code>MYSCHEMA</code></td></tr>
  </table>
  <br>Configure globally in <b>OnModelCreating</b>:
  <pre class="cmd-block">protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Apply UPPERCASE naming to every entity
    foreach (var entity in modelBuilder.Model.GetEntityTypes())
    {
        entity.SetTableName(entity.GetTableName()!.ToUpper());
        foreach (var prop in entity.GetProperties())
        {
            var colName = prop.GetColumnName();
            if (colName != null)
                prop.SetColumnName(colName.ToUpper());
        }
    }
}</pre>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Data types
        st.markdown(
            """<div class="content-card">
<div class="card-title">🔢 Oracle Data-Type Mapping Standards</div>
<div class="card-body">
  Always specify Oracle-native column types explicitly in Fluent API or Data Annotations to
  avoid provider defaults that may differ across environments.
  <table class="shortcut-table">
    <tr><th>.NET Type</th><th>Oracle Column Type</th><th>Fluent API Example</th></tr>
    <tr><td>int / long</td><td>NUMBER(10) / NUMBER(19)</td><td><code>.HasColumnType("NUMBER(10)")</code></td></tr>
    <tr><td>decimal / double</td><td>NUMBER(p,s)</td><td><code>.HasColumnType("NUMBER(18,4)")</code></td></tr>
    <tr><td>string (short)</td><td>VARCHAR2(n)</td><td><code>.HasColumnType("VARCHAR2(200)")</code></td></tr>
    <tr><td>string (long)</td><td>CLOB</td><td><code>.HasColumnType("CLOB")</code></td></tr>
    <tr><td>DateTime</td><td>TIMESTAMP</td><td><code>.HasColumnType("TIMESTAMP")</code></td></tr>
    <tr><td>DateOnly</td><td>DATE</td><td><code>.HasColumnType("DATE")</code></td></tr>
    <tr><td>bool</td><td>NUMBER(1) 0/1</td><td><code>.HasColumnType("NUMBER(1)")</code></td></tr>
    <tr><td>Guid</td><td>RAW(16)</td><td><code>.HasColumnType("RAW(16)")</code></td></tr>
    <tr><td>byte[]</td><td>BLOB</td><td><code>.HasColumnType("BLOB")</code></td></tr>
  </table>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Sequences and IDs
        st.markdown(
            """<div class="content-card">
<div class="card-title">🔑 Primary Keys &amp; Sequences (Standard)</div>
<div class="card-body">
  Oracle does not support <code>IDENTITY</code> columns in all versions.
  Use <b>Sequences</b> for auto-generated numeric PKs — this is the team standard.
  <pre class="cmd-block">// Entity
public class Order
{
    public long Id { get; set; }
    // ...
}

// Fluent API in OnModelCreating
modelBuilder.Entity&lt;Order&gt;(b =&gt;
{
    b.ToTable("ORDERS");
    b.HasKey(e =&gt; e.Id);
    b.Property(e =&gt; e.Id)
     .HasColumnName("ID")
     .HasColumnType("NUMBER(19)")
     .UseHiLo("SEQ_ORDERS");   // HiLo uses a sequence under the hood
});</pre>
  <ul>
    <li>Prefer <b>HiLo</b> pattern (<code>UseHiLo</code>) over <code>UseSequence</code> for better insert performance.</li>
    <li>Name every sequence <code>SEQ_&lt;TABLENAME&gt;</code>.</li>
    <li>For <b>GUID</b> PKs use <code>RAW(16)</code> and set <code>ValueGeneratedOnAdd</code> with a client-side <code>Guid.NewGuid()</code> default.</li>
  </ul>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Migrations
        st.markdown(
            """<div class="content-card">
<div class="card-title">🔄 Migrations — Standards &amp; Commands</div>
<div class="card-body">
  <table class="shortcut-table">
    <tr><th>Task</th><th>Command</th></tr>
    <tr><td>Add a new migration</td><td><code>dotnet ef migrations add &lt;Name&gt;</code></td></tr>
    <tr><td>Apply migrations to DB</td><td><code>dotnet ef database update</code></td></tr>
    <tr><td>Generate SQL script</td><td><code>dotnet ef migrations script --idempotent</code></td></tr>
    <tr><td>Remove last migration</td><td><code>dotnet ef migrations remove</code></td></tr>
    <tr><td>List migrations</td><td><code>dotnet ef migrations list</code></td></tr>
  </table>
  <br><b>Team Standards:</b>
  <ul>
    <li>Always review the generated migration file before applying — Oracle SQL differs from SQL Server.</li>
    <li>Use <code>--idempotent</code> scripts for DBA-applied deployments in Production.</li>
    <li>Never auto-run <code>database update</code> in Production from application startup; use controlled scripts.</li>
    <li>Keep migration names descriptive: <code>AddCustomerEmailIndex</code>, not <code>Migration1</code>.</li>
    <li>Every migration must be peer-reviewed before merging to the main branch.</li>
  </ul>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Stored Procedures
        st.markdown(
            """<div class="content-card">
<div class="card-title">⚙️ Stored Procedures &amp; Raw SQL</div>
<div class="card-body">
  <b>Calling a stored procedure:</b>
  <pre class="cmd-block">var result = await context.Database
    .ExecuteSqlRawAsync(
        "BEGIN MY_SCHEMA.UPDATE_STATUS(:p_id, :p_status); END;",
        new OracleParameter("p_id", orderId),
        new OracleParameter("p_status", newStatus));
</pre>
  <b>Mapping a procedure result to an entity:</b>
  <pre class="cmd-block">var orders = await context.Orders
    .FromSqlRaw("SELECT * FROM TABLE(MY_SCHEMA.GET_ORDERS(:p_cust))",
        new OracleParameter("p_cust", customerId))
    .ToListAsync();
</pre>
  <b>Standards:</b>
  <ul>
    <li>Always use <b>named parameters</b> (<code>:param_name</code>) — never positional.</li>
    <li>Prefix every parameter binding with <code>:</code> (Oracle syntax, not <code>@</code>).</li>
    <li>Use <code>OracleParameter</code> from <code>Oracle.ManagedDataAccess.Client</code> — never raw string interpolation (SQL injection risk).</li>
    <li>Document stored procedure signatures in the same PR as the EF mapping.</li>
  </ul>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Best practices
        st.markdown(
            """<div class="content-card">
<div class="card-title">✅ Best Practices Everyone Must Follow</div>
<div class="feature-grid">
  <div class="feature-pill">
    <strong>🔠 Always Uppercase Names</strong>
    <p>Configure table and column names as UPPERCASE in <code>OnModelCreating</code>. Never rely on default casing.</p>
  </div>
  <div class="feature-pill">
    <strong>📌 Explicit Column Types</strong>
    <p>Always specify Oracle column types in Fluent API. Never leave them implicit — defaults differ between providers.</p>
  </div>
  <div class="feature-pill">
    <strong>🧪 Test Migrations Locally</strong>
    <p>Run migrations against a local or dev Oracle instance before raising a PR. Attach the idempotent SQL script to the PR.</p>
  </div>
  <div class="feature-pill">
    <strong>🚫 No Raw String Queries</strong>
    <p>Always use parameterised queries (<code>FromSqlRaw</code> + <code>OracleParameter</code>). String interpolation in SQL is forbidden.</p>
  </div>
  <div class="feature-pill">
    <strong>⏱️ Async All the Way</strong>
    <p>Use <code>ToListAsync</code>, <code>FirstOrDefaultAsync</code>, <code>SaveChangesAsync</code>. Blocking calls on a DB thread pool are banned.</p>
  </div>
  <div class="feature-pill">
    <strong>🧹 Dispose DbContext</strong>
    <p>Always resolve <code>DbContext</code> via DI with scoped lifetime. Never create it with <code>new</code> manually.</p>
  </div>
  <div class="feature-pill">
    <strong>📏 Schema Per Module</strong>
    <p>Each bounded context or module uses its own Oracle schema. Cross-schema queries must be documented and approved.</p>
  </div>
  <div class="feature-pill">
    <strong>🔒 Secrets Out of Source</strong>
    <p>Oracle credentials belong in Azure Key Vault / environment secrets. Never hardcode in appsettings.json committed to Git.</p>
  </div>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        # Quick-reference table
        st.markdown(
            """<div class="content-card">
<div class="card-title">📋 Quick-Reference Checklist</div>
<div class="card-body">
<table class="shortcut-table">
  <tr><th>#</th><th>Standard</th><th>Why It Matters</th></tr>
  <tr><td>1</td><td>Match Oracle.EntityFrameworkCore version to EF Core version</td><td>Prevents runtime incompatibility</td></tr>
  <tr><td>2</td><td>Use UPPERCASE table &amp; column names</td><td>Avoids ORA-00942 errors</td></tr>
  <tr><td>3</td><td>Specify Oracle column types explicitly</td><td>Data integrity &amp; portability</td></tr>
  <tr><td>4</td><td>Use HiLo sequences for numeric PKs</td><td>Reduces round-trips, improves insert speed</td></tr>
  <tr><td>5</td><td>Use named Oracle parameters (:name)</td><td>Security &amp; clarity</td></tr>
  <tr><td>6</td><td>Review migration SQL before applying</td><td>Oracle DDL differs from SQL Server</td></tr>
  <tr><td>7</td><td>Never auto-migrate in Production startup</td><td>Prevents accidental data loss</td></tr>
  <tr><td>8</td><td>Use scoped DbContext via DI</td><td>Prevents connection leaks</td></tr>
  <tr><td>9</td><td>All DB calls must be async</td><td>Scalability &amp; thread-pool health</td></tr>
  <tr><td>10</td><td>Store credentials in secrets/Key Vault</td><td>Security compliance</td></tr>
</table>
</div>
</div>""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # .NET SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == ".NET":
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🟣 What is .NET? (For Complete Beginners)</div>
  <div class="card-body">
    <b>.NET</b> (pronounced "dot net") is a <em>free, open-source developer platform</em> created by
    Microsoft. Think of it as a powerful toolbox that lets you build all kinds of software —
    websites, mobile apps, desktop apps, games, cloud services, and more — using a common set
    of tools and languages (mainly <b>C#</b>, F#, and VB.NET).<br><br>
    <b>Why should you learn it?</b><br>
    ✅ Used by millions of developers worldwide<br>
    ✅ Backed by Microsoft and a huge open-source community<br>
    ✅ Runs on Windows, macOS, and Linux<br>
    ✅ Excellent performance — one of the fastest web frameworks in the world<br>
    ✅ Great job market demand<br><br>
    <b>Simple analogy:</b> If programming is like cooking, .NET is the professional kitchen
    (with all utensils, ovens, and recipes) — C# is the chef who works in that kitchen.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📜 .NET Release History &amp; Associated C# Versions</div>
  <div class="card-body">
    Every version of .NET comes paired with a version of C# — the primary language used to write .NET apps.
    Here's the full picture from the very beginning:<br><br>
    <table class="shortcut-table">
      <tr><th>.NET Version</th><th>Release Year</th><th>C# Version</th><th>Support Type</th><th>Key Highlights</th></tr>
      <tr><td>.NET Framework 1.0</td><td>2002</td><td>C# 1.0</td><td>End of Life</td><td>The very first .NET — Windows only, introduced CLR &amp; BCL</td></tr>
      <tr><td>.NET Framework 1.1</td><td>2003</td><td>C# 1.2</td><td>End of Life</td><td>Bug fixes, ASP.NET improvements</td></tr>
      <tr><td>.NET Framework 2.0</td><td>2005</td><td>C# 2.0</td><td>End of Life</td><td>Generics, anonymous methods, nullable types</td></tr>
      <tr><td>.NET Framework 3.0</td><td>2006</td><td>C# 2.0</td><td>End of Life</td><td>WPF, WCF, WF introduced</td></tr>
      <tr><td>.NET Framework 3.5</td><td>2007</td><td>C# 3.0</td><td>End of Life</td><td>LINQ, lambda expressions, extension methods</td></tr>
      <tr><td>.NET Framework 4.0</td><td>2010</td><td>C# 4.0</td><td>End of Life</td><td>TPL (Task Parallel Library), dynamic keyword</td></tr>
      <tr><td>.NET Framework 4.5</td><td>2012</td><td>C# 5.0</td><td>End of Life</td><td>async/await introduced</td></tr>
      <tr><td>.NET Framework 4.6</td><td>2015</td><td>C# 6.0</td><td>End of Life</td><td>RyuJIT compiler, string interpolation</td></tr>
      <tr><td>.NET Framework 4.7</td><td>2017</td><td>C# 7.x</td><td>End of Life</td><td>Tuples, pattern matching, local functions</td></tr>
      <tr><td>.NET Framework 4.8</td><td>2019</td><td>C# 7.3</td><td>Maintenance</td><td>Last ever .NET Framework — still supported on Windows</td></tr>
      <tr><td><b>.NET Core 1.0</b></td><td>2016</td><td>C# 6.0</td><td>End of Life</td><td>First cross-platform .NET — Linux/macOS support!</td></tr>
      <tr><td>.NET Core 2.0</td><td>2017</td><td>C# 7.1</td><td>End of Life</td><td>.NET Standard 2.0 support, massive API expansion</td></tr>
      <tr><td>.NET Core 2.1</td><td>2018</td><td>C# 7.3</td><td>End of Life</td><td>LTS release, Span&lt;T&gt;, SignalR</td></tr>
      <tr><td>.NET Core 3.0</td><td>2019</td><td>C# 8.0</td><td>End of Life</td><td>WPF/WinForms on Core, Blazor Server</td></tr>
      <tr><td>.NET Core 3.1</td><td>2019</td><td>C# 8.0</td><td>End of Life (2022)</td><td>LTS — most used Core version; gRPC support</td></tr>
      <tr><td><b>.NET 5</b></td><td>2020</td><td>C# 9.0</td><td>End of Life</td><td>Unified .NET — merged Core + Framework vision; no "Core" branding</td></tr>
      <tr><td><b>.NET 6</b></td><td>2021</td><td>C# 10.0</td><td>End of Life (2024)</td><td>LTS — minimal APIs, .NET MAUI preview, hot reload</td></tr>
      <tr><td>.NET 7</td><td>2022</td><td>C# 11.0</td><td>End of Life</td><td>STS — rate limiting, output caching, regex improvements</td></tr>
      <tr><td><b>.NET 8</b></td><td>2023</td><td>C# 12.0</td><td><b>LTS ✅ Current</b></td><td>Native AOT, Blazor United, primary constructors, collection expressions</td></tr>
      <tr><td>.NET 9</td><td>2024</td><td>C# 13.0</td><td>STS</td><td>LINQ improvements, params spans, Task.WhenEach</td></tr>
      <tr><td><b>.NET 10</b></td><td>2025 (Nov)</td><td>C# 14.0</td><td><b>LTS (Upcoming)</b></td><td>In development — next long-term support release</td></tr>
    </table>
    <br>
    <b>LTS</b> = Long-Term Support (3 years). <b>STS</b> = Standard-Term Support (18 months).
    <b>Rule of thumb:</b> Use an LTS version for production apps — currently <b>.NET 8</b>.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚖️ .NET Framework vs .NET Standard vs .NET (Core / 5+)</div>
  <div class="card-body">
    This is one of the most confusing things for beginners — three names that all say ".NET"!
    Let's break it down with plain English and a comparison table.<br><br>
    <b>Think of it this way:</b><br>
    🏠 <b>.NET Framework</b> = An old house (Windows-only, comfy but can't be moved)<br>
    📐 <b>.NET Standard</b> = A set of blueprints (a contract that different .NETs agree to follow)<br>
    🚀 <b>.NET (Core / 5+)</b> = The new modern building (cross-platform, fast, the future)<br><br>
    <table class="shortcut-table">
      <tr><th>Feature</th><th>.NET Framework</th><th>.NET Standard</th><th>.NET (Core / 5+)</th></tr>
      <tr><td>What it is</td><td>Original full Windows .NET</td><td>A specification/interface (not a runtime)</td><td>Modern, unified cross-platform .NET</td></tr>
      <tr><td>Runs on</td><td>Windows only</td><td>N/A — it's a standard, not a runtime</td><td>Windows, macOS, Linux</td></tr>
      <tr><td>Status</td><td>Maintenance (no new features)</td><td>Superseded by .NET 5+ (still used in libraries)</td><td>Active — all future development here</td></tr>
      <tr><td>Latest version</td><td>4.8.1</td><td>2.1</td><td>.NET 9 (LTS: .NET 8)</td></tr>
      <tr><td>Who should use it</td><td>Legacy apps that can't migrate</td><td>Library authors targeting multiple runtimes</td><td>Everyone building new apps</td></tr>
      <tr><td>Performance</td><td>Good</td><td>N/A</td><td>Excellent (much faster)</td></tr>
      <tr><td>Open Source</td><td>Partially</td><td>Yes</td><td>Yes (fully open source)</td></tr>
      <tr><td>WinForms / WPF</td><td>✅ Full support</td><td>❌ Not a runtime</td><td>✅ Supported since .NET Core 3.0</td></tr>
      <tr><td>ASP.NET / Web API</td><td>✅ ASP.NET 4.x</td><td>❌ Not a runtime</td><td>✅ ASP.NET Core (much faster)</td></tr>
      <tr><td>NuGet packages</td><td>Targets net4x</td><td>Targets netstandard2.x</td><td>Targets net6, net7, net8 etc.</td></tr>
    </table>
    <br>
    <b>When do you see .NET Standard today?</b> When you look at a NuGet library that says
    <code>netstandard2.0</code> — it means that library works in both .NET Framework AND .NET Core/5+.
    It's a compatibility bridge. For <em>new libraries</em>, target .NET 8 directly.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a .NET Console Program</div>
  <div class="card-body">
    Here's the simplest possible .NET program (.NET 6+ with top-level statements), with every line explained:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// File: Program.cs  — this is the entry point of your app</span>
&#8203;
<span class="cmd-comment">// 1. 'using' brings in a namespace so you can use its classes without full path</span>
using System;
&#8203;
<span class="cmd-comment">// 2. 'namespace' groups your code logically (like a folder for code)</span>
namespace MyFirstApp
{
    <span class="cmd-comment">// 3. 'class' is a blueprint for objects</span>
    class Program
    {
        <span class="cmd-comment">// 4. Main() is where your program starts running</span>
        static void Main(string[] args)
        {
            <span class="cmd-comment">// 5. Console.WriteLine prints text to the screen + newline</span>
            Console.WriteLine("Hello, .NET World! 🐼");
&#8203;
            <span class="cmd-comment">// 6. Variables store data — 'string' holds text</span>
            string name = "Developer";
            int age = 25;
&#8203;
            <span class="cmd-comment">// 7. String interpolation — $ prefix lets you embed variables</span>
            Console.WriteLine($"Name: {name}, Age: {age}");
&#8203;
            <span class="cmd-comment">// 8. Console.ReadLine() waits for user to type something</span>
            Console.Write("Press Enter to exit...");
            Console.ReadLine();
        }
    }
}
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🚀 How to Create &amp; Run Your First .NET App</div>
  <div class="card-body">
    <b>Step 1 — Install the .NET SDK:</b> Download from <a href="https://dotnet.microsoft.com/download" target="_blank">dotnet.microsoft.com/download</a><br>
    After installing, open a terminal and verify:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment"># Check .NET is installed and see the version</span>
dotnet --version
&#8203;
<span class="cmd-comment"># Create a new console application</span>
dotnet new console -n MyFirstApp
cd MyFirstApp
&#8203;
<span class="cmd-comment"># Run the app</span>
dotnet run
&#8203;
<span class="cmd-comment"># Build without running</span>
dotnet build
&#8203;
<span class="cmd-comment"># List all available project templates</span>
dotnet new list
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📋 Quick Reference — What to Use When</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>Situation</th><th>Use This</th></tr>
      <tr><td>Building a new web API or website</td><td>ASP.NET Core (.NET 8)</td></tr>
      <tr><td>Building a Windows desktop app</td><td>WPF or WinForms on .NET 8</td></tr>
      <tr><td>Building a cross-platform desktop app</td><td>.NET MAUI</td></tr>
      <tr><td>Building a browser app in C#</td><td>Blazor WebAssembly</td></tr>
      <tr><td>Maintaining an old Windows-only app</td><td>.NET Framework 4.8 (maintenance mode)</td></tr>
      <tr><td>Creating a NuGet library for broad compatibility</td><td>Target netstandard2.0 or net8</td></tr>
      <tr><td>Cloud / microservices</td><td>.NET 8 with Docker</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # UNIT TESTING SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "Unit Testing":
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🧪 What is Unit Testing? (For Complete Beginners)</div>
  <div class="card-body">
    <b>Unit testing</b> means writing small, automated pieces of code that verify a tiny,
    isolated piece (a "unit") of your application works correctly — <em>before a human ever
    clicks a button</em>.<br><br>
    <b>Think of it like this:</b> Imagine you built a calculator. A unit test would
    automatically check: "Does 2 + 2 really return 4?" — and it checks that <em>every single
    time</em> you change any code. If you accidentally break the addition logic later, the
    test immediately shouts "FAILED!" and saves you from shipping a broken calculator.<br><br>
    <b>Why should every developer write unit tests?</b><br>
    ✅ <b>Catch bugs early</b> — find problems in seconds, not in production<br>
    ✅ <b>Refactor confidently</b> — change code without fear; tests tell you if you broke something<br>
    ✅ <b>Living documentation</b> — tests show exactly how code is supposed to behave<br>
    ✅ <b>Faster debugging</b> — failing test pinpoints exactly which unit broke<br>
    ✅ <b>Required in most professional teams</b> — companies expect developers to write tests<br><br>
    <b>The 3A Pattern (Arrange-Act-Assert)</b> — Every unit test follows this structure:<br>
    🔵 <b>Arrange</b> — Set up the data and objects you need<br>
    🟢 <b>Act</b> — Call the method/function you are testing<br>
    🔴 <b>Assert</b> — Verify the result is what you expected
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚖️ xUnit vs NUnit vs MSTest — Complete Comparison</div>
  <div class="card-body">
    There are three major unit testing frameworks for .NET. All three do the same job — the
    differences are syntax, features, and community preference. Here's everything you need to know:<br><br>
    <table class="shortcut-table">
      <tr><th>Feature</th><th>xUnit</th><th>NUnit</th><th>MSTest</th></tr>
      <tr><td>Created by</td><td>James Newkirk &amp; Brad Wilson (ex-NUnit creators)</td><td>Open-source community</td><td>Microsoft</td></tr>
      <tr><td>First released</td><td>2007</td><td>2000 (oldest!)</td><td>2005</td></tr>
      <tr><td>Current version</td><td>xUnit 2.x / 3.x</td><td>NUnit 3.x / 4.x</td><td>MSTest v2 / v3</td></tr>
      <tr><td>Preferred by</td><td>.NET Core / modern teams</td><td>Enterprise / Java-background devs</td><td>Visual Studio / Microsoft teams</td></tr>
      <tr><td>Test marker attribute</td><td>[Fact] / [Theory]</td><td>[Test] / [TestCase]</td><td>[TestMethod] / [DataTestMethod]</td></tr>
      <tr><td>Test class attribute</td><td>None needed</td><td>[TestFixture]</td><td>[TestClass]</td></tr>
      <tr><td>Setup method</td><td>Constructor</td><td>[SetUp]</td><td>[TestInitialize]</td></tr>
      <tr><td>Teardown method</td><td>IDisposable.Dispose()</td><td>[TearDown]</td><td>[TestCleanup]</td></tr>
      <tr><td>One-time setup</td><td>IClassFixture&lt;T&gt;</td><td>[OneTimeSetUp]</td><td>[ClassInitialize]</td></tr>
      <tr><td>Parameterised tests</td><td>[Theory] + [InlineData]</td><td>[TestCase(...)]</td><td>[DataTestMethod] + [DataRow]</td></tr>
      <tr><td>Assertion library</td><td>Assert.Equal / Throws etc.</td><td>Assert.That / Classic Assert</td><td>Assert.AreEqual / ThrowsException</td></tr>
      <tr><td>Parallel test execution</td><td>✅ By default (per class)</td><td>✅ Configurable</td><td>⚠️ Limited (opt-in)</td></tr>
      <tr><td>IDE integration</td><td>Excellent (VS, Rider, VS Code)</td><td>Excellent</td><td>Best in Visual Studio</td></tr>
      <tr><td>dotnet test support</td><td>✅ Native</td><td>✅ Native</td><td>✅ Native</td></tr>
      <tr><td>NuGet package</td><td>xunit, xunit.runner.visualstudio</td><td>NUnit, NUnit3TestAdapter</td><td>MSTest.TestFramework, MSTest.TestAdapter</td></tr>
      <tr><td>Install template</td><td>dotnet new xunit</td><td>dotnet new nunit</td><td>dotnet new mstest</td></tr>
      <tr><td>Community popularity (2024)</td><td>🥇 Most popular in .NET Core</td><td>🥈 Very popular (esp. legacy)</td><td>🥉 Common in MS-heavy shops</td></tr>
      <tr><td>Learning curve</td><td>Easy</td><td>Easy (familiar to JUnit devs)</td><td>Easy</td></tr>
      <tr><td>Best for</td><td>New .NET projects, open-source</td><td>Teams coming from Java/JUnit</td><td>Teams deep in Visual Studio ecosystem</td></tr>
    </table>
    <br>
    <b>🏆 Bottom line for beginners:</b> Pick <b>xUnit</b> for new projects — it's the de facto
    standard in modern .NET. Use NUnit if your team already uses it or if you're from a Java
    background. Use MSTest if you're in a pure Microsoft environment.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🧮 Same Example in All Three Frameworks — Calculator Tests</div>
  <div class="card-body">
    We'll test this simple <b>Calculator</b> class in xUnit, NUnit, and MSTest — so you can see exactly
    how the same test looks in each framework. The business logic never changes, only the test attributes do.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// ── The class we are testing (Calculator.cs) — same for all three frameworks</span>
public class Calculator
{
    public int Add(int a, int b)      =&gt; a + b;
    public int Subtract(int a, int b) =&gt; a - b;
    public int Multiply(int a, int b) =&gt; a * b;
    public double Divide(int a, int b)
    {
        if (b == 0) throw new DivideByZeroException("Cannot divide by zero.");
        return (double)a / b;
    }
}
</div>
""",
            unsafe_allow_html=True,
        )

        tabs_ut = st.tabs(["xUnit", "NUnit", "MSTest"])

        with tabs_ut[0]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment">// ── XUNIT ────────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new xunit -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: xunit, xunit.runner.visualstudio, Microsoft.NET.Test.Sdk</span>
&#8203;
using Xunit;
&#8203;
public class CalculatorTests
{
    <span class="cmd-comment">// [Fact] = a single test with no parameters</span>
    [Fact]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        <span class="cmd-comment">// Arrange — set up what you need</span>
        var calc = new Calculator();
&#8203;
        <span class="cmd-comment">// Act — call the method</span>
        int result = calc.Add(2, 3);
&#8203;
        <span class="cmd-comment">// Assert — verify the result</span>
        Assert.Equal(5, result);
    }
&#8203;
    [Fact]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        var calc = new Calculator();
        int result = calc.Subtract(3, 10);
        Assert.Equal(-7, result);
    }
&#8203;
    <span class="cmd-comment">// [Theory] + [InlineData] = parameterised test — runs once per InlineData row</span>
    [Theory]
    [InlineData(2, 3,  6)]
    [InlineData(5, 4, 20)]
    [InlineData(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        var calc = new Calculator();
        Assert.Equal(expected, calc.Multiply(a, b));
    }
&#8203;
    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        var calc = new Calculator();
&#8203;
        <span class="cmd-comment">// Assert.Throws verifies that an exception IS thrown</span>
        Assert.Throws&lt;DivideByZeroException&gt;(() =&gt; calc.Divide(10, 0));
    }
&#8203;
    [Fact]
    public void Divide_TenByTwo_ReturnsFive()
    {
        var calc = new Calculator();
        double result = calc.Divide(10, 2);
        Assert.Equal(5.0, result);
    }
}
</div>
""",
                unsafe_allow_html=True,
            )

        with tabs_ut[1]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment">// ── NUNIT ────────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new nunit -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk</span>
&#8203;
using NUnit.Framework;
&#8203;
<span class="cmd-comment">// [TestFixture] marks this class as containing tests (optional in NUnit 3+)</span>
[TestFixture]
public class CalculatorTests
{
    private Calculator _calc;
&#8203;
    <span class="cmd-comment">// [SetUp] runs BEFORE each test — like a constructor for setup</span>
    [SetUp]
    public void SetUp()
    {
        _calc = new Calculator();
    }
&#8203;
    <span class="cmd-comment">// [Test] marks a single test method</span>
    [Test]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        <span class="cmd-comment">// Arrange (done in SetUp), Act, Assert</span>
        int result = _calc.Add(2, 3);
&#8203;
        <span class="cmd-comment">// Assert.That is NUnit's modern assertion syntax</span>
        Assert.That(result, Is.EqualTo(5));
    }
&#8203;
    [Test]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        int result = _calc.Subtract(3, 10);
        Assert.That(result, Is.EqualTo(-7));
    }
&#8203;
    <span class="cmd-comment">// [TestCase] = parameterised test — one attribute per set of inputs</span>
    [TestCase(2, 3,  6)]
    [TestCase(5, 4, 20)]
    [TestCase(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        Assert.That(_calc.Multiply(a, b), Is.EqualTo(expected));
    }
&#8203;
    [Test]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        <span class="cmd-comment">// Assert.Throws in NUnit</span>
        Assert.Throws&lt;DivideByZeroException&gt;(() =&gt; _calc.Divide(10, 0));
    }
&#8203;
    [Test]
    public void Divide_TenByTwo_ReturnsFive()
    {
        double result = _calc.Divide(10, 2);
        Assert.That(result, Is.EqualTo(5.0));
    }
&#8203;
    <span class="cmd-comment">// [TearDown] runs AFTER each test — for cleanup</span>
    [TearDown]
    public void TearDown()
    {
        <span class="cmd-comment">// dispose resources if needed</span>
    }
}
</div>
""",
                unsafe_allow_html=True,
            )

        with tabs_ut[2]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment">// ── MSTEST ───────────────────────────────────────────────────────</span>
<span class="cmd-comment">// Install: dotnet new mstest -n MyApp.Tests</span>
<span class="cmd-comment">// Packages: MSTest.TestFramework, MSTest.TestAdapter, Microsoft.NET.Test.Sdk</span>
&#8203;
using Microsoft.VisualStudio.TestTools.UnitTesting;
&#8203;
<span class="cmd-comment">// [TestClass] marks this class as containing tests</span>
[TestClass]
public class CalculatorTests
{
    private Calculator _calc;
&#8203;
    <span class="cmd-comment">// [TestInitialize] runs BEFORE each test</span>
    [TestInitialize]
    public void TestInitialize()
    {
        _calc = new Calculator();
    }
&#8203;
    <span class="cmd-comment">// [TestMethod] marks a single test method</span>
    [TestMethod]
    public void Add_TwoPositiveNumbers_ReturnsCorrectSum()
    {
        int result = _calc.Add(2, 3);
&#8203;
        <span class="cmd-comment">// Assert.AreEqual(expected, actual) is MSTest's style</span>
        Assert.AreEqual(5, result);
    }
&#8203;
    [TestMethod]
    public void Subtract_LargerFromSmaller_ReturnsNegative()
    {
        int result = _calc.Subtract(3, 10);
        Assert.AreEqual(-7, result);
    }
&#8203;
    <span class="cmd-comment">// [DataTestMethod] + [DataRow] = parameterised test</span>
    [DataTestMethod]
    [DataRow(2, 3,  6)]
    [DataRow(5, 4, 20)]
    [DataRow(0, 9,  0)]
    public void Multiply_ValidInputs_ReturnsProduct(int a, int b, int expected)
    {
        Assert.AreEqual(expected, _calc.Multiply(a, b));
    }
&#8203;
    [TestMethod]
    [ExpectedException(typeof(DivideByZeroException))]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        <span class="cmd-comment">// [ExpectedException] tells MSTest: this test PASSES if this exception is thrown</span>
        _calc.Divide(10, 0);
    }
&#8203;
    [TestMethod]
    public void Divide_TenByTwo_ReturnsFive()
    {
        double result = _calc.Divide(10, 2);
        Assert.AreEqual(5.0, result);
    }
&#8203;
    <span class="cmd-comment">// [TestCleanup] runs AFTER each test</span>
    [TestCleanup]
    public void TestCleanup()
    {
        <span class="cmd-comment">// cleanup resources if needed</span>
    }
}
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">▶️ How to Run Your Tests</div>
  <div class="card-body">
    All three frameworks work with the same CLI commands:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment"># Run all tests in the project</span>
dotnet test
&#8203;
<span class="cmd-comment"># Run with verbose output to see each test name</span>
dotnet test --verbosity normal
&#8203;
<span class="cmd-comment"># Run only tests whose name contains a keyword</span>
dotnet test --filter "Add"
&#8203;
<span class="cmd-comment"># Run tests in a specific file/class</span>
dotnet test --filter "FullyQualifiedName~CalculatorTests"
&#8203;
<span class="cmd-comment"># Generate a test results report (TRX format)</span>
dotnet test --logger "trx;LogFileName=TestResults.trx"
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📋 Unit Testing Quick Reference &amp; Best Practices</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>#</th><th>Practice</th><th>Why It Matters</th></tr>
      <tr><td>1</td><td>Name tests as: MethodName_Scenario_ExpectedResult</td><td>Instantly clear what failed and why</td></tr>
      <tr><td>2</td><td>One assertion per test (ideally)</td><td>Pinpoints exactly what broke</td></tr>
      <tr><td>3</td><td>Never test framework code (string.Length, DateTime.Now)</td><td>You trust the framework; test YOUR logic</td></tr>
      <tr><td>4</td><td>Use mocks for external dependencies (DB, API, file system)</td><td>Tests stay fast and isolated</td></tr>
      <tr><td>5</td><td>Keep tests independent — no shared state between tests</td><td>Test order should never matter</td></tr>
      <tr><td>6</td><td>Aim for 80%+ code coverage on business logic</td><td>Good safety net for refactoring</td></tr>
      <tr><td>7</td><td>Run tests on every commit (CI/CD)</td><td>Catch breaks before they reach main branch</td></tr>
      <tr><td>8</td><td>Tests should be FAST (milliseconds each)</td><td>Slow tests get skipped</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # LINQ SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "LINQ":
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔍 What is LINQ? (For Complete Beginners)</div>
  <div class="card-body">
    <b>LINQ</b> stands for <b>Language Integrated Query</b>. It's a powerful C# feature that lets
    you query and manipulate collections of data (lists, arrays, databases, XML, etc.) using
    a clean, readable syntax — right inside your C# code, without switching to SQL or
    another language.<br><br>
    <b>Simple analogy:</b> Imagine you have a big box of coloured Lego bricks. LINQ is like
    having a magic wand that lets you say:<br>
    🪄 "Give me all the <b>red</b> bricks" → <code>.Where(b =&gt; b.Color == "Red")</code><br>
    🪄 "Sort them by <b>size</b>" → <code>.OrderBy(b =&gt; b.Size)</code><br>
    🪄 "Just tell me <b>how many</b> there are" → <code>.Count()</code><br><br>
    <b>Why should you learn LINQ?</b><br>
    ✅ It's built into C# — no extra packages needed<br>
    ✅ Makes data manipulation code 5–10x shorter and more readable<br>
    ✅ Works on in-memory collections AND databases (via Entity Framework)<br>
    ✅ Helps you avoid messy for-loops for filtering/sorting<br>
    ✅ Essential knowledge for every C# developer<br><br>
    <b>Where can you use LINQ?</b><br>
    📦 <b>LINQ to Objects</b> — query any C# collection (List, Array, Dictionary)<br>
    🗄️ <b>LINQ to SQL / LINQ to Entities</b> — query databases through EF Core<br>
    📄 <b>LINQ to XML</b> — query and transform XML documents
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a LINQ Query — Two Styles</div>
  <div class="card-body">
    LINQ has two syntax styles — both do the same thing. Learn both because you'll see both
    in the real world:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// Our sample data — a list of students</span>
var students = new List&lt;Student&gt;
{
    new Student { Name = "Alice", Age = 22, Grade = 90 },
    new Student { Name = "Bob",   Age = 19, Grade = 72 },
    new Student { Name = "Carol", Age = 25, Grade = 85 },
    new Student { Name = "Dave",  Age = 21, Grade = 60 },
    new Student { Name = "Eve",   Age = 23, Grade = 95 },
};
&#8203;
<span class="cmd-comment">// ── STYLE 1: Query Syntax (looks like SQL) ──────────────────────</span>
<span class="cmd-comment">//  from  [variable]  in  [source]         ← "look at each item in..."</span>
<span class="cmd-comment">//  where [condition]                       ← "only keep items where..."</span>
<span class="cmd-comment">//  orderby [property]                      ← "sort by..."</span>
<span class="cmd-comment">//  select [what to return]                 ← "return this..."</span>
&#8203;
var topStudentsQuery =
    from s in students
    where s.Grade &gt;= 80
    orderby s.Grade descending
    select s.Name;
&#8203;
<span class="cmd-comment">// ── STYLE 2: Method Syntax (most common in modern C#) ──────────</span>
<span class="cmd-comment">//  Uses chain of extension methods with lambda expressions (=&gt;)</span>
&#8203;
var topStudentsMethod = students
    .Where(s =&gt; s.Grade &gt;= 80)         <span class="cmd-comment">// filter</span>
    .OrderByDescending(s =&gt; s.Grade)   <span class="cmd-comment">// sort</span>
    .Select(s =&gt; s.Name);              <span class="cmd-comment">// transform/project</span>
&#8203;
<span class="cmd-comment">// Both give: ["Eve", "Alice", "Carol"]</span>
foreach (var name in topStudentsMethod)
    Console.WriteLine(name);
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📚 Essential LINQ Methods — With Examples</div>
  <div class="card-body">
    Here are the most important LINQ methods every developer uses daily:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// Sample data</span>
var numbers = new List&lt;int&gt; { 3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5 };
var products = new List&lt;Product&gt; {
    new Product { Name = "Laptop",  Price = 999,  Category = "Electronics" },
    new Product { Name = "Phone",   Price = 699,  Category = "Electronics" },
    new Product { Name = "Desk",    Price = 249,  Category = "Furniture"   },
    new Product { Name = "Chair",   Price = 199,  Category = "Furniture"   },
    new Product { Name = "Monitor", Price = 399,  Category = "Electronics" },
};
&#8203;
<span class="cmd-comment">// ── FILTERING ──────────────────────────────────────────────────</span>
var evenNums  = numbers.Where(n =&gt; n % 2 == 0);          <span class="cmd-comment">// [4, 2, 6]</span>
var expensive = products.Where(p =&gt; p.Price &gt; 400);       <span class="cmd-comment">// Laptop, Phone</span>
&#8203;
<span class="cmd-comment">// ── SORTING ────────────────────────────────────────────────────</span>
var sorted    = numbers.OrderBy(n =&gt; n);                   <span class="cmd-comment">// ascending</span>
var desc      = numbers.OrderByDescending(n =&gt; n);         <span class="cmd-comment">// descending</span>
var multiSort = products.OrderBy(p =&gt; p.Category)
                        .ThenByDescending(p =&gt; p.Price);   <span class="cmd-comment">// category, then price</span>
&#8203;
<span class="cmd-comment">// ── PROJECTION (transform shape of data) ───────────────────────</span>
var names     = products.Select(p =&gt; p.Name);              <span class="cmd-comment">// just names</span>
var summaries = products.Select(p =&gt; new {                 <span class="cmd-comment">// anonymous type</span>
    p.Name, Label = $"{p.Name} - ${p.Price}"
});
&#8203;
<span class="cmd-comment">// ── AGGREGATION ────────────────────────────────────────────────</span>
int total     = numbers.Sum();                             <span class="cmd-comment">// 44</span>
double avg    = numbers.Average();                         <span class="cmd-comment">// 4.0</span>
int max       = numbers.Max();                             <span class="cmd-comment">// 9</span>
int min       = numbers.Min();                             <span class="cmd-comment">// 1</span>
int count     = numbers.Count();                           <span class="cmd-comment">// 11</span>
decimal total2 = products.Sum(p =&gt; p.Price);               <span class="cmd-comment">// 2545</span>
&#8203;
<span class="cmd-comment">// ── GROUPING ───────────────────────────────────────────────────</span>
var byCategory = products.GroupBy(p =&gt; p.Category);
foreach (var group in byCategory) {
    Console.WriteLine($"{group.Key}: {group.Count()} items");
}
<span class="cmd-comment">// Output: Electronics: 3 items  |  Furniture: 2 items</span>
&#8203;
<span class="cmd-comment">// ── ELEMENT OPERATIONS ─────────────────────────────────────────</span>
var first  = products.First(p =&gt; p.Price &gt; 300);           <span class="cmd-comment">// throws if none</span>
var firstN = products.FirstOrDefault(p =&gt; p.Price &gt; 9000); <span class="cmd-comment">// null if none — safer!</span>
var single = products.Single(p =&gt; p.Name == "Desk");       <span class="cmd-comment">// throws if 0 or 2+</span>
var last   = products.Last();
&#8203;
<span class="cmd-comment">// ── CHECKING ───────────────────────────────────────────────────</span>
bool anyExp  = products.Any(p =&gt; p.Price &gt; 900);           <span class="cmd-comment">// true</span>
bool allExp  = products.All(p =&gt; p.Price &gt; 100);           <span class="cmd-comment">// true</span>
bool hasDesk = products.Any(p =&gt; p.Name == "Desk");        <span class="cmd-comment">// true</span>
&#8203;
<span class="cmd-comment">// ── DISTINCT / SKIP / TAKE ─────────────────────────────────────</span>
var unique   = numbers.Distinct();                         <span class="cmd-comment">// [3,1,4,5,9,2,6]</span>
var page1    = products.Skip(0).Take(2);                   <span class="cmd-comment">// pagination: first 2</span>
var page2    = products.Skip(2).Take(2);                   <span class="cmd-comment">// pagination: next 2</span>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚡ Deferred vs Immediate Execution — Critical Concept!</div>
  <div class="card-body">
    <b>This is the #1 thing beginners misunderstand about LINQ.</b><br><br>
    Most LINQ queries are <b>deferred</b> — they don't actually run until you iterate the results
    (with <code>foreach</code>, <code>.ToList()</code>, <code>.ToArray()</code> etc.).<br><br>
    Think of a LINQ query as a <em>recipe</em>, not a cooked meal. The query describes WHAT to
    do — but the cooking (execution) only happens when you actually ask for the food.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">// DEFERRED execution — query defined but NOT run yet</span>
var query = students.Where(s =&gt; s.Grade &gt;= 80);  <span class="cmd-comment">// ← no DB/loop hit here</span>
&#8203;
students.Add(new Student { Name = "Frank", Age = 20, Grade = 92 });  <span class="cmd-comment">// add after query</span>
&#8203;
<span class="cmd-comment">// Query runs HERE — Frank IS included because execution is now</span>
foreach (var s in query)
    Console.WriteLine(s.Name);   <span class="cmd-comment">// Alice, Carol, Eve, Frank ← Frank appears!</span>
&#8203;
<span class="cmd-comment">// IMMEDIATE execution — use ToList(), ToArray(), Count(), First() etc.</span>
var snapshot = students.Where(s =&gt; s.Grade &gt;= 80).ToList(); <span class="cmd-comment">// runs NOW, Frank included</span>
&#8203;
<span class="cmd-comment">// Rule of thumb:</span>
<span class="cmd-comment">// • Add .ToList() when you want a fixed snapshot of results</span>
<span class="cmd-comment">// • Add .ToList() to avoid running the query multiple times</span>
<span class="cmd-comment">// • In EF Core: always .ToListAsync() to execute DB queries</span>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📋 LINQ Quick-Reference Cheat Sheet</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>Method</th><th>What it does</th><th>Example</th></tr>
      <tr><td>Where</td><td>Filter items</td><td>.Where(x =&gt; x.Age &gt; 18)</td></tr>
      <tr><td>Select</td><td>Transform/project items</td><td>.Select(x =&gt; x.Name)</td></tr>
      <tr><td>OrderBy / OrderByDescending</td><td>Sort ascending / descending</td><td>.OrderBy(x =&gt; x.Name)</td></tr>
      <tr><td>GroupBy</td><td>Group items by key</td><td>.GroupBy(x =&gt; x.Category)</td></tr>
      <tr><td>First / FirstOrDefault</td><td>Get first match (or null)</td><td>.FirstOrDefault(x =&gt; x.Id == 1)</td></tr>
      <tr><td>Single / SingleOrDefault</td><td>Exactly one match expected</td><td>.Single(x =&gt; x.Email == email)</td></tr>
      <tr><td>Any</td><td>Does any item match?</td><td>.Any(x =&gt; x.IsActive)</td></tr>
      <tr><td>All</td><td>Do ALL items match?</td><td>.All(x =&gt; x.Age &gt;= 18)</td></tr>
      <tr><td>Count</td><td>How many items?</td><td>.Count(x =&gt; x.IsActive)</td></tr>
      <tr><td>Sum / Average / Min / Max</td><td>Math aggregates</td><td>.Sum(x =&gt; x.Price)</td></tr>
      <tr><td>Distinct</td><td>Remove duplicates</td><td>.Distinct()</td></tr>
      <tr><td>Skip / Take</td><td>Pagination</td><td>.Skip(10).Take(5)</td></tr>
      <tr><td>ToList / ToArray</td><td>Execute immediately</td><td>.ToList()</td></tr>
      <tr><td>SelectMany</td><td>Flatten nested collections</td><td>.SelectMany(x =&gt; x.Tags)</td></tr>
      <tr><td>Join</td><td>Join two collections</td><td>.Join(other, x =&gt; x.Id, y =&gt; y.Id, ...)</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # BLAZOR SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "Blazor":
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔥 What is Blazor? (For Complete Beginners)</div>
  <div class="card-body">
    <b>Blazor</b> is Microsoft's framework that lets you build <em>interactive web UIs using C#</em>
    instead of JavaScript. With Blazor, the same C# skills you use for back-end development can
    now power your front-end web experience.<br><br>
    <b>Simple analogy:</b> Normally, web browsers only speak "JavaScript". Blazor gives you a
    translator (WebAssembly) so the browser can now also understand C# — letting you write
    web apps entirely in the language you already know.<br><br>
    <b>Why should you learn Blazor?</b><br>
    ✅ Write full-stack web apps in pure C# — no JavaScript required<br>
    ✅ Share code between front-end and back-end (same models, same validation)<br>
    ✅ Backed by Microsoft — integrated into .NET 8<br>
    ✅ Component-based architecture (similar to React/Angular concepts)<br>
    ✅ Huge growth in adoption — more and more companies use it
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📜 Blazor History — From Beginning to Today</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>Year</th><th>Milestone</th><th>What Changed</th></tr>
      <tr><td>2017</td><td>Steve Sanderson's experimental prototype</td><td>Proof-of-concept: C# running in browser via WebAssembly</td></tr>
      <tr><td>2018</td><td>Blazor announced at NDC Oslo</td><td>Microsoft officially backs the project</td></tr>
      <tr><td>2019 (.NET Core 3.0)</td><td><b>Blazor Server released</b> (production-ready)</td><td>First official Blazor model — runs on server via SignalR</td></tr>
      <tr><td>2020 (.NET 5)</td><td><b>Blazor WebAssembly released</b> (production-ready)</td><td>C# runs directly in the browser — no server needed for UI</td></tr>
      <tr><td>2022 (.NET 6)</td><td>Blazor improvements</td><td>Hot reload, better performance, .NET MAUI Blazor hybrid</td></tr>
      <tr><td>2023 (.NET 7)</td><td>Enhanced navigation, streaming rendering</td><td>Better UX, improved SEO, empty Blazor WASM template</td></tr>
      <tr><td>2023 (.NET 8)</td><td><b>Blazor United / Full-Stack Blazor</b></td><td>Merged Server + WASM into one model with render mode selection per component</td></tr>
      <tr><td>2024 (.NET 9)</td><td>Blazor Web App enhancements</td><td>Reconnection UI, improved form handling, faster WASM startup</td></tr>
    </table>
    <br>
    <b>What replaced what?</b><br>
    🔴 <b>Web Forms (ASP.NET)</b> → replaced by <b>Blazor Server</b> (for server-side interactive UIs)<br>
    🔴 <b>Silverlight / Flash</b> → replaced by <b>Blazor WebAssembly</b> (for rich browser apps without plugins)<br>
    🔴 <b>JavaScript SPA frameworks (React/Angular/Vue)</b> → Blazor WASM is the C# alternative
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚖️ Blazor Server vs Blazor WebAssembly — Side-by-Side</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>Feature</th><th>Blazor Server</th><th>Blazor WebAssembly (WASM)</th></tr>
      <tr><td>Where does C# run?</td><td>On the <b>server</b></td><td>In the <b>browser</b> (via WebAssembly)</td></tr>
      <tr><td>How UI updates reach browser</td><td>SignalR (WebSocket) connection</td><td>Direct DOM updates in browser</td></tr>
      <tr><td>Initial load time</td><td>⚡ Very fast (small download)</td><td>🐢 Slower (downloads .NET runtime)</td></tr>
      <tr><td>Works offline?</td><td>❌ No — needs server connection</td><td>✅ Yes — once downloaded</td></tr>
      <tr><td>Server scalability</td><td>⚠️ One connection per user</td><td>✅ Stateless — scales easily</td></tr>
      <tr><td>Access to server resources</td><td>✅ Direct DB/file access</td><td>❌ Must call an API</td></tr>
      <tr><td>Latency for interactions</td><td>⚠️ Small delay (network round-trip)</td><td>✅ Instant (local execution)</td></tr>
      <tr><td>Security</td><td>✅ Code stays on server (not exposed)</td><td>⚠️ Code runs in browser (decompilable)</td></tr>
      <tr><td>Best for</td><td>Internal tools, admin panels, dashboards</td><td>Public apps, PWAs, offline scenarios</td></tr>
      <tr><td>.NET template</td><td>dotnet new blazorserver</td><td>dotnet new blazorwasm</td></tr>
    </table>
    <br>
    <b>.NET 8 Blazor Web App</b> — the new default template merges both! You can choose the
    rendering mode <em>per page or per component</em>: Static SSR, Interactive Server, Interactive WASM,
    or Auto (tries WASM, falls back to Server). This is the recommended way for new projects.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card" style="border-left: 4px solid #40916C;">
  <div class="card-title">🏗️ Anatomy of a Blazor Component</div>
  <div class="card-body">
    A Blazor component is a <code>.razor</code> file that combines HTML markup, C# code, and CSS styling
    in one place. Here's every part explained:
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div class="cmd-block">
<span class="cmd-comment">&lt;!-- File: Counter.razor — a simple counter component --&gt;</span>
&#8203;
<span class="cmd-comment">&lt;!-- ① @page directive — URL route for this component --&gt;</span>
@page "/counter"
&#8203;
<span class="cmd-comment">&lt;!-- ② @using / @inject — import namespaces or inject services --&gt;</span>
@using MyApp.Services
@inject ILogger&lt;Counter&gt; Logger
&#8203;
<span class="cmd-comment">&lt;!-- ③ HTML template — standard HTML + Razor syntax --&gt;</span>
&lt;h1&gt;🔢 Counter&lt;/h1&gt;
&#8203;
&lt;p&gt;Current count: &lt;strong&gt;@currentCount&lt;/strong&gt;&lt;/p&gt;
&#8203;
<span class="cmd-comment">&lt;!-- ④ @onclick — event binding — calls C# method on click --&gt;</span>
&lt;button class="btn btn-primary" @onclick="IncrementCount"&gt;
    Click me!
&lt;/button&gt;
&#8203;
&lt;button class="btn btn-secondary" @onclick="ResetCount"&gt;
    Reset
&lt;/button&gt;
&#8203;
<span class="cmd-comment">&lt;!-- ⑤ @code block — C# code lives here --&gt;</span>
@code {
    <span class="cmd-comment">// ⑥ Private field — holds state for this component</span>
    private int currentCount = 0;
&#8203;
    <span class="cmd-comment">// ⑦ [Parameter] — accepts values from a parent component</span>
    [Parameter]
    public int StartValue { get; set; } = 0;
&#8203;
    <span class="cmd-comment">// ⑧ OnInitialized — lifecycle method, runs when component first loads</span>
    protected override void OnInitialized()
    {
        currentCount = StartValue;
        Logger.LogInformation("Counter initialized at {Value}", StartValue);
    }
&#8203;
    <span class="cmd-comment">// ⑨ Event handler method</span>
    private void IncrementCount()
    {
        currentCount++;
        Logger.LogInformation("Count incremented to {Value}", currentCount);
    }
&#8203;
    private void ResetCount() =&gt; currentCount = StartValue;
}
&#8203;
<span class="cmd-comment">&lt;!-- ⑩ Optional: scoped CSS — in Counter.razor.css file --&gt;</span>
<span class="cmd-comment">&lt;!-- h1 { color: #1A1A1A; } /* only applies to this component */ --&gt;</span>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🚀 How to Create &amp; Run a Blazor App</div>
  <div class="card-body">
    <b>Prerequisites:</b> .NET 8 SDK installed (<code>dotnet --version</code> to check)
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        tabs_blazor = st.tabs(["Blazor Web App (.NET 8)", "Blazor Server (.NET 7-)", "Blazor WASM (.NET 7-)"])

        with tabs_blazor[0]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor Web App — Recommended for .NET 8+ (unified model) ──</span>
&#8203;
<span class="cmd-comment"># Create new Blazor Web App</span>
dotnet new blazor -n MyBlazorApp
cd MyBlazorApp
&#8203;
<span class="cmd-comment"># Run the app (opens in browser at https://localhost:5001)</span>
dotnet run
&#8203;
<span class="cmd-comment"># Run with hot reload (auto-refreshes on file save)</span>
dotnet watch run
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — the startup file (.NET 8 Blazor Web App)</span>
var builder = WebApplication.CreateBuilder(args);
&#8203;
<span class="cmd-comment">// Add Blazor services — InteractiveServer enables server-side interactivity</span>
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()      <span class="cmd-comment">// for server render mode</span>
    .AddInteractiveWebAssemblyComponents(); <span class="cmd-comment">// for WASM render mode</span>
&#8203;
var app = builder.Build();
&#8203;
app.UseStaticFiles();
app.UseAntiforgery();
&#8203;
<span class="cmd-comment">// Map Razor components — App.razor is the root component</span>
app.MapRazorComponents&lt;App&gt;()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode();
&#8203;
app.Run();
</div>
""",
                unsafe_allow_html=True,
            )

        with tabs_blazor[1]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor Server (.NET 6/7 style) ──────────────────────────────</span>
&#8203;
dotnet new blazorserver -n MyBlazorServer
cd MyBlazorServer
dotnet run
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — Blazor Server (.NET 6/7)</span>
var builder = WebApplication.CreateBuilder(args);
&#8203;
<span class="cmd-comment">// AddServerSideBlazor registers SignalR + Blazor rendering pipeline</span>
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
&#8203;
<span class="cmd-comment">// Register your own services here</span>
builder.Services.AddSingleton&lt;WeatherForecastService&gt;();
&#8203;
var app = builder.Build();
&#8203;
app.UseStaticFiles();
app.UseRouting();
&#8203;
app.MapBlazorHub();              <span class="cmd-comment">// SignalR endpoint for Blazor</span>
app.MapFallbackToPage("/_Host"); <span class="cmd-comment">// fallback to _Host.cshtml</span>
&#8203;
app.Run();
</div>
""",
                unsafe_allow_html=True,
            )

        with tabs_blazor[2]:
            st.markdown(
                """
<div class="cmd-block">
<span class="cmd-comment"># ── Blazor WebAssembly (standalone, .NET 6/7 style) ─────────────</span>
&#8203;
dotnet new blazorwasm -n MyBlazorWasm
cd MyBlazorWasm
dotnet run
&#8203;
<span class="cmd-comment"># Hosted (with ASP.NET Core back-end API)</span>
dotnet new blazorwasm --hosted -n MyBlazorWasmHosted
</div>
<br>
<div class="cmd-block">
<span class="cmd-comment">// Program.cs — Blazor WASM (runs in browser)</span>
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
&#8203;
var builder = WebAssemblyHostBuilder.CreateDefault(args);
&#8203;
<span class="cmd-comment">// App is the root component; #app is the HTML element it renders into</span>
builder.RootComponents.Add&lt;App&gt;("#app");
builder.RootComponents.Add&lt;HeadOutlet&gt;("head::after");
&#8203;
<span class="cmd-comment">// HttpClient for calling APIs — base address is the current host</span>
builder.Services.AddScoped(sp =&gt; new HttpClient {
    BaseAddress = new Uri(builder.HostEnvironment.BaseAddress)
});
&#8203;
await builder.Build().RunAsync();
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📁 Blazor Project Structure — What Every File Does</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>File / Folder</th><th>Purpose</th></tr>
      <tr><td>Program.cs</td><td>App startup, service registration, middleware pipeline</td></tr>
      <tr><td>App.razor</td><td>Root component — sets up routing</td></tr>
      <tr><td>Routes.razor (.NET 8)</td><td>Router configuration</td></tr>
      <tr><td>Pages/</td><td>Page components (have @page directive)</td></tr>
      <tr><td>Components/ (or Shared/)</td><td>Reusable components (no @page directive)</td></tr>
      <tr><td>wwwroot/</td><td>Static files: CSS, images, JavaScript</td></tr>
      <tr><td>wwwroot/app.css</td><td>Global CSS styles</td></tr>
      <tr><td>ComponentName.razor.css</td><td>Scoped CSS — only applies to that component</td></tr>
      <tr><td>appsettings.json</td><td>Configuration settings</td></tr>
      <tr><td>_Imports.razor</td><td>@using statements for all components (like a global using file)</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚠️ Key Things to Be Aware Of in Blazor</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>#</th><th>Topic</th><th>What to Know</th></tr>
      <tr><td>1</td><td>Component lifecycle</td><td>Learn OnInitialized, OnParametersSet, OnAfterRender — called at specific moments</td></tr>
      <tr><td>2</td><td>StateHasChanged()</td><td>Call this to force UI re-render when state changes outside event handlers</td></tr>
      <tr><td>3</td><td>@bind directive</td><td>Two-way data binding: @bind="myVariable" syncs input value and C# field</td></tr>
      <tr><td>4</td><td>EventCallback</td><td>Use EventCallback&lt;T&gt; to pass events from child to parent components</td></tr>
      <tr><td>5</td><td>Cascading Parameters</td><td>Share data through a component tree without passing through every level</td></tr>
      <tr><td>6</td><td>JavaScript Interop</td><td>Call JS from C# with IJSRuntime.InvokeAsync — needed for browser APIs</td></tr>
      <tr><td>7</td><td>WASM first load</td><td>First load is slow (downloads .NET runtime ~5–10MB) — use loading spinner</td></tr>
      <tr><td>8</td><td>Authentication</td><td>Use AuthenticationStateProvider; Blazor supports cookie, JWT, OIDC auth</td></tr>
      <tr><td>9</td><td>Render modes (.NET 8)</td><td>@rendermode InteractiveServer / InteractiveWebAssembly / InteractiveAuto</td></tr>
      <tr><td>10</td><td>No direct DOM access</td><td>Don't manipulate DOM with JS directly — let Blazor manage it</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # C# SECTION
    # ══════════════════════════════════════════════════════════════════════════
      elif section == "C#":
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">💠 What is C#? (For Complete Beginners)</div>
  <div class="card-body">
    <b>C#</b> (pronounced "C sharp") is a modern, object-oriented programming language created by
    Microsoft in 2000. It was designed by <b>Anders Hejlsberg</b> (who also designed TypeScript and
    previously Turbo Pascal &amp; Delphi).<br><br>
    C# runs on the <b>.NET platform</b> — Microsoft's powerful developer toolkit. Think of .NET as
    a professional kitchen and C# as the chef's language: structured, expressive, and incredibly
    powerful.<br><br>
    <b>🏠 Layman terms:</b> Imagine you want to give instructions to a robot (your computer). C# is
    a language that the robot understands perfectly — and it's designed to be clear, logical, and
    hard to misuse. It's like writing a recipe: step-by-step instructions that the robot follows
    exactly.<br><br>
    <b>What can you build with C#?</b><br>
    ✅ Web apps &amp; APIs (ASP.NET Core)<br>
    ✅ Desktop apps (WPF, WinForms, MAUI)<br>
    ✅ Mobile apps (Xamarin / .NET MAUI)<br>
    ✅ Games (Unity — the world's most popular game engine)<br>
    ✅ Cloud services (Azure)<br>
    ✅ IoT &amp; embedded systems<br>
    ✅ AI/ML pipelines with ML.NET<br><br>
    <b>🏆 Competitors &amp; Comparison</b><br>
    <table class="shortcut-table">
      <tr><th>Language</th><th>Creator</th><th>Primary Use</th><th>How C# compares</th></tr>
      <tr><td><b>Java</b></td><td>Oracle / Sun</td><td>Enterprise, Android</td><td>C# has more modern syntax, better async support, better tooling on Windows</td></tr>
      <tr><td><b>Python</b></td><td>Guido van Rossum</td><td>Data science, scripting, AI</td><td>C# is faster and statically typed; Python is easier for quick scripts</td></tr>
      <tr><td><b>C++</b></td><td>Bjarne Stroustrup</td><td>Systems, games (raw performance)</td><td>C# is much safer (managed memory), easier to write; C++ is faster but complex</td></tr>
      <tr><td><b>TypeScript / JS</b></td><td>Microsoft / Netscape</td><td>Web front-end, Node.js</td><td>C# is a backend/full-stack alternative; TypeScript is browser-first</td></tr>
      <tr><td><b>Go (Golang)</b></td><td>Google</td><td>Cloud, microservices, CLIs</td><td>Go is simpler &amp; minimal; C# is more feature-rich and enterprise-friendly</td></tr>
      <tr><td><b>Kotlin</b></td><td>JetBrains / Google</td><td>Android, JVM</td><td>Very similar modern feel; C# targets .NET, Kotlin targets JVM/Android</td></tr>
      <tr><td><b>Swift</b></td><td>Apple</td><td>iOS, macOS apps</td><td>Swift is Apple-ecosystem only; C# is cross-platform</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚡ What Makes C# Special? (What Others Can't Easily Do)</div>
  <div class="card-body">
    <div class="feature-grid">
      <div class="feature-pill">
        <strong>🔗 Unified Full-Stack</strong>
        <p>Build front-end (Blazor), back-end (ASP.NET), mobile (MAUI), and games (Unity) — all in the same language.</p>
      </div>
      <div class="feature-pill">
        <strong>⚡ async/await Pioneer</strong>
        <p>C# popularised async/await (2012 — before JS, Python, or Kotlin added it). Asynchronous code reads like synchronous code.</p>
      </div>
      <div class="feature-pill">
        <strong>🧩 LINQ</strong>
        <p>Language-Integrated Query — query arrays, databases, XML, JSON with SQL-like syntax directly in C# code. No other mainstream language has this built-in.</p>
      </div>
      <div class="feature-pill">
        <strong>🛡️ Nullable Reference Types</strong>
        <p>C# 8 introduced compile-time null-safety — the compiler warns you before you cause a NullReferenceException at runtime.</p>
      </div>
      <div class="feature-pill">
        <strong>🏎️ Records &amp; Immutability</strong>
        <p>C# 9 added record types — immutable data objects with value equality built-in. Less boilerplate than Java POJOs or Python dataclasses.</p>
      </div>
      <div class="feature-pill">
        <strong>🎮 Unity Game Development</strong>
        <p>C# is the scripting language for Unity — used to build 60%+ of all mobile games worldwide.</p>
      </div>
      <div class="feature-pill">
        <strong>🔬 Pattern Matching</strong>
        <p>Advanced switch expressions, positional patterns, property patterns — cleaner than if/else chains, more powerful than Java's instanceof.</p>
      </div>
      <div class="feature-pill">
        <strong>📦 NuGet Ecosystem</strong>
        <p>Over 300,000 open-source packages on NuGet.org — the .NET package manager integrates seamlessly into Visual Studio.</p>
      </div>
      <div class="feature-pill">
        <strong>🖥️ Native AOT &amp; Performance</strong>
        <p>C# / .NET 8 supports Native AOT compilation — produces tiny, fast executables without needing the .NET runtime installed.</p>
      </div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🎯 Why Should You Learn C#?</div>
  <div class="card-body">
    <b>For job seekers:</b><br>
    ✅ Consistently top 5 in the TIOBE programming language index<br>
    ✅ High demand in enterprise, finance, healthcare, gaming, government sectors<br>
    ✅ Microsoft Azure cloud = massive C# / .NET ecosystem<br>
    ✅ Average salary: $95,000–$145,000/year (USA, 2025–2026)<br><br>
    <b>For students &amp; career changers:</b><br>
    ✅ One of the best-structured languages to <em>learn programming fundamentals</em><br>
    ✅ Strongly typed — the compiler catches your mistakes before they run<br>
    ✅ Excellent documentation (Microsoft Docs / learn.microsoft.com)<br>
    ✅ Free tools: Visual Studio Community, VS Code, .NET SDK — all free<br><br>
    <b>For game developers:</b><br>
    ✅ Unity uses C# — learn it once, build games for PC, mobile, console, AR/VR<br><br>
    <b>🏠 Layman analogy:</b> Learning C# is like learning to drive a Mercedes — once you know it,
    you can drive anything. And it's in huge demand everywhere.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🌍 What is C# Compatible With?</div>
  <div class="card-body">
    <b>Operating Systems:</b>
    <div class="platform-row">
      <div class="platform-badge">🪟 Windows</div>
      <div class="platform-badge">🐧 Linux</div>
      <div class="platform-badge">🍎 macOS</div>
      <div class="platform-badge">📱 Android (MAUI)</div>
      <div class="platform-badge">📱 iOS (MAUI)</div>
      <div class="platform-badge">☁️ Azure Cloud</div>
      <div class="platform-badge">🐳 Docker / Kubernetes</div>
      <div class="platform-badge">🎮 Xbox / Console</div>
    </div>
    <br>
    <b>Frameworks &amp; Runtimes:</b><br>
    <table class="shortcut-table">
      <tr><th>Framework</th><th>Use Case</th></tr>
      <tr><td>ASP.NET Core</td><td>Web APIs, MVC websites, Razor Pages</td></tr>
      <tr><td>Blazor</td><td>Interactive web UI in C# (browser + server)</td></tr>
      <tr><td>.NET MAUI</td><td>Cross-platform mobile &amp; desktop (Android, iOS, Windows, macOS)</td></tr>
      <tr><td>WPF / WinForms</td><td>Windows desktop apps</td></tr>
      <tr><td>Unity</td><td>2D/3D games across all platforms</td></tr>
      <tr><td>ML.NET</td><td>Machine learning &amp; AI</td></tr>
      <tr><td>Azure Functions</td><td>Serverless cloud computing</td></tr>
      <tr><td>gRPC / SignalR</td><td>Real-time communication &amp; microservices</td></tr>
    </table>
    <br>
    <b>Databases C# works with:</b> SQL Server, Oracle, PostgreSQL, MySQL, SQLite, MongoDB, Redis, CosmosDB — via EF Core or raw ADO.NET.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🏗️ What Types of Apps Are Best Built with C#?</div>
  <div class="card-body">
    <div class="feature-grid">
      <div class="feature-pill">
        <strong>🌐 Web APIs &amp; Microservices</strong>
        <p>ASP.NET Core is one of the fastest web frameworks. Used by Stack Overflow, Microsoft, and thousands of enterprises.</p>
      </div>
      <div class="feature-pill">
        <strong>🏢 Enterprise Line-of-Business Apps</strong>
        <p>CRM, ERP, inventory systems — C# with WPF or ASP.NET is the go-to in corporate environments.</p>
      </div>
      <div class="feature-pill">
        <strong>🎮 Video Games (Unity)</strong>
        <p>Pokémon GO, Cuphead, Cities: Skylines, Among Us — all built with Unity + C#.</p>
      </div>
      <div class="feature-pill">
        <strong>📱 Cross-Platform Mobile Apps</strong>
        <p>.NET MAUI: one codebase → iOS + Android + Windows + macOS apps.</p>
      </div>
      <div class="feature-pill">
        <strong>☁️ Cloud &amp; Serverless</strong>
        <p>Azure Functions, Azure App Services — C# is Azure's first-class citizen.</p>
      </div>
      <div class="feature-pill">
        <strong>🖥️ Windows Desktop Apps</strong>
        <p>WPF (rich UI) and WinForms (classic) remain popular for internal business tools.</p>
      </div>
      <div class="feature-pill">
        <strong>🤖 AI / ML</strong>
        <p>ML.NET for machine learning pipelines; integration with Python AI models via REST.</p>
      </div>
      <div class="feature-pill">
        <strong>🔧 Dev Tools &amp; CLIs</strong>
        <p>Roslyn compiler, PowerShell, NuGet — all built in C#/.NET.</p>
      </div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">⚠️ Challenges of Learning C#</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>#</th><th>Challenge</th><th>Why it's tricky</th><th>How to overcome it</th></tr>
      <tr><td>1</td><td>Understanding types &amp; generics</td><td>C# is strongly typed — you must declare what type every variable is</td><td>Practice with simple examples; the compiler is your teacher</td></tr>
      <tr><td>2</td><td>OOP concepts (classes, interfaces)</td><td>Object-Oriented Programming has many abstract concepts</td><td>Build small real projects (a bank account class, a to-do list)</td></tr>
      <tr><td>3</td><td>async/await &amp; threading</td><td>Asynchronous code can feel confusing at first</td><td>Start with simple async methods, avoid manual threading early</td></tr>
      <tr><td>4</td><td>Understanding .NET vs C#</td><td>Beginners confuse the language (C#) with the platform (.NET)</td><td>Think: C# = the language; .NET = the platform it runs on</td></tr>
      <tr><td>5</td><td>Visual Studio complexity</td><td>VS has hundreds of features — overwhelming at first</td><td>Learn only what you need: create project → write code → run it</td></tr>
      <tr><td>6</td><td>Dependency Injection</td><td>A key .NET pattern that beginners find confusing</td><td>Learn it after you understand interfaces and constructors</td></tr>
      <tr><td>7</td><td>LINQ learning curve</td><td>LINQ syntax (lambdas, method chains) is unfamiliar at first</td><td>Start with simple .Where() and .Select() calls</td></tr>
      <tr><td>8</td><td>C# version differences</td><td>Articles may use C# 5 code vs C# 12 code — looks very different</td><td>Always check the C# version the tutorial targets</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🚀 How to Learn C# (Complete Beginner Roadmap)</div>
  <div class="card-body">
    <b>🏠 Layman analogy:</b> Learning C# is like learning to cook. Start with boiling water,
    then make an omelette, then a full meal — don't try a 5-course dinner on day one!<br><br>
    <b>Phase 1 — Install &amp; Hello World (Day 1–3)</b><br>
    <div class="wf-diagram">
      <div class="wf-node">Install .NET SDK</div>
      <div class="wf-arrow">→</div>
      <div class="wf-node">Install VS Code or Visual Studio</div>
      <div class="wf-arrow">→</div>
      <div class="wf-node">dotnet new console</div>
      <div class="wf-arrow">→</div>
      <div class="wf-node-green">Run Hello World ✅</div>
    </div>
    <br>
    <b>Phase 2 — Core Language Basics (Week 1–3)</b><br>
    Variables &amp; types → Operators → if/else → loops (for, while, foreach) → methods → arrays<br><br>
    <b>Phase 3 — Object-Oriented Programming (Week 4–6)</b><br>
    Classes → Objects → Constructors → Properties → Inheritance → Interfaces → Abstract classes<br><br>
    <b>Phase 4 — Intermediate C# (Month 2)</b><br>
    Generics → Collections (List, Dictionary) → LINQ → Exception handling → File I/O → async/await<br><br>
    <b>Phase 5 — Real Framework (Month 3+)</b><br>
    Pick ONE: ASP.NET Core (web) OR Unity (games) OR WPF (desktop) and build a project<br><br>
    <b>🎓 Free Learning Resources:</b><br>
    ✅ <b>learn.microsoft.com/dotnet/csharp</b> — official Microsoft C# tour (best starting point)<br>
    ✅ <b>dotnet.microsoft.com/learn</b> — free interactive browser-based tutorials<br>
    ✅ <b>CS50 (Harvard)</b> — free intro to programming using C#<br>
    ✅ <b>YouTube: Tim Corey, Nick Chapsas, IAmTimCorey</b> — top C# instructors<br>
    ✅ <b>freeCodeCamp C# Certification</b> — free structured course<br><br>
    <b>💡 Tip for non-technical beginners:</b> Don't learn C# in isolation — pick a project that
    excites you (a small game, a personal expense tracker, a website) and learn what you need to
    build it. Purpose-driven learning is 10× faster.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📜 C# Version Timeline — Evolution from 1.0 to 13.0</div>
  <div class="card-body">
    <table class="shortcut-table">
      <tr><th>C# Version</th><th>.NET Version</th><th>Year</th><th>Headline Features</th></tr>
      <tr><td><b>C# 1.0</b></td><td>.NET Framework 1.0</td><td>2002</td><td>Classes, interfaces, delegates, events, properties, value types, garbage collection</td></tr>
      <tr><td><b>C# 2.0</b></td><td>.NET Framework 2.0</td><td>2005</td><td>Generics, iterators (yield), nullable types, anonymous methods, partial classes</td></tr>
      <tr><td><b>C# 3.0</b></td><td>.NET Framework 3.5</td><td>2007</td><td>LINQ, lambda expressions, extension methods, auto-properties, anonymous types, var</td></tr>
      <tr><td><b>C# 4.0</b></td><td>.NET Framework 4.0</td><td>2010</td><td>dynamic keyword, optional/named parameters, covariance &amp; contravariance</td></tr>
      <tr><td><b>C# 5.0</b></td><td>.NET Framework 4.5</td><td>2012</td><td>async/await — the biggest game-changer for non-blocking code</td></tr>
      <tr><td><b>C# 6.0</b></td><td>.NET Framework 4.6 / .NET Core 1.0</td><td>2015</td><td>String interpolation ($""), null-conditional (?.), expression-bodied members, nameof</td></tr>
      <tr><td><b>C# 7.0–7.3</b></td><td>.NET Framework 4.7 / .NET Core 2.x</td><td>2017</td><td>Tuples, out variables, pattern matching (is), local functions, throw expressions</td></tr>
      <tr><td><b>C# 8.0</b></td><td>.NET Core 3.0 / 3.1</td><td>2019</td><td>Nullable reference types, switch expressions, ranges &amp; indices (^, ..), async streams</td></tr>
      <tr><td><b>C# 9.0</b></td><td>.NET 5</td><td>2020</td><td>Records, init-only setters, top-level statements, pattern matching enhancements</td></tr>
      <tr><td><b>C# 10.0</b></td><td>.NET 6</td><td>2021</td><td>Global using, file-scoped namespaces, record structs, constant interpolated strings</td></tr>
      <tr><td><b>C# 11.0</b></td><td>.NET 7</td><td>2022</td><td>Required members, raw string literals, list patterns, generic attributes, UTF-8 strings</td></tr>
      <tr><td><b>C# 12.0</b></td><td>.NET 8 ✅ LTS</td><td>2023</td><td>Primary constructors, collection expressions, inline arrays, default lambda params</td></tr>
      <tr><td><b>C# 13.0</b></td><td>.NET 9</td><td>2024</td><td>params collections, new lock type, field keyword in properties, iterator async improvements</td></tr>
      <tr><td><b>C# 14.0</b></td><td>.NET 10 (LTS, Nov 2025)</td><td>2025</td><td>In development — upcoming features being drafted in language design GitHub</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔄 C# Feature Evolution — Same Topic Across All Versions</div>
  <div class="card-body">
    Tracking how <b>"printing a person's name and age"</b> evolved across C# versions shows why
    newer syntax exists and what problem it solves.<br><br>

    <b>📌 C# 1.0 — String concatenation (2002)</b>
    <div class="cmd-block">
string name = "Alice";
int age = 30;
Console.WriteLine("Name: " + name + ", Age: " + age);
// ❌ Issue: verbose, hard to read, error-prone with many variables
    </div>
    <b>📌 C# 5.0 — String.Format (improvement, ~2012)</b>
    <div class="cmd-block">
Console.WriteLine(String.Format("Name: {0}, Age: {1}", name, age));
// Better, but {0} {1} placeholders are still confusing
    </div>
    <b>📌 C# 6.0 — String Interpolation ✅ (2015)</b>
    <div class="cmd-block">
Console.WriteLine($"Name: {name}, Age: {age}");
// ✅ Clean, readable — variables inline with the string
// 🏠 Layman: Like filling in blanks in a sentence: "Name: [name], Age: [age]"
    </div>
    <b>📌 C# 9.0 — Top-level statements (2020)</b>
    <div class="cmd-block">
// No class or Main method needed!
string name = "Alice";
int age = 30;
Console.WriteLine($"Name: {name}, Age: {age}");
// ✅ Perfect for scripts and beginners — less boilerplate
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

    <b>📌 Tracking "Null Checking" evolution</b><br><br>
    <b>C# 1.0–5.0 — Classic null check</b>
    <div class="cmd-block">
if (user != null)
{
    Console.WriteLine(user.Name);
}
// ❌ Easy to forget, causes NullReferenceException at runtime
    </div>
    <b>C# 6.0 — Null-conditional operator (?.) (2015)</b>
    <div class="cmd-block">
Console.WriteLine(user?.Name);
// ✅ If user is null, returns null instead of crashing
// 🏠 Layman: "If the person exists, tell me their name; otherwise say nothing"
    </div>
    <b>C# 6.0 — Null-coalescing (??)</b>
    <div class="cmd-block">
string displayName = user?.Name ?? "Guest";
// ✅ "Use user's name, OR if null, use 'Guest'"
    </div>
    <b>C# 8.0 — Nullable reference types (compile-time safety)</b>
    <div class="cmd-block">
// In .csproj: &lt;Nullable&gt;enable&lt;/Nullable&gt;
string? name = null;   // ✅ explicitly nullable
string  name2 = null;  // ❌ Compiler WARNING — this should never be null!
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

    <b>📌 Tracking "Data class / model" evolution</b><br><br>
    <b>C# 1.0–8.0 — Classic class with properties</b>
    <div class="cmd-block">
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    // Need to manually write Equals(), GetHashCode(), ToString()
}
    </div>
    <b>C# 9.0 — Record types ✅ (2020)</b>
    <div class="cmd-block">
public record Person(string Name, int Age);
// ✅ One line! Auto-generates constructor, Equals, GetHashCode, ToString
// ✅ Immutable by default
// 🏠 Layman: A record is like a stamped official form — once filled, it doesn't change

var p1 = new Person("Alice", 30);
var p2 = new Person("Alice", 30);
Console.WriteLine(p1 == p2); // true — value equality!
// In a regular class, this would be false (reference equality)
    </div>
    <b>C# 9.0 — with expressions (non-destructive mutation)</b>
    <div class="cmd-block">
var p3 = p1 with { Age = 31 };
// Creates a new Person with everything from p1, but Age = 31
// ✅ Immutable data + easy "update"
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

    <b>📌 Tracking "Switch / branching" evolution</b><br><br>
    <b>C# 1.0 — Classic switch</b>
    <div class="cmd-block">
string day = "Monday";
string type;
switch (day)
{
    case "Saturday":
    case "Sunday":
        type = "Weekend";
        break;
    default:
        type = "Weekday";
        break;
}
    </div>
    <b>C# 8.0 — Switch expression ✅ (2019)</b>
    <div class="cmd-block">
string type = day switch
{
    "Saturday" or "Sunday" => "Weekend",
    _ => "Weekday"
};
// ✅ Concise, returns a value, no 'break' needed
// 🏠 Layman: Like a lookup table — "for this input, give me that output"
    </div>
    <b>C# 8.0 — Property pattern matching</b>
    <div class="cmd-block">
string category = person switch
{
    { Age: < 18 }             => "Minor",
    { Age: >= 18, Age: < 65 } => "Adult",
    _                         => "Senior"
};
// ✅ Reads like English rules
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

    <b>📌 Tracking "Async programming" evolution</b><br><br>
    <b>C# 1.0–4.0 — Callbacks / BeginInvoke (painful)</b>
    <div class="cmd-block">
// Old way — callbacks make "callback hell"
webClient.DownloadStringCompleted += (s, e) => {
    Console.WriteLine(e.Result);  // runs when done
};
webClient.DownloadStringAsync(new Uri("https://example.com"));
// ❌ Hard to read, hard to debug, hard to chain
    </div>
    <b>C# 5.0 — async/await ✅ (2012 — game changer!)</b>
    <div class="cmd-block">
async Task FetchDataAsync()
{
    string result = await httpClient.GetStringAsync("https://example.com");
    Console.WriteLine(result);
}
// ✅ Reads like synchronous code — no callbacks!
// 🏠 Layman: Like ordering food at a restaurant — you sit, wait (await), and your
//   food arrives (result) without blocking everyone else in the restaurant
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin:1.2rem 0">

    <b>📌 Tracking "Collections / Filtering" evolution (LINQ)</b><br><br>
    <b>C# 1.0–2.0 — Manual loop filtering</b>
    <div class="cmd-block">
List&lt;int&gt; numbers = new List&lt;int&gt; { 1, 2, 3, 4, 5, 6 };
List&lt;int&gt; evens = new List&lt;int&gt;();
foreach (int n in numbers)
{
    if (n % 2 == 0) evens.Add(n);
}
    </div>
    <b>C# 3.0 — LINQ ✅ (2007)</b>
    <div class="cmd-block">
var evens = numbers.Where(n => n % 2 == 0).ToList();
// ✅ One line, expressive
// 🏠 Layman: "Give me only the items WHERE my condition is true"

// Query syntax (SQL-like):
var evens2 = (from n in numbers where n % 2 == 0 select n).ToList();
    </div>
    <b>C# 12.0 — Collection expressions ✅ (2023)</b>
    <div class="cmd-block">
int[] nums = [1, 2, 3, 4, 5];   // ✅ New [ ] syntax — same for arrays, lists, spans
List&lt;int&gt; more = [1, 2, ..nums]; // ✅ Spread operator — merge collections easily
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🎓 What a New .NET Developer Must Be Strong In</div>
  <div class="card-body">
    These are the <b>non-negotiable foundations</b> that every C# / .NET developer is expected to
    understand deeply — not just know the syntax, but <em>understand why</em>.<br><br>
    <table class="shortcut-table">
      <tr><th>Priority</th><th>Topic</th><th>Why it matters</th><th>🏠 Layman analogy</th></tr>
      <tr><td>🔴 Must</td><td>Value types vs Reference types</td><td>Determines how variables are copied, passed, and stored in memory</td><td>A house (reference) vs a house blueprint (value)</td></tr>
      <tr><td>🔴 Must</td><td>Classes, Objects, Constructors</td><td>Everything in C# is an object — foundation of OOP</td><td>A class is a cookie cutter; objects are the cookies</td></tr>
      <tr><td>🔴 Must</td><td>Interfaces</td><td>Used everywhere in .NET for abstraction and dependency injection</td><td>A contract: "I promise to have these methods"</td></tr>
      <tr><td>🔴 Must</td><td>async/await</td><td>Every modern API, database call, HTTP request is async</td><td>Ordering food without blocking the restaurant kitchen</td></tr>
      <tr><td>🔴 Must</td><td>LINQ (basic)</td><td>Used in every .NET codebase to query collections and databases</td><td>SQL for your in-memory lists</td></tr>
      <tr><td>🔴 Must</td><td>Exception handling (try/catch/finally)</td><td>Production code must handle failures gracefully</td><td>A safety net under a tightrope walker</td></tr>
      <tr><td>🔴 Must</td><td>Generics (List&lt;T&gt;, Dictionary&lt;K,V&gt;)</td><td>Reusable, type-safe code — used constantly</td><td>A box that works for any type of item</td></tr>
      <tr><td>🟡 Should</td><td>Dependency Injection (DI)</td><td>The .NET DI container is used in every ASP.NET Core app</td><td>A vending machine — request what you need, get it</td></tr>
      <tr><td>🟡 Should</td><td>Delegates &amp; Events</td><td>Foundation of UI frameworks (WPF, WinForms) and callbacks</td><td>A referee who calls players when needed</td></tr>
      <tr><td>🟡 Should</td><td>Nullable reference types</td><td>Helps write null-safe code — huge source of runtime bugs otherwise</td><td>Marking "this can be empty" clearly on a form</td></tr>
      <tr><td>🟡 Should</td><td>Records &amp; immutability</td><td>Modern C# style for data transfer objects (DTOs)</td><td>A sealed certificate — can't be changed after issuing</td></tr>
      <tr><td>🟡 Should</td><td>Pattern matching</td><td>Cleaner conditionals — used heavily in modern C# codebases</td><td>A smart sorting machine that routes items by rules</td></tr>
      <tr><td>🟢 Nice</td><td>Reflection</td><td>Inspect types at runtime — used in frameworks, serialisation</td><td>An x-ray machine for code</td></tr>
      <tr><td>🟢 Nice</td><td>Span&lt;T&gt; / Memory&lt;T&gt;</td><td>High-performance zero-allocation slicing of buffers</td><td>A window into a larger array — no copying</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">🔬 Anatomy of a C# Program — Every Part Explained</div>
  <div class="card-body">
    Let's dissect this complete C# program and label every concept:<br><br>
    <div class="cmd-block">
// ① Using directive — imports a namespace (like "import" in Python / Java)
using System;
using System.Collections.Generic;

// ② Namespace — groups related classes together (like a folder)
namespace MyApp.Learning
{
    // ③ Class — a blueprint / template for creating objects
    //    "public" = accessible from other code
    public class BankAccount
    {
        // ④ Field — a private variable that stores state inside the class
        private decimal _balance;

        // ⑤ Property — controlled access to a field (get/set)
        //    "public" = readable from outside, "private set" = only settable inside
        public string Owner { get; private set; }

        // ⑥ Constructor — special method called when an object is created
        //    "this" refers to the current instance
        public BankAccount(string owner, decimal initialBalance)
        {
            Owner    = owner;        // ← set the property
            _balance = initialBalance;
        }

        // ⑦ Method — a named action the class can perform
        //    returns void (nothing), takes a decimal parameter
        public void Deposit(decimal amount)
        {
            // ⑧ Exception handling — catch and handle errors gracefully
            if (amount &lt;= 0)
                throw new ArgumentException("Amount must be positive.");

            _balance += amount;
            // ⑨ String interpolation — embed expressions inside strings
            Console.WriteLine($"Deposited {amount:C}. New balance: {_balance:C}");
        }

        // ⑩ Expression-bodied method (C# 6+) — one-liner method
        public decimal GetBalance() =&gt; _balance;
    }

    // ⑪ Derived class — inherits from BankAccount (Inheritance)
    public class SavingsAccount : BankAccount
    {
        // ⑫ Auto-property with init-only setter (C# 9)
        public decimal InterestRate { get; init; }

        public SavingsAccount(string owner, decimal balance, decimal rate)
            : base(owner, balance)      // ← calls the parent constructor
        {
            InterestRate = rate;
        }

        // ⑬ Method override — customise inherited behaviour
        public void ApplyInterest()
        {
            decimal interest = GetBalance() * InterestRate;
            Deposit(interest);
        }
    }

    // ⑭ Interface — a contract: any class implementing this MUST have these members
    public interface IReportable
    {
        void PrintReport();
    }

    // ⑮ Record — immutable data type (C# 9), auto-generates Equals/ToString
    public record Transaction(string Type, decimal Amount, DateTime Date);

    // ⑯ Program entry point
    public class Program
    {
        // ⑰ Main method — where execution begins
        //    async Task = supports awaiting async operations
        public static async Task Main(string[] args)
        {
            // ⑱ Object instantiation — create an instance from the class blueprint
            var account = new SavingsAccount("Alice", 1000m, 0.05m);

            account.Deposit(500m);
            account.ApplyInterest();

            // ⑲ var keyword — type inferred by compiler (C# 3+)
            var balance = account.GetBalance();

            // ⑳ LINQ — query a collection with lambda expressions
            var transactions = new List&lt;Transaction&gt;
            {
                new("Deposit",  500m,  DateTime.Now),
                new("Interest", 75m,   DateTime.Now),
            };

            // Filter: only deposits
            var deposits = transactions.Where(t =&gt; t.Type == "Deposit").ToList();

            // ㉑ async/await — non-blocking I/O operation
            await Task.Delay(10); // simulate async work

            Console.WriteLine($"Final balance for {account.Owner}: {balance:C}");
        }
    }
}
    </div>
    <br>
    <b>📖 Concept Index:</b><br>
    <table class="shortcut-table">
      <tr><th>Symbol</th><th>Concept</th><th>🏠 Layman Explanation</th></tr>
      <tr><td>①</td><td>using directive</td><td>Like plugging in a toolbox before using its tools</td></tr>
      <tr><td>②</td><td>Namespace</td><td>A folder/category to organise related code</td></tr>
      <tr><td>③</td><td>Class</td><td>A blueprint — defines what an object looks like and can do</td></tr>
      <tr><td>④</td><td>Field (private)</td><td>A secret drawer inside the object — only it can access it directly</td></tr>
      <tr><td>⑤</td><td>Property (get/set)</td><td>A controlled window into the secret drawer — you choose who can read/write</td></tr>
      <tr><td>⑥</td><td>Constructor</td><td>The setup instructions when you first build the object</td></tr>
      <tr><td>⑦</td><td>Method</td><td>An action/verb — what the object can do</td></tr>
      <tr><td>⑧</td><td>Exception handling</td><td>A safety net — "if something goes wrong, do this instead of crashing"</td></tr>
      <tr><td>⑨</td><td>String interpolation</td><td>Fill-in-the-blank for text: "Hello, {name}!"</td></tr>
      <tr><td>⑩</td><td>Expression-bodied member</td><td>A shorthand one-liner for simple methods</td></tr>
      <tr><td>⑪</td><td>Inheritance</td><td>A child class gets everything from the parent and adds its own things</td></tr>
      <tr><td>⑫</td><td>init-only property</td><td>Can only be set during object creation — locked afterwards</td></tr>
      <tr><td>⑬</td><td>Method override</td><td>The child rewrites a parent method to behave differently</td></tr>
      <tr><td>⑭</td><td>Interface</td><td>A signed contract: "I promise to provide these capabilities"</td></tr>
      <tr><td>⑮</td><td>Record</td><td>A sealed, official form — values set once, never changed</td></tr>
      <tr><td>⑯–⑰</td><td>Program entry / Main</td><td>The front door of your program — execution starts here</td></tr>
      <tr><td>⑱</td><td>Object instantiation (new)</td><td>Using the blueprint to build an actual object</td></tr>
      <tr><td>⑲</td><td>var keyword</td><td>Let the compiler figure out the type — you don't need to spell it out</td></tr>
      <tr><td>⑳</td><td>LINQ + lambda</td><td>A filter/query sentence: "From this list, give me items WHERE …"</td></tr>
      <tr><td>㉑</td><td>async/await</td><td>Wait for a slow task without freezing everything else</td></tr>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📚 Key C# Concepts — Technical + Layman Explanations</div>
  <div class="card-body">

    <div class="card-section-title">1. VALUE TYPES vs REFERENCE TYPES</div>
    <b>Technical:</b> Value types (int, bool, struct, enum) are stored on the <em>stack</em> and
    copied when assigned. Reference types (class, string, array) are stored on the <em>heap</em>
    and passing them passes a reference (pointer) to the same object.<br>
    <b>🏠 Layman:</b> Value type = handing someone a photocopy of a document (they get their own copy).
    Reference type = sharing a Google Doc link (both people see and edit the same document).<br>
    <div class="cmd-block">
int a = 5;
int b = a;    // b is a COPY — changing b doesn't affect a
b = 10;
Console.WriteLine(a); // 5 — unchanged ✅

var list1 = new List&lt;int&gt; { 1, 2, 3 };
var list2 = list1;    // list2 POINTS to the same list
list2.Add(4);
Console.WriteLine(list1.Count); // 4 — list1 also changed! ⚠️
    </div>

    <div class="card-section-title">2. GENERICS</div>
    <b>Technical:</b> Generics allow you to write type-safe, reusable code using a type
    parameter (&lt;T&gt;). The compiler enforces the type at compile time — no runtime casting needed.<br>
    <b>🏠 Layman:</b> A generic box: "This box holds exactly one type of thing — you decide which
    type when you order the box. After that, you can only put that type in."<br>
    <div class="cmd-block">
// Without generics — dangerous (any object, cast required)
ArrayList oldList = new ArrayList();
oldList.Add(42);
oldList.Add("oops");        // compiles but runtime crash if you expect int!

// With generics — safe ✅
List&lt;int&gt; safeList = new List&lt;int&gt;();
safeList.Add(42);
// safeList.Add("oops");    // ❌ Compile-time error — caught before it runs!

// Generic method
T Max&lt;T&gt;(T a, T b) where T : IComparable&lt;T&gt;
    =&gt; a.CompareTo(b) &gt; 0 ? a : b;

Console.WriteLine(Max(3, 7));              // 7
Console.WriteLine(Max("apple", "banana")); // banana
    </div>

    <div class="card-section-title">3. DELEGATES &amp; EVENTS</div>
    <b>Technical:</b> A delegate is a type-safe function pointer — a variable that holds a
    reference to a method. Events are a publisher/subscriber pattern built on delegates.<br>
    <b>🏠 Layman:</b> A delegate is like a job posting: "I need someone who can take an int and
    return a string." Any method matching that description can fill the role.
    An event is like a doorbell: when pressed, all registered listeners are notified.<br>
    <div class="cmd-block">
// Delegate type declaration
delegate string Formatter(int value);

// Methods that match the delegate signature
string ToHex(int n)    =&gt; $"0x{n:X}";
string ToBinary(int n) =&gt; Convert.ToString(n, 2);

Formatter fmt = ToHex;
Console.WriteLine(fmt(255)); // 0xFF

fmt = ToBinary;
Console.WriteLine(fmt(10));  // 1010

// Built-in delegate types: Action (void), Func (returns value), Predicate (bool)
Action&lt;string&gt; greet    = name =&gt; Console.WriteLine($"Hello, {name}!");
Func&lt;int, int, int&gt; add = (a, b) =&gt; a + b;
greet("Alice");               // Hello, Alice!
Console.WriteLine(add(3, 4)); // 7
    </div>

    <div class="card-section-title">4. LINQ (Language Integrated Query)</div>
    <b>Technical:</b> LINQ provides declarative query syntax for any IEnumerable&lt;T&gt; or
    IQueryable&lt;T&gt; source — collections, databases (EF Core), XML, JSON.<br>
    <b>🏠 Layman:</b> LINQ is like SQL for your C# lists. "Give me all customers FROM my list
    WHERE their city is London, ORDER BY name, and take only the TOP 5."<br>
    <div class="cmd-block">
var people = new List&lt;(string Name, int Age, string City)&gt;
{
    ("Alice", 30, "London"),
    ("Bob",   25, "Paris"),
    ("Carol", 35, "London"),
    ("Dave",  28, "Berlin"),
};

// Method syntax (most common)
var londonAdults = people
    .Where(p =&gt; p.City == "London" &amp;&amp; p.Age &gt;= 30)
    .OrderBy(p =&gt; p.Name)
    .Select(p =&gt; p.Name)
    .ToList();
// Result: ["Alice", "Carol"]

// Aggregation
int    totalAge = people.Sum(p =&gt; p.Age);      // 118
double avgAge   = people.Average(p =&gt; p.Age);  // 29.5
int    oldest   = people.Max(p =&gt; p.Age);      // 35
    </div>

    <div class="card-section-title">5. ASYNC / AWAIT</div>
    <b>Technical:</b> async/await is syntactic sugar over the Task Parallel Library (TPL).
    An async method returns Task or Task&lt;T&gt;. The await keyword yields control back to the
    caller while waiting for the awaited task — without blocking the thread.<br>
    <b>🏠 Layman:</b> Imagine a waiter at a restaurant. Without async, the waiter stands at your
    table until your food is cooked (blocking everyone). With async, the waiter takes your order,
    goes to serve others, and comes back when your food is ready.<br>
    <div class="cmd-block">
async Task&lt;string&gt; FetchWebPageAsync(string url)
{
    using var client = new HttpClient();
    // Await = "start this, come back when done, don't block"
    string content = await client.GetStringAsync(url);
    return content.Substring(0, 200);
}

// Run multiple async tasks in parallel
async Task RunParallelAsync()
{
    var task1 = FetchWebPageAsync("https://example.com");
    var task2 = FetchWebPageAsync("https://microsoft.com");

    // Wait for BOTH to complete simultaneously
    string[] results = await Task.WhenAll(task1, task2);
    Console.WriteLine($"Got {results.Length} pages");
}
    </div>

    <div class="card-section-title">6. DEPENDENCY INJECTION (DI)</div>
    <b>Technical:</b> DI is a design pattern where dependencies (services) are injected into a
    class via its constructor rather than the class creating them. .NET has a built-in DI container
    (IServiceCollection / IServiceProvider).<br>
    <b>🏠 Layman:</b> Instead of a chef buying their own ingredients (tight coupling), the
    restaurant manager delivers them to the kitchen (injection). The chef doesn't need to know
    where the ingredients come from — they just use them.<br>
    <div class="cmd-block">
// Interface (the contract)
public interface IEmailService
{
    Task SendAsync(string to, string subject, string body);
}

// Real implementation
public class SmtpEmailService : IEmailService
{
    public async Task SendAsync(string to, string subject, string body)
        =&gt; await Task.Run(() =&gt; Console.WriteLine($"Sending email to {to}"));
}

// Consumer — receives IEmailService via constructor injection
public class OrderService
{
    private readonly IEmailService _email;

    public OrderService(IEmailService email) =&gt; _email = email;

    public async Task PlaceOrderAsync(string customerEmail)
    {
        await _email.SendAsync(customerEmail, "Order confirmed", "Thanks!");
    }
}

// Registration in ASP.NET Core (Program.cs)
// builder.Services.AddScoped&lt;IEmailService, SmtpEmailService&gt;();
// ✅ Swap SmtpEmailService for MockEmailService in tests — zero code changes!
    </div>

    <div class="card-section-title">7. EXCEPTION HANDLING</div>
    <b>Technical:</b> Exceptions propagate up the call stack until caught by a try/catch block.
    finally always runs (cleanup). Custom exceptions inherit from Exception.<br>
    <b>🏠 Layman:</b> Exception handling is like a safety net in a circus. If an acrobat
    (method) falls (throws an exception), the net (catch) catches them. The stage crew
    (finally) always tidies up, regardless of what happened.<br>
    <div class="cmd-block">
public decimal Divide(decimal a, decimal b)
{
    if (b == 0)
        throw new DivideByZeroException("Cannot divide by zero!");
    return a / b;
}

try
{
    decimal result = Divide(10, 0);
    Console.WriteLine(result);
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Math error: {ex.Message}"); // handled ✅
}
catch (Exception ex)
{
    Console.WriteLine($"Unexpected: {ex.Message}"); // catch-all fallback
}
finally
{
    Console.WriteLine("This always runs — good for cleanup (close files, etc.)");
}

// Custom exception
public class InsufficientFundsException : Exception
{
    public decimal RequiredAmount { get; }
    public InsufficientFundsException(decimal amount)
        : base($"Need {amount:C} more in your account.") =&gt; RequiredAmount = amount;
}
    </div>

    <div class="card-section-title">8. PATTERN MATCHING (C# 7–12)</div>
    <b>Technical:</b> Pattern matching allows conditional logic based on the shape/type/value of
    data using is, switch expressions, property patterns, list patterns, and relational patterns.<br>
    <b>🏠 Layman:</b> Pattern matching is like a smart sorting machine at a post office. Instead
    of writing many separate "if it's a large box, do X; if it's a small envelope, do Y" rules,
    you write one clear set of patterns and the machine routes each parcel automatically.<br>
    <div class="cmd-block">
object shape = new Circle(5.0);

// Type pattern (C# 7)
if (shape is Circle c)
    Console.WriteLine($"Area: {Math.PI * c.Radius * c.Radius:F2}");

// Switch expression with property pattern (C# 8)
double area = shape switch
{
    Circle    { Radius: var r }              =&gt; Math.PI * r * r,
    Rectangle { Width: var w, Height: var h } =&gt; w * h,
    Triangle  { Base: var b, Height: var h }  =&gt; 0.5 * b * h,
    null =&gt; throw new ArgumentNullException(nameof(shape)),
    _    =&gt; throw new NotSupportedException("Unknown shape")
};

// List pattern (C# 11)
int[] nums = { 1, 2, 3 };
string desc = nums switch
{
    []          =&gt; "empty",
    [var x]     =&gt; $"single: {x}",
    [1, 2, ..]  =&gt; "starts with 1, 2",
    _           =&gt; "other"
};
    </div>

  </div>
</div>
""",
            unsafe_allow_html=True,
        )

      elif section == "Topic Suggestions":
        db_available = _get_supabase_client() is not None
        st.markdown(
            """
<div class="content-card">
  <div class="card-title">📊 Topic Suggestions</div>
  <div class="card-body">
    See which topics the community is requesting most. Use the
    <strong>Add your suggested topic</strong> button in the sidebar to vote for a
    new topic — the most-requested ones will be added to the learning hub.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        if not db_available:
            st.info(
                "ℹ️  No database credentials configured. "
                "Connect Supabase to persist and display community topic suggestions."
            )
        else:
            rows = fetch_topic_suggestions()
            if not rows:
                st.info("No topic suggestions yet. Be the first to suggest one!")
            else:
                from collections import Counter
                counts = Counter(r["topic"] for r in rows if r.get("topic"))
                sorted_topics = counts.most_common()
                st.markdown("### 🏆 Most-Requested Topics")
                for rank, (topic, count) in enumerate(sorted_topics, start=1):
                    import re
                    hashtag = "#" + re.sub(r"[^a-zA-Z0-9]", "", topic.replace("&", "and").replace("+", "plus"))
                    req_label = "request" if count == 1 else "requests"
                    st.markdown(
                        f"**{rank}.** {topic} &nbsp; `{hashtag}` &nbsp; — &nbsp; "
                        f"**{count}** {req_label}",
                        unsafe_allow_html=True,
                    )

    st.markdown(_footer_html(), unsafe_allow_html=True)
    components.html(_scroll_nav_html(), height=0)
    components.html(_copy_buttons_html(), height=0)


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

