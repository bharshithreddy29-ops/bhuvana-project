"""
Live Web Scraper for E-commerce Platforms
Scrapes real-time product data from Amazon, Flipkart, and other platforms
"""
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote_plus
import random
import warnings
warnings.filterwarnings('ignore')


class LiveProductScraper:
    """Scrape live product data from e-commerce platforms"""
    
    def __init__(self):
        # User agents to rotate and avoid blocking
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        self.session = requests.Session()
        self.timeout = 10
        
    def get_headers(self):
        """Get random headers to avoid blocking"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape_amazon(self, query, max_results=10):
        """Scrape Amazon India for products"""
        products = []
        try:
            url = f"https://www.amazon.in/s?k={quote_plus(query)}"
            response = self.session.get(url, headers=self.get_headers(), timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find product cards
                items = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for item in items[:max_results]:
                    try:
                        # Extract product name
                        title_elem = item.find('h2', {'class': 'a-size-mini'}) or item.find('span', {'class': 'a-size-medium'})
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)
                        
                        # Extract price
                        price_elem = item.find('span', {'class': 'a-price-whole'})
                        if not price_elem:
                            continue
                        price_text = price_elem.get_text(strip=True).replace(',', '').replace('₹', '')
                        price = float(price_text) if price_text else 0
                        
                        # Extract image
                        img_elem = item.find('img', {'class': 's-image'})
                        image_url = img_elem['src'] if img_elem else ''
                        
                        # Extract rating (optional)
                        rating_elem = item.find('span', {'class': 'a-icon-alt'})
                        rating = rating_elem.get_text(strip=True) if rating_elem else 'N/A'
                        
                        products.append({
                            'product_name': title,
                            'brand': self.extract_brand(title),
                            'price': price,
                            'platform': 'Amazon',
                            'image_url': image_url,
                            'rating': rating,
                            'category': self.categorize_product(title)
                        })
                        
                    except Exception as e:
                        print(f"Error parsing Amazon item: {e}")
                        continue
                        
        except Exception as e:
            print(f"Amazon scraping error: {e}")
        
        return products
    
    def scrape_flipkart(self, query, max_results=10):
        """Scrape Flipkart for products"""
        products = []
        try:
            url = f"https://www.flipkart.com/search?q={quote_plus(query)}"
            response = self.session.get(url, headers=self.get_headers(), timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Flipkart uses different class names - try multiple selectors
                items = soup.find_all('div', {'class': '_1AtVbE'}) or soup.find_all('div', {'class': '_2kHMtA'})
                
                for item in items[:max_results]:
                    try:
                        # Extract product name
                        title_elem = item.find('a', {'class': 'IRpwTa'}) or item.find('div', {'class': '_4rR01T'})
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)
                        
                        # Extract price
                        price_elem = item.find('div', {'class': '_30jeq3'}) or item.find('div', {'class': '_1_WHN1'})
                        if not price_elem:
                            continue
                        price_text = price_elem.get_text(strip=True).replace(',', '').replace('₹', '')
                        price = float(price_text) if price_text else 0
                        
                        # Extract image
                        img_elem = item.find('img', {'class': '_396cs4'})
                        image_url = img_elem['src'] if img_elem else ''
                        
                        # Extract rating
                        rating_elem = item.find('div', {'class': '_3LWZlK'})
                        rating = rating_elem.get_text(strip=True) if rating_elem else 'N/A'
                        
                        products.append({
                            'product_name': title,
                            'brand': self.extract_brand(title),
                            'price': price,
                            'platform': 'Flipkart',
                            'image_url': image_url,
                            'rating': rating,
                            'category': self.categorize_product(title)
                        })
                        
                    except Exception as e:
                        print(f"Error parsing Flipkart item: {e}")
                        continue
                        
        except Exception as e:
            print(f"Flipkart scraping error: {e}")
        
        return products
    
    def scrape_myntra(self, query, max_results=10):
        """Scrape Myntra for fashion products"""
        products = []
        try:
            # Myntra requires specific handling
            url = f"https://www.myntra.com/{quote_plus(query)}"
            response = self.session.get(url, headers=self.get_headers(), timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Myntra uses complex class names
                items = soup.find_all('li', {'class': 'product-base'})
                
                for item in items[:max_results]:
                    try:
                        title_elem = item.find('h4', {'class': 'product-product'})
                        if not title_elem:
                            continue
                        title = title_elem.get_text(strip=True)
                        
                        price_elem = item.find('span', {'class': 'product-discountedPrice'})
                        if not price_elem:
                            continue
                        price_text = price_elem.get_text(strip=True).replace(',', '').replace('₹', '').replace('Rs. ', '')
                        price = float(price_text) if price_text else 0
                        
                        img_elem = item.find('img')
                        image_url = img_elem['src'] if img_elem else ''
                        
                        products.append({
                            'product_name': title,
                            'brand': self.extract_brand(title),
                            'price': price,
                            'platform': 'Myntra',
                            'image_url': image_url,
                            'rating': 'N/A',
                            'category': 'Fashion'
                        })
                        
                    except Exception as e:
                        print(f"Error parsing Myntra item: {e}")
                        continue
                        
        except Exception as e:
            print(f"Myntra scraping error: {e}")
        
        return products
    
    def search_all_platforms(self, query, max_per_platform=10):
        """Search across all platforms"""
        all_products = []
        
        print(f"🔍 Searching for '{query}' across platforms...")
        
        # Amazon
        print("  - Scraping Amazon...")
        amazon_products = self.scrape_amazon(query, max_per_platform)
        all_products.extend(amazon_products)
        time.sleep(1)  # Rate limiting
        
        # Flipkart
        print("  - Scraping Flipkart...")
        flipkart_products = self.scrape_flipkart(query, max_per_platform)
        all_products.extend(flipkart_products)
        time.sleep(1)
        
        # Myntra (for fashion items)
        if any(keyword in query.lower() for keyword in ['shoe', 'shirt', 'jeans', 'dress', 'fashion', 'clothes']):
            print("  - Scraping Myntra...")
            myntra_products = self.scrape_myntra(query, max_per_platform)
            all_products.extend(myntra_products)
            time.sleep(1)
        
        print(f"✓ Found {len(all_products)} products across platforms")
        return all_products
    
    def extract_brand(self, title):
        """Extract brand from product title"""
        # Common brands
        brands = [
            'Apple', 'Samsung', 'Nike', 'Adidas', 'Puma', 'Levi', 'Sony', 'LG',
            'Dell', 'HP', 'Lenovo', 'Asus', 'Amul', 'Nestle', 'Britannia',
            'Coca Cola', 'Pepsi', 'Lays', 'Boat', 'OnePlus', 'Realme', 'Xiaomi'
        ]
        
        title_upper = title.upper()
        for brand in brands:
            if brand.upper() in title_upper:
                return brand
        
        # Extract first word as brand
        words = title.split()
        return words[0] if words else 'Unknown'
    
    def categorize_product(self, title):
        """Categorize product based on title"""
        title_lower = title.lower()
        
        categories = {
            'Electronics': ['phone', 'mobile', 'laptop', 'computer', 'tablet', 'headphone', 'earphone', 'camera', 'tv', 'watch'],
            'Fashion': ['shoe', 'shirt', 'jeans', 'dress', 't-shirt', 'jacket', 'sneaker', 'sandal'],
            'Groceries': ['milk', 'bread', 'rice', 'oil', 'noodles', 'chips', 'snacks'],
            'Beauty': ['lipstick', 'makeup', 'cream', 'shampoo', 'perfume'],
            'Home': ['furniture', 'chair', 'table', 'bed', 'sofa'],
            'Sports': ['gym', 'fitness', 'yoga', 'sports', 'cricket', 'football']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'General'


# Test the scraper
if __name__ == "__main__":
    scraper = LiveProductScraper()
    
    # Test search
    query = "nike shoes"
    results = scraper.search_all_platforms(query, max_per_platform=5)
    
    print(f"\n📦 Results for '{query}':\n")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product['product_name']}")
        print(f"   Platform: {product['platform']}")
        print(f"   Price: ₹{product['price']}")
        print(f"   Brand: {product['brand']}")
        print()
