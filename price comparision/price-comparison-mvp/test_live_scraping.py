"""Test live scraping functionality"""
from services.live_scraper import LiveProductScraper

print("Testing Live Product Scraper...")
print("=" * 60)

scraper = LiveProductScraper()

# Test Amazon scraping
print("\n🔍 Testing Amazon scraping for 'nike shoes'...")
results = scraper.scrape_amazon('nike shoes', max_results=3)

if results:
    print(f"\n✓ Found {len(results)} products from Amazon:\n")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product['product_name'][:60]}")
        print(f"   Price: ₹{product['price']}")
        print(f"   Rating: {product['rating']}")
        print()
else:
    print("⚠ No results found (might be blocked or page structure changed)")

print("\nNote: Web scraping might be blocked by anti-bot measures.")
print("If no results, the app will fall back to local datasets.")
