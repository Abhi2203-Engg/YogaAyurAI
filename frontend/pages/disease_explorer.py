"""
Disease Explorer Page
Browse all diseases, filter, and view deep Ayurvedic profiles.
"""

import streamlit as st
from backend.data_loader import load_data, get_all_diseases, get_all_doshas
from backend.recommendation_engine import get_recommendations, get_similar_diseases, fuzzy_search_disease
from frontend.ui_helpers import (
    inject_css, section_header, info_card, badges_from_csv, severity_badge, badge
)


def render():
    inject_css()
    df = load_data()

    st.markdown("## 📋 Disease Explorer")
    st.markdown(
        "Browse 100+ diseases from the Ayurvedic knowledge base. "
        "Filter by severity, dosha, or age group — then click any disease for its full profile."
    )
    st.markdown("---")

    # ── Filters sidebar ──────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔧 Filters")
        severity_options = ["All"] + sorted(df["Symptom Severity"].dropna().unique().tolist())
        sel_severity = st.selectbox("Severity", severity_options)

        dosha_options = ["All"] + get_all_doshas(df)
        sel_dosha = st.selectbox("Dosha", dosha_options)

        age_options = ["All"] + sorted(df["Age Group"].dropna().unique().tolist())
        sel_age = st.selectbox("Age Group", age_options)

        gender_options = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
        sel_gender = st.selectbox("Gender", gender_options)

    # ── Apply filters ────────────────────────────────────────
    filtered = df.copy()
    if sel_severity != "All":
        filtered = filtered[filtered["Symptom Severity"] == sel_severity]
    if sel_dosha != "All":
        filtered = filtered[filtered["Doshas"].str.contains(sel_dosha, na=False)]
    if sel_age != "All":
        filtered = filtered[filtered["Age Group"] == sel_age]
    if sel_gender != "All":
        filtered = filtered[filtered["Gender"].str.contains(sel_gender, na=False)]

    # ── Search bar ───────────────────────────────────────────
    search_term = st.text_input(
        "Search diseases",
        placeholder="Type a disease name …",
        label_visibility="visible",
    )
    if search_term:
        suggestions = fuzzy_search_disease(search_term, top_n=20)
        filtered = filtered[filtered["Disease"].isin(suggestions)]

    disease_list = get_all_diseases(filtered)
    st.caption(f"Showing {len(disease_list)} diseases")

    if not disease_list:
        st.warning("No diseases match the current filters.")
        return

    # ── Disease grid / selector ──────────────────────────────
    col_list, col_detail = st.columns([1, 2])

    with col_list:
        selected_disease = st.radio(
            "Select a disease",
            options=disease_list,
            label_visibility="collapsed",
        )

    with col_detail:
        if selected_disease:
            _render_disease_detail(selected_disease)


def _render_disease_detail(disease_name: str):
    rec = get_recommendations(disease_name)
    if not rec:
        st.error("Could not load data for this disease.")
        return

    # ── Title & names ────────────────────────────────────────
    st.markdown(
        f"### 🌿 {rec['disease']}  "
        f"<span style='font-size:0.9rem;color:#555;'>({rec['hindi_name']} / {rec['marathi_name']})</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Severity:** {severity_badge(rec['severity'])}  &nbsp;&nbsp; "
        f"**Duration:** `{rec['duration']}`  &nbsp;&nbsp; "
        f"**Prakriti:** {badge(rec['prakriti'], 'purple')}",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🩺 Clinical", "🌿 Ayurveda", "🧘 Yoga & Diet", "⚕️ Medical"])

    # ── Tab 1 : Clinical ─────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            info_card("Symptoms", rec["symptoms"])
            info_card("Diagnosis & Tests", rec["diagnosis"])
            info_card("Risk Factors", rec["risk_factors"])
        with c2:
            info_card("Sleep Patterns", rec["sleep_patterns"])
            info_card("Stress Levels", rec["stress_levels"])
            info_card("Environmental Factors", rec["environmental_factors"])
        info_card("Prognosis", rec["prognosis"])
        info_card("Complications", rec["complications"])

    # ── Tab 2 : Ayurveda ─────────────────────────────────────
    with tab2:
        st.markdown(
            "**Doshas:** " + badges_from_csv(rec["doshas"], "purple"),
            unsafe_allow_html=True,
        )
        st.markdown(
            "**Ayurvedic Herbs:** " + badges_from_csv(rec["ayurvedic_herbs"], "green"),
            unsafe_allow_html=True,
        )
        info_card("Formulation", rec["formulation"])
        info_card("Herbal / Alternative Remedies", rec["herbal_remedies"])
        info_card("Seasonal Variation", rec["seasonal_variation"])

    # ── Tab 3 : Yoga & Diet ──────────────────────────────────
    with tab3:
        st.markdown(
            "**Yoga & Physical Therapy:** " + badges_from_csv(rec["yoga"], "teal"),
            unsafe_allow_html=True,
        )
        st.markdown("")
        info_card("Diet & Lifestyle Recommendations", rec["diet"])
        info_card("Dietary Habits", rec["dietary_habits"])
        info_card("Patient Recommendations", rec["patient_recommendations"])

    # ── Tab 4 : Medical ──────────────────────────────────────
    with tab4:
        info_card("Medical Intervention", rec["medical_intervention"])
        info_card("Current Medications", rec["current_medications"])
        info_card("Prevention", rec["prevention"])

    # ── Similar diseases ─────────────────────────────────────
    st.markdown("---")
    section_header("🔗", "Similar Conditions")
    similar = get_similar_diseases(disease_name, top_n=5)
    if not similar.empty:
        # exclude itself
        similar = similar[similar["Disease"].str.lower() != disease_name.lower()]
        for _, row in similar.head(5).iterrows():
            st.markdown(
                f"• **{row['Disease']}** — _{row['Symptoms'][:80]}…_"
            )
    else:
        st.caption("No similar conditions found.")
