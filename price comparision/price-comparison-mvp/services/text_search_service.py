"""
Enhanced Text Search Service with Live Scraping Support
Searches products using both local datasets and live web scraping
"""
import os
from data_sources.source_manager import SourceManager


class TextSearchService:
    def __init__(self, use_live_scraping=True):
        """
        Initialize search service
        
        Args:
            use_live_scraping: If True, scrape live data from e-commerce sites
        """
        data_source = os.environ.get('DATA_SOURCE', 'dataset')
        self.source_manager = SourceManager(data_source=data_source)
        self.use_live_scraping = use_live_scraping
        
        # Initialize live scraper if enabled
        self.live_scraper = None
        if use_live_scraping:
            try:
                from services.live_scraper import LiveProductScraper
                self.live_scraper = LiveProductScraper()
                print("✓ Live scraping enabled")
            except ImportError as e:
                print(f"⚠ Live scraping not available: {e}")
                self.use_live_scraping = False

    def search_products(self, query, platform=None, use_live=None):
        """
        Search products using configured data source and/or live scraping
        
        Args:
            query: Search query string
            platform: Specific platform to search (optional)
            use_live: Override to force live/dataset search
        
        Returns:
            List of product dictionaries
        """
        if not query:
            return []
        
        # Determine whether to use live scraping
        should_use_live = use_live if use_live is not None else self.use_live_scraping
        
        results = []
        
        # Try live scraping first if enabled
        if should_use_live and self.live_scraper:
            try:
                print(f"🔍 Searching live data for: '{query}'")
                live_results = self.live_scraper.search_all_platforms(query, max_per_platform=10)
                results.extend(live_results)
                print(f"✓ Found {len(live_results)} live products")
            except Exception as e:
                print(f"⚠ Live scraping failed: {e}")
                print("  Falling back to local datasets...")
        
        # If no live results or live scraping disabled, use local datasets
        if not results:
            try:
                dataset_results = self.source_manager.search_products(query, platform=platform)
                results.extend(dataset_results or [])
                if results:
                    print(f"✓ Found {len(results)} products in local datasets")
            except Exception as e:
                print(f"⚠ Dataset search error: {e}")
        
        return results or []
    
    def search_live_only(self, query):
        """Search only live data from e-commerce platforms"""
        if not self.live_scraper:
            print("⚠ Live scraping not available")
            return []
        
        try:
            return self.live_scraper.search_all_platforms(query, max_per_platform=10)
        except Exception as e:
            print(f"Live search error: {e}")
            return []
    
    def search_datasets_only(self, query, platform=None):
        """Search only local datasets"""
        try:
            return self.source_manager.search_products(query, platform=platform) or []
        except Exception as e:
            print(f"Dataset search error: {e}")
            return []
