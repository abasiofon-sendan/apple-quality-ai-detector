"""
Project Bootstrap Installer
Apple Formalin Detection System

This script:
1. Verifies Python version
2. Upgrades pip
3. Installs required project packages
4. Verifies installation
"""

import subprocess
import sys

REQUIRED_PACKAGES = [
    "tensorflow",
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
    "python-dotenv"
]


def run(command):
    """Run a shell command."""
    subprocess.check_call(command)


def install(package):
    """Install a package."""
    print(f"Installing {package}...")
    run([sys.executable, "-m", "pip", "install", package])


def verify(package):
    """Verify package installation."""
    module = package.replace("-", "_")

    # Common import name differences
    aliases = {
        "Pillow": "PIL",
        "opencv-python": "cv2",
        "scikit-learn": "sklearn",
        "python-dotenv": "dotenv",
        "python-multipart": "multipart",
    }

    module = aliases.get(package, module) or module

    try:
        __import__(module)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package}")


def main():

    print("=" * 60)
    print("Apple Formalin Detection Project Installer")
    print("=" * 60)

    print("\nUpgrading pip...\n")

    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    print("\nInstalling packages...\n")

    for package in REQUIRED_PACKAGES:
        install(package)

    print("\nVerifying installation...\n")

    for package in REQUIRED_PACKAGES:
        verify(package)

    print("\nInstallation Complete!")
    print("Next:")
    print("    pip freeze > requirements.txt")


if __name__ == "__main__":
    main()