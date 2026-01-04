import json
import os

class DatasetSource:
    def __init__(self):
        self.datasets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasets')

    def load_products(self, platform):
        """Load products from JSON dataset for a specific platform."""
        file_path = os.path.join(self.datasets_dir, f'{platform}_products.json')
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            return json.load(f)

    def search_products(self, query, platform=None):
        """Search products by name across all or specific platform."""
        results = []
        query_lower = query.lower().strip()
        
        # All available dataset files
        all_platforms = [
            'amazon', 'flipkart', 'myntra', 'ajio', 'blinkit', 'zepto', 
            'instamart', 'bigbasket', 'meesho', 'shopsy', 'nykaa',
            'electronics_amazon', 'fashion_myntra', 'home_kitchen', 
            'beauty_nykaa', 'sports_fitness'
        ]
        
        platforms = [platform] if platform else all_platforms
        
        for plat in platforms:
            try:
                products = self.load_products(plat)
                for product in products:
                    product_name = product.get('product_name', '').lower()
                    brand = product.get('brand', '').lower()
                    category = product.get('category', '').lower()
                    
                    # More flexible search - check name, brand, and category
                    if (query_lower in product_name or 
                        query_lower in brand or 
                        query_lower in category or
                        any(word in product_name for word in query_lower.split()) or
                        any(word in brand for word in query_lower.split())):
                        
                        product['platform'] = plat
                        results.append(product)
            except Exception as e:
                # Skip files that don't exist or have errors
                continue
                
        return results
