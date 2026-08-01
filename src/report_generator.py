
"""
===============================================================================
AppleGuard AI — Report Generator
===============================================================================

Stage 1 Responsibilities
------------------------
- Create standardized report payloads
- Store uploaded image references
- Generate JSON reports
- Create report filenames
- Manage report directories
- Prepare data for future PDF generation
===============================================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image as RLImage,
)
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from src.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    REPORT_TITLE,
    REPORTS_JSON_DIR,
    REPORTS_PDF_DIR,
    SAVE_REPORTS_LOCALLY,
)
from src.helpers import (
    ensure_directory,
    format_datetime,
    generate_timestamp,
    save_json,
)

# =============================================================================
# LOGGER
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# INITIALIZE REPORT DIRECTORIES
# =============================================================================

ensure_directory(REPORTS_JSON_DIR)


# =============================================================================
# REPORT METADATA
# =============================================================================

def create_report_metadata() -> dict[str, Any]:
    """Create standard metadata included in every report."""

    return {
        "project_name": PROJECT_NAME,
        "project_version": PROJECT_VERSION,
        "report_title": REPORT_TITLE,
        "generated_at": format_datetime(),
        "generator": "AppleGuard AI Report Generator",
    }


# =============================================================================
# REPORT PAYLOAD CREATION
# =============================================================================

def create_report_payload(
    prediction_result: dict[str, Any],
    image_name: str | None = None,
    image_path: str | Path | None = None,
    gradcam_path: str | Path | None = None,
    additional_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a standardized report payload."""

    payload = {
        "metadata": create_report_metadata(),
        "image_name": image_name or "unknown_image",
        "uploaded_image_path": str(image_path) if image_path else None,
        "gradcam_image_path": str(gradcam_path) if gradcam_path else None,
        "prediction": prediction_result,
    }

    if additional_data:
        payload["additional_data"] = additional_data

    return payload


# =============================================================================
# FILENAME GENERATION
# =============================================================================
def generate_report_filename(
    prefix: str = "prediction_report",
    extension: str = "json",
) -> str:
    """Generate a unique timestamped report filename."""

    timestamp = generate_timestamp()

    return f"{prefix}_{timestamp}.{extension}"


# =============================================================================
# JSON REPORT GENERATION
# =============================================================================

def generate_json_report(
    prediction_result: dict[str, Any],
    image_name: str | None = None,
    image_path: str | Path | None = None,
    gradcam_path: str | Path | None = None,
    output_path: str | Path | None = None,
    additional_data: dict[str, Any] | None = None,
) -> Path:
    """Generate a JSON prediction report."""

    payload = create_report_payload(
        prediction_result=prediction_result,
        image_name=image_name,
        image_path=image_path,
        gradcam_path=gradcam_path,
        additional_data=additional_data,
    )

    if output_path is None:
        filename = generate_report_filename(extension="json")
        output_path = REPORTS_JSON_DIR / filename

    output_path = Path(output_path)

    if SAVE_REPORTS_LOCALLY:
        save_json(output_path, payload)
        logger.info("JSON report saved to: %s", output_path)

    return output_path


# =============================================================================
# REPORT SUMMARY
# =============================================================================

def create_report_summary(report_payload: dict[str, Any]) -> str:
    """Create a human-readable report summary."""

    prediction = report_payload.get("prediction", {})

    predicted_class = prediction.get("predicted_class", "Unknown")
    confidence = prediction.get("confidence_percentage", "Unknown")
    model_name = prediction.get("model_name", "Unknown")

    return (
        f"AppleGuard AI Report | "
        f"Class: {predicted_class} | "
        f"Confidence: {confidence} | "
        f"Model: {model_name}"
    )


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "create_report_metadata",
    "create_report_payload",
    "create_report_summary",
    "generate_json_report",
    "generate_report_filename",
]


# =============================================================================
# STANDARD LIBRARY IMPORTS (ADD THIS AT THE TOP IF NOT PRESENT)
# =============================================================================

import csv

# =============================================================================
# CONFIG IMPORTS (ADD THIS TO THE EXISTING CONFIG IMPORTS)
# =============================================================================
# Add REPORTS_CSV_DIR to the config import list
from src.config import REPORTS_CSV_DIR

# =============================================================================
# INITIALIZE CSV REPORT DIRECTORY
# =============================================================================

ensure_directory(REPORTS_CSV_DIR)


# =============================================================================
# CSV REPORT GENERATION
# =============================================================================

def generate_csv_report(
    prediction_result: dict[str, Any],
    image_name: str | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Generate a CSV report for a single prediction."""

    if output_path is None:
        filename = generate_report_filename(extension="csv")
        output_path = REPORTS_CSV_DIR / filename

    output_path = Path(output_path)

    ensure_directory(output_path.parent)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Field", "Value"])
        writer.writerow(["Image Name", image_name or "unknown_image"])
        writer.writerow([
            "Predicted Class",
            prediction_result.get("predicted_class", "Unknown"),
        ])
        writer.writerow([
            "Confidence",
            prediction_result.get("confidence_percentage", "Unknown"),
        ])
        writer.writerow([
            "Model Name",
            prediction_result.get("model_name", "Unknown"),
        ])
        writer.writerow([
            "Prediction Time (s)",
            prediction_result.get("prediction_time_seconds", "Unknown"),
        ])

        probabilities = prediction_result.get("probabilities", {})

        for class_name, probability in probabilities.items():
            writer.writerow([
                f"Probability - {class_name}",
                f"{probability * 100:.2f}%",
            ])

    logger.info("CSV report saved to: %s", output_path)

    return output_path


# =============================================================================
# SUMMARY TABLE CREATION
# =============================================================================

def create_summary_table(
    prediction_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create a compact summary table for multiple predictions."""

    summary: list[dict[str, Any]] = []

    for index, result in enumerate(prediction_results, start=1):
        summary.append({
            "index": index,
            "predicted_class": result.get("predicted_class", "Unknown"),
            "confidence": result.get("confidence_percentage", "Unknown"),
            "model_name": result.get("model_name", "Unknown"),
        })

    return summary


# =============================================================================
# BATCH JSON REPORT GENERATION
# =============================================================================

def generate_batch_json_report(
    prediction_results: list[dict[str, Any]],
    image_names: list[str] | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Generate a JSON report containing multiple predictions."""

    if image_names is None:
        image_names = [f"image_{i + 1}" for i in range(len(prediction_results))]

    payload = {
        "metadata": create_report_metadata(),
        "report_type": "batch_prediction_report",
        "total_predictions": len(prediction_results),
        "summary": create_summary_table(prediction_results),
        "predictions": [
            {
                "image_name": image_names[index],
                "prediction": prediction_results[index],
            }
            for index in range(len(prediction_results))
        ],
    }

    if output_path is None:
        filename = generate_report_filename(
            prefix="batch_prediction_report",
            extension="json",
        )
        output_path = REPORTS_JSON_DIR / filename

    output_path = Path(output_path)

    save_json(output_path, payload)

    logger.info("Batch JSON report saved to: %s", output_path)

    return output_path


# =============================================================================
# BATCH CSV REPORT GENERATION
# =============================================================================

def generate_batch_csv_report(
    prediction_results: list[dict[str, Any]],
    image_names: list[str] | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Generate a CSV report for multiple predictions."""

    if image_names is None:
        image_names = [f"image_{i + 1}" for i in range(len(prediction_results))]

    if output_path is None:
        filename = generate_report_filename(
            prefix="batch_prediction_report",
            extension="csv",
        )
        output_path = REPORTS_CSV_DIR / filename

    output_path = Path(output_path)

    ensure_directory(output_path.parent)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Image Name",
            "Predicted Class",
            "Confidence",
            "Model Name",
            "Prediction Time (s)",
        ])

        for image_name, result in zip(image_names, prediction_results):
            writer.writerow([
                image_name,
                result.get("predicted_class", "Unknown"),
                result.get("confidence_percentage", "Unknown"),
                result.get("model_name", "Unknown"),
                result.get("prediction_time_seconds", "Unknown"),
            ])

    logger.info("Batch CSV report saved to: %s", output_path)

    return output_path


# =============================================================================
# REPORT INDEX GENERATION
# =============================================================================

def generate_report_index() -> dict[str, list[str]]:
    """Generate an index of available report files."""

    json_reports = [
        str(path.name)
        for path in sorted(REPORTS_JSON_DIR.glob("*.json"))
    ]

    csv_reports = [
        str(path.name)
        for path in sorted(REPORTS_CSV_DIR.glob("*.csv"))
    ]

    return {
        "json_reports": json_reports,
        "csv_reports": csv_reports,
    }


# =============================================================================
# EXTEND PUBLIC EXPORTS
# =============================================================================

__all__.extend([
    "create_summary_table",
    "generate_batch_csv_report",
    "generate_batch_json_report",
    "generate_csv_report",
    "generate_report_index",
])


# =============================================================================
# INITIALIZE PDF REPORT DIRECTORY
# =============================================================================

# ensure_directory(REPORTS_PDF_DIR)


# =============================================================================
# PDF HEADER LAYOUT
# =============================================================================

def create_pdf_header_table(
    prediction_result: dict[str, Any],
    image_path: str | Path | None = None,
) -> Table:
    """Create the top PDF layout with prediction info on the left and
    the uploaded image on the right."""

    info_data = [
        ["Prediction", prediction_result.get("predicted_class", "Unknown")],
        ["Confidence", prediction_result.get("confidence_percentage", "Unknown")],
        ["Model", prediction_result.get("model_name", "Unknown")],
        [
            "Prediction Time",
            f"{prediction_result.get('prediction_time_seconds', 0):.4f} s",
        ],
    ]

    info_table = Table(info_data, colWidths=[120, 170])

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    if image_path and Path(image_path).exists():
        uploaded_image = RLImage(str(image_path), width=140, height=140)
    else:
        uploaded_image = Paragraph(
            "<i>No uploaded image available</i>",
            getSampleStyleSheet()["BodyText"],
        )

    layout = Table(
        [[info_table, uploaded_image]],
        colWidths=[320, 180],
    )

    layout.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 1, colors.lightgrey),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    return layout


# =============================================================================
# PROBABILITY TABLE
# =============================================================================

def create_probability_table(probabilities: dict[str, float]) -> Table:
    """Create a table showing class probabilities."""

    data = [["Class", "Probability"]]

    for class_name, probability in probabilities.items():
        data.append([
            class_name,
            f"{probability * 100:.2f}%",
        ])

    table = Table(data, colWidths=[220, 120])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E8B57")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
    ]))

    return table


# =============================================================================
# PDF REPORT GENERATION
# =============================================================================

def generate_pdf_report(
    prediction_result: dict[str, Any],
    image_name: str | None = None,
    image_path: str | Path | None = None,
    gradcam_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> Path:
    """Generate a professional PDF prediction report."""

    if output_path is None:
        filename = generate_report_filename(extension="pdf")
        output_path = REPORTS_PDF_DIR / filename

    output_path = Path(output_path)

    ensure_directory(output_path.parent)

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # -------------------------------------------------------------------------
    # Title
    # -------------------------------------------------------------------------

    title = Paragraph(
        f"<b>{REPORT_TITLE}</b>",
        styles["Title"],
    )

    elements.append(title)
    elements.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # Header section with image on the RIGHT
    # -------------------------------------------------------------------------

    header_table = create_pdf_header_table(
        prediction_result=prediction_result,
        image_path=image_path,
    )

    elements.append(header_table)
    elements.append(Spacer(1, 18))

    # -------------------------------------------------------------------------
    # Probability section
    # -------------------------------------------------------------------------

    elements.append(Paragraph(
        "<b>Class Probabilities</b>",
        styles["Heading2"],
    ))

    probabilities = prediction_result.get("probabilities", {})

    elements.append(create_probability_table(probabilities))
    elements.append(Spacer(1, 18))

    # -------------------------------------------------------------------------
    # Grad-CAM section
    # -------------------------------------------------------------------------

    if gradcam_path and Path(gradcam_path).exists():
        elements.append(Paragraph(
            "<b>Grad-CAM Visualization</b>",
            styles["Heading2"],
        ))

        gradcam_image = RLImage(str(gradcam_path), width=380, height=280)

        elements.append(gradcam_image)
        elements.append(Spacer(1, 18))

    # -------------------------------------------------------------------------
    # Footer
    # -------------------------------------------------------------------------

    footer = Paragraph(
        (
            f"<font size='9'>Generated by {PROJECT_NAME} "
            f"v{PROJECT_VERSION} on {format_datetime()}</font>"
        ),
        styles["BodyText"],
    )

    elements.append(Spacer(1, 20))
    elements.append(footer)

    document.build(elements)

    logger.info("PDF report saved to: %s", output_path)

    return output_path


# =============================================================================
# COMPLETE REPORT GENERATION
# =============================================================================

def generate_complete_report(
    prediction_result: dict[str, Any],
    image_name: str | None = None,
    image_path: str | Path | None = None,
    gradcam_path: str | Path | None = None,
) -> dict[str, Path]:
    """Generate JSON, CSV, and PDF reports together."""

    json_report = generate_json_report(
        prediction_result=prediction_result,
        image_name=image_name,
        image_path=image_path,
        gradcam_path=gradcam_path,
    )

    csv_report = generate_csv_report(
        prediction_result=prediction_result,
        image_name=image_name,
    )

    pdf_report = generate_pdf_report(
        prediction_result=prediction_result,
        image_name=image_name,
        image_path=image_path,
        gradcam_path=gradcam_path,
    )

    return {
        "json": json_report,
        "csv": csv_report,
        "pdf": pdf_report,
    }


# =============================================================================
# EXTEND PUBLIC EXPORTS
# =============================================================================

__all__.extend([
    "generate_complete_report",
    "generate_pdf_report",
])



# =============================================================================
# DEVELOPMENT SELF-TEST
# =============================================================================

if __name__ == "__main__":
    sample_prediction = {
        "predicted_class": "Fresh",
        "confidence": 0.93,
        "confidence_percentage": "93.00%",
        "probabilities": {
            "Formalin-mixed": 0.07,
            "Fresh": 0.93,
        },
        "model_name": "Custom CNN",
        "prediction_time_seconds": 0.0412,
        "is_confident": True,
    }

    report_path = generate_json_report(
        prediction_result=sample_prediction,
        image_name="apple_sample.jpg",
        image_path="uploads/apple_sample.jpg",
        gradcam_path="outputs/apple_gradcam.png",
    )

    print("JSON report generated successfully")
    print(f"Saved to: {report_path.resolve()}")

