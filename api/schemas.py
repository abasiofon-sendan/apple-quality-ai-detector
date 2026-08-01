## `api/schemas.py`


"""
===============================================================================
AppleGuard AI — FastAPI Schemas
===============================================================================

Project      : AppleGuard AI
Module       : api.schemas
Author       : Group 16

Purpose
-------
Defines all request and response models used by the AppleGuard AI FastAPI
backend.

Responsibilities
----------------
• Request validation
• Response serialization
• API documentation
• Shared data models

This module intentionally contains NO business logic.

Prediction, preprocessing, Grad-CAM generation, and report generation remain
inside the src package.
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# =============================================================================
# PROBABILITY RESPONSE
# =============================================================================

class ProbabilityResponse(BaseModel):
    """
    Prediction probabilities for each AppleGuard class.
    """

    Fresh: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability that the apple is fresh.",
        examples=[0.9324],
    )

    Formalin_Mixed: float = Field(
        ...,
        alias="Formalin-mixed",
        ge=0.0,
        le=1.0,
        description="Probability that the apple is potentially formalin-mixed.",
        examples=[0.0676],
    )

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "Fresh": 0.9324,
                "Formalin-mixed": 0.0676,
            }
        },
    )

# =============================================================================
# PREDICTION RESPONSE
# =============================================================================

class PredictionResponse(BaseModel):
    """
    Standard AppleGuard prediction response.
    """

    model: str = Field(
        ...,
        description="Model used for the prediction.",
        examples=["appleguard_cnn_v1"],
    )

    prediction: str = Field(
        ...,
        description="Predicted class label.",
        examples=["Fresh"],
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Raw confidence score between 0 and 1.",
        examples=[0.9324],
    )

    confidence_percent: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Confidence score expressed as a percentage.",
        examples=[93.24],
    )

    probabilities: dict[str, float] = Field(
        ...,
        description="Probability distribution across all classes.",
    )

    is_confident: bool = Field(
        ...,
        description="Whether the prediction exceeds the configured confidence threshold.",
        examples=[True],
    )

    selection_mode: str | None = Field(
        default=None,
        description="Prediction selection strategy (single_model, combined, etc.).",
        examples=["single_model"],
    )

    models_evaluated: int | None = Field(
        default=None,
        ge=1,
        description="Number of models evaluated during combined prediction.",
        examples=[3],
    )

    all_predictions: list[dict[str, Any]] | None = Field(
        default=None,
        description="Detailed results from all evaluated models.",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the prediction response was generated.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "appleguard_cnn_v1",
                "prediction": "Fresh",
                "confidence": 0.9324,
                "confidence_percent": 93.24,
                "probabilities": {
                    "Fresh": 0.9324,
                    "Formalin-mixed": 0.0676,
                },
                "is_confident": True,
                "selection_mode": "single_model",
                "models_evaluated": 1,
            }
        },
    )

# =============================================================================
# HEALTH RESPONSE
# =============================================================================

class HealthResponse(BaseModel):
    """
    API health check response.
    """

    status: str = Field(
        ...,
        description="Current API health status.",
        examples=["healthy"],
    )

    version: str = Field(
        ...,
        description="API version.",
        examples=["1.0.0"],
    )

    models_loaded: int = Field(
        ...,
        ge=0,
        description="Number of AI models successfully loaded.",
        examples=[3],
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of the health check.",
    )

# =============================================================================
# MODEL INFORMATION
# =============================================================================

class ModelInfo(BaseModel):
    """
    Registered model information.
    """

    name: str = Field(
        ...,
        description="Registered model name.",
        examples=["appleguard_cnn_v1"],
    )

    available: bool = Field(
        ...,
        description="Whether the model file is available and loadable.",
        examples=[True],
    )

    is_default: bool = Field(
        ...,
        description="Whether this model is configured as the default model.",
        examples=[True],
    )

# =============================================================================
# REPORT RESPONSE (FUTURE USE)
# =============================================================================

class ReportResponse(BaseModel):
    """
    Report generation response.
    """

    success: bool = Field(
        ...,
        description="Whether report generation succeeded.",
    )

    report_type: str = Field(
        ...,
        description="Generated report format.",
        examples=["pdf"],
    )

    filename: str = Field(
        ...,
        description="Generated report filename.",
        examples=["appleguard_report_20260731_143501.pdf"],
    )

    download_url: str | None = Field(
        default=None,
        description="Optional download URL for the generated report.",
    )

# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "HealthResponse",
    "ModelInfo",
    "PredictionResponse",
    "ProbabilityResponse",
    "ReportResponse",
]
