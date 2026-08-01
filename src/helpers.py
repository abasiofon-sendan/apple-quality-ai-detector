
"""
===============================================================================
AppleGuard AI — Helper Utilities Module
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
Reusable helper functions shared across the AppleGuard AI project.

This module contains only stateless utility functions and MUST NOT:
- Load AI models
- Perform predictions
- Preprocess images
- Create FastAPI routes
- Render Streamlit UI
- Generate PDF reports
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import base64
import hashlib
import json
import logging
import re
import time
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any

from PIL import Image

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from src.config import (
    ALLOWED_IMAGE_TYPES,
    MAX_FILE_SIZE_MB,
    ROOT_DIR,
)

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# CONSOLE LOGGING UTILITIES
# =============================================================================

def print_info(message: str) -> None:
    """Print an informational message."""

    logger.info(message)
    print(f"[INFO] {message}")


def print_success(message: str) -> None:
    """Print a success message."""

    logger.info(message)
    print(f"[SUCCESS] {message}")


def print_error(message: str) -> None:
    """Print an error message."""

    logger.error(message)
    print(f"[ERROR] {message}")


# =============================================================================
# DIRECTORY UTILITIES
# =============================================================================

def ensure_directory(directory: str | Path) -> Path:
    """Create a directory if it does not exist."""

    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_project_root() -> Path:
    """Return the project root directory."""

    return ROOT_DIR


# =============================================================================
# FILE UTILITIES
# =============================================================================

def safe_filename(filename: str) -> str:
    """Return a filesystem-safe filename."""

    filename = Path(filename).name

    # Keep letters, numbers, underscore, dash, dot, and spaces
    filename = re.sub(r"[^\w .-]", "_", filename)

    return filename.strip()


def file_exists(path: str | Path) -> bool:
    """Check whether a file exists."""

    return Path(path).is_file()


def directory_exists(path: str | Path) -> bool:
    """Check whether a directory exists."""

    return Path(path).is_dir()


# =============================================================================
# VALIDATION UTILITIES
# =============================================================================

def validate_image_extension(filename: str) -> bool:
    """Validate that an uploaded file has an allowed image extension."""

    extension = Path(filename).suffix.lower().replace(".", "")

    return extension in ALLOWED_IMAGE_TYPES


def validate_file_size(file_size: int) -> bool:
    """Validate uploaded file size in bytes."""

    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    return file_size <= max_bytes



# =============================================================================
# IMAGE UTILITIES
# =============================================================================

def image_to_bytes(image: Image.Image, image_format: str = "PNG") -> bytes:
    """Convert a PIL image into bytes."""

    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()


def bytes_to_image(data: bytes) -> Image.Image:
    """Convert bytes into a PIL image."""

    from io import BytesIO

    return Image.open(BytesIO(data))


def encode_image_base64(image: Image.Image) -> str:
    """Encode a PIL image into Base64."""

    image_bytes = image_to_bytes(image)

    return base64.b64encode(image_bytes).decode("utf-8")


def decode_image_base64(encoded: str) -> Image.Image:
    """Decode a Base64 image string into a PIL image."""

    image_bytes = base64.b64decode(encoded)

    return bytes_to_image(image_bytes)


# =============================================================================
# SERIALIZATION UTILITIES
# =============================================================================

def save_json(path: str | Path, data: Any) -> None:
    """Save data as a JSON file."""

    path = Path(path)

    ensure_directory(path.parent)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(path: str | Path) -> Any:
    """Load JSON data from a file."""

    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def save_text(path: str | Path, text: str) -> None:
    """Save plain text to a file."""

    path = Path(path)

    ensure_directory(path.parent)

    path.write_text(text, encoding="utf-8")


def load_text(path: str | Path) -> str:
    """Load plain text from a file."""

    return Path(path).read_text(encoding="utf-8")


# =============================================================================
# SECURITY UTILITIES
# =============================================================================

def generate_uuid() -> str:
    """Generate a UUID4 string."""

    return str(uuid.uuid4())


def calculate_sha256(data: bytes | str) -> str:
    """Calculate SHA-256 hash for bytes or text."""

    if isinstance(data, str):
        data = data.encode("utf-8")

    return hashlib.sha256(data).hexdigest()


# =============================================================================
# FORMATTING UTILITIES
# =============================================================================

def format_datetime(dt: datetime | None = None) -> str:
    """Return a formatted datetime string."""

    
    dt = dt or datetime.now(timezone.utc)



    
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")




def generate_timestamp() -> str:
    """Return a timestamp suitable for filenames."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_confidence(confidence: float) -> str:
    """Format a confidence value as a percentage string."""

    return f"{confidence * 100:.2f}%"


def format_probability(probability: float) -> str:
    """Format a probability value as a percentage string."""

    return f"{probability * 100:.2f}%"


def format_file_size(size: int) -> str:
    """Convert bytes into a human-readable string."""

    units = ("B", "KB", "MB", "GB")

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} GB"

# =============================================================================
# LOGGING UTILITIES
# =============================================================================

def setup_logger(name: str) -> logging.Logger:
    """Create or retrieve a logger."""

    return logging.getLogger(name)


# =============================================================================
# TIMING UTILITIES
# =============================================================================

@contextmanager
def execution_timer(task_name: str = "Task") -> Generator[None]:
    """Measure execution time using a context manager."""

    start = time.perf_counter()

    yield

    elapsed = time.perf_counter() - start

    logger.info("%s completed in %.4f seconds.", task_name, elapsed)


def timer(func):
    """Decorator to time function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        logger.info("%s executed in %.4f seconds.", func.__name__, elapsed)

        return result

    return wrapper


# =============================================================================
# GENERAL UTILITIES
# =============================================================================

def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value within a range."""

    return max(minimum, min(value, maximum))


def percentage(value: float, total: float) -> float:
    """Calculate a percentage safely."""

    if total == 0:
        return 0.0

    return (value / total) * 100


def capitalize_words(text: str) -> str:
    """Capitalize every word in a string."""

    return text.title()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate long text safely."""

    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    # Console logging
    "print_info",
    "print_success",
    "print_error",

    # Directory utilities
    "ensure_directory",
    "get_project_root",

    # File utilities
    "safe_filename",
    "file_exists",
    "directory_exists",

    # Validation
    "validate_image_extension",
    "validate_file_size",

    # Image utilities
    "image_to_bytes",
    "bytes_to_image",
    "encode_image_base64",
    "decode_image_base64",

    # Serialization
    "save_json",
    "load_json",
    "save_text",
    "load_text",

    # Security
    "generate_uuid",
    "calculate_sha256",

    # Formatting
    "format_datetime",
    "generate_timestamp",
    "format_confidence",
    "format_probability",
    "format_file_size",

    # Logging
    "setup_logger",

    # Timing
    "execution_timer",
    "timer",

    # General utilities
    "clamp",
    "percentage",
    "capitalize_words",
    "truncate_text",
]

