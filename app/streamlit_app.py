"""
===============================================================================
AppleGuard AI — Streamlit Application Entry Point
===============================================================================

Single-page flat UI: sidebar (model selector) + two-column main area
(upload left, prediction result right).

Run with:
    streamlit run app/streamlit_app.py
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from src.config import (
    APP_TITLE,
    DEFAULT_MODEL,
    LAYOUT,
    SIDEBAR_STATE,
    get_available_models,
)
from app.components import (
    render_app_footer,
    render_app_header,
    render_empty_state,
    render_prediction_workflow,
    render_sidebar,
    render_upload_section,
)
from app.styles import get_flat_styles

VERSION = "1.0.0"

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍎",
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

st.markdown(get_flat_styles(), unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

if "appleguard_model" not in st.session_state:
    st.session_state.appleguard_model = DEFAULT_MODEL

# =============================================================================
# AVAILABLE MODELS (FastAPI backend first, local fallback)
# =============================================================================

try:
    from api.api_Client import get_available_models as fetch_backend_models

    backend_models = fetch_backend_models()
    available_models = [
        model["name"]
        for model in backend_models
        if model.get("available", False)
    ]
except Exception:
    available_models = []

if not available_models:
    available_models = get_available_models()

if not available_models:
    st.error("No AI models are available.")
    st.stop()

current_model = st.session_state.get("appleguard_model", DEFAULT_MODEL)
if current_model not in available_models:
    current_model = available_models[0]

# =============================================================================
# SIDEBAR — MODEL SELECTION
# =============================================================================

selected_model = render_sidebar(available_models, current_model)
st.session_state.appleguard_model = selected_model

# =============================================================================
# HEADER
# =============================================================================

render_app_header()

# =============================================================================
# MAIN CONTENT — TWO-COLUMN LAYOUT
# =============================================================================

uploaded_file, result_col = render_upload_section()

if uploaded_file is not None:
    render_prediction_workflow(uploaded_file, selected_model, result_col)
else:
    with result_col:
        render_empty_state()

# =============================================================================
# FOOTER
# =============================================================================

render_app_footer()