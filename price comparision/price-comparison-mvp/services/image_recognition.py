"""
Advanced Image Recognition Service using Deep Learning
Supports product classification, visual search, and feature extraction
"""
import os
import numpy as np
import cv2
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    from tensorflow.keras.preprocessing import image as keras_image
    from tensorflow.keras.models import Model
    _HAS_TF = True
except ImportError:
    _HAS_TF = False
    print("TensorFlow not available. Using fallback mode.")

import joblib
from ml_config import IMAGE_RECOGNITION, PRETRAINED_DIR
import imagehash


class ImageRecognitionService:
    """Advanced image recognition with deep learning"""
    
    def __init__(self):
        self.model = None
        self.feature_extractor = None
        self.label_encoder = None
        self.model_loaded = False
        self.image_embeddings = {}  # Cache for image embeddings
        
        if _HAS_TF:
            self.load_or_create_model()
        else:
            print("Running in fallback mode without TensorFlow")
    
    def load_or_create_model(self):
        """Load existing model or create new one from pre-trained MobileNetV2"""
        try:
            model_path = IMAGE_RECOGNITION['model_path']
            
            # Try to load existing model
            if os.path.exists(model_path):
                self.model = keras.models.load_model(model_path)
                print(f"✓ Loaded existing model from {model_path}")
            else:
                # Create feature extractor from MobileNetV2
                print("Creating new model from MobileNetV2 pre-trained weights...")
                base_model = MobileNetV2(
                    weights='imagenet',
                    include_top=False,
                    input_shape=IMAGE_RECOGNITION['input_shape'],
                    pooling='avg'
                )
                
                # Create feature extractor
                self.feature_extractor = base_model
                self.model = base_model  # Use as-is for feature extraction
                print("✓ Created MobileNetV2 feature extractor")
            
            # Load label encoder if exists
            encoder_path = IMAGE_RECOGNITION['label_encoder_path']
            if os.path.exists(encoder_path):
                self.label_encoder = joblib.load(encoder_path)
                print("✓ Loaded label encoder")
            
            self.model_loaded = True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Preprocess image for model input"""
        try:
            # Load and resize image
            img = keras_image.load_img(image_path, target_size=target_size)
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def extract_features(self, image_path):
        """Extract feature embeddings from image"""
        if not self.model_loaded or not _HAS_TF:
            return self.fallback_features(image_path)
        
        try:
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return None
            
            # Extract features
            features = self.feature_extractor.predict(img_array, verbose=0)
            return features.flatten()
        
        except Exception as e:
            print(f"Error extracting features: {e}")
            return self.fallback_features(image_path)
    
    def classify_product(self, image_path):
        """Classify product from image"""
        if not self.model_loaded:
            return self.fallback_classification(image_path)
        
        try:
            # Extract features
            features = self.extract_features(image_path)
            
            # For now, use feature-based classification
            # In production, you'd have a trained classifier on top
            category = self.classify_from_features(features, image_path)
            
            return {
                'category': category,
                'confidence': 0.85,  # Placeholder
                'features': features.tolist() if features is not None else None
            }
        
        except Exception as e:
            print(f"Error classifying product: {e}")
            return self.fallback_classification(image_path)
    
    def classify_from_features(self, features, image_path):
        """Classify based on extracted features (placeholder logic)"""
        # This is a simplified version - in production, you'd use a trained classifier
        filename = os.path.basename(image_path).lower()
        
        category_keywords = {
            'electronics': ['phone', 'laptop', 'headphone', 'camera', 'tv', 'mobile', 'computer'],
            'fashion': ['shoes', 'shirt', 'jeans', 'dress', 'bag', 'clothes', 'wear'],
            'groceries': ['milk', 'bread', 'chips', 'cola', 'noodles', 'food', 'snack'],
            'beauty': ['lipstick', 'cream', 'makeup', 'cosmetic', 'skincare'],
            'home': ['furniture', 'chair', 'table', 'bed', 'decor'],
        }
        
        for category, keywords in category_keywords.items():
            if any(kw in filename for kw in keywords):
                return category
        
        return 'general'
    
    def find_similar_images(self, query_image_path, image_database, top_k=10):
        """Find similar images using feature similarity"""
        if not self.model_loaded:
            return []
        
        try:
            # Extract query features
            query_features = self.extract_features(query_image_path)
            if query_features is None:
                return []
            
            # Calculate similarities
            similarities = []
            for img_path in image_database:
                # Get or compute features for database image
                if img_path in self.image_embeddings:
                    db_features = self.image_embeddings[img_path]
                else:
                    db_features = self.extract_features(img_path)
                    if db_features is not None:
                        self.image_embeddings[img_path] = db_features
                
                if db_features is not None:
                    # Cosine similarity
                    similarity = np.dot(query_features, db_features) / (
                        np.linalg.norm(query_features) * np.linalg.norm(db_features)
                    )
                    similarities.append((img_path, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        
        except Exception as e:
            print(f"Error finding similar images: {e}")
            return []
    
    def extract_color_palette(self, image_path, num_colors=5):
        """Extract dominant colors from image"""
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Reshape image to be a list of pixels
            pixels = img.reshape(-1, 3).astype(np.float32)
            
            # Use K-means to find dominant colors
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, palette = cv2.kmeans(
                pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
            )
            
            # Convert to integer
            palette = palette.astype(int)
            
            # Calculate percentage of each color
            _, counts = np.unique(labels, return_counts=True)
            percentages = counts / len(labels)
            
            # Create color info
            colors = []
            for i, (color, percentage) in enumerate(zip(palette, percentages)):
                colors.append({
                    'rgb': color.tolist(),
                    'hex': '#{:02x}{:02x}{:02x}'.format(*color),
                    'percentage': float(percentage)
                })
            
            return sorted(colors, key=lambda x: x['percentage'], reverse=True)
        
        except Exception as e:
            print(f"Error extracting colors: {e}")
            return []
    
    def get_image_hash(self, image_path):
        """Generate perceptual hash for image deduplication"""
        try:
            img = Image.open(image_path)
            return str(imagehash.average_hash(img))
        except Exception as e:
            print(f"Error generating image hash: {e}")
            return None
    
    def detect_image_quality(self, image_path):
        """Assess image quality (blur, brightness, etc.)"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Calculate Laplacian variance (blur detection)
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(img)
            
            # Determine quality
            quality = {
                'blur_score': float(laplacian_var),
                'is_blurry': laplacian_var < 100,  # Threshold
                'brightness': float(brightness),
                'is_too_dark': brightness < 50,
                'is_too_bright': brightness > 200,
                'overall_quality': 'good' if laplacian_var >= 100 and 50 <= brightness <= 200 else 'poor'
            }
            
            return quality
        
        except Exception as e:
            print(f"Error detecting image quality: {e}")
            return None
    
    def fallback_features(self, image_path):
        """Simple feature extraction without deep learning"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Resize to standard size
            img = cv2.resize(img, (64, 64))
            
            # Calculate color histogram
            hist_b = cv2.calcHist([img], [0], None, [8], [0, 256])
            hist_g = cv2.calcHist([img], [1], None, [8], [0, 256])
            hist_r = cv2.calcHist([img], [2], None, [8], [0, 256])
            
            # Concatenate and normalize
            features = np.concatenate([hist_b, hist_g, hist_r]).flatten()
            features = features / (features.sum() + 1e-7)
            
            return features
        
        except Exception as e:
            print(f"Error in fallback features: {e}")
            return None
    
    def fallback_classification(self, image_path):
        """Fallback classification without deep learning"""
        filename = os.path.basename(image_path).lower()
        
        # Enhanced keyword matching
        categories = {
            'electronics': ['phone', 'laptop', 'headphone', 'camera', 'tv', 'iphone', 'samsung', 'mobile'],
            'fashion': ['shoes', 'shirt', 'jeans', 'dress', 'tshirt', 'nike', 'adidas', 'clothes'],
            'groceries': ['milk', 'bread', 'chips', 'cola', 'noodles', 'amul', 'britannia'],
            'beauty': ['lipstick', 'cream', 'makeup', 'foundation', 'nykaa'],
            'home': ['furniture', 'chair', 'table', 'bed', 'sofa'],
        }
        
        for category, keywords in categories.items():
            if any(kw in filename for kw in keywords):
                return {
                    'category': category,
                    'confidence': 0.7,
                    'features': None
                }
        
        return {
            'category': 'general',
            'confidence': 0.5,
            'features': None
        }
