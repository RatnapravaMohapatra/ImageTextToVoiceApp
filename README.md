# ImageTextToVoiceApp
This Flask-based web app lets users upload images, extract text using pytesseract, translate it with Googletrans, and generate audio using gTTS in multiple languages. It features user authentication, animated UI with HTML/CSS, and stores data using SQLite.

# Image Text Extractor & Translator 🌍📸

A Flask application that extracts text from images using OCR (Optical Character Recognition) and translates it to multiple languages with text-to-speech capabilities.

![Demo]





## Features ✨

- 🖼️ Upload images containing text
- 🔍 Extract text using Tesseract OCR
- 🌐 Translate to 5 languages (Tamil, French, Hindi, Telugu, Malayalam)
- 🔊 Convert translated text to speech


https://github.com/user-attachments/assets/7f9329a5-111e-4439-bd70-b6eb2712e3ea

- 🔒 User authentication (login/signup)
- 🎨 Beautiful responsive UI with animations

## Technologies Used 🛠️

**Backend:**
- Python Flask
- SQLite (database)
- Tesseract OCR
- Google Translate API
- gTTS (Google Text-to-Speech)



**Frontend:**
- HTML5, CSS3

## Prerequisites 📋

- Python 3.8+
- Tesseract OCR installed ([Windows](https://github.com/UB-Mannheim/tesseract/wiki))
- For macOS: `brew install tesseract`
- For Linux: `sudo apt install tesseract-ocr`

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image-text-extractor.git
   cd image-text-extractor
