"""
Project Bootstrap Installer
Apple Formalin Detection System

Workflow:
1. Check Python version
2. Check if required packages already exist
3. If everything exists -> Happy Coding!
4. Otherwise install requirements.txt
5. Verify installation
"""

import importlib
import subprocess
import sys
from pathlib import Path

CORE_PACKAGES = {
    "tensorflow": "TensorFlow",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "cv2": "OpenCV",
    "PIL": "Pillow",
    "sklearn": "Scikit-Learn",
    "fastapi": "FastAPI",
    "streamlit": "Streamlit",
}


def run(command):
    subprocess.check_call(command)


def package_exists(module):
    try:
        importlib.import_module(module)
        return True
    except ImportError:
        return False


def verify_environment():
    print("\nChecking project environment...\n")

    missing = []

    for module, name in CORE_PACKAGES.items():

        if package_exists(module):
            print(f"✓ {name}")
        else:
            print(f"✗ {name}")
            missing.append(module)

    return missing


def install_dependencies():

    requirements = Path("requirements.txt")

    if not requirements.exists():
        print("\nERROR: requirements.txt not found.")
        sys.exit(1)

    print("\nInstalling project dependencies...\n")

    run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-cache-dir",
        "-r",
        "requirements.txt"
    ])


def main():

    print("=" * 60)
    print("Apple Formalin Detection System")
    print("Project Bootstrap Installer")
    print("=" * 60)

    print(f"\nPython Version: {sys.version.split()[0]}")

    missing = verify_environment()

    if not missing:

        print("\nEnvironment already configured.")
        print("Happy Coding! 🚀")
        return

    print("\nSome required packages are missing.")
    print("Installing dependencies...")

    install_dependencies()

    missing = verify_environment()

    if not missing:
        print("\nEnvironment successfully configured.")
        print("Happy Coding! 🚀")
    else:
        print("\nSetup incomplete.")
        print("The following packages are still missing:")

        for package in missing:
            print(f" - {package}")

        print("\nPlease review requirements.txt or your installation logs.")


if __name__ == "__main__":
    main()