
"""
AppleGuard AI — Theme System
Stage 2: Advanced theme manager with CSS generation
"""

from __future__ import annotations

import streamlit as st

# =============================================================================
# THEME DEFINITIONS
# =============================================================================

THEMES = {
    "Apple Fresh": {
        "primary": "#2E8B57",
        "secondary": "#D8F3DC",
        "background": "#F7FFF9",
        "surface": "#FFFFFF",
        "text": "#1B4332",
        "accent": "#52B788",
        "border": "#B7E4C7",
    },

    "Midnight Dark": {
        "primary": "#22C55E",
        "secondary": "#334155",
        "background": "#0F172A",
        "surface": "#1E293B",
        "text": "#F8FAFC",
        "accent": "#4ADE80",
        "border": "#475569",
    },

    "Formalin Alert": {
        "primary": "#D90429",
        "secondary": "#F8D7DA",
        "background": "#FFF5F5",
        "surface": "#FFFFFF",
        "text": "#4A0E12",
        "accent": "#EF233C",
        "border": "#F5C2C7",
    },

    "Laboratory Blue": {
        "primary": "#1565C0",
        "secondary": "#BBDEFB",
        "background": "#F4F9FF",
        "surface": "#FFFFFF",
        "text": "#0D47A1",
        "accent": "#42A5F5",
        "border": "#90CAF9",
    },
}


# =============================================================================
# DEFAULT THEME
# =============================================================================

from src.config import DEFAULT_THEME

# =============================================================================
# THEME UTILITIES
# =============================================================================

def get_theme(theme_name: str = DEFAULT_THEME) -> dict:
    """Return a theme dictionary."""

    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def get_available_themes() -> list[str]:
    """Return all available theme names."""

    return list(THEMES.keys())


# =============================================================================
# CSS GENERATOR
# =============================================================================

def generate_theme_css(theme: dict) -> str:
    """Generate CSS for the selected theme."""

    return f"""
    <style>
    /* Main App */
    .stApp {{
        background-color: {theme['background']};
        color: {theme['text']};
    }}

    /* Container */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {theme['primary']} !important;
        font-weight: 700;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.25rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }}

    .stButton > button:hover {{
        background-color: {theme['accent']};
        transform: translateY(-1px);
    }}

    /* File uploader */
    .stFileUploader {{
        border: 2px dashed {theme['primary']};
        border-radius: 14px;
        padding: 1rem;
        background-color: {theme['surface']};
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-left: 5px solid {theme['primary']};
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {theme['surface']};
        border-right: 1px solid {theme['border']};
    }}

    /* Cards */
    .theme-card {{
        background-color: {theme['surface']};
        border: 1px solid {theme['border']};
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }}

    /* Footer */
    .app-footer {{
        text-align: center;
        color: {theme['text']};
        opacity: 0.75;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {theme['border']};
        font-size: 0.9rem;
    }}
    </style>
    """


# =============================================================================
# THEME SELECTOR
# =============================================================================

def theme_selector() -> str:
    """Render the sidebar theme selector."""

    if "appleguard_theme" not in st.session_state:
        st.session_state.appleguard_theme = DEFAULT_THEME

    selected = st.sidebar.selectbox(
        "🎨 Theme",
        get_available_themes(),
        index=get_available_themes().index(
            st.session_state.appleguard_theme
        ),
    )

    st.session_state.appleguard_theme = selected

    return selected


# =============================================================================
# APPLY THEME
# =============================================================================

def apply_theme(theme_name: str = DEFAULT_THEME) -> dict:
    """Apply the selected theme to Streamlit."""

    theme = get_theme(theme_name)

    st.markdown(generate_theme_css(theme), unsafe_allow_html=True)

    return theme


# =============================================================================
# QUICK PREVIEW CARD
# =============================================================================

def render_theme_preview(theme_name: str) -> None:
    """Render a small preview card for the selected theme."""

    theme = get_theme(theme_name)

    st.sidebar.markdown(
        f"""
        <div style="
            background:{theme['surface']};
            border:1px solid {theme['border']};
            border-radius:12px;
            padding:0.75rem;
            margin-top:1rem;
        ">
            <div style="color:{theme['primary']}; font-weight:700;">
                {theme_name}
            </div>
            <div style="margin-top:0.5rem;">
                <span style="
                    display:inline-block;
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:{theme['primary']};
                    margin-right:6px;
                "></span>
                <span style="
                    display:inline-block;
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:{theme['accent']};
                    margin-right:6px;
                "></span>
                <span style="
                    display:inline-block;
                    width:18px;
                    height:18px;
                    border-radius:50%;
                    background:{theme['surface']};
                    border:1px solid {theme['border']};
                "></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# COMPLETE THEME INITIALIZER
# =============================================================================

def initialize_theme() -> dict:
    """Initialize theme selection, preview, and application."""

    selected = theme_selector()
    render_theme_preview(selected)

    return apply_theme(selected)


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "DEFAULT_THEME",
    "THEMES",
    "apply_theme",
    "generate_theme_css",
    "get_available_themes",
    "get_theme",
    "initialize_theme",
    "render_theme_preview",
    "theme_selector",
]


# =============================================================================
# DEVELOPMENT TEST
# =============================================================================

if __name__ == "__main__":
    print("AppleGuard AI Theme System — Stage 2")
    print("-" * 50)

    for name in get_available_themes():
        theme = get_theme(name)
        print(f"{name:18} | {theme['primary']} | {theme['background']}")

