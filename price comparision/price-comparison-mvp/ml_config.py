"""
ML Configuration for Price Comparison AI/ML Project
Contains paths, hyperparameters, and settings for all ML models
"""
import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
PRETRAINED_DIR = os.path.join(MODELS_DIR, 'pretrained')
TRAINING_DATA_DIR = os.path.join(BASE_DIR, 'training_data')
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

# Ensure directories exist
os.makedirs(PRETRAINED_DIR, exist_ok=True)
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

# Image Recognition Configuration
IMAGE_RECOGNITION = {
    'model_path': os.path.join(PRETRAINED_DIR, 'mobilenet_v2_product_classifier.h5'),
    'feature_extractor_path': os.path.join(PRETRAINED_DIR, 'feature_extractor.h5'),
    'label_encoder_path': os.path.join(PRETRAINED_DIR, 'label_encoder.pkl'),
    'input_shape': (224, 224, 3),
    'confidence_threshold': 0.5,
    'top_k_predictions': 5,
    'batch_size': 32,
    'use_pretrained': True,  # Use MobileNetV2 pre-trained on ImageNet
}

# Price Prediction Configuration
PRICE_PREDICTION = {
    'model_path': os.path.join(PRETRAINED_DIR, 'price_predictor.pkl'),
    'scaler_path': os.path.join(PRETRAINED_DIR, 'price_scaler.pkl'),
    'lookback_days': 30,
    'forecast_days': 7,
    'confidence_interval': 0.95,
    'anomaly_threshold': 2.5,  # Standard deviations
}

# Recommendation Engine Configuration
RECOMMENDATIONS = {
    'model_path': os.path.join(PRETRAINED_DIR, 'recommendation_model.pkl'),
    'user_similarity_path': os.path.join(PRETRAINED_DIR, 'user_similarity.pkl'),
    'item_similarity_path': os.path.join(PRETRAINED_DIR, 'item_similarity.pkl'),
    'min_recommendations': 5,
    'max_recommendations': 20,
    'similarity_threshold': 0.3,
    'use_hybrid': True,  # Combine collaborative and content-based
}

# NLP Configuration
NLP = {
    'word_embeddings_path': os.path.join(PRETRAINED_DIR, 'word_embeddings.bin'),
    'vocabulary_path': os.path.join(PRETRAINED_DIR, 'vocabulary.pkl'),
    'tfidf_vectorizer_path': os.path.join(PRETRAINED_DIR, 'tfidf_vectorizer.pkl'),
    'max_query_length': 100,
    'embedding_dim': 300,
    'use_spell_correction': True,
    'language': 'english',
}

# Computer Vision Configuration
COMPUTER_VISION = {
    'logo_detector_path': os.path.join(PRETRAINED_DIR, 'logo_detector.h5'),
    'ocr_language': 'eng',
    'min_logo_confidence': 0.7,
    'enable_ocr': True,
    'color_palette_size': 5,  # Number of dominant colors to extract
}

# Training Configuration
TRAINING = {
    'epochs': 50,
    'batch_size': 32,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'early_stopping_patience': 5,
    'reduce_lr_patience': 3,
    'save_best_only': True,
}

# Inference Configuration
INFERENCE = {
    'use_gpu': False,  # Set to True if GPU is available
    'max_batch_size': 64,
    'cache_predictions': True,
    'cache_ttl': 3600,  # Cache time-to-live in seconds
}

# Data Augmentation Configuration (for training)
DATA_AUGMENTATION = {
    'rotation_range': 20,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'horizontal_flip': True,
    'zoom_range': 0.2,
    'fill_mode': 'nearest',
}

# Product Categories
PRODUCT_CATEGORIES = [
    'Electronics',
    'Fashion',
    'Home & Kitchen',
    'Beauty & Personal Care',
    'Sports & Fitness',
    'Groceries',
    'Books',
    'Toys',
    'Automotive',
    'Health',
]

# E-commerce Platforms
PLATFORMS = [
    'Amazon',
    'Flipkart',
    'Myntra',
    'Nykaa',
    'Blinkit',
    'Zepto',
    'BigBasket',
    'Instamart',
    'Meesho',
    'Ajio',
    'Shopsy',
]

# Logging Configuration
LOGGING = {
    'enabled': True,
    'log_predictions': True,
    'log_performance': True,
    'log_file': os.path.join(BASE_DIR, 'logs', 'ml_service.log'),
}
