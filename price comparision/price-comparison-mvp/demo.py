#!/usr/bin/env python3
"""
Demo script to showcase Price Comparison MVP features
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def demo_text_search():
    """Demonstrate text search functionality"""
    print("=== Text Search Demo ===")
    
    # Test searches
    test_queries = ["milk", "maggi", "shoes", "jeans"]
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        try:
            response = requests.get(f"{BASE_URL}/api/search", params={"q": query})
            if response.status_code == 200:
                data = response.json()
                print(f"Found {data['count']} results:")
                for result in data['results'][:3]:  # Show top 3
                    print(f"  - {result['product_name']} | {result['platform']} | ₹{result['price']}")
                    if result.get('is_best_price'):
                        print("    ⭐ BEST PRICE!")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)

def demo_price_comparison():
    """Show price comparison across platforms"""
    print("\n=== Price Comparison Demo ===")
    
    # Search for a common product
    query = "milk"
    try:
        response = requests.get(f"{BASE_URL}/api/search", params={"q": query})
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            
            print(f"\nPrice comparison for '{query}':")
            print("-" * 50)
            
            # Group by product name
            products = {}
            for result in results:
                name = result['product_name']
                if name not in products:
                    products[name] = []
                products[name].append(result)
            
            for product_name, variants in products.items():
                print(f"\n{product_name}:")
                sorted_variants = sorted(variants, key=lambda x: x['price'])
                for variant in sorted_variants:
                    best_indicator = " ⭐ BEST" if variant.get('is_best_price') else ""
                    print(f"  {variant['platform']:12} | ₹{variant['price']:6.2f}{best_indicator}")
                
                if len(sorted_variants) > 1:
                    savings = sorted_variants[-1]['price'] - sorted_variants[0]['price']
                    print(f"  💰 Save ₹{savings:.2f} by choosing the best price!")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run the demo"""
    print("🛒 Price Comparison MVP Demo")
    print("=" * 40)
    print("Make sure the Flask app is running on http://localhost:5000")
    print()
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ Server not responding. Please start the Flask app first.")
            return
    except Exception:
        print("❌ Cannot connect to server. Please start the Flask app first.")
        return
    
    print("✅ Server is running!")
    
    # Run demos
    demo_text_search()
    demo_price_comparison()
    
    print("\n" + "=" * 40)
    print("Demo completed! Visit http://localhost:5000 to try the web interface.")

if __name__ == "__main__":
    main()