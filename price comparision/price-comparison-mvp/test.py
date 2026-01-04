#!/usr/bin/env python3
"""
Test script for Price Comparison MVP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.text_search_service import TextSearchService
from services.price_compare_service import PriceCompareService
from services.image_service import ImageService
from data_sources.source_manager import SourceManager

def test_text_search():
    """Test text search functionality"""
    print("Testing Text Search Service...")
    
    search_service = TextSearchService()
    
    # Test searches
    test_queries = ["milk", "maggi", "shoes", "bread"]
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        results = search_service.search_products(query)
        print(f"Found {len(results)} results")
        
        for result in results[:2]:  # Show first 2 results
            print(f"  - {result['product_name']} | {result['platform']} | Rs.{result['price']}")
    
    print("Text search test completed")

def test_price_comparison():
    """Test price comparison service"""
    print("\nTesting Price Comparison Service...")
    
    search_service = TextSearchService()
    compare_service = PriceCompareService()
    
    # Get some products
    results = search_service.search_products("milk")
    
    if results:
        compared = compare_service.compare_prices(results)
        print(f"Compared {len(compared)} products")
        
        # Show best prices
        best_prices = [p for p in compared if p.get('is_best_price')]
        print(f"Found {len(best_prices)} best price products")
        
        for product in best_prices[:2]:
            print(f"  * {product['product_name']} | {product['platform']} | Rs.{product['price']}")
    
    print("Price comparison test completed")

def test_data_sources():
    """Test data source manager"""
    print("\nTesting Data Sources...")
    
    source_manager = SourceManager()
    platforms = source_manager.get_all_platforms()
    print(f"Available platforms: {platforms}")
    
    # Test loading from each platform
    for platform in platforms[:3]:  # Test first 3 platforms
        products = source_manager.load_products(platform)
        print(f"{platform}: {len(products)} products")
    
    print("Data sources test completed")

def test_image_service():
    """Test image service (basic functionality)"""
    print("\nTesting Image Service...")
    
    image_service = ImageService()
    
    # Test keyword extraction from filename
    test_files = ["milk_product.jpg", "nike_shoes.png", "maggi_noodles.jpg"]
    
    for filename in test_files:
        keywords = image_service.extract_keywords_from_filename(filename)
        print(f"{filename}: {keywords}")
    
    print("Image service test completed")

def main():
    """Run all tests"""
    print("Running Price Comparison MVP Tests")
    print("=" * 50)
    
    try:
        test_data_sources()
        test_text_search()
        test_price_comparison()
        test_image_service()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("The application is ready to run.")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()