import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # File-based storage configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    DATA_SOURCE = 'dataset'  # File-based dataset storage
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'image_classifier.pkl')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
