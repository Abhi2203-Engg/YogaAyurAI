"""
Shared UI helpers — colours, cards, badges, section headers.
"""

import streamlit as st

# ─── Brand palette ────────────────────────────────────────
PRIMARY      = "#2E7D32"   # deep green
SECONDARY    = "#FF8F00"   # amber
ACCENT       = "#1565C0"   # indigo
BG_CARD      = "#F9FBF9"
BORDER       = "#C8E6C9"

DOSHA_COLOURS = {
    "Vata":  "#7E57C2",
    "Pitta": "#EF5350",
    "Kapha": "#26A69A",
}

SEVERITY_COLOURS = {
    "Mild":                "#43A047",
    "Mild to Moderate":    "#FFA726",
    "Moderate":            "#FB8C00",
    "Moderate to Severe":  "#E53935",
    "Severe":              "#B71C1C",
    "High":                "#E53935",
}


# ─── Page config (call once at app entry) ─────────────────
def set_page_config():
    st.set_page_config(
        page_title="YogaAyurAI",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ─── Global CSS ───────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Global ── */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .block-container { padding-top: 1.5rem; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        }
        [data-testid="stSidebar"] * { color: #E8F5E9 !important; }
        [data-testid="stSidebar"] .stRadio label { color: #E8F5E9 !important; }

        /* ── Metric cards ── */
        .metric-card {
            background: #F1F8E9;
            border-left: 4px solid #43A047;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 10px;
        }
        .metric-card h4 { margin: 0 0 4px 0; color: #1B5E20; font-size: 0.85rem; }
        .metric-card p  { margin: 0; font-size: 1.4rem; font-weight: 700; color: #2E7D32; }

        /* ── Info cards ── */
        .info-card {
            background: #FAFAFA;
            border: 1px solid #C8E6C9;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 12px;
        }
        .info-card h5 {
            margin: 0 0 6px 0;
            color: #1B5E20;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ── Badges ── */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin: 2px 3px;
        }
        .badge-green  { background:#C8E6C9; color:#1B5E20; }
        .badge-amber  { background:#FFE0B2; color:#E65100; }
        .badge-red    { background:#FFCDD2; color:#B71C1C; }
        .badge-purple { background:#E1BEE7; color:#6A1B9A; }
        .badge-blue   { background:#BBDEFB; color:#0D47A1; }
        .badge-teal   { background:#B2EBF2; color:#006064; }

        /* ── Hero banner ── */
        .hero-banner {
            background: linear-gradient(135deg, #1B5E20, #2E7D32, #388E3C);
            color: #fff;
            border-radius: 14px;
            padding: 36px 40px;
            margin-bottom: 28px;
            text-align: center;
        }
        .hero-banner h1 { font-size: 2.4rem; margin: 0 0 8px 0; }
        .hero-banner p  { font-size: 1.05rem; opacity: 0.9; margin: 0; }

        /* ── Search result card ── */
        .result-card {
            background: #fff;
            border: 1px solid #C8E6C9;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 10px;
            transition: box-shadow 0.2s;
        }
        .result-card:hover { box-shadow: 0 3px 10px rgba(46,125,50,0.15); }

        /* ── Section divider ── */
        hr.section-divider {
            border: none;
            border-top: 2px solid #C8E6C9;
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─── Reusable components ──────────────────────────────────

def hero(title: str, subtitle: str = ""):
    st.markdown(
        f"""<div class="hero-banner">
            <h1>{title}</h1>
            {'<p>' + subtitle + '</p>' if subtitle else ''}
        </div>""",
        unsafe_allow_html=True,
    )


def section_header(icon: str, text: str):
    st.markdown(f"### {icon} {text}")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


def info_card(label: str, value: str):
    st.markdown(
        f"""<div class="info-card">
            <h5>{label}</h5>
            <span>{value}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str):
    st.markdown(
        f"""<div class="metric-card">
            <h4>{label}</h4>
            <p>{value}</p>
        </div>""",
        unsafe_allow_html=True,
    )


def badge(text: str, colour: str = "green") -> str:
    return f'<span class="badge badge-{colour}">{text}</span>'


def badges_from_csv(csv_str: str, colour: str = "green") -> str:
    parts = [p.strip() for p in str(csv_str).split(",") if p.strip() and p.strip().lower() != "nan"]
    return " ".join(badge(p, colour) for p in parts)


def severity_badge(severity: str) -> str:
    s = severity.lower()
    if "severe" in s and "moderate" in s:
        col = "red"
    elif "severe" in s:
        col = "red"
    elif "moderate" in s:
        col = "amber"
    else:
        col = "green"
    return badge(severity, col)
