"""
===============================================================================
AppleGuard AI Bootstrap Installer
===============================================================================

Project:
    AppleGuard AI
    AI-Powered Detection of Fresh and Formalin-Mixed Apples

Description
-----------
This script prepares the local development environment before running
the project.

Rather than requiring contributors to manually install dependencies,
this installer automatically verifies the development environment and
installs any missing packages.

Workflow
--------
1. Verify Python version.
2. Verify pip is available.
3. Check whether required packages are already installed.
4. Install missing packages from requirements.txt.
5. Verify installation.
6. Display a detailed installation summary.

Typical Usage
-------------
python install.py

This script is intended to be executed once after cloning the repository,
or whenever project dependencies are updated.

Author
------
AppleGuard AI Development Team
University of Uyo
===============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
#
# Only standard library modules are used in this installer so that it can
# execute successfully even before project dependencies have been installed.
# =============================================================================

import importlib
import subprocess
import sys
from pathlib import Path

# =============================================================================
# INSTALLER CONFIGURATION
# =============================================================================
#
# Central configuration values used throughout the installer.
#
# Modifying these values allows future project updates without changing the
# installation logic.
# =============================================================================

PROJECT_NAME = "AppleGuard AI"

PROJECT_VERSION = "1.0.0"

MINIMUM_PYTHON_VERSION = (3, 10)

REQUIREMENTS_FILE = Path("requirements.txt")


# =============================================================================
# REQUIRED PACKAGES
# =============================================================================
#
# Dictionary mapping Python module names to user-friendly package names.
#
# The module name is used when attempting to import the package while the
# friendly name is displayed in the installation report.
#
# Format
# ------
# module_name : Display Name
# =============================================================================

CORE_PACKAGES = {
    "tensorflow": "TensorFlow",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "cv2": "OpenCV",
    "PIL": "Pillow",
    "sklearn": "Scikit-Learn",
    "matplotlib": "Matplotlib",
    "fastapi": "FastAPI",
    "uvicorn": "Uvicorn",
    "streamlit": "Streamlit",
    "requests": "Requests",
    "PIL.Image": "Pillow Image",
}


# =============================================================================
# CONSOLE DISPLAY HELPERS
# =============================================================================
#
# These helper functions standardize console output throughout the installer.
#
# Having dedicated display functions keeps the code clean and ensures all
# messages share the same formatting style.
# =============================================================================

LINE_WIDTH = 78


def print_header() -> None:
    """
    Display the installer header.

    Returns
    -------
    None
    """

    print("\n" + "=" * LINE_WIDTH)
    print(f"{PROJECT_NAME} Bootstrap Installer".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def print_section(title: str) -> None:
    """
    Display a section heading.

    Parameters
    ----------
    title : str
        Section title displayed in the console.

    Returns
    -------
    None
    """

    print(f"\n{title}")
    print("-" * len(title))


def print_success(message: str) -> None:
    """
    Display a successful operation.

    Parameters
    ----------
    message : str
        Success message.

    Returns
    -------
    None
    """

    print(f"✓ {message}")


def print_error(message: str) -> None:
    """
    Display an error message.

    Parameters
    ----------
    message : str
        Error message.

    Returns
    -------
    None
    """

    print(f"✗ {message}")


def print_info(message: str) -> None:
    """
    Display an informational message.

    Parameters
    ----------
    message : str
        Information to display.

    Returns
    -------
    None
    """

    print(f"• {message}")


# =============================================================================
# PYTHON ENVIRONMENT VERIFICATION
# =============================================================================
#
# Before attempting to install project dependencies, we verify that the
# user's development environment satisfies the minimum project
# requirements.
#
# The following checks are performed:
#
# • Python version
# • pip availability
# • Virtual environment status
#
# These checks help identify common setup problems before package
# installation begins.
#
# =============================================================================


def verify_python_version() -> None:
    """
    Verify that the current Python version meets the project's minimum
    supported version.

    Raises
    ------
    SystemExit
        If the installed Python version is too old.
    """

    print_section("Checking Python Version")

    current_version = sys.version_info[:3]

    print_info(
        f"Detected Python {current_version[0]}.{current_version[1]}.{current_version[2]}"
    )

    if current_version < MINIMUM_PYTHON_VERSION:
        print_error(
            f"Python {MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]} "
            "or newer is required."
        )

        sys.exit(1)

    print_success("Python version is supported.")


def verify_pip() -> None:
    """
    Verify that pip is installed and available.

    Raises
    ------
    SystemExit
        If pip cannot be executed.
    """

    print_section("Checking pip")

    try:
        subprocess.check_output([sys.executable, "-m", "pip", "--version"])

        print_success("pip is available.")

    except Exception:
        print_error("pip is not installed or cannot be accessed.")

        sys.exit(1)


def verify_virtual_environment() -> None:
    """
    Display whether the installer is running inside a virtual
    environment.

    Running inside a virtual environment is recommended but not
    mandatory.
    """

    print_section("Checking Virtual Environment")

    in_virtual_environment = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if in_virtual_environment:
        print_success("Virtual environment detected.")

    else:
        print_info("No virtual environment detected.")

        print_info("Using one is recommended to isolate project dependencies.")


# =============================================================================
# PACKAGE VERIFICATION
# =============================================================================
#
# These helper functions determine whether each required package has
# already been installed.
#
# Packages that are already available are skipped during installation,
# making repeated executions of this installer much faster.
#
# =============================================================================


def package_exists(module_name: str) -> bool:
    """
    Determine whether a Python module can be imported.

    Parameters
    ----------
    module_name : str

        Module to test.

    Returns
    -------
    bool

        True if the module exists.
    """

    try:
        importlib.import_module(module_name)

        return True

    except ImportError:
        return False


def verify_environment() -> list[str]:
    """
    Check every required project dependency.

    Returns
    -------
    list[str]

        List of missing Python modules.
    """

    print_section("Checking Installed Packages")

    missing_packages = []

    for module_name, display_name in CORE_PACKAGES.items():
        if package_exists(module_name):
            print_success(display_name)

        else:
            print_error(display_name)

            missing_packages.append(module_name)

    print()

    print_info(f"Installed : {len(CORE_PACKAGES) - len(missing_packages)}")

    print_info(f"Missing   : {len(missing_packages)}")

    return missing_packages


# =============================================================================
# DEPENDENCY INSTALLATION
# =============================================================================
#
# This section is responsible for installing the project's required
# Python packages from the requirements.txt file.
#
# Installation is only performed when one or more required packages are
# missing from the local development environment.
#
# =============================================================================


def requirements_file_exists() -> bool:
    """
    Check whether the project's requirements.txt file exists.

    Returns
    -------
    bool
        True if the file exists.
    """

    print_section("Checking Project Requirements")

    if REQUIREMENTS_FILE.exists():
        print_success(f"Found {REQUIREMENTS_FILE.name}")

        return True

    print_error(f"{REQUIREMENTS_FILE.name} not found.")

    print_info("Make sure you are running this script from the project root directory.")

    return False


def install_dependencies() -> bool:
    """
    Install all required project dependencies.

    Packages are installed using the project's requirements.txt file.

    Returns
    -------
    bool

        True if installation completed successfully.
    """

    print_section("Installing Project Dependencies")

    if not requirements_file_exists():
        return False

    print_info("This may take several minutes...")
    print_info("Please wait while packages are being installed.\n")

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "-r",
                str(REQUIREMENTS_FILE),
            ]
        )

        print_success("Project dependencies installed successfully.")

        return True

    except subprocess.CalledProcessError:
        print_error("Package installation failed.")

        print_info("Please review the installation output above for details.")

        return False


# =============================================================================
# POST-INSTALLATION VERIFICATION
# =============================================================================
#
# After package installation completes, we immediately perform another
# verification pass.
#
# This confirms that every required package can now be imported
# successfully before allowing the project to continue.
#
# =============================================================================


def verify_installation() -> bool:
    """
    Verify that all required packages were installed successfully.

    Returns
    -------
    bool

        True if every required package is available.
    """

    print_section("Verifying Installation")

    missing_packages = verify_environment()

    if len(missing_packages) == 0:
        print_success("All required packages are available.")

        return True

    print_error("Some packages are still missing.")

    print("\nMissing Packages")

    print("----------------")

    for package in missing_packages:
        print(f"• {package}")

    return False


# =============================================================================
# INSTALLATION SUMMARY
# =============================================================================
#
# This section displays the final outcome of the installation process.
#
# It provides a concise overview of whether the development environment
# is ready for running the AppleGuard AI project.
#
# =============================================================================


def print_final_summary(success: bool) -> None:
    """
    Display the final installation summary.

    Parameters
    ----------
    success : bool

        Indicates whether the installation completed successfully.

    Returns
    -------
    None
    """

    print("\n" + "=" * LINE_WIDTH)
    print("INSTALLATION SUMMARY".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)

    print(f"Project : {PROJECT_NAME}")

    print(f"Version : {PROJECT_VERSION}")

    print(f"Python  : {sys.version.split()[0]}")

    print(f"Packages Checked : {len(CORE_PACKAGES)}")

    if success:
        print("\nStatus  : READY ✅")

        print_success("Environment successfully configured.")

        print_success("You can now start developing with AppleGuard AI.")

        print("\nNext Steps")
        print("----------")
        print("1. Start the FastAPI backend")
        print("   python run.py api\n")

        print("2. Start the Streamlit application")
        print("   python run.py app\n")

        print("Or start both together")
        print("   python run.py all")

        print("\nHappy Coding! 🚀")

    else:
        print("\nStatus  : FAILED ❌")

        print_error("The environment is not fully configured.")

        print_info("Review the installation log above.")

        print_info("Correct the reported errors and run install.py again.")

    print("=" * LINE_WIDTH)


# =============================================================================
# MAIN INSTALLATION WORKFLOW
# =============================================================================
#
# This function coordinates the complete installation process.
#
# Workflow
# --------
# 1. Display installer header.
# 2. Verify Python version.
# 3. Verify pip installation.
# 4. Check virtual environment.
# 5. Verify installed packages.
# 6. Install missing dependencies if required.
# 7. Verify installation.
# 8. Display installation summary.
#
# =============================================================================


def main() -> None:
    """
    Execute the AppleGuard AI bootstrap installer.

    Returns
    -------
    None
    """

    print_header()

    verify_python_version()

    verify_pip()

    verify_virtual_environment()

    missing_packages = verify_environment()

    if not missing_packages:
        print("\n")

        print_success("All required packages are already installed.")

        print_success("No installation is required.")

        print_final_summary(True)

        return

    print("\n")

    print_info(f"{len(missing_packages)} required package(s) are missing.")

    print_info("Starting dependency installation...")

    installation_success = install_dependencies()

    if not installation_success:
        print_final_summary(False)

        sys.exit(1)

    verification_success = verify_installation()

    print_final_summary(verification_success)

    if not verification_success:
        sys.exit(1)


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================
#
# This allows the installer to be executed directly from the command line.
#
# Example
# -------
#
# python install.py
#
# =============================================================================

if __name__ == "__main__":
    main()
