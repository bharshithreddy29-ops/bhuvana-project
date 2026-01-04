from data_sources.dataset_source import DatasetSource
from data_sources.api_source import APISource

class SourceManager:
    def __init__(self, data_source='dataset', api_key=None):
        self.data_source = data_source
        if data_source == 'dataset':
            self.source = DatasetSource()
        elif data_source == 'api':
            self.source = APISource(api_key)
        else:
            raise ValueError("Invalid data source. Choose 'dataset' or 'api'.")

    def search_products(self, query, platform=None):
        """Unified method to search products regardless of source."""
        return self.source.search_products(query, platform)

    def load_products(self, platform):
        """Unified method to load products regardless of source."""
        return self.source.load_products(platform)

    def get_all_platforms(self):
        """Get list of all available platforms."""
        if hasattr(self.source, 'get_platforms'):
            return self.source.get_platforms()
        return ['blinkit', 'zepto', 'instamart', 'bigbasket', 'flipkart', 'amazon', 'ajio', 'myntra', 'meesho', 'shopsy', 'nykaa']
    
    def get_all_products(self):
        """Get all products from all platforms."""
        all_products = []
        platforms = self.get_all_platforms()
        
        for platform in platforms:
            try:
                products = self.load_products(platform)
                # Add platform info to each product if not already present
                for product in products:
                    if 'platform' not in product:
                        product['platform'] = platform
                all_products.extend(products)
            except Exception as e:
                # Silently skip platforms with no data
                pass
        
        return all_products
