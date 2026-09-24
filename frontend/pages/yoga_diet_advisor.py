"""
Yoga & Diet Advisor Page
Personalised recommendations based on disease, dosha, age, and gender.
"""

import streamlit as st
from backend.data_loader import load_data, get_all_diseases, get_all_doshas
from backend.recommendation_engine import get_recommendations
from frontend.ui_helpers import (
    inject_css, section_header, info_card, badges_from_csv, badge, hero
)

YOGA_BENEFITS = {
    "Pranayama": "Regulates breath and calms the nervous system.",
    "Anulom Vilom": "Balances left and right brain hemispheres; relieves stress.",
    "Kapalbhati": "Detoxifies lungs and improves digestive fire (Agni).",
    "Surya Namaskar": "Full-body activation; boosts metabolism and circulation.",
    "Meditation": "Reduces cortisol; deepens mind-body connection.",
    "Yoga Nidra": "Deeply restorative sleep yoga; relieves insomnia.",
    "Paschimottanasana": "Stretches spine and hamstrings; aids digestion.",
    "Trikonasana": "Strengthens legs and core; opens hip flexors.",
}

DOSHA_DIET_TIPS = {
    "Vata": [
        "Favour warm, oily, and grounding foods (soups, stews, ghee).",
        "Eat at regular meal times; avoid raw and cold food.",
        "Prefer sweet, sour, and salty tastes.",
        "Stay well hydrated with warm herbal teas.",
    ],
    "Pitta": [
        "Choose cooling, sweet, and bitter foods (cucumber, mint, coconut).",
        "Avoid spicy, acidic, and fermented foods.",
        "Eat meals in a calm environment; avoid skipping meals.",
        "Cool drinks (room-temperature) are preferred over hot.",
    ],
    "Kapha": [
        "Choose light, dry, and warm foods (legumes, leafy greens).",
        "Avoid heavy, oily, cold, and sweet foods.",
        "Eat smaller portions; largest meal at midday.",
        "Favour pungent, bitter, and astringent tastes.",
    ],
}


def render():
    inject_css()
    df = load_data()

    hero("🧘 Yoga & Diet Advisor", "Personalised Ayurvedic wellness plans for your condition and constitution.")

    # ── Profile form ─────────────────────────────────────────
    with st.form("profile_form"):
        st.markdown("#### 👤 Your Health Profile")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            disease = st.selectbox("Condition / Disease", ["— Select —"] + get_all_diseases(df))
        with c2:
            dosha = st.selectbox("Your Dosha (Prakriti)", ["— Select —", "Vata", "Pitta", "Kapha"])
        with c3:
            age_opts = sorted(df["Age Group"].dropna().unique().tolist())
            age_group = st.selectbox("Age Group", ["— Select —"] + age_opts)
        with c4:
            gender = st.selectbox("Gender", ["— Select —", "Male", "Female", "All genders"])

        submitted = st.form_submit_button("🌿 Generate My Plan", use_container_width=True, type="primary")

    if not submitted:
        _show_dosha_guide()
        return

    if disease == "— Select —":
        st.warning("Please select a condition to generate your plan.")
        _show_dosha_guide()
        return

    ag = "" if age_group == "— Select —" else age_group
    gn = "" if gender == "— Select —" else gender
    ds = "" if dosha == "— Select —" else dosha

    rec = get_recommendations(disease, age_group=ag, gender=gn, dosha=ds)
    if not rec:
        st.error("Could not load recommendations. Please try another disease.")
        return

    st.markdown("---")

    # ── Yoga plan ────────────────────────────────────────────
    section_header("🧘", "Recommended Yoga & Physical Therapy")
    yoga_str = rec.get("yoga", "")
    yoga_practices = [y.strip() for y in yoga_str.split(",") if y.strip() and y.strip().lower() != "nan"]

    if yoga_practices:
        cols = st.columns(min(len(yoga_practices), 3))
        for idx, practice in enumerate(yoga_practices):
            with cols[idx % 3]:
                desc = YOGA_BENEFITS.get(practice, "A beneficial Ayurvedic yoga practice.")
                st.markdown(
                    f"""<div style="background:#E8F5E9;border-radius:10px;padding:14px;
                    border-left:4px solid #2E7D32;margin-bottom:10px;">
                    <strong>🧘 {practice}</strong><br>
                    <span style="font-size:0.85rem;color:#555;">{desc}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )
    else:
        st.info("No specific yoga therapy listed for this condition.")

    st.markdown("---")

    # ── Diet plan ────────────────────────────────────────────
    section_header("🥗", "Diet & Lifestyle Recommendations")

    c_diet, c_dosha = st.columns([3, 2])

    with c_diet:
        info_card("Condition-Specific Diet", rec.get("diet", "N/A"))
        info_card("Dietary Habits Advised", rec.get("dietary_habits", "N/A"))
        info_card("Patient Recommendations", rec.get("patient_recommendations", "N/A"))

        st.markdown(
            "**Foods to be aware of (allergies / sensitivities):** "
            + badges_from_csv(rec.get("ayurvedic_herbs", ""), "amber"),
            unsafe_allow_html=True,
        )

    with c_dosha:
        resolved_dosha = ds if ds else (rec.get("doshas", "").split(",")[0].strip())
        if resolved_dosha in DOSHA_DIET_TIPS:
            st.markdown(f"#### ☯ {resolved_dosha} Dosha Diet Tips")
            for tip in DOSHA_DIET_TIPS[resolved_dosha]:
                st.markdown(f"✅ {tip}")
        else:
            st.info("Select your Dosha above to see constitution-specific diet tips.")

    st.markdown("---")

    # ── Herbal remedies ──────────────────────────────────────
    section_header("🌿", "Ayurvedic Herbs & Formulations")
    c_herb1, c_herb2 = st.columns(2)
    with c_herb1:
        info_card("Recommended Herbs", rec.get("ayurvedic_herbs", "N/A"))
        info_card("Formulation / Dosage", rec.get("formulation", "N/A"))
    with c_herb2:
        info_card("Herbal / Alternative Remedies", rec.get("herbal_remedies", "N/A"))
        info_card("Seasonal Consideration", rec.get("seasonal_variation", "N/A"))

    st.caption(
        "⚠️ *Herbal formulations should be taken under the guidance of a certified Ayurvedic practitioner.*"
    )


def _show_dosha_guide():
    """Show a quick dosha guide when no disease is selected."""
    st.markdown("---")
    section_header("☯", "Understanding Your Dosha (Prakriti)")
    c1, c2, c3 = st.columns(3)
    dosha_info = {
        "Vata": ("🌬️", "#7E57C2", "#EDE7F6",
                 "Air & Space — governs movement, creativity and nerve impulses.",
                 ["Dry skin, cold hands/feet", "Light sleeper", "Creative but anxious", "Irregular digestion"]),
        "Pitta": ("🔥", "#EF5350", "#FFEBEE",
                  "Fire & Water — governs metabolism, digestion and transformation.",
                  ["Medium build, warm body", "Strong digestion", "Sharp intellect", "Prone to inflammation"]),
        "Kapha": ("🌊", "#26A69A", "#E0F2F1",
                  "Earth & Water — governs structure, immunity and lubrication.",
                  ["Stocky build, soft skin", "Calm temperament", "Strong memory", "Prone to weight gain"]),
    }
    for col, (dosha, (icon, colour, bg, desc, traits)) in zip([c1, c2, c3], dosha_info.items()):
        with col:
            trait_html = "".join(f"<li>{t}</li>" for t in traits)
            st.markdown(
                f"""<div style="background:{bg};border-radius:12px;padding:16px;
                border-top:4px solid {colour};">
                <h4 style="color:{colour};margin:0 0 6px 0;">{icon} {dosha}</h4>
                <p style="font-size:0.85rem;color:#333;margin:0 0 8px 0;">{desc}</p>
                <ul style="font-size:0.82rem;color:#444;padding-left:18px;margin:0;">{trait_html}</ul>
                </div>""",
                unsafe_allow_html=True,
            )
