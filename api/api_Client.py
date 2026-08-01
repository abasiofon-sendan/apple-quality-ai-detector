
"""
===============================================================================
AppleGuard AI — Streamlit API Client
===============================================================================
Handles communication between the Streamlit frontend and the FastAPI backend.
===============================================================================
"""

from __future__ import annotations

from io import BytesIO

import requests
from PIL import Image


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def predict_image(uploaded_file, model_name: str) -> dict:
    """Send an uploaded image to the FastAPI prediction endpoint."""

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "image/jpeg",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/predict",
        params={"model_name": model_name},
        files=files,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def predict_best_model(uploaded_file) -> dict:
    """Send an image to the combined prediction endpoint."""

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "image/jpeg",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/predict/combined",
        files=files,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def generate_gradcam(uploaded_file, model_name: str) -> Image.Image:
    """Request a Grad-CAM overlay from the FastAPI backend."""

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "image/jpeg",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/gradcam",
        params={"model_name": model_name},
        files=files,
        timeout=60,
    )

    response.raise_for_status()

    return Image.open(BytesIO(response.content)).convert("RGB")


def get_available_models() -> list[dict]:
    """Fetch available models from the backend."""

    response = requests.get(
        f"{API_BASE_URL}/models",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

