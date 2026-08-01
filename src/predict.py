
"""
===============================================================================
AppleGuard AI — Prediction Engine
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
Core inference engine responsible for loading trained TensorFlow models
and generating predictions for uploaded apple images.

Responsibilities
----------------
- Load and cache TensorFlow models
- Prepare images for inference
- Generate prediction probabilities
- Handle binary classification outputs
- Return standardized prediction dictionaries

This module MUST NOT:
- Create FastAPI routes
- Render Streamlit UI
- Generate PDF reports
- Train models
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import logging
import time
from typing import Any

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras import Model

# =============================================================================
# LOCAL IMPORTS
# =============================================================================

from src.config import (
    CLASS_NAMES,
    CONFIDENCE_THRESHOLD,
    DEFAULT_MODEL,
    MODEL_METADATA,
    MODELS,
    get_model_path,
)


from src.helpers import (
    format_confidence,
    print_error,
    print_info,
    print_success,
)
from src.preprocess import prepare_image_for_prediction

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# MODEL CACHE
# =============================================================================

_MODEL_CACHE: dict[str, Model] = {}


# =============================================================================
# MODEL LOADING
# =============================================================================

def load_model(model_name: str = DEFAULT_MODEL) -> Model:
    """Load a TensorFlow model and cache it in memory."""

    if model_name in _MODEL_CACHE:
        logger.info("Using cached model: %s", model_name)
        return _MODEL_CACHE[model_name]

    model_path = get_model_path(model_name)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    print_info(f"Loading model: {model_name}")

    model = tf.keras.models.load_model(model_path)

    _MODEL_CACHE[model_name] = model

    print_success(f"Model loaded successfully: {model_name}")

    return model


def load_default_model() -> Model:
    """Load the default deployment model."""

    return load_model(DEFAULT_MODEL)


# =============================================================================
# CACHE UTILITIES
# =============================================================================

def clear_model_cache() -> None:
    """Clear all cached models."""

    _MODEL_CACHE.clear()

    logger.info("Model cache cleared.")


def get_cached_models() -> list[str]:
    """Return the names of currently cached models."""

    return list(_MODEL_CACHE.keys())


# =============================================================================
# PREDICTION VALIDATION
# =============================================================================

def validate_prediction_output(probabilities: np.ndarray) -> np.ndarray:
    """Validate and flatten model prediction output."""

    probabilities = np.asarray(probabilities).flatten()

    if probabilities.size == 0:
        raise ValueError("Model returned an empty prediction output.")

    return probabilities


# =============================================================================
# PROBABILITY PROCESSING
# =============================================================================

def process_binary_probabilities(
    probabilities: np.ndarray,
) -> dict[str, float]:
    """Convert binary model output into a class-probability dictionary."""

    probabilities = validate_prediction_output(probabilities)

    # Sigmoid output: [p]
    if probabilities.size == 1:
        formalin_probability = float(probabilities[0])
        fresh_probability = 1.0 - formalin_probability

        return {
            "Formalin-mixed": formalin_probability,
            "Fresh": fresh_probability,
        }

    # Softmax output: [p_formalin, p_fresh]
    if probabilities.size == 2:
        return {
            CLASS_NAMES[0]: float(probabilities[0]),
            CLASS_NAMES[1]: float(probabilities[1]),
        }

    raise ValueError(
        f"Unsupported binary output shape: {probabilities.shape}"
    )


# =============================================================================
# PREDICTION RESULT CREATION
# =============================================================================

def create_prediction_result(
    predicted_class: str,
    confidence: float,
    probabilities: dict[str, float],
    model_name: str,
    prediction_time: float,
) -> dict[str, Any]:
    """Create a standardized prediction result dictionary."""

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "confidence_percentage": format_confidence(confidence),
        "probabilities": probabilities,
        "model_name": model_name,
        "prediction_time_seconds": round(prediction_time, 4),
        "is_confident": confidence >= CONFIDENCE_THRESHOLD,
        "model_metadata": MODEL_METADATA.get(model_name, {}),
    }


# =============================================================================
# CORE IMAGE PREDICTION
# =============================================================================

# =============================================================================
# CORE IMAGE PREDICTION
# =============================================================================
def predict_image(
    image: Any,
    model_name: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Predict whether an apple image is Fresh or Formalin-mixed."""

    start_time = time.perf_counter()

    try:
        # -------------------------------------------------------------
        # Load model
        # -------------------------------------------------------------
        model = load_model(model_name)

        # -------------------------------------------------------------
        # Preprocess image
        # -------------------------------------------------------------
        processed_image = prepare_image_for_prediction(image)

        logger.info(
            "Running prediction using model: %s",
            model_name,
        )

        # -------------------------------------------------------------
        # Run inference
        # -------------------------------------------------------------
        raw_output = model.predict(processed_image, verbose=0)

        # -------------------------------------------------------------
        # Convert to probabilities
        # -------------------------------------------------------------
        probabilities = process_binary_probabilities(raw_output)

        predicted_class = max(
            probabilities,
            key=lambda class_name: probabilities[class_name],
        )

        confidence = probabilities[predicted_class]

        prediction_time = time.perf_counter() - start_time

        result = create_prediction_result(
            predicted_class=predicted_class,
            confidence=confidence,
            probabilities=probabilities,
            model_name=model_name,
            prediction_time=prediction_time,
        )

        logger.info(
            "Prediction completed | class=%s confidence=%.4f time=%.4fs",
            predicted_class,
            confidence,
            prediction_time,
        )

        return result

    except Exception as error:
        logger.exception("Prediction failed.")
        print_error(f"Prediction failed: {error}")
        raise


# =============================================================================
# DEFAULT MODEL PREDICTION
# =============================================================================

def predict_with_default_model(image: Any) -> dict[str, Any]:
    """Predict using the configured default model."""

    return predict_image(image, DEFAULT_MODEL)


# =============================================================================
# API COMPATIBILITY WRAPPERS
# =============================================================================

def predict_with_selected_model(image: Any, model_name: str) -> dict[str, Any]:
    """
    Predict using a specific registered model.

    This wrapper exists for FastAPI compatibility.
    """

    return predict_image(
        image=image,
        model_name=model_name,
    )


def predict_with_best_model(image: Any) -> dict[str, Any]:
    """
    Run prediction across all available models and return the
    highest-confidence result.
    """

    comparison_results = compare_models(image)

    if not comparison_results:
        raise RuntimeError("No models available for comparison.")

    best_result = max(
        comparison_results,
        key=lambda result: result.get("confidence", 0.0),
    )

    return {
        **best_result,
        "selection_mode": "best_model",
        "models_evaluated": len(comparison_results),
        "all_predictions": comparison_results,
    }




# =============================================================================
# MULTI-MODEL COMPARISON
# =============================================================================

def compare_models(
    image: Image.Image,
    model_names: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Run the same image through multiple models for comparison."""

    from src.config import get_available_models

    if model_names is None:
        model_names = get_available_models()

    results: dict[str, dict[str, Any]] = {}

    for model_name in model_names:
        try:
            results[model_name] = predict_image(image, model_name)
        except Exception as error:
            results[model_name] = {
                "error": str(error),
                "model_name": model_name,
            }

    return results


# =============================================================================
# CONVENIENCE UTILITIES
# =============================================================================

def get_prediction_summary(result: dict[str, Any]) -> str:
    """Create a human-readable prediction summary."""

    return (
        f"Prediction: {result['predicted_class']} | "
        f"Confidence: {result['confidence_percentage']} | "
        f"Model: {result['model_name']}"
    )


# =============================================================================
# MODEL ACCESS
# =============================================================================

def get_model(model_name: str):
    """Return a loaded model instance by name."""

    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}")

    return load_model(model_name)



# =============================================================================
# MODEL REGISTRY HELPERS
# =============================================================================

def model_exists(model_name: str) -> bool:
    """Return True if a registered model exists on disk."""

    try:
        model_path = get_model_path(model_name)
        return model_path.exists()
    except Exception:
        return False


def get_available_model_names() -> list[str]:
    """Return the names of all registered models that exist on disk."""

    return [
        name
        for name in MODEL_METADATA.keys()
        if model_exists(name)
    ]


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================


# =============================================================================
# FILE-BASED PREDICTION
# =============================================================================

def predict_image_from_path(
    image_path: str,
    model_name: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Load an image from disk and run prediction."""

    from src.preprocess import load_image_from_path

    image = load_image_from_path(image_path)

    return predict_image(image, model_name)


# =============================================================================
# BYTES-BASED PREDICTION
# =============================================================================

def predict_image_from_bytes(
    image_bytes: bytes,
    model_name: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Predict from raw image bytes."""

    from src.preprocess import load_image_from_bytes

    image = load_image_from_bytes(image_bytes)

    return predict_image(image, model_name)


# =============================================================================
# BASE64-BASED PREDICTION
# =============================================================================

def predict_image_from_base64(
    encoded_image: str,
    model_name: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Predict from a Base64-encoded image string."""

    from src.preprocess import load_image_from_base64

    image = load_image_from_base64(encoded_image)

    return predict_image(image, model_name)


# =============================================================================
# GRAD-CAM INTEGRATION
# =============================================================================

def predict_with_gradcam(
    image: Image.Image,
    model_name: str = DEFAULT_MODEL,
) -> tuple[dict[str, Any], Image.Image]:
    """Run prediction and generate a Grad-CAM explanation image."""

    from src.gradcam import GradCAM

    # Run prediction first
    result = predict_image(image, model_name)

    # Load model and prepare image
    model = load_model(model_name)
    processed_image = prepare_image_for_prediction(image)

    # Generate Grad-CAM
    gradcam = GradCAM(model)

    heatmap = gradcam.generate_heatmap(processed_image)

    overlay = gradcam.overlay(image, heatmap)

    return result, overlay


# =============================================================================
# BATCH PREDICTION
# =============================================================================

def predict_batch(
    images: list[Image.Image],
    model_name: str = DEFAULT_MODEL,
) -> list[dict[str, Any]]:
    """Run predictions for multiple images sequentially."""

    results: list[dict[str, Any]] = []

    for index, image in enumerate(images, start=1):
        try:
            result = predict_image(image, model_name)
            result["batch_index"] = index
            results.append(result)

        except Exception as error:
            results.append({
                "batch_index": index,
                "error": str(error),
                "model_name": model_name,
            })

    return results


# =============================================================================
# STARTUP DIAGNOSTICS
# =============================================================================

def run_prediction_diagnostics() -> dict[str, Any]:
    """Run lightweight diagnostics for the prediction engine."""

    diagnostics = {
        "tensorflow_version": tf.__version__,
        "default_model": DEFAULT_MODEL,
        "cached_models": get_cached_models(),
        "class_names": CLASS_NAMES,
        "gpu_available": bool(tf.config.list_physical_devices("GPU")),
    }

    try:
        model_path = get_model_path(DEFAULT_MODEL)
        diagnostics["default_model_exists"] = model_path.exists()
        diagnostics["default_model_path"] = str(model_path)

    except Exception as error:
        diagnostics["default_model_exists"] = False
        diagnostics["error"] = str(error)

    return diagnostics


# =============================================================================
# PUBLIC EXPORTS (EXTENDED)
# =============================================================================

__all__: list[str] = []

__all__.extend([
    "predict_batch",
    "predict_image_from_base64",
    "predict_image_from_bytes",
    "predict_image_from_path",
    "predict_with_gradcam",
    "run_prediction_diagnostics",
    # Model loading
    "load_model",
    "load_default_model",
    "clear_model_cache",
    "get_cached_models",

    # Validation
    "validate_prediction_output",
    "process_binary_probabilities",

    # Prediction
    "predict_image",
    "predict_with_default_model",
    "compare_models",

    # Utilities
    "create_prediction_result",
    "get_prediction_summary",
        
    "get_available_model_names",
    "model_exists",
    
    "predict_with_best_model",
    "predict_with_selected_model",



])


# =============================================================================
# DEVELOPMENT SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print_info("Running AppleGuard prediction engine diagnostics...")

    diagnostics = run_prediction_diagnostics()

    print()
    print("Prediction Engine Diagnostics")
    print("-" * 40)

    for key, value in diagnostics.items():
        print(f"{key}: {value}")

    print()
    print_success("Prediction engine initialized successfully.")



