#!/bin/bash

echo "========================================"
echo "  CAL Fund Analyzer - Clean Architecture"
echo "========================================"
echo ""
echo "Checking dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python from python.org"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo "Using: $PYTHON_CMD"
echo ""
echo "Installing backend dependencies..."

cd backend
pip3 install -r requirements.txt --quiet || pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Starting Flask server..."
echo ""
echo "========================================"
echo "  Server will start on port 5000"
echo "  Open your browser to:"
echo "  http://localhost:5000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

$PYTHON_CMD server.py

