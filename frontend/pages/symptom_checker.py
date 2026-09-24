"""
Symptom Checker Page
Enter symptoms → get ranked disease matches with Ayurvedic insights.
"""

import streamlit as st
from backend.data_loader import load_data, get_all_symptoms
from backend.recommendation_engine import search_by_symptoms
from frontend.ui_helpers import (
    inject_css, section_header, badges_from_csv, severity_badge
)


def render():
    inject_css()
    df = load_data()

    st.markdown("## 🔍 Symptom Checker")
    st.markdown(
        "Describe your symptoms in plain language or pick from the suggestions below. "
        "YogaAyurAI will match them against the Ayurvedic knowledge base and rank the most relevant conditions."
    )
    st.markdown("---")

    # ── Symptom input ────────────────────────────────────────
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        symptom_query = st.text_input(
            "Enter your symptoms",
            placeholder="e.g. severe headache, nausea, light sensitivity",
            label_visibility="collapsed",
        )
    with col_btn:
        search_clicked = st.button("🔎 Search", use_container_width=True, type="primary")

    # Quick-pick chips
    all_symptoms = get_all_symptoms(df)
    st.markdown("**Quick picks:**")
    selected_chips = st.multiselect(
        "Select known symptoms",
        options=all_symptoms,
        default=[],
        label_visibility="collapsed",
        placeholder="Choose one or more symptoms …",
    )
    if selected_chips:
        chip_query = ", ".join(selected_chips)
        if st.button("➕ Add to search", key="chip_add"):
            symptom_query = chip_query + (", " + symptom_query if symptom_query else "")

    combined_query = (
        symptom_query + (", " + ", ".join(selected_chips) if selected_chips and not search_clicked else "")
        if not search_clicked
        else symptom_query
    )
    if selected_chips and not symptom_query:
        combined_query = ", ".join(selected_chips)

    st.markdown("---")

    if not combined_query.strip() and not search_clicked:
        st.info("👆 Type or select symptoms above and press **Search** to begin.")
        _show_examples()
        return

    if combined_query.strip():
        with st.spinner("Analysing symptoms …"):
            results = search_by_symptoms(combined_query, top_n=12)

        if results.empty:
            st.warning("No matching conditions found. Try different or broader symptom terms.")
            return

        section_header("📋", f"Top {len(results)} Matching Conditions")

        for i, row in results.iterrows():
            score_pct = int(row["_score"] * 100)
            with st.expander(
                f"**{row['Disease']}** &nbsp;·&nbsp; {row.get('Hindi Name','')} &nbsp;|&nbsp; Match: {score_pct}%",
                expanded=(i == 0),
            ):
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(f"**Symptoms:** {row['Symptoms']}")
                    st.markdown(
                        f"**Severity:** {severity_badge(str(row.get('Symptom Severity', '')))}",
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Duration:** {row.get('Duration of Treatment', 'N/A')}")
                    st.markdown(
                        "**Doshas:** " + badges_from_csv(row.get("Doshas", ""), "purple"),
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        "**Ayurvedic Herbs:** " + badges_from_csv(row.get("Ayurvedic Herbs", ""), "green"),
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "**Yoga Therapy:** " + badges_from_csv(row.get("Yoga & Physical Therapy", ""), "teal"),
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Prognosis:** {row.get('Prognosis', 'N/A')}")

                st.markdown("**Diet & Lifestyle:** " + str(row.get("Diet and Lifestyle Recommendations", "")))

                # Confidence bar
                st.progress(min(score_pct / 100, 1.0), text=f"Relevance: {score_pct}%")


def _show_examples():
    st.markdown("#### 💡 Example Searches")
    examples = [
        "frequent urination, fatigue, weight gain",
        "joint pain, swelling, stiffness",
        "severe headache, nausea",
        "itchy rash, redness",
        "difficulty sleeping, restlessness",
    ]
    cols = st.columns(len(examples))
    for col, ex in zip(cols, examples):
        with col:
            st.markdown(
                f'<div style="background:#F1F8E9;border-radius:8px;padding:8px 12px;'
                f'font-size:0.82rem;color:#1B5E20;border:1px solid #C8E6C9;">{ex}</div>',
                unsafe_allow_html=True,
            )
