
"""
===============================================================================
AppleGuard AI — Grad-CAM Visualization Module
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
Provides Grad-CAM (Gradient-weighted Class Activation Mapping)
visualizations for CNN-based explainability.

Responsibilities
----------------
- Locate the last convolutional layer
- Generate Grad-CAM heatmaps
- Overlay heatmaps on original images
- Save Grad-CAM visualizations
- Convert between NumPy arrays and PIL Images

This module MUST NOT:
- Perform predictions
- Load models automatically
- Generate reports
- Render Streamlit UI
- Create FastAPI routes
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import logging
from pathlib import Path

import numpy as np
import tensorflow as tf

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from matplotlib import cm
from PIL import Image
from tensorflow.keras.models import Model

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from src.config import (
    ENABLE_GRADCAM,
    LAST_CONV_LAYER_NAME,
)
from src.helpers import ensure_directory

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# VALIDATION
# =============================================================================

def validate_gradcam_enabled() -> None:
    """Ensure Grad-CAM is enabled in configuration."""

    if not ENABLE_GRADCAM:
        raise RuntimeError(
            "Grad-CAM is disabled in the configuration."
        )


# =============================================================================
# LAYER DISCOVERY
# =============================================================================


def find_last_conv_layer(model: Model) -> str:
    """Automatically locate the last convolutional layer, including nested models."""

    for layer in reversed(model.layers):

        # Direct Conv2D layer
        if isinstance(layer, tf.keras.layers.Conv2D):
            logger.info(
                "Grad-CAM using layer: %s",
                layer.name,
            )
            return layer.name

        # Nested model (MobileNetV3, EfficientNet, etc.)
        if isinstance(layer, tf.keras.Model):
            for nested_layer in reversed(layer.layers):
                if isinstance(nested_layer, tf.keras.layers.Conv2D):
                    logger.info(
                        "Grad-CAM using nested layer: %s",
                        nested_layer.name,
                    )
                    return nested_layer.name

    raise ValueError(
        "No Conv2D layer found in the supplied model or nested submodels."
    )



# =============================================================================
# HEATMAP GENERATION
# =============================================================================

def generate_heatmap(
    model: Model,
    image: np.ndarray,
    last_conv_layer_name: str | None = None,
    class_index: int | None = None,
) -> np.ndarray:
    """Generate a normalized Grad-CAM heatmap."""

    validate_gradcam_enabled()

    layer_name = (
        last_conv_layer_name
        or LAST_CONV_LAYER_NAME
        or find_last_conv_layer(model)
    )

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(layer_name).output,
            model.output,
        ],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image)

        # -------------------------------------------------------------
        # Handle binary sigmoid models and multi-class softmax models
        # -------------------------------------------------------------
        if predictions.shape[-1] == 1:
            # Binary classifier (sigmoid)
            class_channel = predictions[:, 0]
        else:
            # Multi-class classifier (softmax)
            if class_index is None:
                class_index = int(tf.argmax(predictions[0]))

            class_channel = predictions[:, class_index]

    gradients = tape.gradient(class_channel, conv_outputs)

    if gradients is None:
        raise RuntimeError(
            "Unable to compute Grad-CAM gradients."
        )

    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(0, 1, 2),
    )

    conv_outputs = conv_outputs[0]

    # Weight feature maps by pooled gradients
    heatmap = tf.reduce_sum(
        conv_outputs * pooled_gradients,
        axis=-1,
    )

    # Apply ReLU
    heatmap = tf.maximum(heatmap, 0)

    max_value = tf.reduce_max(heatmap)

    # Prevent division by zero
    if float(max_value) == 0.0:
        heatmap_shape = tuple(tf.shape(heatmap).numpy())
        return np.zeros(shape=heatmap_shape, dtype=np.float32)

    heatmap = heatmap / max_value

    return heatmap.numpy().astype(np.float32)



# =============================================================================
# HEATMAP OVERLAY
# =============================================================================

def overlay_heatmap(
    original_image: Image.Image,
    heatmap: np.ndarray,
    alpha: float = 0.4,
) -> Image.Image:
    """Overlay a Grad-CAM heatmap onto an image."""

    # Convert heatmap to 0-255 range
    heatmap_uint8 = np.uint8(255 * heatmap)

    # Apply JET colormap
    colormap = cm.get_cmap("jet")

    colored_heatmap = colormap(np.arange(256))[:, :3]

    colored_heatmap = colored_heatmap[heatmap_uint8]

    heatmap_image = Image.fromarray(
        np.uint8(colored_heatmap * 255)
    )

    heatmap_image = heatmap_image.resize(original_image.size)

    blended = Image.blend(
        original_image.convert("RGB"),
        heatmap_image,
        alpha,
    )

    return blended


# =============================================================================
# IMAGE CONVERSION UTILITIES
# =============================================================================

def array_to_image(array: np.ndarray) -> Image.Image:
    """Convert a NumPy array to a PIL image."""

    if array.dtype != np.uint8:
        array = (
            np.clip(array, 0, 1) * 255
        ).astype(np.uint8)

    return Image.fromarray(array)


def image_to_array(image: Image.Image) -> np.ndarray:
    """Convert a PIL image to a NumPy array."""

    return np.asarray(image)


# =============================================================================
# FILE UTILITIES
# =============================================================================

def save_gradcam(
    image: Image.Image,
    output_path: str | Path,
) -> Path:
    """Save a Grad-CAM visualization to disk."""

    output_path = Path(output_path)

    ensure_directory(output_path.parent)

    image.save(output_path)

    logger.info(
        "Grad-CAM saved to: %s",
        output_path,
    )

    return output_path


# =============================================================================
# GRADCAM WRAPPER CLASS
# =============================================================================
class GradCAM:
    """High-level Grad-CAM helper for repeated use with a model."""

    def __init__(
        self,
        model: Model,
        last_conv_layer_name: str | None = None,
    ) -> None:

        self.model = model

        self.last_conv_layer_name = (
            last_conv_layer_name
            or LAST_CONV_LAYER_NAME
            or find_last_conv_layer(model)
        )

    def generate_heatmap(
        self,
        image: np.ndarray,
        class_index: int | None = None,
    ) -> np.ndarray:
        """Generate a Grad-CAM heatmap."""

        return generate_heatmap(
            model=self.model,
            image=image,
            last_conv_layer_name=self.last_conv_layer_name,
            class_index=class_index,
        )

    def overlay(
        self,
        original_image: Image.Image,
        heatmap: np.ndarray,
        alpha: float = 0.4,
    ) -> Image.Image:
        """Overlay a heatmap on an image."""

        return overlay_heatmap(
            original_image=original_image,
            heatmap=heatmap,
            alpha=alpha,
        )

    def generate_overlay(
        self,
        original_image: Image.Image,
        preprocessed_image: np.ndarray,
        alpha: float = 0.4,
    ) -> Image.Image:
        """Generate heatmap and overlay in one step."""

        heatmap = self.generate_heatmap(preprocessed_image)

        return self.overlay(
            original_image=original_image,
            heatmap=heatmap,
            alpha=alpha,
         )
        # =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "GradCAM",
    "array_to_image",
    "find_last_conv_layer",
    "generate_heatmap",
    "image_to_array",
    "overlay_heatmap",
    "save_gradcam",
    "validate_gradcam_enabled",
]

# =============================================================================
# DEVELOPMENT SELF-TEST
# =============================================================================

if __name__ == "__main__":
    logger.info("Grad-CAM module loaded successfully.")

    # Simple overlay smoke test
    test_image = Image.new("RGB", (224, 224), color="white")

    dummy_heatmap = np.random.rand(224, 224).astype(np.float32)

    overlay = overlay_heatmap(test_image, dummy_heatmap)

    print("Overlay size:", overlay.size)

    logger.info("Grad-CAM self-test completed successfully.")
    

