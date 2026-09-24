"""
Data Loader Module
Loads and preprocesses the AyurGenixAI dataset.
"""

import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AyurGenixAI_Dataset.csv")

_df_cache = None


def load_data() -> pd.DataFrame:
    """Load and cache the dataset."""
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]

    # Strip whitespace from all string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    _df_cache = df
    return df


def get_all_diseases(df: pd.DataFrame) -> list[str]:
    """Return sorted unique disease names."""
    return sorted(df["Disease"].dropna().unique().tolist())


def get_all_symptoms(df: pd.DataFrame) -> list[str]:
    """Return a flat, deduplicated list of all individual symptoms."""
    all_symptoms = set()
    for symptoms_str in df["Symptoms"].dropna():
        for s in symptoms_str.split(","):
            cleaned = s.strip().lower()
            if cleaned:
                all_symptoms.add(cleaned)
    return sorted(all_symptoms)


def get_all_doshas(df: pd.DataFrame) -> list[str]:
    """Return sorted unique doshas."""
    doshas = set()
    for d in df["Doshas"].dropna():
        for part in d.split(","):
            doshas.add(part.strip())
    return sorted(doshas)


def get_disease_record(df: pd.DataFrame, disease_name: str) -> pd.Series | None:
    """Fetch the first matching row for a disease."""
    match = df[df["Disease"].str.lower() == disease_name.lower()]
    if match.empty:
        return None
    return match.iloc[0]


def get_columns() -> list[str]:
    """Return column names of the dataset."""
    return load_data().columns.tolist()


def get_dosha_distribution(df: pd.DataFrame) -> dict:
    """Count diseases per dosha type."""
    counts = {}
    for d in df["Doshas"].dropna():
        for part in d.split(","):
            key = part.strip()
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def get_age_group_distribution(df: pd.DataFrame) -> dict:
    """Count diseases per age group."""
    return df["Age Group"].value_counts().to_dict()


def get_severity_distribution(df: pd.DataFrame) -> dict:
    """Count diseases per severity level."""
    return df["Symptom Severity"].value_counts().to_dict()
