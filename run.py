"""
===============================================================================
AppleGuard AI Project Launcher
===============================================================================

Project
-------
AppleGuard AI
AI-Powered Detection of Fresh and Formalin-Mixed Apples

Description
-----------
This script serves as the central launcher for the AppleGuard AI project.

Rather than requiring developers to remember multiple commands, this
launcher provides a single entry point for starting the project's
services.

The launcher can start:

• FastAPI Backend
• Streamlit Frontend
• Both services simultaneously (Development Mode)

Running both services together is intended only for local development.
For production deployment, the API and Streamlit application should be
deployed as independent services.

Usage
-----

Start the FastAPI backend

    python run.py api

Start the Streamlit application

    python run.py app

Start both services

    python run.py all

Project Structure
-----------------

run.py
    ├── Launch FastAPI
    ├── Launch Streamlit
    └── Launch Both Services

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
# This launcher uses only Python's standard library together with the
# project's central configuration module.
#
# The standard library handles:
#
# • Command-line argument parsing
# • Launching subprocesses
# • Managing multiple processes
# • Graceful shutdown
# • Time delays during startup
#
# Project configuration such as API ports and host addresses are loaded
# from src.config to ensure every component uses the same settings.
# =============================================================================

from __future__ import annotations

import argparse
import subprocess
import sys
import time

from src.config import (
    API_HOST,
    API_PORT,
    PROJECT_NAME,
    PROJECT_VERSION,
)

# =============================================================================
# LAUNCHER CONFIGURATION
# =============================================================================
#
# These constants control the behaviour of the launcher itself.
#
# STARTUP_DELAY
# -------------
# Number of seconds to wait after launching the FastAPI server before
# starting the Streamlit application.
#
# This gives the backend enough time to initialize and begin listening
# for incoming requests.
#
# LINE_WIDTH
# ----------
# Used to create consistently formatted console output throughout the
# launcher.
# =============================================================================

STARTUP_DELAY = 2

LINE_WIDTH = 78

# =============================================================================
# CONSOLE DISPLAY HELPERS
# =============================================================================
#
# The launcher prints informative messages while starting the various
# project services. Rather than repeatedly writing print() statements
# throughout the code, all console output is handled through the helper
# functions below.
#
# Advantages
# ----------
# • Consistent formatting across the project.
# • Cleaner and easier-to-read launcher code.
# • Simple to modify the appearance of console messages.
# • Consistent with config.py and install.py.
#
# =============================================================================


def print_header() -> None:
    """
    Display the launcher banner.

    This banner is displayed whenever the launcher starts and provides
    basic information about the project.

    Returns
    -------
    None
    """

    print("\n" + "=" * LINE_WIDTH)
    print(f"{PROJECT_NAME} Launcher".center(LINE_WIDTH))
    print(f"Version {PROJECT_VERSION}".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def print_section(title: str) -> None:
    """
    Display a section heading.

    Parameters
    ----------
    title : str
        Name of the current launcher operation.

    Returns
    -------
    None
    """

    print(f"\n{title}")
    print("-" * len(title))


def print_success(message: str) -> None:
    """
    Display a success message.

    Parameters
    ----------
    message : str
        Message describing a successful operation.

    Returns
    -------
    None
    """

    print(f"✓ {message}")


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


def print_warning(message: str) -> None:
    """
    Display a warning message.

    Parameters
    ----------
    message : str
        Warning to display.

    Returns
    -------
    None
    """

    print(f"⚠ {message}")


def print_error(message: str) -> None:
    """
    Display an error message.

    Parameters
    ----------
    message : str
        Error description.

    Returns
    -------
    None
    """

    print(f"✗ {message}")


def print_separator() -> None:
    """
    Print a horizontal separator.

    Useful for visually separating major launcher events.

    Returns
    -------
    None
    """

    print("-" * LINE_WIDTH)


# =============================================================================
# PROJECT VALIDATION
# =============================================================================
#
# Before launching any service, we verify that the expected project
# structure exists. This helps collaborators detect missing files or
# folders before runtime.
#
# =============================================================================

from pathlib import Path


def verify_project_structure() -> bool:
    """
    Verify that the required project files and folders exist.

    Returns
    -------
    bool
        True if every required item exists.
    """

    print_section("Project Validation")

    project_root = Path(__file__).resolve().parent

    required_items = {
        "API Folder": project_root / "api",
        "App Folder": project_root / "app",
        "Source Folder": project_root / "src",
        "Models Folder": project_root / "models",
        "Assets Folder": project_root / "assets",
        "Reports Folder": project_root / "reports",
        "Requirements": project_root / "requirements.txt",
        "Install Script": project_root / "install.py",
        "API Main": project_root / "api" / "main.py",
        "Streamlit App": project_root / "app" / "streamlit_app.py",
    }

    all_ok = True

    for name, path in required_items.items():
        if path.exists():
            print_success(name)

        else:
            print_error(f"{name} not found")

            all_ok = False

    return all_ok


# =============================================================================
# APPLICATION LAUNCHERS
# =============================================================================
#
# The functions below are responsible for starting the various services
# that make up the AppleGuard AI application.
#
# Responsibilities
# ----------------
# • Launch the FastAPI backend.
# • Launch the Streamlit frontend.
# • Launch both services for local development.
#
# These functions DO NOT:
#
# • Load AI models.
# • Perform image preprocessing.
# • Run predictions.
# • Execute application logic.
#
# Their only responsibility is starting and managing processes.
#
# =============================================================================


def run_api() -> None:
    """
    Launch the FastAPI backend server.

    The backend exposes REST API endpoints that the Streamlit
    application communicates with.

    Returns
    -------
    None
    """

    print_section("Launching FastAPI Backend")

    print_info(f"Host : {API_HOST}")

    print_info(f"Port : {API_PORT}")

    print_info("Starting Uvicorn server...\n")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api.main:app",
                "--host",
                API_HOST,
                "--port",
                str(API_PORT),
                "--reload",
            ],
            check=True,
        )

    except KeyboardInterrupt:
        print("\n")

        print_warning("FastAPI server stopped by user.")

    except subprocess.CalledProcessError:
        print_error("Unable to start the FastAPI server.")

        sys.exit(1)


def run_app() -> None:
    """
    Launch the Streamlit frontend.

    The Streamlit application acts as the graphical user interface
    for AppleGuard AI and communicates with the FastAPI backend.

    Returns
    -------
    None
    """

    print_section("Launching Streamlit Application")

    print_info("Opening Streamlit...\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py"],
            check=True,
        )

    except KeyboardInterrupt:
        print("\n")

        print_warning("Streamlit application closed by user.")

    except subprocess.CalledProcessError:
        print_error("Unable to start the Streamlit application.")

        sys.exit(1)


def run_all() -> None:
    """
    Launch both FastAPI and Streamlit.

    This mode is intended ONLY for local development.

    Workflow
    --------
    1. Start the FastAPI backend.
    2. Wait briefly for the API to initialize.
    3. Launch the Streamlit application.
    4. When Streamlit exits, terminate the API server.

    Returns
    -------
    None
    """

    print_section("Launching AppleGuard AI")

    print_info("Starting FastAPI backend...")

    try:
        api_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api.main:app",
                "--host",
                API_HOST,
                "--port",
                str(API_PORT),
            ]
        )

    except Exception:
        print_error("Failed to launch the FastAPI backend.")

        sys.exit(1)

    print_success("FastAPI backend started.")

    print_info(f"Backend available at http://{API_HOST}:{API_PORT}")

    print_info(f"Waiting {STARTUP_DELAY} seconds for backend initialization...")

    time.sleep(STARTUP_DELAY)

    print("\n")

    print_info("Launching Streamlit frontend...")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py"],
            check=True,
        )

    except KeyboardInterrupt:
        print("\n")

        print_warning("Application closed by user.")

    finally:
        print("\n")

        print_info("Stopping FastAPI backend...")

        api_process.terminate()

        api_process.wait(timeout=10)

        print_success("Backend stopped successfully.")


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================
#
# The launcher is controlled from the command line using argparse.
#
# Supported Commands
# ------------------
#
# python run.py api
#     Starts only the FastAPI backend.
#
# python run.py app
#     Starts only the Streamlit frontend.
#
# python run.py all
#     Starts both FastAPI and Streamlit.
#
# Any invalid command is automatically rejected and the available options
# are displayed to the user.
#
# =============================================================================
# =============================================================================
# INTERACTIVE DEVELOPER MENU
# =============================================================================


def interactive_menu() -> None:
    """
    Display the interactive launcher menu.
    """

    while True:
        print_separator()

        print("Developer Console")
        print()

        print("1. Install Dependencies")
        print("2. Start FastAPI Backend")
        print("3. Start Streamlit Frontend")
        print("4. Launch Complete Application")
        print("5. Project Information")
        print("6. Validate Project Structure")
        print("7. Exit")

        print_separator()

        choice = input("Select an option: ").strip()

        if choice == "1":
            subprocess.run([sys.executable, "install.py"])

        elif choice == "2":
            run_api()

        elif choice == "3":
            run_app()

        elif choice == "4":
            run_all()

        elif choice == "5":
            print_section("Project Information")

            print_info(f"Project : {PROJECT_NAME}")

            print_info(f"Version : {PROJECT_VERSION}")

            print_info(f"API Host : {API_HOST}")

            print_info(f"API Port : {API_PORT}")

        elif choice == "6":
            verify_project_structure()

        elif choice == "7":
            print_success("Thank you for using AppleGuard AI.")

            break

        else:
            print_error("Invalid selection.")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Launch AppleGuard AI services.")

    parser.add_argument(
        "target",
        nargs="?",
        choices=["api", "app", "all"],
        help=("api  - Launch FastAPI\napp  - Launch Streamlit\nall  - Launch both"),
    )
    return parser.parse_args()


# =============================================================================
# MAIN APPLICATION WORKFLOW
# =============================================================================
#
# This function coordinates the launcher.
#
# Workflow
# --------
#
# 1. Display launcher information.
# 2. Parse command-line arguments.
# 3. Execute the selected launcher.
# 4. Handle unexpected errors.
#
# Keeping all program flow inside main() follows Python best practices and
# improves readability.
#
# =============================================================================


def main() -> None:
    """
    Launch the requested AppleGuard AI service.

    Returns
    -------
    None
    """

    print_header()

    arguments = parse_arguments()

    verify_project_structure()

    if arguments.target is None:
        interactive_menu()

        return

    launchers = {"api": run_api, "app": run_app, "all": run_all}

    print_info(f"Selected Mode : {arguments.target.upper()}")

    print_separator()

    try:
        launchers[arguments.target]()

    except KeyboardInterrupt:
        print()

        print_warning("Launcher interrupted.")

    except Exception as error:
        print_error(str(error))

        sys.exit(1)

    launchers = {"api": run_api, "app": run_app, "all": run_all}

    print_info(f"Selected Mode : {arguments.target.upper()}")

    print_separator()

    try:
        launchers[arguments.target]()

    except KeyboardInterrupt:
        print("\n")

        print_warning("Launcher interrupted by user.")

        print_success("AppleGuard AI shutdown completed.")

    except Exception as error:
        print("\n")

        print_error("An unexpected error occurred.")

        print_error(str(error))

        sys.exit(1)


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================
#
# This is the entry point of the launcher.
#
# When run.py is executed directly:
#
#     python run.py api
#
# Python executes the code below and starts the selected service.
#
# Importing this file from another module will NOT automatically launch
# any services because main() is only called when this file is executed
# directly.
#
# =============================================================================

if __name__ == "__main__":
    main()
