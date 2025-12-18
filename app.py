from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash  # Added flash
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from functools import wraps
from utils.disease_predictor import DiseasePredictor
from utils.location_service import LocationService
from utils.tts_service import TTSService
from utils.chatbot_service import ChatbotService
from config import Config
from googletrans import Translator
from ml_models import Database  # NEW: Import Database class

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key-change-this-to-random-string'  # NEW: Required for sessions and flash

# Initialize services
print("🚀 Initializing SCDAS - Smart Rice Disease Detection System...")
disease_predictor = DiseasePredictor(Config.MODEL_PATH)
location_service = LocationService()
tts_service = TTSService()
chatbot_service = ChatbotService()
db = Database()  # NEW: Initialize database
print("✅ All services initialized successfully!")


# NEW: Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/')
@login_required  # NEW: Protect home page
def index():
    return render_template('index.html', user=db.get_user_info(session['user_id']))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with phone and PIN"""
    if request.method == 'POST':
        phone = request.form.get('phone')
        pin = request.form.get('pin')
        full_name = request.form.get('full_name')
        village = request.form.get('village')
        
        user_id = db.create_user(phone, pin, full_name, village)
        
        if user_id:
            session['user_id'] = user_id
            flash('Registration successful! Welcome to SCDAS', 'success')
            return redirect(url_for('index'))
        else:
            flash('This phone number is already registered. Please login.', 'danger')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with phone and PIN"""
    if request.method == 'POST':
        phone = request.form.get('phone')
        pin = request.form.get('pin')
        
        user_id = db.verify_user(phone, pin)
        
        if user_id:
            session['user_id'] = user_id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid phone number or PIN', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/predict', methods=['POST'])
@login_required  # NEW: Protect prediction route
def predict():
    """Handle image upload and disease prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        upload_path = Path(app.config['UPLOAD_FOLDER'])
        upload_path.mkdir(parents=True, exist_ok=True)
        
        filepath = upload_path / filename
        file.save(str(filepath))
        
        print(f"📁 Image saved: {filename}")
        
        # Get disease prediction
        prediction = disease_predictor.predict(str(filepath))
        print(f"🔍 Detected: {prediction['disease']} ({prediction['confidence']}%)")
        
        # Validation - Check if confidence is too low
        MIN_CONFIDENCE_THRESHOLD = 40  # Minimum confidence to consider valid
        
        if prediction['confidence'] < MIN_CONFIDENCE_THRESHOLD:
            return render_template('error.html', 
                error_message="⚠️ Please upload a valid rice crop image. The uploaded image doesn't appear to be a rice plant or the image quality is too low.",
                image_path=str(filepath))
        
        # Get GPS location data
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location_info = location_service.get_location_info(latitude, longitude)
        
        # Prepare result
        result = {
            'disease': prediction['disease'],
            'confidence': prediction['confidence'],
            'symptoms': prediction['symptoms'],
            'treatment': prediction['treatment'],
            'prevention': prediction['prevention'],
            'image_path': str(filepath),
            'timestamp': timestamp,
            'location': location_info
        }
        
        # NEW: Save to user's database history
        db.add_diagnosis(session['user_id'], result)
        
        return render_template('result.html', result=result, user=db.get_user_info(session['user_id']))
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG'}), 400


@app.route('/text-to-speech', methods=['POST'])
@login_required  # NEW: Protect TTS route
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'en')

    if language == 'te':
        translator = Translator()
        text = translator.translate(text, src='en', dest='te').text

    audio_file = tts_service.convert_to_speech(text, language)

    if audio_file:
        return jsonify({'audio_url': audio_file})
    else:
        return jsonify({'error': 'Failed to generate audio'}), 500


@app.route('/chatbot', methods=['GET', 'POST'])
@login_required  # NEW: Protect chatbot route
def chatbot():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message', '')
        
        response = chatbot_service.get_response(user_message)
        
        return jsonify({'response': response})
    
    return render_template('chatbot.html', user=db.get_user_info(session['user_id']))


@app.route('/history')
@login_required  # NEW: Protect history route
def history():
    # NEW: Get user's history from database
    diagnosis_history = db.get_user_history(session['user_id'])
    return render_template('history.html', history=diagnosis_history, user=db.get_user_info(session['user_id']))


@app.route('/clear-history')
@login_required  # NEW: Protect clear history route
def clear_history():
    # NEW: Clear user's database history
    db.clear_user_history(session['user_id'])
    flash('History cleared successfully', 'success')
    return redirect(url_for('history'))


@app.route('/delete-diagnosis/<int:diagnosis_id>')
@login_required
def delete_diagnosis(diagnosis_id):
    """Delete a single diagnosis"""
    db.delete_diagnosis(diagnosis_id, session['user_id'])
    flash('Diagnosis deleted', 'success')
    return redirect(url_for('history'))


if __name__ == '__main__':
    print("📂 Creating necessary directories...")
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path('models').mkdir(parents=True, exist_ok=True)
    Path('static/audio').mkdir(parents=True, exist_ok=True)
    print("✅ Directories created!")
    
    print("\n" + "="*60)
    print("🌾 SCDAS - Smart Rice Disease Detection & Advisory System")
    print("="*60)
    print("📍 Server starting at: http://localhost:5000")
    print("📋 Features: AI Detection | GPS Location | Voice Output | Chatbot")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
