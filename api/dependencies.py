## `api/dependencies.py`

"""
===============================================================================
AppleGuard AI — FastAPI Dependencies
===============================================================================

Project      : AppleGuard AI
Module       : api.dependencies
Author       : Group 16

Purpose
-------
Reusable FastAPI dependencies shared across API routes.

Responsibilities
----------------
• Image upload validation
• Image loading and verification
• Model name validation
• Shared dependency injection
• Consistent HTTP error handling

This module intentionally contains NO prediction logic.

Prediction, preprocessing, Grad-CAM generation and report generation remain
inside the src package.
===============================================================================
"""

from __future__ import annotations

from io import BytesIO
from typing import Final

from fastapi import File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from src.config import (
    ALLOWED_IMAGE_TYPES,
    DEFAULT_MODEL,
    MODELS,
)

# =============================================================================
# CONSTANTS
# =============================================================================

MAX_UPLOAD_SIZE_MB: Final[int] = 10

SUPPORTED_FORMATS_MESSAGE: Final[str] = (
    f"Supported formats: {', '.join(ALLOWED_IMAGE_TYPES)}"
)

# =============================================================================
# IMAGE FILE VALIDATION
# =============================================================================

def validate_upload_file(
    file: UploadFile = File(...),
) -> UploadFile:
    """
    Validate an uploaded image file.

    Parameters
    ----------
    file : UploadFile
        Uploaded file from the FastAPI request.

    Returns
    -------
    UploadFile
        Validated upload file object.

    Raises
    ------
    HTTPException
        If the uploaded file is missing or has an unsupported format.
    """

    if file.filename is None or not file.filename.strip():
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded.",
        )

    if file.content_type is None:
        raise HTTPException(
            status_code=400,
            detail="Unable to determine uploaded file type.",
        )

    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                f"{SUPPORTED_FORMATS_MESSAGE}"
            ),
        )

    return file

# =============================================================================
# IMAGE LOADING
# =============================================================================

async def load_uploaded_image(
    file: UploadFile,
) -> Image.Image:
    """
    Load an uploaded image into memory and convert it to RGB.

    Parameters
    ----------
    file : UploadFile
        Validated uploaded image file.

    Returns
    -------
    PIL.Image.Image
        RGB image object.

    Raises
    ------
    HTTPException
        If the image cannot be decoded or is invalid.
    """

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        image = Image.open(BytesIO(contents))

        # Verify image integrity
        image.verify()

        # Reopen after verify()
        image = Image.open(BytesIO(contents))

        return image.convert("RGB")

    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        ) from error

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read uploaded image: {error}",
        ) from error

# =============================================================================
# MODEL VALIDATION
# =============================================================================

def validate_model_name(
    model_name: str = DEFAULT_MODEL,
) -> str:
    """
    Validate the requested model name.

    Parameters
    ----------
    model_name : str
        Requested model identifier.

    Returns
    -------
    str
        Validated model name.

    Raises
    ------
    HTTPException
        If the model is not registered in the configuration.
    """

    if model_name not in MODELS:
        available = ", ".join(MODELS.keys())

        raise HTTPException(
            status_code=404,
            detail=(
                f"Unknown model '{model_name}'. "
                f"Available models: {available}"
            ),
        )

    return model_name

# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "load_uploaded_image",
    "validate_model_name",
    "validate_upload_file",
]
