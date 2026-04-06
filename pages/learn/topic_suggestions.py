import streamlit as st
from services.supabase_client import _get_supabase_client, fetch_topic_suggestions


def render_topic_suggestions():
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

