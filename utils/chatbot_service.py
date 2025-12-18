import json
import random
import re
from pathlib import Path

class ChatbotService:
    def __init__(self):
        self.intents = self.load_intents()
    
    def load_intents(self):
        """Load chatbot intents and responses"""
        intents_file = Path('data/chatbot_intents.json')
        try:
            with open(intents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ chatbot_intents.json not found. Using default intents.")
            return self.get_default_intents()
        except Exception as e:
            print(f"⚠️ Error loading intents: {e}")
            return self.get_default_intents()
    
    def get_default_intents(self):
        """Default rice cultivation FAQs"""
        return {
            'intents': [
                {
                    'tag': 'greeting',
                    'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'namaste'],
                    'responses': [
                        'Namaste! How can I assist you with rice cultivation today?',
                        'Hello! I am here to help with rice farming questions.',
                        'Hi there! Ask me anything about rice crop management.'
                    ]
                },
                {
                    'tag': 'rice_varieties',
                    'patterns': ['rice variety', 'varieties', 'which rice', 'best rice', 'rice types'],
                    'responses': [
                        'Popular rice varieties in India: Basmati 370, Pusa 1121, IR-64, Swarna, Samba Mahsuri. Choose based on your region, soil type, and market demand.',
                        'For disease resistance, consider varieties like Improved Samba Mahsuri (resistant to bacterial blight) or Improved Pusa Basmati (resistant to blast).'
                    ]
                },
                {
                    'tag': 'rice_fertilizer',
                    'patterns': ['fertilizer for rice', 'rice fertiliser', 'npk for rice', 'rice nutrients'],
                    'responses': [
                        'Rice requires NPK in ratio 120:60:40 kg/ha. Apply nitrogen in 3 splits: 50% basal, 25% at tillering, 25% at panicle initiation. Add zinc sulfate (25 kg/ha) if soil is deficient.',
                        'Use organic manures like FYM (12-15 tons/ha) before planting. Apply green manure crops (dhaincha, sesbania) for better soil health.'
                    ]
                },
                {
                    'tag': 'rice_diseases',
                    'patterns': ['rice disease', 'disease in paddy', 'rice problems', 'unhealthy rice'],
                    'responses': [
                        'Common rice diseases: Blast, Bacterial Leaf Blight, Brown Spot, Tungro. Upload an image to our system for accurate diagnosis and treatment recommendations.',
                        'Preventive measures: Use certified seeds, maintain proper spacing, avoid excessive nitrogen, ensure good drainage, and practice crop rotation.'
                    ]
                },
                {
                    'tag': 'blast_disease',
                    'patterns': ['blast', 'neck blast', 'leaf blast'],
                    'responses': [
                        'Blast is caused by fungus Magnaporthe oryzae. Spray Tricyclazole 75% WP (0.6g/L) or Carbendazim 50% WP (1g/L). Apply at tillering, booting, and flowering stages.',
                        'Prevention: Use resistant varieties, avoid excessive nitrogen, practice alternate wetting and drying, and apply silicon-based fertilizers.'
                    ]
                },
                {
                    'tag': 'bacterial_blight',
                    'patterns': ['bacterial blight', 'leaf blight', 'blight disease'],
                    'responses': [
                        'Bacterial Leaf Blight is caused by Xanthomonas oryzae. Spray Copper Oxychloride (3g/L) or Streptocycline (100 ppm). Remove and destroy infected plants.',
                        'Use resistant varieties like Improved Samba Mahsuri. Maintain balanced fertilization and proper water management.'
                    ]
                }
            ]
        }
    
    def get_response(self, user_message):
        """Get chatbot response based on user input"""
        user_message = user_message.lower()
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if re.search(r'\b' + pattern + r'\b', user_message):
                    return random.choice(intent['responses'])
        
        return "I am not sure about that. Please ask about rice varieties, fertilizers, diseases, or specific problems like blast, bacterial blight, or tungro."
