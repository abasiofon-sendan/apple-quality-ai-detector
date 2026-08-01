
"""
AppleGuard AI — Professional UI Styles
Phase 1: Foundation styling system
"""

from __future__ import annotations

# =============================================================================
# GLOBAL APPLICATION STYLES
# =============================================================================

def get_global_styles(theme: dict) -> str:
    """Return the complete global stylesheet for AppleGuard AI."""

    return f"""
    <style>

    /* ================================================================
       IMPORTS
    ================================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');


    /* ================================================================
       ROOT VARIABLES
    ================================================================ */
    :root {{
        --primary: {theme['primary']};
        --secondary: {theme['secondary']};
        --background: {theme['background']};
        --surface: {theme['surface']};
        --text: {theme['text']};
        --accent: {theme['accent']};
        --border: {theme.get('border', '#E5E7EB')};

        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.12);

        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 22px;
    }}


    /* ================================================================
       GLOBAL RESET
    ================================================================ */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: var(--background);
        color: var(--text);
    }}

    .main .block-container {{
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}


    /* ================================================================
       TYPOGRAPHY
    ================================================================ */
    h1 {{
        color: var(--primary) !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 0.5rem !important;
    }}

    h2 {{
        color: var(--primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
    }}

    h3 {{
        color: var(--primary) !important;
        font-size: 1.35rem !important;
        font-weight: 600 !important;
    }}

    p, li, span, label {{
        color: var(--text);
        line-height: 1.65;
    }}


    /* ================================================================
       HERO SECTION
    ================================================================ */
    .hero-container {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: var(--radius-lg);
        padding: 3rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }}

    .hero-container::before {{
        content: '';
        position: absolute;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 50%;
    }}

    .hero-title {{
        color: white !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.75rem !important;
    }}

    .hero-subtitle {{
        color: rgba(255, 255, 255, 0.92) !important;
        font-size: 1.1rem;
        max-width: 760px;
        margin-bottom: 1rem;
    }}


    /* ================================================================
       PROFESSIONAL CARDS
    ================================================================ */
    .card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }}

    .card-title {{
        color: var(--primary);
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }}


    /* ================================================================
       UPLOAD AREA
    ================================================================ */
    .upload-section {{
        background: var(--surface);
        border: 2px dashed var(--primary);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }}

    .upload-icon {{
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }}

    .upload-title {{
        color: var(--primary);
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}


    /* ================================================================
       RESULT STATUS CARDS
    ================================================================ */
    .result-fresh {{
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 6px solid #10B981;
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 1rem 0;
    }}

    .result-formalin {{
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 6px solid #EF4444;
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 1rem 0;
    }}


    /* ================================================================
       METRICS
    ================================================================ */
    div[data-testid="stMetric"] {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        box-shadow: var(--shadow-sm);
    }}


    /* ================================================================
       BUTTONS
    ================================================================ */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.4rem;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }}


    /* ================================================================
       SIDEBAR
    ================================================================ */
    section[data-testid="stSidebar"] {{
        background: var(--surface);
        border-right: 1px solid var(--border);
    }}


    /* ================================================================
       FOOTER
    ================================================================ */
    .app-footer {{
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
        color: var(--text);
        opacity: 0.75;
        font-size: 0.9rem;
    }}

    </style>
    """


# =============================================================================
# HERO SECTION HELPER
# =============================================================================

def render_hero_section() -> str:
    """Return a professional hero section HTML block."""

    return """
    <div class="hero-container">
        <div class="hero-title">🍎 AppleGuard AI</div>
        <div class="hero-subtitle">
            AI-powered apple quality detection with explainable Grad-CAM
            visualization, confidence analysis, and professional PDF reporting.
        </div>
    </div>
    """


# =============================================================================
# FOOTER HELPER
# =============================================================================

def render_footer() -> str:
    """Return the application footer."""

    return """
    <div class="app-footer">
        AppleGuard AI • University of Uyo • Computer Engineering • 2026
    </div>
    """


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "get_global_styles",
    "render_footer",
    "render_hero_section",
]


# =============================================================================
# INTERACTIVE COMPONENT STYLES — PHASE 2
# =============================================================================

def get_interactive_styles(theme: dict) -> str:
    """Return interactive dashboard component styles."""

    return f"""
    <style>

    /* ================================================================
       PROBABILITY BARS
    ================================================================ */
    .probability-container {{
        margin-bottom: 1rem;
    }}

    .probability-label {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
        margin-bottom: 0.35rem;
        color: {theme['text']};
    }}

    .probability-track {{
        width: 100%;
        height: 12px;
        background: {theme['secondary']};
        border-radius: 999px;
        overflow: hidden;
    }}

    .probability-fill {{
        height: 100%;
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        border-radius: 999px;
        transition: width 0.8s ease-in-out;
    }}


    /* ================================================================
       CONFIDENCE BADGES
    ================================================================ */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }}

    .badge-high {{
        background: rgba(16, 185, 129, 0.15);
        color: #047857;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .badge-medium {{
        background: rgba(245, 158, 11, 0.15);
        color: #B45309;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .badge-low {{
        background: rgba(239, 68, 68, 0.15);
        color: #B91C1C;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}


    /* ================================================================
       IMAGE PREVIEW FRAME
    ================================================================ */
    .image-frame {{
        background: {theme['surface']};
        border: 1px solid {theme.get('border', '#E5E7EB')};
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
    }}

    .image-frame-title {{
        color: {theme['primary']};
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-size: 1rem;
    }}


    /* ================================================================
       GRAD-CAM COMPARISON LAYOUT
    ================================================================ */
    .comparison-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }}

    .comparison-card {{
        background: {theme['surface']};
        border: 1px solid {theme.get('border', '#E5E7EB')};
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }}

    .comparison-title {{
        color: {theme['primary']};
        font-weight: 700;
        margin-bottom: 0.75rem;
        text-align: center;
    }}


    /* ================================================================
       REPORT DOWNLOAD PANEL
    ================================================================ */
    .report-panel {{
        background: linear-gradient(135deg, {theme['surface']} 0%, {theme['secondary']} 100%);
        border: 1px solid {theme.get('border', '#E5E7EB')};
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    }}

    .report-title {{
        color: {theme['primary']};
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}

    .report-description {{
        color: {theme['text']};
        opacity: 0.9;
        margin-bottom: 1rem;
    }}


    /* ================================================================
       PROCESSING / LOADING CARD
    ================================================================ */
    .processing-card {{
        background: {theme['surface']};
        border: 1px solid {theme.get('border', '#E5E7EB')};
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
    }}

    .processing-spinner {{
        width: 48px;
        height: 48px;
        border: 4px solid {theme['secondary']};
        border-top: 4px solid {theme['primary']};
        border-radius: 50%;
        animation: appleguard-spin 1s linear infinite;
        margin: 0 auto 1rem auto;
    }}

    @keyframes appleguard-spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    .processing-title {{
        color: {theme['primary']};
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }}


    /* ================================================================
       SUCCESS HIGHLIGHT STRIP
    ================================================================ */
    .success-strip {{
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.04) 100%);
        border-left: 5px solid #10B981;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: {theme['text']};
    }}

    </style>
    """


# =============================================================================
# HELPER COMPONENTS
# =============================================================================

def render_probability_bar(label: str, probability: float) -> str:
    """Return a probability bar HTML block."""

    percentage = max(0.0, min(probability * 100, 100.0))

    return f"""
    <div class="probability-container">
        <div class="probability-label">
            <span>{label}</span>
            <span>{percentage:.2f}%</span>
        </div>
        <div class="probability-track">
            <div class="probability-fill" style="width: {percentage:.2f}%;"></div>
        </div>
    </div>
    """


def render_confidence_badge(confidence: float) -> str:
    """Return a confidence badge based on the confidence score."""

    percentage = confidence * 100

    if percentage >= 85:
        badge_class = "badge-high"
        icon = "✅"
        label = "High Confidence"
    elif percentage >= 60:
        badge_class = "badge-medium"
        icon = "⚠️"
        label = "Moderate Confidence"
    else:
        badge_class = "badge-low"
        icon = "❌"
        label = "Low Confidence"

    return f"""
    <span class="badge {badge_class}">
        <span>{icon}</span>
        <span>{label} ({percentage:.1f}%)</span>
    </span>
    """


def render_processing_indicator(message: str = "Analyzing apple image...") -> str:
    """Return a processing indicator card."""

    return f"""
    <div class="processing-card">
        <div class="processing-spinner"></div>
        <div class="processing-title">AppleGuard AI Processing</div>
        <div>{message}</div>
    </div>
    """


# =============================================================================
# EXTEND PUBLIC EXPORTS
# =============================================================================

__all__.extend([
    "get_interactive_styles",
    "render_confidence_badge",
    "render_probability_bar",
    "render_processing_indicator",
])


# =============================================================================
# ADVANCED POLISH & RESPONSIVE STYLES — PHASE 3
# =============================================================================

def get_responsive_styles(theme: dict) -> str:
    """Return responsive, accessibility, and advanced polish styles."""

    return f"""
    <style>

    /* ================================================================
       RESPONSIVE DESIGN
    ================================================================ */
    @media (max-width: 1024px) {{
        .hero-container {{
            padding: 2rem 1.5rem;
        }}

        .hero-title {{
            font-size: 2.4rem !important;
        }}

        .comparison-container {{
            grid-template-columns: 1fr;
        }}
    }}

    @media (max-width: 768px) {{
        .main .block-container {{
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .hero-container {{
            padding: 1.5rem 1.25rem;
            border-radius: 18px;
        }}

        .hero-title {{
            font-size: 2rem !important;
            line-height: 1.2;
        }}

        .hero-subtitle {{
            font-size: 1rem;
        }}

        h1 {{
            font-size: 2rem !important;
        }}

        h2 {{
            font-size: 1.5rem !important;
        }}

        .card {{
            padding: 1rem;
        }}

        .upload-section {{
            padding: 1.25rem;
        }}
    }}


    /* ================================================================
       DARK THEME OPTIMIZATION
    ================================================================ */
    .stApp[data-theme="dark"] .card,
    .stApp[data-theme="dark"] .comparison-card,
    .stApp[data-theme="dark"] .report-panel,
    .stApp[data-theme="dark"] .processing-card {{
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }}


    /* ================================================================
       ACCESSIBILITY IMPROVEMENTS
    ================================================================ */
    *:focus-visible {{
        outline: 3px solid {theme['accent']} !important;
        outline-offset: 2px !important;
        border-radius: 6px;
    }}

    .stButton > button:focus-visible {{
        box-shadow: 0 0 0 4px rgba(66, 165, 245, 0.25);
    }}

    .badge {{
        min-height: 32px;
    }}


    /* ================================================================
       PRINT / PDF PREVIEW STYLES
    ================================================================ */
    @media print {{
        .hero-container {{
            background: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            box-shadow: none !important;
        }}

        .hero-title,
        .hero-subtitle {{
            color: #000000 !important;
        }}

        .card,
        .comparison-card,
        .report-panel {{
            box-shadow: none !important;
            border: 1px solid #000000 !important;
            break-inside: avoid;
        }}

        .app-footer {{
            border-top: 1px solid #000000 !important;
        }}
    }}


    /* ================================================================
       COMPACT DASHBOARD MODE
    ================================================================ */
    .compact-mode .card {{
        padding: 0.9rem;
        margin-bottom: 0.75rem;
    }}

    .compact-mode .hero-container {{
        padding: 1.5rem;
    }}

    .compact-mode .hero-title {{
        font-size: 2rem !important;
    }}


    /* ================================================================
       PROFESSIONAL TABLE STYLING
    ================================================================ */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        background: {theme['surface']};
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }}

    .styled-table thead {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['accent']} 100%);
    }}

    .styled-table thead th {{
        color: white;
        font-weight: 700;
        padding: 0.9rem 1rem;
        text-align: left;
    }}

    .styled-table tbody td {{
        padding: 0.85rem 1rem;
        border-bottom: 1px solid {theme.get('border', '#E5E7EB')};
    }}

    .styled-table tbody tr:hover {{
        background: rgba(0, 0, 0, 0.02);
    }}


    /* ================================================================
       SCROLLABLE ANALYSIS PANEL
    ================================================================ */
    .analysis-panel {{
        background: {theme['surface']};
        border: 1px solid {theme.get('border', '#E5E7EB')};
        border-radius: 16px;
        padding: 1rem;
        max-height: 420px;
        overflow-y: auto;
    }}

    .analysis-panel::-webkit-scrollbar {{
        width: 8px;
    }}

    .analysis-panel::-webkit-scrollbar-track {{
        background: {theme['secondary']};
        border-radius: 999px;
    }}

    .analysis-panel::-webkit-scrollbar-thumb {{
        background: {theme['primary']};
        border-radius: 999px;
    }}


    /* ================================================================
       MICRO-INTERACTIONS
    ================================================================ */
    .fade-in {{
        animation: appleguard-fade-in 0.4s ease-out;
    }}

    @keyframes appleguard-fade-in {{
        from {{
            opacity: 0;
            transform: translateY(6px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .pulse-success {{
        animation: appleguard-pulse 2s infinite;
    }}

    @keyframes appleguard-pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }}
        70% {{ box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}


    /* ================================================================
       STATUS CHIPS
    ================================================================ */
    .status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
    }}

    .status-ready {{
        background: rgba(16, 185, 129, 0.12);
        color: #047857;
    }}

    .status-processing {{
        background: rgba(59, 130, 246, 0.12);
        color: #1D4ED8;
    }}

    .status-warning {{
        background: rgba(245, 158, 11, 0.12);
        color: #B45309;
    }}

    </style>
    """


# =============================================================================
# ADVANCED HELPER COMPONENTS
# =============================================================================

def render_status_chip(label: str, status: str = "ready") -> str:
    """Return a small status chip component."""

    mapping = {
        "ready": ("status-ready", "🟢"),
        "processing": ("status-processing", "🔵"),
        "warning": ("status-warning", "🟡"),
    }

    css_class, icon = mapping.get(status, mapping["ready"])

    return f"""
    <span class="status-chip {css_class}">
        <span>{icon}</span>
        <span>{label}</span>
    </span>
    """


def render_analysis_panel(title: str, content: str) -> str:
    """Return a scrollable analysis panel."""

    return f"""
    <div class="card fade-in">
        <div class="card-title">{title}</div>
        <div class="analysis-panel">
            {content}
        </div>
    </div>
    """


# =============================================================================
# COMPLETE STYLE INITIALIZER
# =============================================================================

def get_complete_styles(theme: dict) -> str:
    """Return the complete AppleGuard styling system."""

    return (
        get_global_styles(theme)
        + get_interactive_styles(theme)
        + get_responsive_styles(theme)
    )


# =============================================================================
# EXTEND PUBLIC EXPORTS
# =============================================================================

__all__.extend([
    "get_complete_styles",
    "get_responsive_styles",
    "render_analysis_panel",
    "render_status_chip",
])


