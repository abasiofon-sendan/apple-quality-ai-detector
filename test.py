
"""
AppleGuard AI — Grad-CAM Test Script
Tests the complete Grad-CAM pipeline using the exported API from gradcam.py
"""

from pathlib import Path

import tensorflow as tf
from PIL import Image

from src.config import (
    MODEL_PATH,
)
from src.gradcam import (
    GradCAM,
    array_to_image,
    find_last_conv_layer,
    generate_heatmap,
    image_to_array,
    overlay_heatmap,
    save_gradcam,
    validate_gradcam_enabled,
)
from src.preprocess import preprocess_image

# =============================================================================
# CONFIGURATION
# =============================================================================

TEST_IMAGE = Path("test_images/apple.jpg")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# =============================================================================
# VALIDATION
# =============================================================================

print("=" * 60)
print("APPLEGUARD AI — GRAD-CAM TEST")
print("=" * 60)

validate_gradcam_enabled()
print("[INFO] Grad-CAM is enabled")

if not TEST_IMAGE.exists():
    raise FileNotFoundError(
        f"Test image not found: {TEST_IMAGE}\\n"
        "Create a folder named 'test_images' and place an apple image inside it."
    )


# =============================================================================
# LOAD MODEL
# =============================================================================

print(f"[INFO] Loading model: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("[INFO] Model loaded successfully")


# =============================================================================
# FIND LAST CONVOLUTIONAL LAYER
# =============================================================================

last_conv_layer = find_last_conv_layer(model)
print(f"[INFO] Last convolutional layer: {last_conv_layer}")


# =============================================================================
# LOAD AND PREPROCESS IMAGE
# =============================================================================

print(f"[INFO] Loading image: {TEST_IMAGE}")

original_image = Image.open(TEST_IMAGE).convert("RGB")

input_tensor = preprocess_image(TEST_IMAGE)
print(f"[INFO] Input tensor shape: {input_tensor.shape}")


# =============================================================================
# RUN PREDICTION
# =============================================================================

predictions = model.predict(input_tensor, verbose=0)
predicted_index = int(predictions.argmax())

print(f"[INFO] Predicted class index: {predicted_index}")


# =============================================================================
# GENERATE HEATMAP
# =============================================================================

heatmap = generate_heatmap(
    model=model,
    image_tensor=input_tensor,
    last_conv_layer_name=last_conv_layer,
    class_index=predicted_index,
)

print(f"[INFO] Heatmap generated: {heatmap.shape}")


# =============================================================================
# CREATE OVERLAY
# =============================================================================

original_array = image_to_array(original_image)

overlay_array = overlay_heatmap(
    image_array=original_array,
    heatmap=heatmap,
    alpha=0.4,
)

overlay_image = array_to_image(overlay_array)

print("[INFO] Overlay created successfully")
print(f"[INFO] Overlay size: {overlay_image.size}")


# =============================================================================
# SAVE RESULTS
# =============================================================================

overlay_path = OUTPUT_DIR / "gradcam_overlay.png"
heatmap_path = OUTPUT_DIR / "gradcam_heatmap.png"

overlay_image.save(overlay_path)
save_gradcam(heatmap, heatmap_path)


# =============================================================================
# OPTIONAL CLASS-BASED API TEST
# =============================================================================

print("[INFO] Testing GradCAM class API...")

gradcam = GradCAM(model)

class_overlay = gradcam.generate(
    image_path=TEST_IMAGE,
    class_index=predicted_index,
    alpha=0.4,
)

class_overlay_path = OUTPUT_DIR / "gradcam_class_overlay.png"
class_overlay.save(class_overlay_path)

print("[INFO] GradCAM class API test successful")


# =============================================================================
# FINAL SUMMARY
# =============================================================================

print()
print("=" * 60)
print("GRAD-CAM TEST COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"Overlay image : {overlay_path}")
print(f"Heatmap image : {heatmap_path}")
print(f"Class overlay : {class_overlay_path}")
print("=" * 60)

