
"""
===============================================================================
AppleGuard AI — Version Information Module
===============================================================================

Project      : AppleGuard AI
Author       : Group 16
Institution  : University of Uyo
Department   : Computer Engineering
Year         : 2026

Description
-----------
Centralized application metadata and version information.

This module provides a single source of truth for:
- Application name
- Semantic version number
- Author information
- Build information
- Environment metadata
- Runtime version summaries
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import platform
import sys
from datetime import datetime, timezone


from typing import Any

# =============================================================================
# APPLICATION METADATA
# =============================================================================

APP_NAME = "AppleGuard AI"
APP_DESCRIPTION = "AI-powered Apple Quality Detection System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Group 16"
APP_ORGANIZATION = "University of Uyo — Department of Computer Engineering"
APP_LICENSE = "Academic Project"
APP_YEAR = "2026"


# =============================================================================
# SEMANTIC VERSION COMPONENTS
# =============================================================================

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0


# =============================================================================
# BUILD INFORMATION
# =============================================================================

BUILD_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BUILD_TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")




# =============================================================================
# VERSION UTILITIES
# =============================================================================

def get_version() -> str:
    """Return the semantic version string."""

    return APP_VERSION


def get_version_tuple() -> tuple[int, int, int]:
    """Return the version as a tuple."""

    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)


def get_build_info() -> dict[str, str]:
    """Return build-related information."""

    return {
        "version": APP_VERSION,
        "build_date": BUILD_DATE,
        "build_timestamp": BUILD_TIMESTAMP,
    }


# =============================================================================
# SYSTEM INFORMATION
# =============================================================================

def get_system_info() -> dict[str, str]:
    """Return basic system information."""

    return {
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
        "platform_release": platform.release(),
        "architecture": platform.machine(),
    }


# =============================================================================
# APPLICATION SUMMARY
# =============================================================================

def get_app_info() -> dict[str, Any]:
    """Return complete application information."""

    return {
        "name": APP_NAME,
        "description": APP_DESCRIPTION,
        "version": APP_VERSION,
        "author": APP_AUTHOR,
        "organization": APP_ORGANIZATION,
        "license": APP_LICENSE,
        "year": APP_YEAR,
        "build": get_build_info(),
        "system": get_system_info(),
    }


def get_banner() -> str:
    """Return a formatted console banner."""

    return (
        f"{APP_NAME} v{APP_VERSION}\\n"
        f"{APP_DESCRIPTION}\\n"
        f"{APP_ORGANIZATION}\\n"
        f"Build: {BUILD_DATE}"
    )


# =============================================================================
# PUBLIC EXPORTS
# =============================================================================

__all__ = [
    "APP_AUTHOR",
    "APP_DESCRIPTION",
    "APP_LICENSE",
    "APP_NAME",
    "APP_ORGANIZATION",
    "APP_VERSION",
    "APP_YEAR",
    "BUILD_DATE",
    "BUILD_TIMESTAMP",
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_PATCH",
    "get_app_info",
    "get_banner",
    "get_build_info",
    "get_system_info",
    "get_version",
    "get_version_tuple",
]


# =============================================================================
# DEVELOPMENT SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print(get_banner())
    print()

    info = get_app_info()

    print("Application Information")
    print("-" * 40)

    for key, value in info.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

