#!/bin/bash

# Silicon Subprime - Virtual Environment Setup Script
# This script creates a Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "=========================================="
echo "Silicon Subprime - Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo "Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
VENV_DIR="venv"
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at ./$VENV_DIR"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "Using existing virtual environment."
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "Warning: requirements.txt not found"
fi
echo ""

# Install Jupyter if not already in requirements
echo "Ensuring Jupyter is installed..."
pip install jupyter jupyterlab
echo "✓ Jupyter installed"
echo ""

# Enable ipywidgets extension for Jupyter
echo "Enabling Jupyter widgets..."
jupyter nbextension enable --py widgetsnbextension --sys-prefix 2>/dev/null || true
echo "✓ Jupyter widgets enabled"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start Jupyter Lab, run:"
echo "  jupyter lab"
echo ""
echo "To start Jupyter Notebook, run:"
echo "  jupyter notebook"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
echo "Game notebooks are located in:"
echo "  ./notebooks/01_Shadow_Book.ipynb"
echo "  ./notebooks/02_The_Syndicate.ipynb"
echo "  ./notebooks/03_Tranche_Defense.ipynb"
echo ""
