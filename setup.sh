#!/bin/bash

echo "=========================================="
echo "        StegoSphere Setup (macOS/Linux)"
echo "=========================================="

# Check for Python 3
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "[ERROR] Python is not installed."
    exit 1
fi

echo "[INFO] Using $PYTHON_CMD"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
else
    echo "[INFO] Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installing/Updating dependencies..."
    pip install -r requirements.txt
else
    echo "[ERROR] requirements.txt not found!"
    exit 1
fi

echo ""
echo "=========================================="
echo "       Setup Complete! Starting App..."
echo "=========================================="
python main.py