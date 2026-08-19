"""
===============================================================================
AppleGuard AI — Streamlit Components (Flat UI)
===============================================================================

Reusable render functions for the single-page, two-column flat interface.
Only the components needed by the core Fresh / Formalin prediction flow are
kept — multi-page nav, theme switching, model comparison, history, Grad-CAM
display, and report downloads have been removed by design.
===============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from PIL import Image

from app.styles import render_footer, render_probability_bar
from src import config
from src.config import UPLOAD_PLACEHOLDER_PATH


# =============================================================================
# APPLICATION HEADER
# =============================================================================

def render_app_header() -> None:
    """Render the slim flat application header."""

    st.markdown(
        """
        <div class="flat-header">
            <div>
                <div class="flat-header-brand">AppleGuard AI</div>
                <div class="flat-header-tag">AI-powered apple quality screening</div>
            </div>
            <div style="text-align:right;">
                <div class="flat-header-tag">Fresh / Formalin-mixed detection</div>
                <div class="flat-header-tag">Deep Learning &bull; Grad-CAM</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar(available_models, current_model) -> str:
    """Render the slim sidebar: branding + model dropdown.

    Returns the selected model name.
    """

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">AppleGuard AI</div>
        <div class="sidebar-sub">Quality Screening</div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("#### 🧠 Model")

    selected_model = st.sidebar.selectbox(
        "Active model",
        available_models,
        index=available_models.index(current_model)
        if current_model in available_models
        else 0,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")

    metadata = config.get_model_metadata(selected_model)

    if metadata:
        accuracy = (
            metadata.get("test_accuracy")
            or metadata.get("validation_accuracy")
            or 0.0
        )
        st.sidebar.markdown(
            f"""
            <div class="flat-card-muted" style="font-size:0.8rem;">
                <b style="color:#111827;">Test Accuracy</b><br>
                {accuracy * 100:.2f}%
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_model


# =============================================================================
# UPLOAD SECTION
# =============================================================================

def render_upload_section():
    """Render the flat upload panel with an optional placeholder image.

    The uploaded image preview replaces the placeholder once a file is chosen.

    Returns a tuple of (uploaded_file, left_column_container, right_column_container).
    """

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown(
            '<div class="flat-card-title">Upload Apple Image</div>',
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose an apple image",
            type=["jpg", "jpeg", "png","webp"],
            label_visibility="collapsed",
        )

        preview_image = None
        if uploaded_file is not None:
            uploaded_file.seek(0)
            preview_image = Image.open(uploaded_file).convert("RGB")
            render_image_preview(preview_image, "Uploaded Image")
        elif UPLOAD_PLACEHOLDER_PATH.exists():
            st.image(str(UPLOAD_PLACEHOLDER_PATH), use_container_width=True)

    return uploaded_file, left_col, right_col


# =============================================================================
# IMAGE PREVIEW
# =============================================================================

def render_image_preview(image, caption: str = "Uploaded Image") -> None:
    """Render a flat-framed image preview."""

    st.markdown(
        f'<div class="image-frame"><div style="text-align:center;font-size:0.85rem;font-weight:600;color:#6B7280;margin-bottom:0.5rem;">{caption}</div></div>',
        unsafe_allow_html=True,
    )
    st.image(image, use_container_width=True)


# =============================================================================
# PREDICTION RESULT CARD
# =============================================================================

def render_prediction_result(prediction: dict[str, Any]) -> None:
    """Render the flat prediction result panel and probability bars."""

    predicted_class = prediction.get("predicted_class", "Unknown")
    confidence = prediction.get("confidence", 0.0)
    confidence_percentage = prediction.get("confidence_percentage", "0.00%")
    probabilities = prediction.get("probabilities", {})
    model_name = prediction.get("model_name", "Unknown")

    is_fresh = str(predicted_class).lower() == "fresh"

    if is_fresh:
        panel_class = "result-fresh"
        icon = ""
        title = "Fresh Apple"
        sub = "The model predicts this apple appears fresh."
    else:
        panel_class = "result-formalin"
        icon = ""
        title = "Formalin-Mixed Apple"
        sub = "Visual patterns associated with potential formalin treatment detected."

    st.markdown(
        f"""
        <div class="result-panel {panel_class}">
            <div class="result-class">{icon} {title}</div>
            <div class="result-confidence">{confidence_percentage}</div>
            <div style="font-size:0.85rem;color:#6B7280;">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="flat-card-title" style="font-size:0.85rem;">Class Probabilities</div>',
        unsafe_allow_html=True,
    )

    if probabilities:
        fresh_prob = probabilities.get("Fresh", 0.0)
        formalin_prob = probabilities.get("Formalin-mixed", 0.0)

        st.markdown(
            render_probability_bar("Fresh", fresh_prob),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_probability_bar("Formalin-mixed", formalin_prob, danger=True),
            unsafe_allow_html=True,
        )

    prediction_time = prediction.get("prediction_time_seconds", 0.0)

    st.markdown(
        f"""
        <div class="meta-line">
            Model: {model_name} &bull; Inference time: {prediction_time:.2f} s
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# COMPLETE PREDICTION WORKFLOW
# =============================================================================

def render_prediction_workflow(uploaded_file, model_name: str, result_container) -> None:
    """Run the prediction on an uploaded image and render the result.

    The preview is rendered inside the left panel by ``render_upload_section``.
    This workflow runs inference (FastAPI backend when reachable, else local
    engine) and draws the result in the right column.
    """

    import traceback

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")

        with st.spinner("Analyzing apple quality..."):
            result = _run_prediction(uploaded_file, image, model_name)

        result["model_name"] = result.get("model_name", model_name)

        with result_container:
            render_prediction_result(result)

    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.caption(traceback.format_exc()[-2000:])


def _run_prediction(uploaded_file, image, model_name: str) -> dict[str, Any]:
    """Run inference using the FastAPI backend when available, else local."""

    from src.predict import predict_image as local_predict

    try:
        from api.api_Client import predict_image as api_predict

        uploaded_file.seek(0)
        result = api_predict(uploaded_file, model_name)

        if isinstance(result, dict) and "error" not in result:
            return result
    except Exception:
        pass

    return local_predict(image, model_name)


# =============================================================================
# EMPTY STATE
# =============================================================================

def render_empty_state() -> None:
    """Render the initial empty state before an image is uploaded."""

    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size:2rem;">🍎</div>
            <div style="margin-top:0.5rem;font-weight:600;color:#111827;">Ready for Analysis</div>
            <div style="margin-top:0.25rem;">
                Upload an apple image to run AI-powered freshness and
                formalin-mixed screening.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# APPLICATION FOOTER
# =============================================================================

def render_app_footer() -> None:
    """Render the application footer."""

    st.markdown(render_footer(), unsafe_allow_html=True)


__all__ = [
    "render_app_footer",
    "render_app_header",
    "render_empty_state",
    "render_image_preview",
    "render_prediction_result",
    "render_prediction_workflow",
    "render_sidebar",
    "render_upload_section",
]
