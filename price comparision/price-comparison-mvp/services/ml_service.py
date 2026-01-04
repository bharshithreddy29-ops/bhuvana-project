import os
import numpy as np
import cv2
from PIL import Image
import joblib
try:
    # Importing tensorflow/keras can be heavy and may not be available in dev environments.
    from tensorflow.keras.models import load_model  # type: ignore
    from tensorflow.keras.preprocessing.image import img_to_array  # type: ignore
    _HAS_TF = True
except Exception:
    load_model = None
    img_to_array = None
    _HAS_TF = False
import warnings
warnings.filterwarnings('ignore')

class MLService:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.model_loaded = False
        self.load_model()

    def load_model(self):
        """Load the trained ML model and label encoder."""
        try:
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'image_classifier.h5')
            encoder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'label_encoder.pkl')

            if not _HAS_TF:
                print("TensorFlow/Keras not available; using fallback classification")
                self.model = None
                self.label_encoder = None
                self.model_loaded = False
                return

            if os.path.exists(model_path):
                self.model = load_model(model_path)
                print("ML model loaded successfully")
            else:
                print("ML model not found, using fallback classification")
                self.model = None

            if os.path.exists(encoder_path):
                self.label_encoder = joblib.load(encoder_path)
                print("Label encoder loaded successfully")
            else:
                print("Label encoder not found, using fallback classification")
                self.label_encoder = None

            self.model_loaded = self.model is not None and self.label_encoder is not None

        except Exception as e:
            print(f"Error loading ML model: {e}")
            self.model_loaded = False

    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Preprocess image for model prediction."""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")

            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Resize image
            image = cv2.resize(image, target_size)

            # Convert to array and normalize
            # Fall back to numpy conversion if keras img_to_array is not available
            if img_to_array is not None:
                image = img_to_array(image)
            else:
                image = image.astype('float32')
            image = image / 255.0

            # Add batch dimension
            image = np.expand_dims(image, axis=0)

            return image

        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def predict_product(self, image_path, confidence_threshold=0.5):
        """Predict product category from image."""
        if not self.model_loaded:
            # Fallback classification based on filename
            return self.fallback_classification(image_path)

        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return self.fallback_classification(image_path)

            # Make prediction
            predictions = self.model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_idx]

            # Check confidence threshold
            if confidence < confidence_threshold:
                print(f"Low confidence ({confidence:.2f}), using fallback classification")
                return self.fallback_classification(image_path)

            # Decode prediction
            predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]

            print(f"ML Prediction: {predicted_class} (confidence: {confidence:.2f})")
            return predicted_class

        except Exception as e:
            print(f"Error during prediction: {e}")
            return self.fallback_classification(image_path)

    def fallback_classification(self, image_path):
        """Fallback classification based on filename and basic image features."""
        filename = os.path.basename(image_path).lower()
        
        # Enhanced keyword-based classification
        classification_map = {
            # Electronics
            'phone': ['iphone', 'samsung', 'mobile', 'smartphone', 'galaxy'],
            'laptop': ['macbook', 'dell', 'hp', 'lenovo', 'laptop', 'computer'],
            'headphones': ['headphone', 'earphone', 'airpods', 'sony', 'beats'],
            'tv': ['television', 'smart tv', 'led', 'oled', 'lg', 'samsung tv'],
            'camera': ['camera', 'canon', 'nikon', 'dslr', 'photography'],
            
            # Fashion
            'shoes': ['shoe', 'sneaker', 'nike', 'adidas', 'boot', 'sandal'],
            'tshirt': ['tshirt', 't-shirt', 'shirt', 'top', 'clothing'],
            'jeans': ['jean', 'pant', 'trouser', 'denim', 'levi'],
            'dress': ['dress', 'gown', 'frock', 'outfit'],
            
            # Home & Kitchen
            'furniture': ['chair', 'table', 'bed', 'sofa', 'furniture'],
            'appliances': ['fridge', 'washing', 'microwave', 'oven', 'mixer'],
            
            # Beauty
            'makeup': ['lipstick', 'foundation', 'mascara', 'makeup'],
            'skincare': ['cream', 'lotion', 'serum', 'facewash', 'moisturizer'],
            
            # Sports
            'sports': ['ball', 'bat', 'racket', 'fitness', 'gym', 'exercise'],
            
            # Groceries
            'milk': ['milk', 'dairy'],
            'bread': ['bread', 'bakery'],
            'chips': ['chips', 'snacks'],
            'cola': ['cola', 'soda', 'drink'],
            'noodles': ['noodles', 'pasta', 'maggi']
        }
        
        # Check filename against all categories
        for category, keywords in classification_map.items():
            if any(keyword in filename for keyword in keywords):
                return category
        
        # If no match found, return general
        return 'general'

    def extract_image_features(self, image_path):
        """Extract basic features from image for fallback classification."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate basic statistics
            features = {
                'mean_intensity': np.mean(gray),
                'std_intensity': np.std(gray),
                'aspect_ratio': image.shape[1] / image.shape[0] if image.shape[0] > 0 else 1
            }

            return features

        except Exception as e:
            print(f"Error extracting features: {e}")
            return None

    def train_model_placeholder(self, training_data_path):
        """Placeholder for model training (would be implemented with actual training data)."""
        print("Model training placeholder - implement with actual training data")
        # This would include:
        # 1. Load training images
        # 2. Preprocess images
        # 3. Split data
        # 4. Train CNN model
        # 5. Save model and label encoder
        pass
