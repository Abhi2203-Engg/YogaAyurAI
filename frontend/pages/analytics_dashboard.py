"""
Analytics Dashboard Page
Visual insights drawn from the AyurGenixAI dataset.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from backend.data_loader import load_data
from backend.analytics import (
    dosha_distribution,
    severity_distribution,
    age_group_distribution,
    gender_distribution,
    seasonal_variation,
    top_ayurvedic_herbs,
    stress_sleep_counts,
    top_diseases_by_symptom_count,
)
from frontend.ui_helpers import inject_css, section_header, metric_card


def render():
    inject_css()
    df = load_data()

    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("Data-driven insights from the AyurGenixAI knowledge base.")
    st.markdown("---")

    # ── Summary metrics ──────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Records", str(len(df)))
    with c2:
        metric_card("Unique Diseases", str(df["Disease"].nunique()))
    with c3:
        metric_card("Severity Levels", str(df["Symptom Severity"].nunique()))
    with c4:
        metric_card("Age Groups", str(df["Age Group"].nunique()))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Dosha & Severity ──────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        section_header("☯", "Dosha Distribution")
        dosha_df = dosha_distribution(df)
        fig = px.pie(
            dosha_df, names="Dosha", values="Count",
            color="Dosha",
            color_discrete_map={"Vata": "#7E57C2", "Pitta": "#EF5350", "Kapha": "#26A69A"},
            hole=0.4,
        )
        fig.update_layout(margin=dict(t=10, b=10), height=280,
                          legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("⚠️", "Symptom Severity")
        sev_df = severity_distribution(df)
        fig2 = px.bar(
            sev_df, x="Count", y="Severity", orientation="h",
            color="Severity",
            color_discrete_sequence=px.colors.qualitative.Safe,
            text="Count",
        )
        fig2.update_layout(showlegend=False, margin=dict(t=10, b=10),
                           height=280, yaxis_title="")
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2: Age & Gender ──────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        section_header("👶", "Age Group Distribution")
        age_df = age_group_distribution(df)
        fig3 = px.bar(
            age_df, x="Age Group", y="Count",
            color="Count", color_continuous_scale="Blues",
            text="Count",
        )
        fig3.update_layout(showlegend=False, margin=dict(t=10, b=10),
                           height=280, coloraxis_showscale=False)
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        section_header("⚧", "Gender Split")
        gen_df = gender_distribution(df)
        fig4 = px.pie(
            gen_df, names="Gender", values="Count",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig4.update_layout(margin=dict(t=10, b=10), height=280,
                           legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig4, use_container_width=True)

    # ── Top herbs ────────────────────────────────────────────
    section_header("🌿", "Top 15 Ayurvedic Herbs")
    herbs_df = top_ayurvedic_herbs(15)
    fig5 = px.bar(
        herbs_df.sort_values("Count"),
        x="Count", y="Herb", orientation="h",
        color="Count", color_continuous_scale="Greens",
        text="Count",
    )
    fig5.update_layout(showlegend=False, margin=dict(t=10, b=10),
                       height=420, coloraxis_showscale=False, yaxis_title="")
    fig5.update_traces(textposition="outside")
    st.plotly_chart(fig5, use_container_width=True)

    # ── Seasonal variation ───────────────────────────────────
    section_header("🍂", "Seasonal Disease Variation")
    season_df = seasonal_variation(df)
    fig6 = px.bar(
        season_df, x="Season", y="Count",
        color="Season",
        color_discrete_sequence=px.colors.qualitative.Set3,
        text="Count",
    )
    fig6.update_layout(showlegend=False, margin=dict(t=10, b=10), height=300)
    fig6.update_traces(textposition="outside")
    st.plotly_chart(fig6, use_container_width=True)

    # ── Stress & Sleep ───────────────────────────────────────
    col5, col6 = st.columns(2)
    ss = stress_sleep_counts(df)

    with col5:
        section_header("😓", "Stress Level Profile")
        stress_df = _dict_to_df(ss["stress"], "Stress Level", "Count")
        fig7 = px.pie(
            stress_df, names="Stress Level", values="Count",
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        fig7.update_layout(margin=dict(t=10, b=10), height=280,
                           legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig7, use_container_width=True)

    with col6:
        section_header("😴", "Sleep Pattern Profile")
        sleep_df = _dict_to_df(ss["sleep"], "Sleep Pattern", "Count")
        fig8 = px.bar(
            sleep_df, x="Sleep Pattern", y="Count",
            color="Count", color_continuous_scale="Purples",
            text="Count",
        )
        fig8.update_layout(showlegend=False, margin=dict(t=10, b=10),
                           height=280, coloraxis_showscale=False)
        fig8.update_traces(textposition="outside")
        st.plotly_chart(fig8, use_container_width=True)

    # ── Diseases by symptom count ────────────────────────────
    section_header("📋", "Diseases by Number of Symptoms")
    symp_df = top_diseases_by_symptom_count(20)
    fig9 = px.bar(
        symp_df.sort_values("Symptom Count"),
        x="Symptom Count", y="Disease", orientation="h",
        color="Symptom Count", color_continuous_scale="Oranges",
        text="Symptom Count",
    )
    fig9.update_layout(showlegend=False, margin=dict(t=10, b=10),
                       height=550, coloraxis_showscale=False, yaxis_title="")
    fig9.update_traces(textposition="outside")
    st.plotly_chart(fig9, use_container_width=True)

    # ── Full data table ──────────────────────────────────────
    with st.expander("🗃️ View Raw Dataset"):
        st.dataframe(df, use_container_width=True, height=400)
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="AyurGenixAI_Dataset.csv",
            mime="text/csv",
        )


def _dict_to_df(d: dict, key_col: str, val_col: str):
    import pandas as pd
    return pd.DataFrame(list(d.items()), columns=[key_col, val_col])
