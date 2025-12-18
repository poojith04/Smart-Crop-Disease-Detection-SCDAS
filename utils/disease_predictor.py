import tensorflow as tf
import numpy as np
from PIL import Image
import json
from pathlib import Path

# Custom InputLayer to handle batch_shape parameter
class CustomInputLayer(tf.keras.layers.InputLayer):
    def __init__(self, batch_shape=None, input_shape=None, **kwargs):
        if batch_shape is not None and input_shape is None:
            input_shape = batch_shape[1:]
        super().__init__(input_shape=input_shape, **kwargs)

class DiseasePredictor:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()
        self.disease_info = self.load_disease_info()
        
    def load_model(self):
        """Load the pre-trained rice disease model"""
        model_file = Path(self.model_path)
        if model_file.exists():
            try:
                # Register custom InputLayer
                custom_objects = {'InputLayer': CustomInputLayer}
                
                print("🔄 Loading rice disease detection model...")
                self.model = tf.keras.models.load_model(
                    str(model_file), 
                    custom_objects=custom_objects,
                    compile=False
                )
                print("✅ Rice disease detection model loaded successfully!")
                print(f"📊 Model input shape: {self.model.input_shape}")
                print(f"📊 Model output classes: {self.model.output_shape[-1]}")
                
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                print("⚠️ System will run with fallback predictions")
                self.model = None
        else:
            print(f"⚠️ Model not found at {self.model_path}")
            print("📁 Please place your 'crop_disease_model.h5' file in the 'models' folder")
            self.model = None
    
    def load_disease_info(self):
        """Load rice disease information and treatment details"""
        disease_file = Path('data/disease_info.json')
        try:
            with open(disease_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ disease_info.json not found. Using default information.")
            return self.get_default_disease_info()
    
    def get_default_disease_info(self):
        """Comprehensive rice disease information for all 10 classes"""
        return {
            'bacterial_leaf_blight': {
                'symptoms': 'Water-soaked lesions on leaf tips and margins, turning yellow to white. Leaves may have a wavy margin. Bacterial ooze visible in early morning.',
                'treatment': 'Apply copper-based bactericides like Copper Oxychloride (3g/L). Use antibiotics like Streptocycline (100 ppm) or Plantomycin. Remove and destroy infected plant parts. Ensure proper drainage.',
                'prevention': 'Use resistant varieties like Improved Samba Mahsuri. Apply balanced fertilizers, avoid excessive nitrogen. Maintain proper water management. Use certified disease-free seeds. Practice crop rotation.'
            },
            'bacterial_leaf_streak': {
                'symptoms': 'Narrow, dark green to brown streaks between leaf veins. Streaks may merge causing leaf to dry. Yellow to orange bacterial ooze appears on lesions.',
                'treatment': 'Spray Copper Oxychloride 50% WP (3g/L) or Streptocycline (100 ppm). Remove infected leaves. Improve field sanitation and drainage.',
                'prevention': 'Plant resistant cultivars. Avoid mechanical injury to plants. Control insect vectors. Use balanced fertilization. Avoid waterlogging conditions.'
            },
            'bacterial_panicle_blight': {
                'symptoms': 'Brown to dark brown discoloration on panicle branches. Grains become brown and chaffy. White bacterial ooze on infected panicles during humid conditions.',
                'treatment': 'Apply Copper Hydroxide or Copper Oxychloride (3g/L) at flowering stage. Use Streptocycline (500 ppm) spray. Remove infected panicles and destroy.',
                'prevention': 'Use disease-free seeds. Apply potassium fertilizers adequately. Avoid excessive nitrogen during reproductive stage. Ensure proper field drainage. Plant at optimal spacing.'
            },
            'blast': {
                'symptoms': 'Diamond-shaped lesions with gray centers and brown margins on leaves. Neck blast causes panicle to break. Collar blast causes stem rot. Fungal spores visible as gray mold.',
                'treatment': 'Apply Tricyclazole 75% WP (0.6g/L) or Isoprothiolane 40% EC (1.5ml/L). Use Carbendazim 50% WP (1g/L). Spray at tillering, booting, and flowering stages. Apply silicon amendments.',
                'prevention': 'Use resistant varieties like Improved Pusa Basmati. Avoid excessive nitrogen fertilization. Maintain optimal water levels (alternate wetting and drying). Practice clean cultivation. Use certified seeds treated with Carbendazim.'
            },
            'brown_spot': {
                'symptoms': 'Circular or oval brown spots with gray center on leaves. Spots have yellow halo. Severe infection causes leaf death. Spots also appear on leaf sheaths and grains.',
                'treatment': 'Spray Mancozeb 75% WP (2g/L) or Chlorothalonil 75% WP (2g/L). Apply Propiconazole 25% EC (1ml/L). Repeat sprays at 10-day intervals. Use silicon-based fertilizers.',
                'prevention': 'Use certified disease-free seeds. Apply balanced fertilization with potassium and silicon. Maintain proper water management. Practice crop rotation. Remove crop residues after harvest.'
            },
            'dead_heart': {
                'symptoms': 'Central shoot (dead heart) dries and turns brown, caused by stem borer. Easy to pull out dead shoot. Leaves show yellowing. In later stages, causes white ear heads (panicle damage).',
                'treatment': 'Apply Chlorantraniliprole 18.5% SC (0.3ml/L) or Cartap Hydrochloride 50% SP (2g/L). Use Fipronil 5% SC (2ml/L). Remove and destroy dead hearts. Release egg parasitoid Trichogramma japonicum.',
                'prevention': 'Remove alternate host weeds. Avoid staggered planting. Use pheromone traps (20/ha). Clip leaf tips before transplanting. Apply neem cake in nursery. Maintain 15cm water level for 3 days after transplanting.'
            },
            'downy_mildew': {
                'symptoms': 'Yellowish or pale green streaks on leaves parallel to veins. White downy fungal growth on lower leaf surface. Stunted growth and reduced tillering. Leaves may twist and curl.',
                'treatment': 'Apply Metalaxyl 8% + Mancozeb 64% WP (2.5g/L) or Dimethomorph 50% WP (1.5g/L). Use Fosetyl-Al 80% WP (2.5g/L). Spray at early disease appearance and repeat after 10 days.',
                'prevention': 'Use resistant varieties. Ensure proper field drainage. Avoid dense planting. Remove infected plants immediately. Avoid excessive nitrogen. Practice seed treatment with Metalaxyl.'
            },
            'hispa': {
                'symptoms': 'White linear streaks on leaves due to scraping of green tissues by adults. Leaf mining by grubs causing white patches. Severe damage leads to leaf drying. Young plants most affected.',
                'treatment': 'Apply Chlorpyrifos 20% EC (2.5ml/L) or Quinalphos 25% EC (2ml/L). Use Thiamethoxam 25% WG (0.2g/L) or Fipronil 5% SC (2ml/L). Spray during early morning when adults are active.',
                'prevention': 'Avoid close spacing. Remove weeds that serve as alternate hosts. Use yellow sticky traps. Apply neem oil (3%). Clip leaf tips before transplanting. Drain water from field during severe attack.'
            },
            'normal': {
                'symptoms': 'Healthy rice plant with no visible disease symptoms. Leaves are green and vigorous. Normal growth and development observed.',
                'treatment': 'No treatment required. Continue good agricultural practices to maintain plant health.',
                'prevention': 'Maintain balanced nutrition (NPK 120:60:40 kg/ha). Practice proper water management (5-7cm during critical stages). Monitor regularly for pests and diseases. Use certified quality seeds. Implement crop rotation and clean cultivation.'
            },
            'tungro': {
                'symptoms': 'Yellow to orange leaf discoloration starting from leaf tip. Stunted growth and reduced tillering. Leaves may show mottled or striped pattern. Delayed flowering. Transmitted by green leafhopper.',
                'treatment': 'No direct cure available. Remove and destroy infected plants immediately to prevent spread. Control vector (green leafhopper) using Imidacloprid 17.8% SL (0.5ml/L) or Thiamethoxam 25% WG (0.2g/L).',
                'prevention': 'Use tungro-resistant varieties. Control green leafhopper vectors with neem oil. Avoid staggered planting. Remove infected plants and ratoons. Use healthy, certified seeds. Apply light traps to monitor vector population. Practice synchronous planting.'
            }
        }
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        try:
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Resize to model's expected input size
            img = img.resize((224, 224))
            img_array = np.array(img)
            
            # Handle grayscale images
            if len(img_array.shape) == 2:
                img_array = np.stack([img_array] * 3, axis=-1)
            
            # Normalize pixel values to 0-1
            img_array = img_array.astype('float32') / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path):
        """Make prediction on the rice plant image"""
        from config import Config
        
        # Preprocess the image
        processed_image = self.preprocess_image(image_path)
        
        if processed_image is None:
            return self._get_fallback_result('blast')
        
        # Make prediction
        if self.model is not None:
            try:
                predictions = self.model.predict(processed_image, verbose=0)
                predicted_class_index = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_index]) * 100
                
                disease_name = Config.DISEASE_CLASSES[predicted_class_index]
                
                print(f"✅ Prediction: {disease_name} (Confidence: {confidence:.2f}%)")
                
                # Get disease information
                info = self.disease_info.get(disease_name, {
                    'symptoms': 'Symptoms information not available.',
                    'treatment': 'Consult with agricultural expert for specific treatment.',
                    'prevention': 'Maintain proper rice crop management practices.'
                })
                
                # Format disease name for display
                display_name = disease_name.replace('_', ' ').title()
                
                return {
                    'disease': display_name,
                    'raw_disease': disease_name,
                    'confidence': round(confidence, 2),
                    'symptoms': info.get('symptoms', 'Not available'),
                    'treatment': info.get('treatment', 'Not available'),
                    'prevention': info.get('prevention', 'Not available')
                }
                
            except Exception as e:
                print(f"❌ Prediction error: {e}")
                return self._get_fallback_result('blast')
        else:
            print("⚠️ Model not loaded. Using fallback prediction.")
            return self._get_fallback_result('blast')
    
    def _get_fallback_result(self, disease_name):
        """Return fallback result when model fails"""
        info = self.disease_info.get(disease_name, {
            'symptoms': 'Symptoms information not available.',
            'treatment': 'Consult with agricultural expert for specific treatment.',
            'prevention': 'Maintain proper rice crop management practices.'
        })
        
        display_name = disease_name.replace('_', ' ').title()
        
        return {
            'disease': display_name,
            'raw_disease': disease_name,
            'confidence': 0.0,
            'symptoms': info.get('symptoms', 'Not available'),
            'treatment': info.get('treatment', 'Not available'),
            'prevention': info.get('prevention', 'Not available')
        }
