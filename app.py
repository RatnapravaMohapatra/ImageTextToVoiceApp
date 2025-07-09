import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
from gtts import gTTS
from googletrans import Translator
import pytesseract
from PIL import Image

# Configure for Render deployment
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'ratna123@789')  # Use environment variable

# Configure paths for Render
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
AUDIO_FOLDER = os.path.join(os.getcwd(), 'static', 'audio')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tesseract configuration - works on both local and Render
tesseract_cmd = os.environ.get('TESSERACT_CMD', 
                              r'C:\Program Files\Tesseract-OCR\tesseract.exe' if os.name == 'nt' 
                              else '/usr/bin/tesseract')
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

translator = Translator()

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def init_db():
    # Use absolute path for database
    db_path = os.path.join(os.getcwd(), 'database.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_path = os.path.join(os.getcwd(), 'database.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username already exists!")
        finally:
            conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_path = os.path.join(os.getcwd(), 'database.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                 (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/upload')
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('upload.html', error="No file selected")
        
        file = request.files['image']
        if file.filename == '':
            return render_template('upload.html', error="No file selected")
            
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                text = pytesseract.image_to_string(Image.open(filepath))
                translations = {
                    'Tamil': translator.translate(text, dest='ta').text,
                    'French': translator.translate(text, dest='fr').text,
                    'Hindi': translator.translate(text, dest='hi').text,
                    'Telugu': translator.translate(text, dest='te').text,
                    'Malayalam': translator.translate(text, dest='ml').text,
                    'English': text
                }
                session['extracted_text'] = text
                session['translations'] = translations
                return render_template('result.html', 
                                      extracted_text=text, 
                                      translated_texts=translations)
            except Exception as e:
                return render_template('upload.html', 
                                     error=f"Error processing image: {str(e)}")
    
    return render_template('upload.html')

@app.route('/audio', methods=['POST'])
def audio():
    if 'translations' not in session:
        return redirect('/upload')
    
    translations = session['translations']
    audio_files = {}
    
    for lang, text in translations.items():
        lang_code = {
            'English': 'en', 'Tamil': 'ta', 'French': 'fr', 
            'Hindi': 'hi', 'Telugu': 'te', 'Malayalam': 'ml'
        }.get(lang, 'en')
        
        audio_filename = f"{lang}_{session['user']}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        
        try:
            tts = gTTS(text=text, lang=lang_code)
            tts.save(audio_path)
            audio_files[lang] = audio_filename
        except Exception as e:
            return render_template('result.html',
                                error=f"Error generating {lang} audio: {str(e)}",
                                extracted_text=session.get('extracted_text', ''),
                                translated_texts=translations)
    
    return render_template('audio.html', audio_files=audio_files)

@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))  # For Render compatibility
    app.run(host='0.0.0.0', port=port)
