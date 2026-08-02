
# """
# AppleGuard AI — Reusable Streamlit Components
# Phase 1: Core layout and presentation components
# """

# from __future__ import annotations

# from typing import BinaryIO

# import streamlit as st

# from styles import (
#     render_confidence_badge,
#     render_footer,
#     render_hero_section,
#     render_probability_bar,
#     render_status_chip,
# )


# # =============================================================================
# # APPLICATION HEADER
# # =============================================================================

# def render_app_header() -> None:
#     """Render the main AppleGuard application header."""

#     st.markdown(render_hero_section(), unsafe_allow_html=True)


# # =============================================================================
# # SIDEBAR PANEL
# # =============================================================================

# def render_sidebar_panel() -> None:
#     """Render the sidebar system panel."""

#     st.sidebar.markdown("---")
#     st.sidebar.subheader("🖥️ System Status")

#     st.sidebar.markdown(
#         render_status_chip("Model Ready", "ready"),
#         unsafe_allow_html=True,
#     )

#     st.sidebar.markdown(
#         render_status_chip("Grad-CAM Ready", "ready"),
#         unsafe_allow_html=True,
#     )

#     st.sidebar.markdown("---")

#     st.sidebar.markdown("### ℹ️ About AppleGuard")

#     st.sidebar.write(
#         "AppleGuard AI is a computer vision system for detecting fresh apples "
#         "and potentially formalin-treated apples using deep learning and explainable AI."
#     )


# # =============================================================================
# # IMAGE UPLOAD SECTION
# # =============================================================================

# def render_upload_section() -> BinaryIO | None:
#     """Render the image upload section."""

#     st.markdown(
#         """
#         <div class="upload-section">
#             <div class="upload-icon">📤</div>
#             <div class="upload-title">Upload Apple Image</div>
#             Supported formats: JPG, JPEG, PNG
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     uploaded_file = st.file_uploader(
#         label="Choose an apple image",
#         type=["jpg", "jpeg", "png"],
#         label_visibility="collapsed",
#     )

#     return uploaded_file


# # =============================================================================
# # IMAGE PREVIEW
# # =============================================================================

# def render_image_preview(image, caption: str = "Uploaded Image") -> None:
#     """Render a professionally framed image preview."""

#     st.markdown(
#         f"""
#         <div class="image-frame">
#             <div class="image-frame-title">{caption}</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.image(image, use_container_width=True)


# # =============================================================================
# # PREDICTION RESULT CARD
# # =============================================================================

# def render_prediction_card(prediction: dict) -> None:
#     """Render the main prediction result card."""

#     predicted_class = prediction.get("predicted_class", "Unknown")
#     confidence = prediction.get("confidence", 0.0)
#     confidence_percentage = prediction.get("confidence_percentage", "0.00%")

#     if predicted_class.lower() == "fresh":
#         card_class = "result-fresh"
#         title = "🍏 Fresh Apple Detected"
#         description = "The model predicts that this apple appears fresh and suitable for consumption."
#     else:
#         card_class = "result-formalin"
#         title = "🚨 Formalin-Mixed Apple Detected"
#         description = (
#             "The model detected visual patterns associated with potentially "
#             "formalin-treated apples. Additional inspection is recommended."
#         )

#     st.markdown(
#         f"""
#         <div class="{card_class}">
#             <h3>{title}</h3>
#             <p>{description}</p>
#             <p><b>Confidence:</b> {confidence_percentage}</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown(
#         render_confidence_badge(confidence),
#         unsafe_allow_html=True,
#     )


# # =============================================================================
# # METRICS DASHBOARD
# # =============================================================================

# def render_metrics_dashboard(prediction: dict) -> None:
#     """Render prediction metrics in a dashboard layout."""

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric(
#             "Prediction",
#             prediction.get("predicted_class", "Unknown"),
#         )

#     with col2:
#         st.metric(
#             "Confidence",
#             prediction.get("confidence_percentage", "0.00%"),
#         )

#     with col3:
#         prediction_time = prediction.get("prediction_time_seconds", 0.0)
#         st.metric("Inference Time", f"{prediction_time:.4f} s")


# # =============================================================================
# # PROBABILITY SECTION
# # =============================================================================

# def render_probability_section(probabilities: dict[str, float]) -> None:
#     """Render animated probability bars for each class."""

#     st.markdown("### 📊 Class Probabilities")

#     sorted_probabilities = sorted(
#         probabilities.items(),
#         key=lambda item: item[1],
#         reverse=True,
#     )

#     for class_name, probability in sorted_probabilities:
#         st.markdown(
#             render_probability_bar(class_name, probability),
#             unsafe_allow_html=True,
#         )


# # =============================================================================
# # GRAD-CAM PLACEHOLDER
# # =============================================================================

# def render_gradcam_placeholder() -> None:
#     """Render a placeholder for Grad-CAM visualization."""

#     st.markdown("### 🔍 Grad-CAM Visualization")

#     st.markdown(
#         """
#         <div class="comparison-container">
#             <div class="comparison-card">
#                 <div class="comparison-title">Original Image</div>
#                 <p>Original image preview will appear here.</p>
#             </div>
#             <div class="comparison-card">
#                 <div class="comparison-title">Grad-CAM Overlay</div>
#                 <p>Grad-CAM heatmap overlay will appear here.</p>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # =============================================================================
# # REPORT PANEL PLACEHOLDER
# # =============================================================================

# def render_report_panel() -> None:
#     """Render the professional report export panel placeholder."""

#     st.markdown("### 📄 Export Reports")

#     st.markdown(
#         """
#         <div class="report-panel">
#             <div class="report-title">Professional Report Export</div>
#             <div class="report-description">
#                 Generate and download prediction reports in JSON, CSV, and PDF formats for documentation and presentation purposes.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.button("📄 JSON Report", use_container_width=True)

#     with col2:
#         st.button("📊 CSV Report", use_container_width=True)

#     with col3:
#         st.button("📑 PDF Report", use_container_width=True)


# # =============================================================================
# # EMPTY STATE
# # =============================================================================

# def render_empty_state() -> None:
#     """Render the initial empty state before an image is uploaded."""

#     st.markdown(
#         """
#         <div class="card" style="text-align:center;">
#             <h3>🍎 Ready for Analysis</h3>
#             <p>
#                 Upload an apple image to begin AI-powered quality detection, confidence analysis, and Grad-CAM explainability visualization.
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # =============================================================================
# # APPLICATION FOOTER
# # =============================================================================

# def render_app_footer() -> None:
#     """Render the application footer."""

#     st.markdown(render_footer(), unsafe_allow_html=True)


# # =============================================================================
# # PUBLIC EXPORTS
# # =============================================================================

# __all__ = [
#     "render_app_header",
#     "render_sidebar_panel",
#     "render_upload_section",
#     "render_image_preview",
#     "render_prediction_card",
#     "render_metrics_dashboard",
#     "render_probability_section",
#     "render_gradcam_placeholder",
#     "render_report_panel",
#     "render_empty_state",
#     "render_app_footer",
# ]


# ## `app/components.py` — Phase 2

# # =============================================================================
# # BACKEND INTEGRATION COMPONENTS
# # =============================================================================

# from pathlib import Path
# from tempfile import NamedTemporaryFile

# from PIL import Image

# from src.gradcam import (
#     GradCAM,
#     find_last_conv_layer,
#     generate_heatmap,
#     overlay_heatmap,
#     image_to_array,
#     array_to_image,
# )
# from src.predict import predict_image
# from src.report_generator import generate_complete_report


# # =============================================================================
# # FILE HANDLING
# # =============================================================================

# def save_uploaded_file(uploaded_file) -> Path:
#     """Save an uploaded Streamlit file to a temporary location."""

#     suffix = Path(uploaded_file.name).suffix

#     with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
#         temp_file.write(uploaded_file.getbuffer())
#         return Path(temp_file.name)


# # =============================================================================
# # PROCESSING STATE
# # =============================================================================

# def render_processing_state() -> None:
#     """Render a processing indicator while the model is running."""

#     st.markdown(
#         """
#         <div class="processing-card">
#             <div class="processing-spinner"></div>
#             <div class="processing-title">AppleGuard AI Processing</div>
#             <div>
#                 Running image preprocessing, model inference, Grad-CAM generation,
#                 and report preparation...
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # =============================================================================
# # GRAD-CAM COMPARISON
# # =============================================================================

# def render_gradcam_comparison(original_image, gradcam_image) -> None:
#     """Render a side-by-side Grad-CAM comparison."""

#     st.markdown("### 🔍 Grad-CAM Explainability")

#     col1, col2 = st.columns(2)

#     with col1:
#         render_image_preview(original_image, "Original Image")

#     with col2:
#         render_image_preview(gradcam_image, "Grad-CAM Overlay")

#     st.markdown(
#         """
#         <div class="success-strip">
#             <b>Interpretation:</b> Red and yellow regions indicate the
#             image areas that contributed most strongly to the model’s prediction.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # =============================================================================
# # REPORT DOWNLOADS
# # =============================================================================

# def render_report_downloads(report_paths: dict[str, Path]) -> None:
#     """Render functional report download buttons."""

#     st.markdown("### 📄 Download Reports")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         with open(report_paths["json"], "rb") as file:
#             st.download_button(
#                 label="📄 JSON Report",
#                 data=file,
#                 file_name=report_paths["json"].name,
#                 mime="application/json",
#                 use_container_width=True,
#             )

#     with col2:
#         with open(report_paths["csv"], "rb") as file:
#             st.download_button(
#                 label="📊 CSV Report",
#                 data=file,
#                 file_name=report_paths["csv"].name,
#                 mime="text/csv",
#                 use_container_width=True,
#             )

#     with col3:
#         with open(report_paths["pdf"], "rb") as file:
#             st.download_button(
#                 label="📑 PDF Report",
#                 data=file,
#                 file_name=report_paths["pdf"].name,
#                 mime="application/pdf",
#                 use_container_width=True,
#             )


# # =============================================================================
# # MESSAGE HELPERS
# # =============================================================================

# def render_error_message(message: str) -> None:
#     """Render a styled error message."""

#     st.error(f"❌ {message}")


# def render_success_message(message: str) -> None:
#     """Render a styled success message."""

#     st.success(f"✅ {message}")


# # =============================================================================
# # GRAD-CAM GENERATION
# # =============================================================================

# def create_gradcam_overlay(model, image_path: Path, class_index: int):
#     """Generate a Grad-CAM overlay image using the existing Grad-CAM API."""

#     gradcam = GradCAM(model)

#     # Use the class API if available
#     if hasattr(gradcam, "generate"):
#         return gradcam.generate(
#             image_path=image_path,
#             class_index=class_index,
#             alpha=0.4,
#         )

#     # Fallback using the functional API
#     from src.preprocess import preprocess_image

#     input_tensor = preprocess_image(image_path)

#     last_conv_layer_name = find_last_conv_layer(model)

#     heatmap = generate_heatmap(
#         model=model,
#         image_tensor=input_tensor,
#         last_conv_layer_name=last_conv_layer_name,
#         class_index=class_index,
#     )

#     original_image = Image.open(image_path).convert("RGB")
#     original_array = image_to_array(original_image)

#     overlay_array = overlay_heatmap(
#         image_array=original_array,
#         heatmap=heatmap,
#         alpha=0.4,
#     )

#     return array_to_image(overlay_array)


# # =============================================================================
# # COMPLETE PREDICTION WORKFLOW
# # =============================================================================

# def render_prediction_workflow(uploaded_file) -> None:
#     """Run the complete AppleGuard prediction workflow."""

#     try:
#         # ------------------------------------------------------------------
#         # Save uploaded image
#         # ------------------------------------------------------------------

#         image_path = save_uploaded_file(uploaded_file)

#         original_image = Image.open(image_path).convert("RGB")

#         # ------------------------------------------------------------------
#         # Show preview
#         # ------------------------------------------------------------------

#         render_image_preview(original_image)

#         # ------------------------------------------------------------------
#         # Run prediction
#         # ------------------------------------------------------------------

#         with st.spinner("Running AppleGuard AI analysis..."):
#             prediction_result = predict_image(image_path)

#         # ------------------------------------------------------------------
#         # Display prediction results
#         # ------------------------------------------------------------------

#         st.markdown("---")
#         st.header("🧠 Prediction Results")

#         render_prediction_card(prediction_result)
#         render_metrics_dashboard(prediction_result)

#         probabilities = prediction_result.get("probabilities", {})

#         if probabilities:
#             render_probability_section(probabilities)

#         # ------------------------------------------------------------------
#         # Generate Grad-CAM
#         # ------------------------------------------------------------------

#         st.markdown("---")

#         model = prediction_result.get("model")

#         if model is not None:
#             predicted_index = prediction_result.get("predicted_index", 0)

#             gradcam_image = create_gradcam_overlay(
#                 model=model,
#                 image_path=image_path,
#                 class_index=predicted_index,
#             )

#             render_gradcam_comparison(original_image, gradcam_image)

#         # ------------------------------------------------------------------
#         # Generate reports
#         # ------------------------------------------------------------------

#         st.markdown("---")

#         report_paths = generate_complete_report(
#             prediction_result=prediction_result,
#             image_name=uploaded_file.name,
#         )

#         render_report_downloads(report_paths)

#         # ------------------------------------------------------------------
#         # Success message
#         # ------------------------------------------------------------------

#         render_success_message("Apple analysis completed successfully.")

#     except Exception as error:
#         render_error_message(f"Prediction workflow failed: {error}")


# # =============================================================================
# # EXTEND PUBLIC EXPORTS
# # =============================================================================

# __all__.extend([
#     "save_uploaded_file",
#     "render_processing_state",
#     "render_gradcam_comparison",
#     "render_report_downloads",
#     "render_error_message",
#     "render_success_message",
#     "create_gradcam_overlay",
#     "render_prediction_workflow",
# ])

"""
===============================================================================
AppleGuard AI — Reusable Streamlit Components
===============================================================================

Combines layout/presentation components with backend-integrated workflow
components (prediction, Grad-CAM, reporting, history, and model comparison).
"""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import streamlit as st
from PIL import Image

from app.styles import (
    render_confidence_badge,
    render_footer,
    render_probability_bar,
    render_status_chip,
)
from src.config import (
    CLASS_NAMES,
    DEFAULT_MODEL,
    ENABLE_GRADCAM,
    HERO_IMAGE_PATH,
    UPLOAD_PLACEHOLDER_PATH,
)



from src.predict import (
    compare_models,
    load_model,
    predict_image,
)

from src.gradcam import (
    GradCAM,
    find_last_conv_layer,
    generate_heatmap,
    overlay_heatmap,
)
from src.helpers import format_datetime

from src.report_generator import generate_complete_report

# =============================================================================
# APPLICATION HEADER
# =============================================================================



def render_app_header() -> None:
    """Render the AppleGuard AI hero header."""

    # Display hero banner if available
    if HERO_IMAGE_PATH.exists():
        st.image(str(HERO_IMAGE_PATH), use_container_width=True)

    st.markdown(
        """
        <div class="hero-section">
            <h1>🍎 AppleGuard AI</h1>
            <p>
                AI-powered apple quality screening using deep learning,
                computer vision, and Grad-CAM explainability.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )





# =============================================================================
# SIDEBAR PANEL
# =============================================================================

def render_sidebar_panel() -> None:
    """Render the sidebar system status / about panel."""

    st.sidebar.markdown("---")
    st.sidebar.subheader("🖥️ System Status")

    st.sidebar.markdown(
        render_status_chip("Model Ready", "ready"),
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        render_status_chip("Grad-CAM Ready" if ENABLE_GRADCAM else "Grad-CAM Disabled",
                            "ready" if ENABLE_GRADCAM else "warning"),
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### ℹ️ About AppleGuard")

    st.sidebar.write(
        "AppleGuard AI is a computer vision system for detecting fresh apples "
        "and potentially formalin-treated apples using deep learning and explainable AI."
    )


# =============================================================================
# PREDICTION HISTORY (SIDEBAR)
# =============================================================================

def _append_to_history(image_name: str, prediction_result: dict[str, Any]) -> None:
    """Append a prediction result to the in-session history."""

    if "appleguard_history" not in st.session_state:
        st.session_state.appleguard_history = []

    st.session_state.appleguard_history.insert(
        0,
        {
            "image_name": image_name,
            "predicted_class": prediction_result.get("predicted_class", "Unknown"),
            "confidence": prediction_result.get("confidence_percentage", "Unknown"),
            "model_name": prediction_result.get("model_name", "Unknown"),
            "timestamp": format_datetime(),
        },
    )

    # Keep the last 20 entries only
    st.session_state.appleguard_history = st.session_state.appleguard_history[:20]


def render_history_sidebar() -> None:
    """Render recent prediction history in the sidebar."""

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🕘 Recent Predictions")

    history = st.session_state.get("appleguard_history", [])

    if not history:
        st.sidebar.caption("No predictions yet this session.")
        return

    for entry in history[:5]:
        icon = "🍏" if entry["predicted_class"].lower() == "fresh" else "🚨"
        st.sidebar.markdown(
            f"{icon} **{entry['image_name']}** — {entry['predicted_class']} "
            f"({entry['confidence']})"
        )

    if st.sidebar.button("Clear history", use_container_width=True):
        st.session_state.appleguard_history = []
        st.rerun()


# =============================================================================
# IMAGE UPLOAD SECTION
# =============================================================================

def render_upload_section():
    """Render the upload area with a custom placeholder image."""

    if UPLOAD_PLACEHOLDER_PATH.exists():
        st.image(str(UPLOAD_PLACEHOLDER_PATH), use_container_width=True)

    st.markdown("### 📤 Upload Apple Image")

    return st.file_uploader(
        "Choose an apple image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )




# =============================================================================
# IMAGE PREVIEW
# =============================================================================

def render_image_preview(image, caption: str = "Uploaded Image") -> None:
    """Render a professionally framed image preview."""

    st.markdown(
        f"""
        <div class="image-frame">
            <div class="image-frame-title">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.image(image, use_container_width=True)


# =============================================================================
# PREDICTION RESULT CARD
# =============================================================================

def render_prediction_card(prediction: dict) -> None:
    """Render the main prediction result card."""

    predicted_class = prediction.get("predicted_class", "Unknown")
    confidence = prediction.get("confidence", 0.0)
    confidence_percentage = prediction.get("confidence_percentage", "0.00%")

    if predicted_class.lower() == "fresh":
        card_class = "result-fresh"
        title = "🍏 Fresh Apple Detected"
        description = "The model predicts that this apple appears fresh and suitable for consumption."
    else:
        card_class = "result-formalin"
        title = "🚨 Formalin-Mixed Apple Detected"
        description = (
            "The model detected visual patterns associated with potentially "
            "formalin-treated apples. Additional inspection is recommended."
        )

    st.markdown(
        f"""
        <div class="{card_class}">
            <h3>{title}</h3>
            <p>{description}</p>
            <p><b>Confidence:</b> {confidence_percentage}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        render_confidence_badge(confidence),
        unsafe_allow_html=True,
    )


# =============================================================================
# METRICS DASHBOARD
# =============================================================================

def render_metrics_dashboard(prediction: dict) -> None:
    """Render prediction metrics in a dashboard layout."""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Prediction", prediction.get("predicted_class", "Unknown"))

    with col2:
        st.metric("Confidence", prediction.get("confidence_percentage", "0.00%"))

    with col3:
        prediction_time = prediction.get("prediction_time_seconds", 0.0)
        st.metric("Inference Time", f"{prediction_time:.4f} s")


# =============================================================================
# PROBABILITY SECTION
# =============================================================================

def render_probability_section(probabilities: dict[str, float]) -> None:
    """Render animated probability bars for each class."""

    st.markdown("### 📊 Class Probabilities")

    sorted_probabilities = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    for class_name, probability in sorted_probabilities:
        st.markdown(
            render_probability_bar(class_name, probability),
            unsafe_allow_html=True,
        )


# =============================================================================
# EMPTY STATE
# =============================================================================

def render_empty_state() -> None:
    """Render the initial empty state before an image is uploaded."""

    st.markdown(
        """
        <div class="card" style="text-align:center;">
            <h3>🍎 Ready for Analysis</h3>
            <p>
                Upload an apple image to begin AI-powered quality detection, confidence analysis, and Grad-CAM explainability visualization.
            </p>
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


# =============================================================================
# FILE HANDLING
# =============================================================================

def save_uploaded_file(uploaded_file) -> Path:
    """Save an uploaded Streamlit file to a temporary location."""

    suffix = Path(uploaded_file.name).suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


# =============================================================================
# GRAD-CAM GENERATION
# =============================================================================

def create_gradcam_overlay(model, image_path: Path, class_index: int):
    """Generate a Grad-CAM overlay image using the existing Grad-CAM API."""

    from src.preprocess import preprocess_image

    gradcam = GradCAM(model)

    last_conv_layer_name = gradcam.last_conv_layer_name or find_last_conv_layer(model)

    original_image = Image.open(image_path).convert("RGB")

    input_array = preprocess_image(original_image)
    input_tensor = input_array[None, ...]  # add batch dimension

    heatmap = generate_heatmap(
        model=model,
        image=input_tensor,
        last_conv_layer_name=last_conv_layer_name,
        class_index=class_index,
    )

    overlay_image = overlay_heatmap(
        original_image=original_image,
        heatmap=heatmap,
        alpha=0.4,
    )

    return overlay_image


# =============================================================================
# GRAD-CAM COMPARISON DISPLAY
# =============================================================================

def render_gradcam_comparison(original_image, gradcam_image) -> None:
    """Render a side-by-side Grad-CAM comparison."""

    st.markdown("### 🔍 Grad-CAM Explainability")

    col1, col2 = st.columns(2)

    with col1:
        render_image_preview(original_image, "Original Image")

    with col2:
        render_image_preview(gradcam_image, "Grad-CAM Overlay")

    st.markdown(
        """
        <div class="success-strip">
            <b>Interpretation:</b> Red and yellow regions indicate the
            image areas that contributed most strongly to the model's prediction.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# REPORT DOWNLOADS
# =============================================================================

def render_report_downloads(report_paths: dict[str, Path]) -> None:
    """Render functional report download buttons."""

    st.markdown("### 📄 Download Reports")

    col1, col2, col3 = st.columns(3)

    with col1, open(report_paths["json"], "rb") as file:
        st.download_button(
            label="📄 JSON Report",
            data=file,
            file_name=report_paths["json"].name,
            mime="application/json",
            use_container_width=True,
        )

    with col2, open(report_paths["csv"], "rb") as file:
        st.download_button(
            label="📊 CSV Report",
            data=file,
            file_name=report_paths["csv"].name,
            mime="text/csv",
            use_container_width=True,
        )

    with col3, open(report_paths["pdf"], "rb") as file:
        st.download_button(
            label="📑 PDF Report",
            data=file,
            file_name=report_paths["pdf"].name,
            mime="application/pdf",
            use_container_width=True,
        )


def render_prediction_workflow(
    uploaded_file,
    model_name: str,
    use_backend: bool = True,
) -> None:
    """Run the complete AppleGuard prediction workflow."""

    # ------------------------------------------------------------------
    # Load uploaded image
    # ------------------------------------------------------------------
    uploaded_file.seek(0)
    image = Image.open(uploaded_file).convert("RGB")

    # Display preview
    render_image_preview(image)

    # ------------------------------------------------------------------
    # Run prediction
    # ------------------------------------------------------------------
    with st.spinner("🧠 Analyzing apple quality..."):

        try:
            uploaded_file.seek(0)

            if use_backend:
                # FastAPI backend prediction
                result = predict_image(uploaded_file, model_name)
            else:
                # Local prediction fallback
                from src.predict import predict_image as local_predict_image

                result = local_predict_image(image, model_name)

            # ----------------------------------------------------------
            # Normalize prediction result
            # ----------------------------------------------------------
            prediction_result = {
                "predicted_class": result.get("predicted_class", "Unknown"),
                "confidence": result.get("confidence", 0.0),
                "confidence_percentage": result.get("confidence_percentage", "0.00%"),
                "probabilities": result.get("probabilities", {}),
                "model_name": result.get("model_name", model_name),
                "prediction_time_seconds": result.get("prediction_time_seconds", 0.0),
                "is_confident": result.get("is_confident", False),
            }

            # ----------------------------------------------------------
            # Display prediction results
            # ----------------------------------------------------------
            st.markdown("---")
            st.header("🧠 Prediction Results")

            render_prediction_card(prediction_result)
            render_metrics_dashboard(prediction_result)

            probabilities = prediction_result.get("probabilities", {})

            if probabilities:
                render_probability_section(probabilities)

            # ----------------------------------------------------------
            # Generate Grad-CAM visualization
            # ----------------------------------------------------------
            try:
                uploaded_file.seek(0)

                gradcam_image = generate_gradcam(
                    uploaded_file,
                    model_name,
                )

                render_gradcam_comparison(image, gradcam_image)

            except Exception as error:
                st.warning(f"Grad-CAM unavailable: {error}")

            # ----------------------------------------------------------
            # Generate downloadable reports
            # ----------------------------------------------------------
            st.markdown("---")
            st.header("📄 Download Reports")

            report_paths = generate_complete_report(
                prediction_result=prediction_result,
                image_name=uploaded_file.name,
            )

            render_report_downloads(report_paths)

            # ----------------------------------------------------------
            # Save prediction history
            # ----------------------------------------------------------
            _append_to_history(
                uploaded_file.name,
                prediction_result,
            )

            st.success(
                "✅ Analysis and report generation completed successfully."
            )

        except Exception as error:
            st.error(f"Prediction failed: {error}")


# =============================================================================
# MESSAGE HELPERS
# =============================================================================

def render_error_message(message: str) -> None:
    """Render a styled error message."""

    st.error(f"❌ {message}")




# =============================================================================
# MODEL COMPARISON WORKFLOW
# =============================================================================

def render_model_comparison(image, model_names: list[str] | None = None) -> None:
    """Run the uploaded image through every registered model and compare."""

    st.markdown("### 🧪 Model Comparison")

    with st.spinner("Comparing all registered models..."):
        results = compare_models(image, model_names)

    rows = []

    for model_name, result in results.items():
        if "error" in result:
            rows.append(
                {
                    "Model": model_name,
                    "Prediction": "Error",
                    "Confidence": "-",
                    "Time (s)": "-",
                    "Details": result["error"],
                }
            )
        else:
            rows.append(
                {
                    "Model": model_name,
                    "Prediction": result.get("predicted_class", "Unknown"),
                    "Confidence": result.get("confidence_percentage", "Unknown"),
                    "Time (s)": f"{result.get('prediction_time_seconds', 0):.4f}",
                    "Details": "OK",
                }
            )

    st.dataframe(rows, use_container_width=True, hide_index=True)

    # Log the best-confidence result to history for continuity
    successful = {k: v for k, v in results.items() if "error" not in v}
    if successful:
        best_model = max(successful, key=lambda name: successful[name]["confidence"])
        _append_to_history(f"[compare] {best_model}", successful[best_model])


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "create_gradcam_overlay",
    "render_app_footer",
    "render_app_header",
    "render_empty_state",
    "render_error_message",
    "render_gradcam_comparison",
    "render_history_sidebar",
    "render_image_preview",
    "render_metrics_dashboard",
    "render_model_comparison",
    "render_prediction_card",
    "render_prediction_workflow",
    "render_probability_section",
    "render_report_downloads",
    "render_sidebar_panel",
    "render_success_message",
    "render_upload_section",
    "save_uploaded_file",
]