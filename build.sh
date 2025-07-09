#!/bin/bash
set -e

# Install system dependencies
echo "Installing Tesseract OCR..."
apt-get update
apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    python3-dev \
    python3-setuptools

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads static/audio  # Fixed typo (was 'mudio')

# Install Python dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt  # Fixed (was '--r')

echo "Build completed successfully!"
