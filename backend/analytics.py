"""
Analytics Module
Generates dataset insights for the dashboard.
"""

import pandas as pd
from backend.data_loader import load_data


def top_diseases_by_symptom_count(n: int = 15) -> pd.DataFrame:
    """Count the number of unique symptoms per disease."""
    df = load_data()
    records = []
    for _, row in df.iterrows():
        symptoms = [s.strip() for s in str(row["Symptoms"]).split(",") if s.strip()]
        records.append({"Disease": row["Disease"], "Symptom Count": len(symptoms)})
    result = (
        pd.DataFrame(records)
        .groupby("Disease")["Symptom Count"]
        .max()
        .reset_index()
        .sort_values("Symptom Count", ascending=False)
        .head(n)
    )
    return result


def dosha_distribution(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_data()
    counts = {}
    for d in df["Doshas"].dropna():
        for part in d.split(","):
            key = part.strip()
            if key:
                counts[key] = counts.get(key, 0) + 1
    return pd.DataFrame(list(counts.items()), columns=["Dosha", "Count"]).sort_values(
        "Count", ascending=False
    )


def severity_distribution(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_data()
    counts = df["Symptom Severity"].value_counts().reset_index()
    counts.columns = ["Severity", "Count"]
    return counts


def age_group_distribution(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_data()
    counts = df["Age Group"].value_counts().reset_index()
    counts.columns = ["Age Group", "Count"]
    return counts


def gender_distribution(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_data()
    counts = df["Gender"].value_counts().reset_index()
    counts.columns = ["Gender", "Count"]
    return counts


def seasonal_variation(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_data()
    counts = {}
    for s in df["Seasonal Variation"].dropna():
        for part in s.split(","):
            key = part.strip()
            if key:
                counts[key] = counts.get(key, 0) + 1
    return pd.DataFrame(list(counts.items()), columns=["Season", "Count"]).sort_values(
        "Count", ascending=False
    )


def top_ayurvedic_herbs(n: int = 15) -> pd.DataFrame:
    df = load_data()
    counts = {}
    _skip = {"nan", "none", "none specific", "none known", "n/a", ""}
    for herbs_str in df["Ayurvedic Herbs"].dropna():
        for herb in herbs_str.split(","):
            key = herb.strip()
            if key.lower() not in _skip:
                counts[key] = counts.get(key, 0) + 1
    result = (
        pd.DataFrame(list(counts.items()), columns=["Herb", "Count"])
        .sort_values("Count", ascending=False)
        .head(n)
    )
    return result


def stress_sleep_counts(df: pd.DataFrame | None = None) -> dict:
    if df is None:
        df = load_data()
    return {
        "stress": df["Stress Levels"].value_counts().to_dict(),
        "sleep": df["Sleep Patterns"].value_counts().to_dict(),
    }
