"""
Project Bootstrap Installer
Apple Formalin Detection System

This script:
1. Checks Python version
2. Installs project dependencies
3. Verifies installation
4. Prints next setup steps

Author: Project Team
"""

import subprocess
import sys

# ==========================
# REQUIRED PROJECT PACKAGES
# ==========================

REQUIRED_PACKAGES = [
    "tensorflow==2.21.0",
    "numpy",
    "pandas",
    "opencv-python",
    "Pillow",
    "matplotlib",
    "scikit-learn",
    "fastapi",
    "uvicorn",
    "python-multipart",
    "streamlit",
    "requests",
    "python-dotenv",
]

# ==========================


def run(command):
    subprocess.check_call(command)


def install(package):
    print(f"Installing {package}...")
    run([sys.executable, "-m", "pip", "install", "--no-cache-dir", package])


def verify(package):

    aliases = {
        "opencv-python": "cv2",
        "Pillow": "PIL",
        "scikit-learn": "sklearn",
        "python-dotenv": "dotenv",
        "python-multipart": "multipart",
    }

    module = package.split("==")[0]
    module = aliases.get(module, module.replace("-", "_")) or module

    try:
        __import__(module)
        print(f"✓ {module}")
    except ImportError:
        print(f"✗ {module}")


def main():

    print("=" * 60)
    print("Apple Formalin Detection Project Installer")
    print("=" * 60)

    print(f"\nPython Version : {sys.version.split()[0]}")
    print("Using existing pip installation.\n")

    print("Installing project packages...\n")

    for package in REQUIRED_PACKAGES:
        install(package)

    print("\nVerifying installation...\n")

    for package in REQUIRED_PACKAGES:
        verify(package)

    print("\nInstallation Complete.")
    print("\nNext Commands:")
    print("pip freeze > requirements.txt")
    print("python -c \"import tensorflow as tf; print(tf.__version__)\"")


if __name__ == "__main__":
    main()