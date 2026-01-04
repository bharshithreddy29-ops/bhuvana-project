import os
from PIL import Image

class ImageService:
    def __init__(self):
        self.upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'images', 'uploads')

    def save_uploaded_image(self, file):
        """Save uploaded image file."""
        if not file or not file.filename:
            return None

        os.makedirs(self.upload_folder, exist_ok=True)
        filepath = os.path.join(self.upload_folder, file.filename)
        file.save(filepath)
        return filepath

    def process_image(self, image_path):
        """Basic image processing."""
        try:
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                img.thumbnail((300, 300))
                processed_path = image_path.replace('.jpg', '_processed.jpg').replace('.png', '_processed.png')
                img.save(processed_path)
                return processed_path
        except Exception:
            return image_path

    def search_by_image(self, image_path):
        """Search products based on filename keywords."""
        keywords = self.extract_keywords_from_filename(image_path)
        
        from services.text_search_service import TextSearchService
        search_service = TextSearchService()
        
        all_results = []
        for keyword in keywords:
            results = search_service.search_products(keyword)
            all_results.extend(results)
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for product in all_results:
            key = (product['product_name'], product['platform'])
            if key not in seen:
                seen.add(key)
                unique_results.append(product)
        
        return unique_results[:20]

    def extract_keywords_from_filename(self, image_path):
        """Extract keywords from filename."""
        filename = os.path.basename(image_path).lower()
        
        keyword_map = {
            'milk': ['milk', 'dairy'],
            'bread': ['bread', 'bakery'],
            'chips': ['chips', 'snacks'],
            'cola': ['cola', 'soda', 'drink'],
            'noodles': ['noodles', 'pasta'],
            'shoes': ['shoes', 'sneakers'],
            'tshirt': ['tshirt', 'shirt'],
            'jeans': ['jeans', 'pants'],
            'phone': ['phone', 'mobile', 'smartphone'],
            'laptop': ['laptop', 'computer']
        }
        
        keywords = []
        for key, words in keyword_map.items():
            if key in filename:
                keywords.extend(words)
        
        return keywords or ['product']