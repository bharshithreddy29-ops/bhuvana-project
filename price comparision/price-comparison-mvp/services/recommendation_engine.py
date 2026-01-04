"""
Recommendation Engine Service
Provides personalized product recommendations using collaborative and content-based filtering
"""
import numpy as np
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler
    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False
    print("scikit-learn not available. Using basic recommendations.")


class RecommendationEngine:
    """ML-powered product recommendation system"""
    
    def __init__(self):
        self.user_interactions = defaultdict(list)  # user_id -> list of product interactions
        self.product_features = {}  # product_id -> feature vector
        self.user_preferences = defaultdict(dict)  # user_id -> preferences
        self.item_similarity_matrix = None
        self.products_catalog = []
        
        if _HAS_SKLEARN:
            self.tfidf_vectorizer = TfidfVectorizer(max_features=100)
            self.scaler = StandardScaler()
        else:
            self.tfidf_vectorizer = None
            self.scaler = None
    
    def add_interaction(self, user_id, product, interaction_type='view', weight=1.0):
        """Record user interaction with a product"""
        self.user_interactions[user_id].append({
            'product': product,
            'type': interaction_type,  # view, search, click, wishlist
            'weight': weight,
            'timestamp': np.datetime64('now')
        })
        
        # Update user preferences
        self._update_user_preferences(user_id, product, weight)
    
    def _update_user_preferences(self, user_id, product, weight):
        """Update user preference profile"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'categories': Counter(),
                'brands': Counter(),
                'price_range': {'min': float('inf'), 'max': 0},
                'platforms': Counter()
            }
        
        prefs = self.user_preferences[user_id]
        
        # Update category preference
        category = product.get('category', 'general')
        prefs['categories'][category] += weight
        
        # Update brand preference
        brand = product.get('brand', '')
        if brand:
            prefs['brands'][brand] += weight
        
        # Update price range
        price = product.get('price', 0)
        if price > 0:
            prefs['price_range']['min'] = min(prefs['price_range']['min'], price)
            prefs['price_range']['max'] = max(prefs['price_range']['max'], price)
        
        # Update platform preference
        platform = product.get('platform', '')
        if platform:
            prefs['platforms'][platform] += weight
    
    def build_item_features(self, products):
        """Build feature vectors for products"""
        self.products_catalog = products
        
        if not _HAS_SKLEARN or not products:
            return
        
        try:
            # Create text representations
            product_texts = []
            for product in products:
                text = f"{product.get('product_name', '')} {product.get('brand', '')} {product.get('category', '')}"
                product_texts.append(text)
            
            # Create TF-IDF features
            tfidf_features = self.tfidf_vectorizer.fit_transform(product_texts)
            
            # Store features
            for i, product in enumerate(products):
                product_id = self._get_product_id(product)
                self.product_features[product_id] = tfidf_features[i].toarray().flatten()
            
            print(f"Built features for {len(products)} products")
        
        except Exception as e:
            print(f"Error building item features: {e}")
    
    def _get_product_id(self, product):
        """Generate unique product ID"""
        return f"{product.get('product_name', '')}_{product.get('platform', '')}"
    
    def compute_item_similarity(self):
        """Compute item-item similarity matrix"""
        if not self.product_features or not _HAS_SKLEARN:
            return
        
        try:
            # Stack feature vectors
            product_ids = list(self.product_features.keys())
            feature_matrix = np.vstack([self.product_features[pid] for pid in product_ids])
            
            # Compute cosine similarity
            similarity_matrix = cosine_similarity(feature_matrix)
            
            # Store as dictionary for easy lookup
            self.item_similarity_matrix = {}
            for i, pid1 in enumerate(product_ids):
                self.item_similarity_matrix[pid1] = {}
                for j, pid2 in enumerate(product_ids):
                    if i != j:
                        self.item_similarity_matrix[pid1][pid2] = similarity_matrix[i][j]
            
            print(f"Computed similarity for {len(product_ids)} products")
        
        except Exception as e:
            print(f"Error computing similarity: {e}")
    
    def get_similar_products(self, product, top_k=10):
        """Find similar products (content-based)"""
        product_id = self._get_product_id(product)
        
        if self.item_similarity_matrix and product_id in self.item_similarity_matrix:
            # Get similarities
            similarities = self.item_similarity_matrix[product_id]
            
            # Sort by similarity
            sorted_items = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
            
            # Get top K similar products
            similar_products = []
            for similar_id, score in sorted_items[:top_k]:
                # Find product in catalog
                for p in self.products_catalog:
                    if self._get_product_id(p) == similar_id:
                        p_copy = p.copy()
                        p_copy['similarity_score'] = float(score)
                        similar_products.append(p_copy)
                        break
            
            return similar_products
        else:
            # Fallback: simple category-based similarity
            return self._simple_similar_products(product, top_k)
    
    def _simple_similar_products(self, product, top_k=10):
        """Simple similarity based on category and price"""
        similar = []
        product_category = product.get('category', '')
        product_price = product.get('price', 0)
        product_name = product.get('product_name', '')
        
        for p in self.products_catalog:
            # Skip same product
            if p.get('product_name') == product_name and p.get('platform') == product.get('platform'):
                continue
            
            score = 0
            
            # Same category
            if p.get('category') == product_category:
                score += 0.5
            
            # Similar price (within 20%)
            if product_price > 0:
                price_diff = abs(p.get('price', 0) - product_price) / product_price
                if price_diff < 0.2:
                    score += 0.3
            
            # Same brand
            if p.get('brand') == product.get('brand'):
                score += 0.2
            
            if score > 0:
                p_copy = p.copy()
                p_copy['similarity_score'] = score
                similar.append(p_copy)
        
        # Sort and return top K
        similar.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar[:top_k]
    
    def get_personalized_recommendations(self, user_id, top_k=20):
        """Get personalized recommendations for user (collaborative + content-based)"""
        if user_id not in self.user_preferences:
            # Cold start: return popular/trending products
            return self.get_trending_products(top_k)
        
        prefs = self.user_preferences[user_id]
        recommendations = []
        
        # Get user's preferred categories
        top_categories = [cat for cat, _ in prefs['categories'].most_common(3)]
        
        # Get user's preferred brands
        top_brands = [brand for brand, _ in prefs['brands'].most_common(3)]
        
        # Score products
        for product in self.products_catalog:
            score = 0
            
            # Category match
            if product.get('category') in top_categories:
                score += 3.0
            
            # Brand match
            if product.get('brand') in top_brands:
                score += 2.0
            
            # Price range match
            price = product.get('price', 0)
            if price > 0:
                price_min = prefs['price_range'].get('min', 0)
                price_max = prefs['price_range'].get('max', float('inf'))
                
                # Prefer products in user's price range
                if price_min <= price <= price_max * 1.2:
                    score += 1.5
            
            # Platform preference
            if product.get('platform') in prefs['platforms']:
                score += 0.5
            
            if score > 0:
                product_copy = product.copy()
                product_copy['recommendation_score'] = score
                recommendations.append(product_copy)
        
        # Sort by score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        # Return top K
        return recommendations[:top_k]
    
    def get_trending_products(self, top_k=20):
        """Get trending products (for cold start)"""
        # In production, this would use actual interaction data
        # For now, return random selection with good variety
        
        if not self.products_catalog:
            return []
        
        # Get diverse products from different categories
        trending = []
        seen_categories = set()
        
        # First pass: one from each category
        for product in self.products_catalog:
            category = product.get('category', 'general')
            if category not in seen_categories:
                product_copy = product.copy()
                product_copy['trending_score'] = 1.0
                trending.append(product_copy)
                seen_categories.add(category)
        
        # Fill remaining slots
        remaining = top_k - len(trending)
        if remaining > 0 and len(self.products_catalog) > len(trending):
            import random
            additional = random.sample(
                [p for p in self.products_catalog if p not in trending],
                min(remaining, len(self.products_catalog) - len(trending))
            )
            for product in additional:
                product_copy = product.copy()
                product_copy['trending_score'] = 0.5
                trending.append(product_copy)
        
        return trending[:top_k]
    
    def get_alternative_products(self, product, top_k=10):
        """Get alternative/substitute products"""
        # Similar products from different platforms
        similar = self.get_similar_products(product, top_k * 3)
        
        # Filter to different platforms
        current_platform = product.get('platform')
        alternatives = [
            p for p in similar 
            if p.get('platform') != current_platform
        ]
        
        return alternatives[:top_k]
    
    def get_cheaper_alternatives(self, product, top_k=10):
        """Find cheaper alternatives to a product"""
        similar = self.get_similar_products(product, top_k * 3)
        current_price = product.get('price', 0)
        
        # Filter cheaper products
        cheaper = [
            p for p in similar 
            if p.get('price', float('inf')) < current_price
        ]
        
        # Sort by price
        cheaper.sort(key=lambda x: x.get('price', 0))
        
        return cheaper[:top_k]
    
    def get_bundle_recommendations(self, product, top_k=5):
        """Recommend products that go well together (frequently bought together)"""
        # In production, this would use association rules mining
        # For now, recommend from complementary categories
        
        category_complements = {
            'electronics': ['accessories', 'cables', 'cases'],
            'fashion': ['accessories', 'footwear'],
            'groceries': ['beverages', 'snacks'],
            'beauty': ['skincare', 'makeup'],
        }
        
        product_category = product.get('category', '').lower()
        complementary_categories = category_complements.get(product_category, [])
        
        bundles = []
        for p in self.products_catalog:
            p_category = p.get('category', '').lower()
            if p_category in complementary_categories or any(comp in p_category for comp in complementary_categories):
                bundles.append(p)
        
        return bundles[:top_k]
