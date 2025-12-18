class Config:
    SECRET_KEY = 'rice-disease-detection-secret-key-2025'
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    MODEL_PATH = 'models/crop_disease_model.h5'  # Your trained model
    
    # Rice crop disease classes (10 classes based on your trained model)
    DISEASE_CLASSES = [
        'bacterial_leaf_blight',
        'bacterial_leaf_streak',
        'bacterial_panicle_blight',
        'blast',
        'brown_spot',
        'dead_heart',
        'downy_mildew',
        'hispa',
        'normal',
        'tungro'
    ]
