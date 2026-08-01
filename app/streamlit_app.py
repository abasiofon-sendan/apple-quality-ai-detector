# """
# ===============================================================================
# AppleGuard AI — Streamlit Application Entry Point
# ===============================================================================

# Project      : AppleGuard AI
# Author       : Group 16
# Institution  : University of Uyo
# Department   : Computer Engineering
# Year         : 2026

# Run with:
#     streamlit run app/app.py
# ===============================================================================
# """

# from __future__ import annotations

# import sys
# from pathlib import Path

# # =============================================================================
# # PROJECT ROOT ON PATH
# # =============================================================================
# # Streamlit adds this file's own directory (app/) to sys.path automatically,
# # which is why `styles.py` / `theme.py` / `components.py` import with bare
# # names. The project root also needs to be importable so `src.*` resolves.

# ROOT_DIR = Path(__file__).resolve().parent.parent
# if str(ROOT_DIR) not in sys.path:
#     sys.path.insert(0, str(ROOT_DIR))

# import streamlit as st

# from src.config import (
#     APP_TITLE,
#     APP_ICON,
#     LAYOUT,
#     SIDEBAR_STATE,
#     DEFAULT_MODEL,
#     ENABLE_MODEL_COMPARISON,
#     ENABLE_PREDICTION_HISTORY,
#     SHOW_MODEL_INFORMATION,
#     SHOW_MODEL_PERFORMANCE,
#     get_available_models,
#     get_model_metadata,
# )

# from app.theme import initialize_theme
# from app.components import (
#     render_app_footer,
#     render_app_header,
#     render_empty_state,
#     render_history_sidebar,
#     render_image_preview,
#     render_model_comparison,
#     render_prediction_workflow,
#     render_sidebar_panel,
#     render_upload_section,
# )


# # =============================================================================
# # PAGE CONFIGURATION — must be the first Streamlit call
# # =============================================================================

# _page_icon = "🍎" if not APP_ICON.exists() else str(APP_ICON)

# st.set_page_config(
#     page_title=APP_TITLE,
#     page_icon=_page_icon,
#     layout=LAYOUT,
#     initial_sidebar_state=SIDEBAR_STATE,
# )


# # =============================================================================
# # THEME (selector + CSS injection)
# # =============================================================================

# initialize_theme()


# # =============================================================================
# # HEADER
# # =============================================================================

# render_app_header()


# # =============================================================================
# # SIDEBAR — MODEL SELECTION
# # =============================================================================

# st.sidebar.markdown("### 🧠 Model Selection")

# available_models = get_available_models()

# if "appleguard_model" not in st.session_state:
#     st.session_state.appleguard_model = DEFAULT_MODEL

# selected_model = st.sidebar.selectbox(
#     "Active model",
#     available_models,
#     index=available_models.index(st.session_state.appleguard_model),
# )
# st.session_state.appleguard_model = selected_model

# if SHOW_MODEL_INFORMATION or SHOW_MODEL_PERFORMANCE:
#     metadata = get_model_metadata(selected_model)

#     with st.sidebar.expander("📊 Model Details", expanded=False):
#         if metadata:
#             accuracy = metadata.get("test_accuracy") or metadata.get("validation_accuracy")
#             precision = metadata.get("test_precision") or metadata.get("validation_precision")
#             recall = metadata.get("test_recall") or metadata.get("validation_recall")

#             if SHOW_MODEL_PERFORMANCE:
#                 if isinstance(accuracy, (int, float)):
#                     st.metric("Accuracy", f"{accuracy * 100:.2f}%")
#                 if isinstance(precision, (int, float)):
#                     st.metric("Precision", f"{precision * 100:.2f}%")
#                 if isinstance(recall, (int, float)):
#                     st.metric("Recall", f"{recall * 100:.2f}%")

#             if metadata.get("recommended"):
#                 st.success("✅ Recommended model")
#         else:
#             st.caption("No performance metrics recorded for this model yet.")

# compare_mode = False

# if ENABLE_MODEL_COMPARISON and len(available_models) > 1:
#     compare_mode = st.sidebar.checkbox(
#         "Compare all registered models",
#         value=False,
#         help="Runs the uploaded image through every registered model instead of just the active one.",
#     )

# render_sidebar_panel()

# if ENABLE_PREDICTION_HISTORY:
#     render_history_sidebar()


# # =============================================================================
# # MAIN CONTENT
# # =============================================================================

# uploaded_file = render_upload_section()

# if uploaded_file is not None:
#     if compare_mode:
#         from PIL import Image

#         image = Image.open(uploaded_file).convert("RGB")
#         render_image_preview(image)
#         render_model_comparison(image, available_models)
#     else:
#         render_prediction_workflow(uploaded_file, model_name=selected_model)
# else:
#     render_empty_state()


# # =============================================================================
# # FOOTER
# # =============================================================================

# render_app_footer()
## `app/app.py`


"""
===============================================================================
AppleGuard AI — Streamlit Application Entry Point
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Run with:
    streamlit run app/app.py
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

# =============================================================================
# PROJECT ROOT ON PATH
# =============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st

from src.config import (
    APP_TITLE,
    DEFAULT_MODEL,
    ENABLE_MODEL_COMPARISON,
    ENABLE_PREDICTION_HISTORY,
    LAYOUT,
    SHOW_MODEL_INFORMATION,
    SHOW_MODEL_PERFORMANCE,
    SIDEBAR_STATE,
    get_model_metadata,
)

from api.api_Client import get_available_models



# Keep the displayed application version local because src.config does not
# export VERSION.
VERSION = "1.0.0"

from app.components import (
    render_app_footer,
    render_app_header,
    render_empty_state,
    render_history_sidebar,
    render_image_preview,
    render_model_comparison,
    render_prediction_workflow,
    render_sidebar_panel,
    render_upload_section,
)
from app.theme import initialize_theme

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================





from src.config import FAVICON_PATH

_page_icon = "🍎" if not FAVICON_PATH.exists() else str(FAVICON_PATH)


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=_page_icon,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

# =============================================================================
# THEME INITIALIZATION
# =============================================================================

initialize_theme()

# =============================================================================
# SESSION STATE
# =============================================================================

if "appleguard_model" not in st.session_state:
    st.session_state.appleguard_model = DEFAULT_MODEL

# =============================================================================
# PREMIUM SAAS SIDEBAR
# =============================================================================

# =============================================================================
# PREMIUM SIDEBAR BRANDING
# =============================================================================

with st.sidebar:

    # ---------------------------------------------------------------------
    # Brand logo
    # ---------------------------------------------------------------------

    logo_path = ROOT_DIR / "assets" / "logo.png"

    if logo_path.exists():
        st.image(str(logo_path), width=220)
    else:
        st.markdown("## 🍎 AppleGuard AI")

    st.caption("AI Quality Screening Platform")

    st.markdown("---")



    # -------------------------------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------------------------------

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔍 Apple Quality Detection",
            "📚 Safety & Quality Guide",
            "📈 Model Performance",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # -------------------------------------------------------------------------
        
    # -------------------------------------------------------------------------
    # MODEL SELECTION
    # -------------------------------------------------------------------------

    st.subheader("🧠 Model Engine")

    # Fetch model information from FastAPI
    model_data = get_available_models()

    # Handle backend offline state
    if model_data and not model_data[0].get("available", True):
        st.error(
            "⚠️ FastAPI backend is not running. "
            "Start it with: uvicorn api.main:app --reload"
        )
        st.stop()

    # Extract only available model names
    available_models = [
        model["name"]
        for model in model_data
        if model.get("available", False)
    ]

    # Safety fallback
    if not available_models:
        st.error("No AI models are available from the backend.")
        st.stop()

    # Current session model
    current_model = st.session_state.get(
        "appleguard_model",
        DEFAULT_MODEL,
    )

    # Reset invalid model names
    if current_model not in available_models:
        current_model = available_models[0]
        st.session_state.appleguard_model = current_model

    # Human-friendly display names
    DISPLAY_NAMES = {
        "custom_cnn": "Custom CNN",
        "mobilenetv3_feature_extraction": "MobileNetV3 Feature Extraction",
        "mobilenetv3_fine_tuned": "MobileNetV3 Fine-Tuned",
    }

    selected_model = st.selectbox(
        "Active model",
        available_models,
        index=available_models.index(current_model),
        format_func=lambda x: DISPLAY_NAMES.get(x, x),
    )

    st.session_state.appleguard_model = selected_model


    # -------------------------------------------------------------------------
    # MODEL DETAILS
    # -------------------------------------------------------------------------

    if SHOW_MODEL_INFORMATION or SHOW_MODEL_PERFORMANCE:

        metadata = get_model_metadata(selected_model)

        with st.expander("📊 Model Details", expanded=False):

            if metadata:

                accuracy = metadata.get("test_accuracy") or metadata.get("validation_accuracy")
                precision = metadata.get("test_precision") or metadata.get("validation_precision")
                recall = metadata.get("test_recall") or metadata.get("validation_recall")

                if SHOW_MODEL_PERFORMANCE:

                    if isinstance(accuracy, (int, float)):
                        st.metric("Accuracy", f"{accuracy * 100:.2f}%")

                    if isinstance(precision, (int, float)):
                        st.metric("Precision", f"{precision * 100:.2f}%")

                    if isinstance(recall, (int, float)):
                        st.metric("Recall", f"{recall * 100:.2f}%")

                if metadata.get("recommended"):
                    st.success("✅ Recommended model")

            else:
                st.caption("No performance metrics recorded for this model yet.")

    # -------------------------------------------------------------------------
    # MODEL COMPARISON
    # -------------------------------------------------------------------------

    compare_mode = False

    if ENABLE_MODEL_COMPARISON and len(available_models) > 1:

        compare_mode = st.checkbox(
            "Compare all registered models",
            value=False,
            help="Run the uploaded image through every registered model.",
        )

    st.markdown("---")

    render_sidebar_panel()

    if ENABLE_PREDICTION_HISTORY:
        render_history_sidebar()

# =============================================================================
# PAGE ROUTING
# =============================================================================

# -----------------------------------------------------------------------------
# HOME PAGE
# -----------------------------------------------------------------------------

if page == "🏠 Home":

    render_app_header()

    st.markdown("## 🍎 AI-Powered Apple Safety Screening")

    st.markdown(
        """
        AppleGuard AI uses **deep learning**, **computer vision**, and
        **explainable AI (Grad-CAM)** to analyze apple surface characteristics
        and classify apples as **Fresh** or **Potentially Formalin-Mixed**.

        The system is designed for **food safety screening, research,
        education, and demonstration purposes**.
        """
    )

    st.markdown("### 🚀 Platform Highlights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Quality Classes", "2")

    with col2:
        st.metric("Available Models", str(len(available_models)))

    with col3:
        st.metric("Version", f"v{VERSION}")

    st.markdown("---")

    st.markdown("### 🔬 Core Capabilities")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.markdown(
            """
            - 🍏 **Fresh Apple Detection**
            - 🚨 **Potential Formalin Screening**
            - 📊 **Confidence Score Analysis**
            - 🔍 **Grad-CAM Explainability**
            """
        )

    with feature_col2:
        st.markdown(
            """
            - 📑 **Professional PDF Reports**
            - 📈 **Model Performance Tracking**
            - 🧠 **Multi-Model Comparison**
            - 🕒 **Prediction History Management**
            """
        )

# -----------------------------------------------------------------------------
# DETECTION PAGE
# -----------------------------------------------------------------------------

elif page == "🔍 Apple Quality Detection":

    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h1 style="font-size:2.25rem;font-weight:700;margin-bottom:0.25rem;">
                Apple Quality Detection Studio
            </h1>
            <p style="color:#64748B;font-size:1rem;">
                Upload an apple image for AI-powered freshness and formalin screening.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = render_upload_section()

    if uploaded_file is not None:

        if compare_mode:

            from PIL import Image

            image = Image.open(uploaded_file).convert("RGB")

            render_image_preview(image)

            render_model_comparison(image, available_models)

        else:

            render_prediction_workflow(
                uploaded_file,
                model_name=selected_model,
            )

    else:
        render_empty_state()

# -----------------------------------------------------------------------------
# SAFETY GUIDE PAGE
# -----------------------------------------------------------------------------

elif page == "📚 Safety & Quality Guide":

    st.markdown("# 📚 Apple Safety & Quality Guide")

    st.info(
        "Use this section to provide guidance about identifying fresh apples, "
        "safe storage practices, washing procedures, and food safety recommendations."
    )

    st.markdown("### 🍏 Fresh Apple Indicators")

    st.markdown(
        """
        - Firm and evenly textured skin
        - Natural color distribution
        - Fresh fruity aroma
        - No unusual chemical smell
        - No excessive glossy coating
        """
    )

    st.markdown("### 🚨 Possible Warning Signs")

    st.markdown(
        """
        - Unnatural excessive shine
        - Strong chemical or preservative odor
        - Unusually rigid surface texture
        - Discoloration inconsistent with the apple variety
        - Sticky or residue-like surface appearance
        """
    )

# -----------------------------------------------------------------------------
# PERFORMANCE PAGE
# -----------------------------------------------------------------------------

elif page == "📈 Model Performance":

    st.markdown("# 📈 Model Performance Dashboard")

    active_metadata = get_model_metadata(selected_model)

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:

        accuracy = (
            active_metadata.get("test_accuracy")
            or active_metadata.get("validation_accuracy")
            or 0
        )

        st.metric("Validation Accuracy", f"{accuracy * 100:.2f}%")

    with metric_col2:

        precision = (
            active_metadata.get("test_precision")
            or active_metadata.get("validation_precision")
            or 0
        )

        st.metric("Precision", f"{precision * 100:.2f}%")

    with metric_col3:

        recall = (
            active_metadata.get("test_recall")
            or active_metadata.get("validation_recall")
            or 0
        )

        st.metric("Recall", f"{float(recall) * 100:.2f}%")

    st.markdown("---")

    st.markdown(f"### 🧠 Active Model: `{selected_model}`")

    st.json(active_metadata or {"message": "No metadata available."})

# -----------------------------------------------------------------------------
# ABOUT PAGE
# -----------------------------------------------------------------------------

elif page == "ℹ️ About":

    st.markdown("# ℹ️ About AppleGuard AI")

    st.markdown(
        f"""
        **AppleGuard AI** is a computer vision research platform developed for
        automated apple quality assessment using **deep learning** and
        **explainable AI techniques**.

        ### Project Information

        - **Institution:** University of Uyo
        - **Department:** Computer Engineering
        - **Team:** Group 16
        - **Version:** v{VERSION}
        - **Framework:** TensorFlow / Keras
        - **Interface:** Streamlit Enterprise UI

        ### Research Objectives

        - Develop an AI-based apple quality screening system.
        - Detect potentially formalin-treated apples from images.
        - Provide interpretable predictions using Grad-CAM.
        - Generate professional downloadable analysis reports.
        """
    )

# =============================================================================
# FOOTER
# =============================================================================

render_app_footer()

