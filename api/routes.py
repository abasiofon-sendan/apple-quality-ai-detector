## `api/routes.py`


"""
===============================================================================
AppleGuard AI — FastAPI Routes
===============================================================================

Project      : AppleGuard AI
Module       : api.routes
Author       : Group 16

Purpose
-------
Defines all REST API endpoints for AppleGuard AI.

Responsibilities
----------------
• Health check endpoint
• Model information endpoint
• Prediction endpoints
• Grad-CAM visualization endpoint

This module acts only as a thin wrapper around the functionality implemented
inside the src package.

No AI logic is implemented here.
===============================================================================
"""


from __future__ import annotations

from io import BytesIO
from typing import Any, cast

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from api.dependencies import (
    load_uploaded_image,
    validate_model_name,
    validate_upload_file,
)
from api.schemas import HealthResponse, ModelInfo, PredictionResponse
from src.config import API_VERSION, DEFAULT_MODEL, get_available_models
from src.gradcam import GradCAM
from src.predict import model_exists, load_model
import src.predict as predict_module


predict_with_selected_model = getattr(
    predict_module,
    "predict_with_selected_model",
)


from src.preprocess import prepare_image_for_prediction

# =============================================================================
# ROUTER
# =============================================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["AppleGuard AI"],
)

# =============================================================================
# HEALTH CHECK
# =============================================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API Health Check",
)
async def health_check() -> HealthResponse:
    """
    Check API availability and model status.
    """

    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        models_loaded=len(get_available_models()),
    )

# =============================================================================
# MODEL INFORMATION
# =============================================================================

@router.get(
    "/models",
    response_model=list[ModelInfo],
    summary="Available Models",
)
async def available_models() -> list[ModelInfo]:
    """
    Return all registered AI models.
    """

    return [
        ModelInfo(
            name=model_name,
            available=model_exists(model_name),
            is_default=(model_name == DEFAULT_MODEL),
        )
        for model_name in get_available_models()
    ]

# =============================================================================
# SINGLE MODEL PREDICTION
# =============================================================================

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Apple Quality",
)
async def predict(
    file: UploadFile = Depends(validate_upload_file),
    model_name: str = Depends(validate_model_name),
) -> PredictionResponse:
    """Predict the quality of an uploaded apple image."""

    image = await load_uploaded_image(file)

    result = predict_with_selected_model(
        image=image,
        model_name=model_name,
    )

    return PredictionResponse(
        model=result["model_name"],
        prediction=result["predicted_class"],
        confidence=result["confidence"],
        confidence_percent=float(
            result["confidence_percentage"].replace("%", "")
        ),
        probabilities=result["probabilities"],
        is_confident=result["is_confident"],
    )

# =============================================================================
# COMBINED MODEL PREDICTION
# =============================================================================
@router.post(
    "/predict/combined",
    response_model=PredictionResponse,
    summary="Combined AI Prediction",
)
async def predict_combined(
    file: UploadFile = Depends(validate_upload_file),
) -> PredictionResponse:

    image = await load_uploaded_image(file)

    results = [
        predict_with_selected_model(image=image, model_name=model_name)
        for model_name in get_available_models()
        if model_exists(model_name)
    ]

    if not results:
        raise RuntimeError("No available models found.")

    result = max(results, key=lambda prediction: prediction.get("confidence", 0))

    return PredictionResponse(
        model=result["model_name"],
        prediction=result["predicted_class"],
        confidence=result["confidence"],
        confidence_percent=float(
            result["confidence_percentage"].replace("%", "")
        ),
        probabilities=result["probabilities"],
        is_confident=result["is_confident"],
        selection_mode="best_model",
        models_evaluated=len(results),
        all_predictions=results,
    )

# =============================================================================
# GRAD-CAM VISUALIZATION
# =============================================================================


@router.post(
    "/gradcam",
    summary="Generate Grad-CAM Visualization",
)
async def generate_gradcam(
    file: UploadFile = Depends(validate_upload_file),
    model_name: str = Depends(validate_model_name),
):
    """
    Generate a Grad-CAM visualization for an uploaded image.
    """

    # Load image from request
    image = await load_uploaded_image(file)

    # Load the selected model directly
    model = load_model(model_name)

    # Prepare image for Grad-CAM
    processed_image = prepare_image_for_prediction(image)

    try:
        # Create Grad-CAM helper
        gradcam = GradCAM(model)

        # Generate heatmap
        heatmap = gradcam.generate_heatmap(processed_image)

        # Overlay heatmap on original image
        overlay_image = gradcam.overlay(
            original_image=image,
            heatmap=heatmap,
            alpha=0.4,
        )

    except Exception as error:
        raise RuntimeError(
            f"Grad-CAM could not be generated for model '{model_name}': {error}"
        ) from error

    # Convert to PNG stream
    buffer = BytesIO()

    overlay_image.save(
        buffer,
        format="PNG",
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png",
    )



# =============================================================================
# ROOT INFORMATION
# =============================================================================

@router.get(
    "/info",
    summary="API Information",
)
async def api_info():
    """
    Return API information and available endpoints.
    """

    return {
        "name": "AppleGuard AI API",
        "version": API_VERSION,
        "endpoints": {
            "health": "/api/v1/health",
            "models": "/api/v1/models",
            "predict": "/api/v1/predict",
            "combined_prediction": "/api/v1/predict/combined",
            "gradcam": "/api/v1/gradcam",
        },
    }

# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = ["router"]

