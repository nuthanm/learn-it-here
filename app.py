import streamlit as st
from config import LEARN_MENU_ITEMS, LATEST_NEW_TOPIC, init_session_state
from components.css import inject_css
from pages.landing import page_landing
from pages.requirements import page_requirements
from pages.learn import page_learn

st.set_page_config(
    page_title="Learn It Here 🐼",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()

# Logo-click navigation
if st.query_params.get("go") == "home":
    del st.query_params["go"]
    if st.session_state.get("page") != "landing":
        st.session_state.page = "landing"
        st.rerun()

inject_css()

page = st.session_state.page
if page == "requirements":
    page_requirements()
elif page == "learn":
    page_learn()
else:
    page_landing()
