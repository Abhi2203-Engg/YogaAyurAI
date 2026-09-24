"""
YogaAyurAI — Main Streamlit Application
Run with:  streamlit run app.py
"""

import streamlit as st
from frontend.ui_helpers import set_page_config, inject_css

# ── Must be first Streamlit call ─────────────────────────
set_page_config()
inject_css()

# ── Sidebar navigation ────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:16px 0 10px 0;">
            <span style="font-size:2.5rem;">🌿</span><br>
            <span style="font-size:1.3rem;font-weight:700;letter-spacing:0.03em;">YogaAyurAI</span><br>
            <span style="font-size:0.78rem;opacity:0.75;">Ayurvedic Intelligence</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    pages = {
        "🏠  Home": "home",
        "🔍  Symptom Checker": "symptom_checker",
        "📋  Disease Explorer": "disease_explorer",
        "🧘  Yoga & Diet Advisor": "yoga_diet_advisor",
        "📊  Analytics Dashboard": "analytics_dashboard",
    }

    selection = st.radio(
        "Navigate",
        list(pages.keys()),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;opacity:0.7;text-align:center;'>"
        "Powered by AyurGenixAI Dataset<br>"
        "v1.0.0 · For educational use only"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Route to page ─────────────────────────────────────────
page_key = pages[selection]

if page_key == "home":
    from frontend.pages.home import render
elif page_key == "symptom_checker":
    from frontend.pages.symptom_checker import render
elif page_key == "disease_explorer":
    from frontend.pages.disease_explorer import render
elif page_key == "yoga_diet_advisor":
    from frontend.pages.yoga_diet_advisor import render
elif page_key == "analytics_dashboard":
    from frontend.pages.analytics_dashboard import render

render()
