
"""
===============================================================================
AppleGuard AI — Image Preprocessing Module
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
This module contains image preprocessing utilities used before AI
inference. Its responsibility is to prepare uploaded images in the exact
format expected by the trained TensorFlow models.

Responsibilities
----------------
- Resize images
- Convert images to RGB
- Normalize pixel values
- Convert PIL images to NumPy arrays
- Create model-ready batches

This module MUST NOT:
- Load TensorFlow models
- Perform predictions
- Generate Grad-CAM visualizations
- Create FastAPI routes
- Render Streamlit UI
- Generate reports
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import logging

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
import numpy as np
from PIL import Image

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from src.config import (
    IMAGE_CHANNELS,
    IMAGE_HEIGHT,
    IMAGE_SIZE,
    IMAGE_WIDTH,
)

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# IMAGE VALIDATION
# =============================================================================

def validate_image(image: object) -> None:
    """Validate that the supplied object can be treated as an image."""

    valid_types = (Image.Image, np.ndarray, bytes)

    if isinstance(image, valid_types):
        return

    # File-like objects (Streamlit UploadedFile, BytesIO, etc.)
    if hasattr(image, "read"):
        return

    raise TypeError(
        f"Expected a PIL.Image.Image, numpy.ndarray, bytes, "
        f"or a file-like object. Got {type(image)!r}."
    )


# =============================================================================
# COLOR CONVERSION
# =============================================================================


def ensure_rgb(image: object) -> Image.Image:
    """Convert various image inputs to a PIL RGB image."""

    validate_image(image)

    # Already a PIL image
    if isinstance(image, Image.Image):
        return image.convert("RGB")

    # NumPy array
    if isinstance(image, np.ndarray):
        return Image.fromarray(image).convert("RGB")

    # Raw bytes
    if isinstance(image, bytes):
        from io import BytesIO

        return Image.open(BytesIO(image)).convert("RGB")

    # File-like object (UploadedFile, BytesIO, etc.)
    if hasattr(image, "read"):
        image.seek(0)
        return Image.open(image).convert("RGB")

    # Should never happen because validate_image already checks
    raise TypeError(f"Unsupported image type: {type(image)!r}")

# =============================================================================
# RESIZING
# =============================================================================

def resize_image(
    image: object,
    size: tuple[int, int] = IMAGE_SIZE,
) -> Image.Image:
    """Resize an image to the target model size."""

    image = ensure_rgb(image)

    return image.resize(size)


# =============================================================================
# ARRAY CONVERSION
# =============================================================================

def image_to_array(image: object) -> np.ndarray:
    """Convert a PIL image to a NumPy array."""

    image = ensure_rgb(image)

    return np.asarray(image, dtype=np.float32)


# =============================================================================
# NORMALIZATION
# =============================================================================

def normalize_image(array: np.ndarray) -> np.ndarray:
    """Normalize pixel values to the range [0, 1]."""

    return array / 255.0


# =============================================================================
# COMPLETE PREPROCESSING PIPELINE
# =============================================================================

def preprocess_image(image: object) -> np.ndarray:
    """Run the complete preprocessing pipeline."""

    image = ensure_rgb(image)

    image = resize_image(image)

    array = image_to_array(image)

    array = normalize_image(array)

    return array
# =============================================================================
# MODEL-READY BATCH PREPARATION
# ====================================================
def prepare_image_for_prediction(image: object) -> np.ndarray:
    """Prepare a single image for TensorFlow model prediction."""

    array = preprocess_image(image)

    # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
    batch = np.expand_dims(array, axis=0).astype(np.float32)

    return batch



# =============================================================================
# FILE LOADING UTILITIES
# =============================================================================

def load_image_from_path(path: str) -> Image.Image:
    """Load an image from a filesystem path."""

    image = Image.open(path)

    return ensure_rgb(image)


def load_image_from_bytes(data: bytes) -> Image.Image:
    """Load an image from raw bytes."""

    from io import BytesIO

    image = Image.open(BytesIO(data))

    return ensure_rgb(image)


def load_image_from_base64(encoded: str) -> Image.Image:
    """Load an image from a Base64-encoded string."""

    import base64

    image_bytes = base64.b64decode(encoded)

    return load_image_from_bytes(image_bytes)


# =============================================================================
# BATCH PREPROCESSING
# =============================================================================

def preprocess_images(images: list[Image.Image]) -> np.ndarray:
    """Preprocess multiple images into a single batch array."""

    processed = [preprocess_image(image) for image in images]

    return np.asarray(processed, dtype=np.float32)


def prepare_images_for_prediction(images: list[Image.Image]) -> np.ndarray:
    """Prepare multiple images for model prediction."""

    return preprocess_images(images)


# =============================================================================
# ARRAY VALIDATION UTILITIES
# =============================================================================

def validate_array_shape(array: np.ndarray) -> None:
    """Validate that an image array has the expected shape."""

    expected_shape = (
        IMAGE_HEIGHT,
        IMAGE_WIDTH,
        IMAGE_CHANNELS,
    )

    if array.shape != expected_shape:
        raise ValueError(
            f"Expected image shape {expected_shape}, got {array.shape}."
        )


# =============================================================================
# CONVENIENCE UTILITIES
# =============================================================================

def preprocess_image_from_path(path: str) -> np.ndarray:
    """Load and preprocess an image from a file path."""

    image = load_image_from_path(path)

    return preprocess_image(image)


def prepare_image_from_path_for_prediction(path: str) -> np.ndarray:
    """Load and prepare an image from a file path for prediction."""

    image = load_image_from_path(path)

    return prepare_image_for_prediction(image)


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    # Validation
    "validate_image",
    "validate_array_shape",

    # Color conversion
    "ensure_rgb",

    # Resizing
    "resize_image",

    # Array conversion
    "image_to_array",

    # Normalization
    "normalize_image",

    # Main preprocessing pipeline
    "preprocess_image",
    "prepare_image_for_prediction",

    # File loading
    "load_image_from_path",
    "load_image_from_bytes",
    "load_image_from_base64",

    # Batch preprocessing
    "preprocess_images",
    "prepare_images_for_prediction",

    # Convenience helpers
    "preprocess_image_from_path",
    "prepare_image_from_path_for_prediction",
]


# =============================================================================
# DEBUGGING & INSPECTION UTILITIES
# =============================================================================

def get_image_statistics(array: np.ndarray) -> dict[str, float | str | tuple[int, ...]]:
    """Return useful statistics about a preprocessed image array."""

    return {
        "shape": array.shape,
        "dtype": str(array.dtype),
        "min": float(array.min()),
        "max": float(array.max()),
        "mean": float(array.mean()),
        "std": float(array.std()),
    }


def log_preprocessing_summary(array: np.ndarray) -> None:
    """Log preprocessing statistics for debugging purposes."""

    stats = get_image_statistics(array)

    logger.info(
        "Preprocessed image | shape=%s dtype=%s range=[%.4f, %.4f] "
        "mean=%.4f std=%.4f",
        stats["shape"],
        stats["dtype"],
        stats["min"],
        stats["max"],
        stats["mean"],
        stats["std"],
    )


# =============================================================================
# DEVELOPMENT SELF-TEST
# =============================================================================

if __name__ == "__main__":
    logger.info("Running preprocess.py self-test...")

    # Create a synthetic test image
    test_image = Image.new("RGB", (500, 500), color="red")

    batch = prepare_image_for_prediction(test_image)

    print("Batch shape :", batch.shape)
    print("Batch dtype :", batch.dtype)
    print("Value range :", batch.min(), batch.max())

    log_preprocessing_summary(batch[0])

    logger.info("Preprocessing module self-test completed successfully.")

