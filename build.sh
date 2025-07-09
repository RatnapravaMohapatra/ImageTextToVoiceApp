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
mkdir -p uploads static/audio

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
