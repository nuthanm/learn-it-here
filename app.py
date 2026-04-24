import streamlit as st
from config import LEARN_MENU_ITEMS, LATEST_NEW_TOPIC, PAGE_REQUIREMENTS, PAGE_LEARN, init_session_state
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

# URL routing: on a fresh load, honour the ?page= query param
_url_page = st.query_params.get("page")
if _url_page in (PAGE_REQUIREMENTS, PAGE_LEARN) and st.session_state.page == "landing":
    st.session_state.page = _url_page

# Logo-click navigation
if st.query_params.get("go") == "home":
    del st.query_params["go"]
    if "page" in st.query_params:
        del st.query_params["page"]
    if st.session_state.get("page") != "landing":
        st.session_state.page = "landing"
        st.rerun()

inject_css()

page = st.session_state.page
if page == PAGE_REQUIREMENTS:
    page_requirements()
elif page == PAGE_LEARN:
    page_learn()
else:
    page_landing()
