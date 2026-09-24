"""
Home / Landing Page
"""

import streamlit as st
import plotly.express as px
from backend.data_loader import load_data
from backend.analytics import dosha_distribution, severity_distribution, top_ayurvedic_herbs
from frontend.ui_helpers import hero, section_header, metric_card, inject_css


def render():
    inject_css()
    df = load_data()

    hero(
        "🌿 YogaAyurAI",
        "Ancient Ayurvedic Wisdom powered by Modern AI — discover personalised healing for body, mind & spirit.",
    )

    # ── Quick stats ──────────────────────────────────────────
    total_diseases = df["Disease"].nunique()
    total_herbs = sum(
        len([h.strip() for h in str(r).split(",") if h.strip()])
        for r in df["Ayurvedic Herbs"].dropna()
    )
    total_yoga = sum(
        len([y.strip() for y in str(r).split(",") if y.strip()])
        for r in df["Yoga & Physical Therapy"].dropna()
    )
    doshas_count = 3  # Vata, Pitta, Kapha

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("🏥 Diseases Covered", str(total_diseases))
    with c2:
        metric_card("🌱 Herb References", str(total_herbs))
    with c3:
        metric_card("🧘 Yoga Therapies", str(total_yoga))
    with c4:
        metric_card("☯ Doshas", str(doshas_count))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ───────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        section_header("☯", "Dosha Distribution")
        dosha_df = dosha_distribution(df)
        fig = px.pie(
            dosha_df,
            names="Dosha",
            values="Count",
            color="Dosha",
            color_discrete_map={"Vata": "#7E57C2", "Pitta": "#EF5350", "Kapha": "#26A69A"},
            hole=0.45,
        )
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", y=-0.1),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        section_header("⚠️", "Symptom Severity Spread")
        sev_df = severity_distribution(df)
        fig2 = px.bar(
            sev_df,
            x="Severity",
            y="Count",
            color="Severity",
            color_discrete_sequence=px.colors.qualitative.Set2,
            text="Count",
        )
        fig2.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Diseases",
            margin=dict(t=10, b=10),
            height=300,
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Top herbs chart ──────────────────────────────────────
    section_header("🌿", "Most Commonly Recommended Ayurvedic Herbs")
    herbs_df = top_ayurvedic_herbs(15)
    fig3 = px.bar(
        herbs_df.sort_values("Count"),
        x="Count",
        y="Herb",
        orientation="h",
        color="Count",
        color_continuous_scale="Greens",
        text="Count",
    )
    fig3.update_layout(
        showlegend=False,
        xaxis_title="Frequency",
        yaxis_title="",
        margin=dict(t=10, b=10),
        height=420,
        coloraxis_showscale=False,
    )
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

    # ── About section ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("ℹ️", "About YogaAyurAI")
    st.markdown(
        """
        **YogaAyurAI** bridges the timeless science of Ayurveda with the power of data-driven AI to help you:

        | Feature | Description |
        |---|---|
        | 🔍 **Symptom Checker** | Enter symptoms to identify potential diseases and receive Ayurvedic guidance |
        | 📋 **Disease Explorer** | Browse the full dataset of 100+ diseases with deep Ayurvedic profiles |
        | 🧘 **Yoga & Diet Advisor** | Get personalised yoga routines and diet plans based on your Dosha & condition |
        | 📊 **Analytics Dashboard** | Visual insights into disease patterns, herbs, and treatment trends |

        > *Disclaimer: This app is for educational and informational purposes only. Always consult a qualified healthcare professional.*
        """,
        unsafe_allow_html=False,
    )
