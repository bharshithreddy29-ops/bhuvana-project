class APISource:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def load_products(self, platform):
        """Placeholder: return empty list for API-backed source in MVP."""
        return []

    def search_products(self, query, platform=None):
        """Placeholder search for API-backed source: returns empty list."""
        return []

    def get_platforms(self):
        return ['blinkit', 'zepto', 'instamart', 'bigbasket', 'flipkart', 'amazon', 'ajio', 'myntra', 'meesho', 'shopsy', 'nykaa']
