"""
===============================================================================
AppleGuard AI — Flat UI Styles (Neutral Slate)
===============================================================================

Flat styling: solid fills, thin 1px borders, small radii, minimal shadows.
Neutral slate palette — black #111827 accent, red #DC2626 for the
formalin class only.
===============================================================================
"""

from __future__ import annotations

PRIMARY = "#111827"
DANGER = "#DC2626"
BACKGROUND = "#F9FAFB"
SURFACE = "#FFFFFF"
BORDER = "#E5E7EB"
TRACK = "#F3F4F6"
TEXT = "#111827"
MUTED = "#6B7280"
FAINT = "#9CA3AF"

SIDEBAR_WIDTH = 22  # rem-equivalent; Streamlit handles px


def get_flat_styles() -> str:
    """Return the complete flat stylesheet for AppleGuard AI."""

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif;
    }}

    .stApp {{
        background: {BACKGROUND};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Headings */
    h1, h2, h3, h4 {{
        color: {TEXT} !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }}
    h1 {{ font-size: 1.9rem !important; }}
    h2 {{ font-size: 1.35rem !important; }}

    a {{
        color: {PRIMARY} !important;
        text-decoration: none !important;
    }}

    /* Slim flat header */
    .flat-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 0.9rem 1.5rem;
        margin-bottom: 1.5rem;
    }}
    .flat-header-brand {{
        font-size: 1.2rem;
        font-weight: 800;
        color: {TEXT};
    }}
    .flat-header-tag {{
        font-size: 0.8rem;
        color: {MUTED};
    }}

    /* Flat cards */
    .flat-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
    }}
    .flat-card-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .flat-card-muted {{
        font-size: 0.85rem;
        color: {MUTED};
        line-height: 1.6;
    }}

    /* Upload dashed box */
    .upload-box {{
        background: {BACKGROUND};
        border: 2px dashed {FAINT};
        border-radius: 8px;
        padding: 2rem 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .upload-box-icon {{ font-size: 2rem; }}
    .upload-box-title {{ font-size: 0.95rem; color: {PRIMARY}; font-weight: 600; }}
    .upload-box-hint {{ font-size: 0.75rem; color: {FAINT}; }}

    /* File uploader override */
    [data-testid="stFileUploaderDropzone"] {{
        background: {BACKGROUND};
        border: 2px dashed {FAINT};
        border-radius: 8px;
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: {PRIMARY};
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        color: {TEXT};
        border-radius: 6px;
        font-weight: 600;
    }}

    /* Image frame */
    .image-frame {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 1rem;
    }}
    .image-frame img {{
        border-radius: 6px;
        width: 100%;
    }}

    /* Result panel */
    .result-panel {{
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
        margin-bottom: 1.25rem;
    }}
    .result-class {{
        font-size: 1.15rem;
        font-weight: 800;
        color: {TEXT};
    }}
    .result-confidence {{
        font-size: 2.2rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }}
    .result-fresh .result-confidence {{ color: {PRIMARY}; }}
    .result-formalin .result-confidence {{ color: {DANGER}; }}
    .result-formalin {{
        border-color: #FECACA;
        background: #FFF5F5;
    }}
    .result-fresh {{
        border-color: {BORDER};
        background: {SURFACE};
    }}

    /* Probability bars */
    .prob-row {{ margin-bottom: 0.9rem; }}
    .prob-label {{
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 600;
        color: {TEXT};
        margin-bottom: 0.3rem;
    }}
    .prob-track {{
        height: 8px;
        background: {TRACK};
        border-radius: 4px;
        overflow: hidden;
    }}
    .prob-fill {{
        height: 100%;
        border-radius: 4px;
        background: {PRIMARY};
    }}
    .prob-fill-danger {{ background: {DANGER}; }}

    /* Meta line (inference time, model) */
    .meta-line {{
        font-size: 0.75rem;
        color: {MUTED};
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px solid {BORDER};
    }}

    /* Empty state */
    .empty-state {{
        text-align: center;
        padding: 3rem 1rem;
        color: {FAINT};
        font-size: 0.9rem;
    }}

    /* Buttons */
    .stButton > button {{
        background: {PRIMARY};
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    .stButton > button:hover {{
        background: #374151;
        color: #fff;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1.5rem;
    }}
    .sidebar-brand {{
        font-size: 1.05rem;
        font-weight: 800;
        color: {TEXT};
        margin-bottom: 0.2rem;
    }}
    .sidebar-sub {{
        font-size: 0.78rem;
        color: {MUTED};
        margin-bottom: 1.5rem;
    }}

    /* Footer */
    .flat-footer {{
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {BORDER};
        color: {FAINT};
        font-size: 0.8rem;
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 0.9rem 1rem;
    }}
    div[data-testid="stMetricValue"] {{ font-weight: 700; }}
    </style>
    """


def render_probability_bar(label: str, probability: float, danger: bool = False) -> str:
    """Return a flat probability bar HTML block."""

    percentage = max(0.0, min(probability * 100, 100.0))
    fill_class = "prob-fill-danger" if danger else "prob-fill"

    return f"""
    <div class="prob-row">
        <div class="prob-label">
            <span>{label}</span>
            <span>{percentage:.2f}%</span>
        </div>
        <div class="prob-track">
            <div class="{fill_class}" style="width: {percentage:.2f}%;"></div>
        </div>
    </div>
    """


def render_footer() -> str:
    """Return the flat application footer."""

    return """
    <div class="flat-footer">
        AppleGuard AI &bull; University of Uyo &bull; Computer Engineering &bull; 2026
    </div>
    """


__all__ = [
    "get_flat_styles",
    "render_probability_bar",
    "render_footer",
]