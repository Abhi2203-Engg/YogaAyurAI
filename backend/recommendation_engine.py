"""
Search & Recommendation Engine
Provides symptom-based search, fuzzy matching and
personalised Ayurvedic recommendations.
"""

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.data_loader import load_data


# ─────────────────────────────────────────────
# Symptom-based disease lookup
# ─────────────────────────────────────────────

def search_by_symptoms(symptom_input: str, top_n: int = 10) -> pd.DataFrame:
    """
    Given a free-text symptom query, return the top-N matching diseases
    ranked by TF-IDF cosine similarity plus a fuzzy bonus.
    """
    df = load_data()
    if not symptom_input.strip():
        return pd.DataFrame()

    corpus = df["Symptoms"].fillna("").tolist()
    query = symptom_input.lower().strip()

    # TF-IDF similarity
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([s.lower() for s in corpus] + [query])
    cosine_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

    # Fuzzy ratio bonus (normalised 0-1)
    fuzzy_scores = np.array([
        fuzz.partial_ratio(query, s.lower()) / 100.0
        for s in corpus
    ])

    combined = 0.7 * cosine_scores + 0.3 * fuzzy_scores

    df = df.copy()
    df["_score"] = combined
    results = df[df["_score"] > 0.05].sort_values("_score", ascending=False).head(top_n)
    return results.reset_index(drop=True)


# ─────────────────────────────────────────────
# Fuzzy disease name search
# ─────────────────────────────────────────────

def fuzzy_search_disease(query: str, top_n: int = 8) -> list[str]:
    """Return disease names closest to the user query."""
    df = load_data()
    diseases = df["Disease"].unique().tolist()
    scored = [(d, fuzz.token_sort_ratio(query.lower(), d.lower())) for d in diseases]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [d for d, score in scored if score >= 35][:top_n]


# ─────────────────────────────────────────────
# Personalised recommendations
# ─────────────────────────────────────────────

def get_recommendations(
    disease_name: str,
    age_group: str = "",
    gender: str = "",
    dosha: str = "",
) -> dict:
    """
    Return a structured recommendations dict for a disease, optionally
    filtered/enriched by patient profile (age, gender, dosha).
    """
    df = load_data()
    rows = df[df["Disease"].str.lower() == disease_name.lower()]
    if rows.empty:
        return {}

    # Try to find a row that best matches the profile
    row = _best_profile_match(rows, age_group, gender, dosha)

    return {
        "disease": row.get("Disease", ""),
        "hindi_name": row.get("Hindi Name", ""),
        "marathi_name": row.get("Marathi Name", ""),
        "symptoms": row.get("Symptoms", ""),
        "diagnosis": row.get("Diagnosis & Tests", ""),
        "severity": row.get("Symptom Severity", ""),
        "duration": row.get("Duration of Treatment", ""),
        "risk_factors": row.get("Risk Factors", ""),
        "doshas": row.get("Doshas", ""),
        "prakriti": row.get("Constitution/Prakriti", ""),
        "ayurvedic_herbs": row.get("Ayurvedic Herbs", ""),
        "formulation": row.get("Formulation", ""),
        "herbal_remedies": row.get("Herbal/Alternative Remedies", ""),
        "diet": row.get("Diet and Lifestyle Recommendations", ""),
        "yoga": row.get("Yoga & Physical Therapy", ""),
        "medical_intervention": row.get("Medical Intervention", ""),
        "prevention": row.get("Prevention", ""),
        "prognosis": row.get("Prognosis", ""),
        "complications": row.get("Complications", ""),
        "patient_recommendations": row.get("Patient Recommendations", ""),
        "sleep_patterns": row.get("Sleep Patterns", ""),
        "stress_levels": row.get("Stress Levels", ""),
        "seasonal_variation": row.get("Seasonal Variation", ""),
        "dietary_habits": row.get("Dietary Habits", ""),
        "environmental_factors": row.get("Environmental Factors", ""),
        "current_medications": row.get("Current Medications", ""),
    }


def _best_profile_match(rows: pd.DataFrame, age_group: str, gender: str, dosha: str) -> dict:
    """Score each row for how well it matches the user profile and return the best."""
    if len(rows) == 1:
        return rows.iloc[0].to_dict()

    scores = []
    for _, row in rows.iterrows():
        score = 0
        if age_group and age_group.lower() in str(row.get("Age Group", "")).lower():
            score += 2
        if gender and gender.lower() in str(row.get("Gender", "")).lower():
            score += 2
        if dosha and dosha.lower() in str(row.get("Doshas", "")).lower():
            score += 3
        scores.append(score)

    best_idx = int(np.argmax(scores))
    return rows.iloc[best_idx].to_dict()


# ─────────────────────────────────────────────
# Similar diseases
# ─────────────────────────────────────────────

def get_similar_diseases(disease_name: str, top_n: int = 5) -> pd.DataFrame:
    """Return diseases with the most symptom overlap."""
    df = load_data()
    target_rows = df[df["Disease"].str.lower() == disease_name.lower()]
    if target_rows.empty:
        return pd.DataFrame()

    target_symptoms = target_rows.iloc[0]["Symptoms"].lower()
    return search_by_symptoms(target_symptoms, top_n=top_n + 1)
