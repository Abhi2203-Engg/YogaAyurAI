# YogaAyurAI 🌿

> **Ancient Ayurvedic Wisdom powered by Modern AI**

A full-stack Python application that uses the **AyurGenixAI Dataset** to deliver personalised Ayurvedic health insights, yoga therapy plans, and diet recommendations.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📁 Project Structure

```
YogaAyurAI/
├── app.py                          # Streamlit entry point
├── requirements.txt
├── AyurGenixAI_Dataset.csv         # Source dataset
│
├── backend/
│   ├── data_loader.py              # CSV ingestion & caching
│   ├── recommendation_engine.py    # TF-IDF + fuzzy search & recommendations
│   └── analytics.py                # Aggregation helpers for charts
│
├── frontend/
│   ├── ui_helpers.py               # Shared CSS, cards, badges, heroes
│   └── pages/
│       ├── home.py                 # Landing page with KPI cards & charts
│       ├── symptom_checker.py      # Free-text symptom → disease search
│       ├── disease_explorer.py     # Browse & filter diseases
│       ├── yoga_diet_advisor.py    # Personalised yoga & diet plans
│       └── analytics_dashboard.py  # Full visual analytics dashboard
│
└── .streamlit/
    └── config.toml                 # Theme configuration
```

---

## ✨ Features

| Page | Description |
|---|---|
| 🏠 **Home** | KPI stats, dosha distribution, severity spread, top herbs chart |
| 🔍 **Symptom Checker** | Enter symptoms in plain language; TF-IDF + fuzzy ranked results |
| 📋 **Disease Explorer** | Browse 100+ diseases; filter by severity, dosha, age, gender |
| 🧘 **Yoga & Diet Advisor** | Personalised yoga + diet plans keyed to your Dosha & condition |
| 📊 **Analytics Dashboard** | 10+ interactive Plotly charts with raw data export |

---

## 🧠 How It Works

### Backend

- **`data_loader.py`** — reads `AyurGenixAI_Dataset.csv` with `pandas`, cleans columns, and caches the DataFrame.
- **`recommendation_engine.py`** — combines **TF-IDF cosine similarity** (70%) and **fuzzy string matching** (30%) to rank disease–symptom matches. Profile-aware scoring picks the best row when multiple entries exist for a disease.
- **`analytics.py`** — aggregation helpers consumed by the dashboard (dosha counts, herb frequency, age groups, etc.).

### Frontend

- Built with **Streamlit** and **Plotly Express**.
- All styling is injected as inline CSS via `ui_helpers.py` — no external assets needed.
- Single-file entry point (`app.py`) with radio-button sidebar navigation.

---

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**.  
Always consult a qualified healthcare professional or certified Ayurvedic practitioner before making health decisions.
