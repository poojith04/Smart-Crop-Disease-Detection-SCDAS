import pyttsx3
from gtts import gTTS
from datetime import datetime
from pathlib import Path

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.audio_folder = Path('static/audio')
        self.audio_folder.mkdir(parents=True, exist_ok=True)
    
    def convert_to_speech(self, text, language='en'):
        """Convert text to speech and save as audio file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"advice_{timestamp}.mp3"
            filepath = self.audio_folder / filename
            
            # Use Google Text-to-Speech for better quality
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(filepath))
            
            print(f"✅ Audio file created: {filename}")
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return None
    
    def convert_offline(self, text):
        """Offline TTS using pyttsx3 (for areas with low connectivity)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ Offline TTS Error: {e}")
            return False
