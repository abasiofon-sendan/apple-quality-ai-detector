
"""
===============================================================================
AppleGuard AI — Central Configuration Module
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
This module acts as the single source of truth for every configuration
used throughout the AppleGuard AI project.

It contains only:
- Project metadata
- Directory paths
- Application settings
- Model registration
- Report settings
- Validation helpers

This module MUST NOT contain:
- Prediction logic
- Image preprocessing
- FastAPI routes
- Streamlit UI code
- Grad-CAM computation
- Report generation logic
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import logging
from pathlib import Path
from typing import Final, TypedDict

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================
from reportlab.lib.units import inch

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# PROJECT INFORMATION
# =============================================================================

PROJECT_NAME: Final[str] = "AppleGuard AI"

PROJECT_DESCRIPTION: Final[str] = (
    "Deep Learning-Based Detection of Fresh and Formalin-Mixed Apples"
)

PROJECT_VERSION: Final[str] = "1.0.0"

AUTHOR: Final[str] = "Group 16"
UNIVERSITY: Final[str] = "University of Uyo"
DEPARTMENT: Final[str] = "Computer Engineering"
ACADEMIC_YEAR: Final[str] = "2026"

LICENSE: Final[str] = "MIT"





# =============================================================================
# STREAMLIT APPLICATION SETTINGS
# =============================================================================

APP_TITLE: Final[str] = "AppleGuard AI"
LAYOUT: Final[str] = "wide"
SIDEBAR_STATE: Final[str] = "expanded"


# =============================================================================
# THEME SETTINGS
# =============================================================================

DEFAULT_THEME: Final[str] = "Apple Fresh"

AVAILABLE_THEMES: Final[tuple[str, ...]] = (
    "Apple Fresh",
    "Midnight Dark",
    "Formalin Alert",
    "Laboratory Blue",
)

ENABLE_THEME_SWITCHING: Final[bool] = True


# =============================================================================
# PROJECT DIRECTORY STRUCTURE
# =============================================================================

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Core directories
API_DIR: Final[Path] = ROOT_DIR / "api"
APP_DIR: Final[Path] = ROOT_DIR / "app"
SRC_DIR: Final[Path] = ROOT_DIR / "src"
MODELS_DIR: Final[Path] = ROOT_DIR / "models"
ASSETS_DIR: Final[Path] = ROOT_DIR / "assets"
REPORTS_DIR: Final[Path] = ROOT_DIR / "reports"
DATA_DIR: Final[Path] = ROOT_DIR / "data"
TESTS_DIR: Final[Path] = ROOT_DIR / "tests"

# Report directories
REPORTS_JSON_DIR: Final[Path] = REPORTS_DIR / "json"
REPORTS_CSV_DIR: Final[Path] = REPORTS_DIR / "csv"
REPORTS_PDF_DIR: Final[Path] = REPORTS_DIR / "pdf"


# =============================================================================
# APPLICATION ASSETS
# =============================================================================

APP_ICON: Final[Path] = ASSETS_DIR / "logo.png"
LOGO_PATH: Final[Path] = ASSETS_DIR / "logo.png"
LOGO_DARK_PATH: Final[Path] = ASSETS_DIR / "logo_dark.png"
FAVICON_PATH: Final[Path] = ASSETS_DIR / "favicon.png"
HERO_IMAGE_PATH: Final[Path] = ASSETS_DIR / "hero.png"
UPLOAD_PLACEHOLDER_PATH: Final[Path] = ASSETS_DIR / "upload_placeholder.png"


# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

class ModelInfo(TypedDict):
    """Static registration information for a trained model."""

    filename: str
    author: str
    architecture: str
    description: str


class ModelMetrics(TypedDict):
    """Evaluation metrics for a trained model."""

    validation_accuracy: float | None
    validation_precision: float | None
    validation_recall: float | None
    validation_loss: float | None
    test_accuracy: float | None
    test_precision: float | None
    test_recall: float | None
    test_f1_score: float | None


class ModelMetadataEntry(ModelMetrics):
    """Model metrics plus recommendation flag."""

    recommended: bool


# -----------------------------------------------------------------------------
# Registered Models
# -----------------------------------------------------------------------------

MODELS: Final[dict[str, ModelInfo]] = {
    "Custom CNN": {
        "filename": "apple_quality_cnn_best.keras",
        "author": "Scientist Egong",
        "architecture": "Custom Convolutional Neural Network",
        "description": (
            "CNN model developed from scratch for binary classification "
            "of fresh and formalin-mixed apples."
        ),
    },
    "Transfer Learning": {
        "filename": "apple_quality_tl_best.keras",
        "author": "Scientist Egong",
        "architecture": "MobileNetV3 Feature Extraction",
        "description": (
            "Transfer Learning model using MobileNetV3 as a frozen "
            "feature extractor."
        ),
    },
    "Fine-Tuned MobileNetV3": {
        "filename": "apple_quality_tl_finetuned_best.keras",
        "author": "Scientist Egong",
        "architecture": "Fine-Tuned MobileNetV3",
        "description": (
            "Transfer Learning model further optimized through fine-tuning."
        ),
    },
}


# -----------------------------------------------------------------------------
# Default Deployment Model
# -----------------------------------------------------------------------------

DEFAULT_MODEL: Final[str] = "Custom CNN"


# =============================================================================
# DATASET CONFIGURATION
# =============================================================================

CLASS_NAMES: Final[list[str]] = [
    "Formalin-mixed",
    "Fresh",
]

NUM_CLASSES: Final[int] = len(CLASS_NAMES)

IMAGE_HEIGHT: Final[int] = 224
IMAGE_WIDTH: Final[int] = 224
IMAGE_CHANNELS: Final[int] = 3

IMAGE_SIZE: Final[tuple[int, int]] = (
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
)

BATCH_SIZE: Final[int] = 64
LABEL_MODE: Final[str] = "binary"


# =============================================================================
# VERIFIED MODEL PERFORMANCE
# =============================================================================

BEST_MODEL_METRICS: Final[ModelMetrics] = {
    "validation_accuracy": 0.8713080286979675,
    "validation_precision": 0.9274924397468567,
    "validation_recall": 0.8924418687820435,
    "validation_loss": 0.31050387024879456,
    "test_accuracy": 0.8792016806722689,
    "test_precision": 0.9375951293759512,
    "test_recall": 0.8927536231884058,
    "test_f1_score": 0.9146250927988122,
}


# =============================================================================
# MODEL METADATA
# =============================================================================

MODEL_METADATA: Final[dict[str, ModelMetadataEntry]] = {
    "Custom CNN": {
        "recommended": True,
        "validation_accuracy": 0.8713080286979675,
        "validation_precision": 0.9274924397468567,
        "validation_recall": 0.8924418687820435,
        "validation_loss": 0.31050387024879456,
        "test_accuracy": 0.8792016806722689,
        "test_precision": 0.9375951293759512,
        "test_recall": 0.8927536231884058,
        "test_f1_score": 0.9146250927988122,
    },
    "Transfer Learning": {
        "recommended": False,
        "validation_accuracy": 0.844936728477478,
        "validation_precision": 0.8960468769073486,
        "validation_recall": 0.8895348906517029,
        "validation_loss": 0.33795616030693054,
        "test_accuracy": None,
        "test_precision": None,
        "test_recall": None,
        "test_f1_score": None,
    },
    "Fine-Tuned MobileNetV3": {
        "recommended": False,
        "validation_accuracy": 0.8713080286979675,
        "validation_precision": 0.9274924397468567,
        "validation_recall": 0.8924418687820435,
        "validation_loss": 0.31050387024879456,
        "test_accuracy": 0.8792016806722689,
        "test_precision": 0.9375951293759512,
        "test_recall": 0.8927536231884058,
        "test_f1_score": 0.9146250927988122,
    },
}



# =============================================================================
# REPORT STORAGE
# =============================================================================

SAVE_REPORTS_LOCALLY: Final[bool] = True
UPLOAD_REPORTS_TO_DRIVE: Final[bool] = False


# =============================================================================
# REPORT CONFIGURATION
# =============================================================================

DEFAULT_REPORT_FORMAT: Final[str] = "pdf"

REPORT_TITLE: Final[str] = "AppleGuard AI Prediction Report"
REPORT_AUTHOR: Final[str] = "AppleGuard AI Team"
REPORT_SUBJECT: Final[str] = (
    "AI-generated report for Fresh vs Formalin-mixed Apple Classification"
)

# PDF page margins (ReportLab uses points)
PDF_MARGIN: Final[int] = 36  # 0.5 inch

# Uploaded image size in PDF
REPORT_IMAGE_WIDTH: Final[float] = 2.2 * inch
REPORT_IMAGE_HEIGHT: Final[float] = 2.2 * inch

# Grad-CAM image size in PDF
GRADCAM_IMAGE_WIDTH: Final[float] = 5.5 * inch
GRADCAM_IMAGE_HEIGHT: Final[float] = 4.0 * inch

ENABLE_JSON_REPORT: Final[bool] = True
ENABLE_CSV_REPORT: Final[bool] = True
ENABLE_PDF_REPORT: Final[bool] = True


# =============================================================================
# PREDICTION CONFIDENCE SETTINGS
# =============================================================================

CONFIDENCE_THRESHOLD: Final[float] = 0.65
CONFIDENCE_DECIMALS: Final[int] = 2

SHOW_CONFIDENCE: Final[bool] = True
SHOW_PROBABILITIES: Final[bool] = True
DISPLAY_TOP_PREDICTION_ONLY: Final[bool] = False


# =============================================================================
# IMAGE UPLOAD SETTINGS
# =============================================================================

ALLOWED_IMAGE_TYPES: Final[list[str]] = [
    "jpg",
    "jpeg",
    "png",
]

MAX_FILE_SIZE_MB: Final[int] = 10


# =============================================================================
# FASTAPI CONFIGURATION
# =============================================================================

API_HOST: Final[str] = "0.0.0.0"
API_PORT: Final[int] = 8000

API_TITLE: Final[str] = "AppleGuard AI API"
API_VERSION: Final[str] = PROJECT_VERSION

API_DESCRIPTION: Final[str] = (
    "REST API for predicting whether an uploaded apple image is Fresh "
    "or Formalin-mixed using Deep Learning."
)


# =============================================================================
# STREAMLIT CONFIGURATION
# =============================================================================

DEFAULT_API_BASE_URL: Final[str] = "http://localhost:8000"
API_TIMEOUT_SECONDS: Final[int] = 60


# =============================================================================
# EXPLAINABILITY SETTINGS
# =============================================================================

ENABLE_GRADCAM: Final[bool] = True

# None = automatically detect the last Conv2D layer
LAST_CONV_LAYER_NAME: Final[str | None] = None


# =============================================================================
# APPLICATION FEATURES
# =============================================================================

ENABLE_MODEL_CACHE: Final[bool] = True
ENABLE_PREDICTION_HISTORY: Final[bool] = True
ENABLE_MODEL_COMPARISON: Final[bool] = True
ENABLE_BATCH_PREDICTION: Final[bool] = False
ENABLE_GPU: Final[bool] = True


# =============================================================================
# USER INTERFACE OPTIONS
# =============================================================================

SHOW_MODEL_INFORMATION: Final[bool] = True
SHOW_MODEL_PERFORMANCE: Final[bool] = True
SHOW_PREDICTION_TIME: Final[bool] = True
SHOW_MODEL_AUTHOR: Final[bool] = True
SHOW_UPLOAD_PREVIEW: Final[bool] = True
SHOW_CLASS_PROBABILITIES: Final[bool] = True


# =============================================================================
# CORS CONFIGURATION
# =============================================================================

CORS_ALLOW_ORIGINS: Final[list[str]] = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]

CORS_ALLOW_CREDENTIALS: Final[bool] = True
CORS_ALLOW_METHODS: Final[list[str]] = ["*"]
CORS_ALLOW_HEADERS: Final[list[str]] = ["*"]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def ensure_directories() -> None:
    """Create all required project directories if they do not exist."""

    directories: list[Path] = [
        MODELS_DIR,
        ASSETS_DIR,
        REPORTS_DIR,
        REPORTS_JSON_DIR,
        REPORTS_CSV_DIR,
        REPORTS_PDF_DIR,
        DATA_DIR,
        TESTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_model_path(model_name: str) -> Path:
    """Return the absolute path of a registered model."""

    if model_name not in MODELS:
        raise KeyError(f"Unknown model: {model_name}")

    return MODELS_DIR / MODELS[model_name]["filename"]


def get_default_model_path() -> Path:
    """Return the path of the default deployment model."""

    return get_model_path(DEFAULT_MODEL)


def get_model_metadata(
    model_name: str,
) -> ModelMetadataEntry | dict[str, object]:
    """Return evaluation metadata for a model."""

    return MODEL_METADATA.get(model_name, {})


def get_available_models() -> list[str]:
    """Return all registered model names."""

    return list(MODELS.keys())


def validate_configuration() -> None:
    """Validate configuration integrity at startup."""

    if DEFAULT_MODEL not in MODELS:
        raise ValueError(
            f"Default model '{DEFAULT_MODEL}' is not registered."
        )

    if IMAGE_HEIGHT <= 0 or IMAGE_WIDTH <= 0:
        raise ValueError("Image dimensions must be greater than zero.")

    if NUM_CLASSES != len(CLASS_NAMES):
        raise ValueError("NUM_CLASSES does not match CLASS_NAMES.")

    for model_name, model_info in MODELS.items():
        if not model_info.get("filename"):
            raise ValueError(f"{model_name} has no filename.")


# =============================================================================
# INITIALIZATION
# =============================================================================

ensure_directories()
validate_configuration()


# =============================================================================
# STARTUP LOGGING
# =============================================================================

logger.info(
    "AppleGuard AI configuration loaded | "
    "project=%s version=%s default_model=%s registered_models=%d "
    "image_size=%dx%d classes=%s api=http://%s:%d",
    PROJECT_NAME,
    PROJECT_VERSION,
    DEFAULT_MODEL,
    len(MODELS),
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    CLASS_NAMES,
    API_HOST,
    API_PORT,
)


# =============================================================================
# END OF CONFIGURATION MODULE
# =============================================================================

