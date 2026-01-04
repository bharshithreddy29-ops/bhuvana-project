import os
from PIL import Image
import io
from services.ml_service import MLService

class ImageService:
    def __init__(self):
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images', 'uploads')
        self.ml_service = MLService()

    def save_uploaded_image(self, file):
        """Save uploaded image file."""
        if not file:
            return None

        filename = file.filename
        if not filename:
            return None

        # Ensure upload directory exists
        os.makedirs(self.upload_folder, exist_ok=True)

        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath

    def process_image(self, image_path):
        """Basic image processing with ML enhancement."""
        try:
            with Image.open(image_path) as img:
                # Basic processing: resize and convert to RGB
                img = img.convert('RGB')
                img.thumbnail((300, 300))

                # Save processed image
                processed_path = image_path.replace('.jpg', '_processed.jpg').replace('.png', '_processed.png')
                img.save(processed_path)
                return processed_path
        except Exception as e:
            print(f"Image processing error: {e}")
            return image_path

    def extract_keywords_from_image(self, image_path):
        """Extract keywords from image using ML model."""
        # Use ML model for prediction
        predicted_category = self.ml_service.predict_product(image_path)

        # Map predicted category to keywords
        keyword_map = {
            'milk': ['milk', 'dairy', 'beverage'],
            'bread': ['bread', 'bakery', 'wheat'],
            'chips': ['chips', 'snacks', 'potato'],
            'cola': ['cola', 'soda', 'drink', 'beverage'],
            'noodles': ['noodles', 'pasta', 'instant'],
            'shoes': ['shoes', 'sneakers', 'footwear'],
            'tshirt': ['tshirt', 'shirt', 'clothing'],
            'jeans': ['jeans', 'pants', 'denim'],
            'dress': ['dress', 'clothing', 'fashion'],
            'general': ['product', 'item']
        }

        keywords = keyword_map.get(predicted_category, ['general'])

        # Fallback to filename-based extraction if needed
        filename_keywords = self.extract_keywords_from_filename(image_path)
        keywords.extend(filename_keywords)

        return list(set(keywords))  # Remove duplicates

    def extract_keywords_from_filename(self, image_path):
        """Extract keywords from filename (fallback method)."""
        filename = os.path.basename(image_path).lower()

        # Simple keyword mapping
        keyword_map = {
            'milk': ['milk', 'dairy'],
            'bread': ['bread', 'bakery'],
            'chips': ['chips', 'snacks'],
            'cola': ['cola', 'soda', 'drink'],
            'noodles': ['noodles', 'pasta'],
            'shoes': ['shoes', 'sneakers'],
            'tshirt': ['tshirt', 'shirt'],
            'jeans': ['jeans', 'pants'],
            'dress': ['dress', 'clothing']
        }

        keywords = []
        for key, words in keyword_map.items():
            if key in filename:
                keywords.extend(words)

        return keywords

    def search_by_image(self, image_path):
        """Search products based on image analysis using ML."""
        keywords = self.extract_keywords_from_image(image_path)

        # Enhanced image-based search with better matching
        from services.text_search_service import TextSearchService
        search_service = TextSearchService()

        all_results = []
        
        # Primary search with extracted keywords
        for keyword in keywords:
            results = search_service.search_products(keyword)
            all_results.extend(results)
        
        # If no results, try broader searches
        if not all_results:
            broad_keywords = ['phone', 'shoes', 'shirt', 'jeans', 'laptop', 'headphones', 'watch', 'bag']
            for keyword in broad_keywords:
                results = search_service.search_products(keyword)
                all_results.extend(results)

        # Remove duplicates and sort by relevance
        seen = set()
        unique_results = []
        for product in all_results:
            key = (product['product_name'], product['platform'])
            if key not in seen:
                seen.add(key)
                # Add relevance score based on keyword match
                product['relevance'] = self.calculate_relevance(product, keywords)
                unique_results.append(product)

        # Sort by relevance and limit results
        unique_results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        return unique_results[:20]

    def calculate_relevance(self, product, keywords):
        """Calculate relevance score for a product based on keywords."""
        score = 0
        product_name = product['product_name'].lower()
        brand = product['brand'].lower()

        for keyword in keywords:
            if keyword in product_name:
                score += 3  # Higher weight for product name match
            if keyword in brand:
                score += 2  # Medium weight for brand match

        return score
