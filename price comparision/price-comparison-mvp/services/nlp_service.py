"""
Natural Language Processing Service for Smart Search
Handles query understanding, spell correction, semantic search, and autocomplete
"""
import os
import re
import string
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from nltk.metrics.distance import edit_distance
    _HAS_NLTK = True
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
except ImportError:
    _HAS_NLTK = False
    print("NLTK not available. Using basic text processing.")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib


class NLPService:
    """Advanced NLP for intelligent search"""
    
    def __init__(self):
        self.lemmatizer = None
        self.stop_words = set()
        self.tfidf_vectorizer = None
        self.vocabulary = {}
        self.product_names = []  # For autocomplete
        
        if _HAS_NLTK:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        
        self.common_brands = {
            'apple', 'samsung', 'nike', 'adidas', 'puma', 'sony', 'lg',
            'dell', 'hp', 'lenovo', 'amul', 'britannia', 'nestle', 'nykaa'
        }
        
        self.category_synonyms = {
            'phone': ['mobile', 'smartphone', 'cellphone', 'handset'],
            'laptop': ['notebook', 'computer', 'pc'],
            'shoes': ['footwear', 'sneakers', 'boots', 'sandals'],
            'shirt': ['tshirt', 't-shirt', 'top', 'tee'],
            'milk': ['dairy', 'beverage'],
            'headphones': ['earphones', 'headset', 'earbuds'],
        }
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters except hyphens (for product names)
        text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        text = self.preprocess_text(text)
        
        if _HAS_NLTK:
            tokens = word_tokenize(text)
        else:
            tokens = text.split()
        
        return tokens
    
    def lemmatize(self, word):
        """Get lemma (base form) of word"""
        if self.lemmatizer:
            return self.lemmatizer.lemmatize(word)
        return word
    
    def remove_stopwords(self, tokens):
        """Remove common stopwords"""
        if self.stop_words:
            return [t for t in tokens if t not in self.stop_words]
        return tokens
    
    def expand_query(self, query):
        """Expand query with synonyms and related terms"""
        tokens = self.tokenize(query)
        expanded_tokens = set(tokens)
        
        # Add synonyms
        for token in tokens:
            if token in self.category_synonyms:
                expanded_tokens.update(self.category_synonyms[token])
        
        return list(expanded_tokens)
    
    def spell_correct(self, word):
        """Correct spelling using edit distance"""
        if not self.vocabulary:
            return word
        
        # If word is correct, return it
        if word in self.vocabulary:
            return word
        
        # Find closest match
        min_distance = float('inf')
        best_match = word
        
        for vocab_word in self.vocabulary:
            if _HAS_NLTK:
                dist = edit_distance(word, vocab_word)
            else:
                dist = self.simple_edit_distance(word, vocab_word)
            
            if dist < min_distance:
                min_distance = dist
                best_match = vocab_word
        
        # Only correct if distance is small
        if min_distance <= 2:
            return best_match
        
        return word
    
    def simple_edit_distance(self, s1, s2):
        """Simple Levenshtein distance calculation"""
        if len(s1) < len(s2):
            return self.simple_edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def correct_query(self, query):
        """Correct spelling in entire query"""
        tokens = self.tokenize(query)
        corrected_tokens = []
        
        for token in tokens:
            # Don't correct brands or very short words
            if token in self.common_brands or len(token) <= 2:
                corrected_tokens.append(token)
            else:
                corrected_tokens.append(self.spell_correct(token))
        
        return ' '.join(corrected_tokens)
    
    def extract_entities(self, query):
        """Extract product entities from query"""
        tokens = self.tokenize(query)
        
        entities = {
            'brands': [],
            'categories': [],
            'attributes': [],
            'price_range': None
        }
        
        # Extract brands
        for token in tokens:
            if token in self.common_brands:
                entities['brands'].append(token)
        
        # Extract categories
        for category, synonyms in self.category_synonyms.items():
            if category in tokens or any(syn in tokens for syn in synonyms):
                entities['categories'].append(category)
        
        # Extract price information
        price_pattern = r'under\s+(\d+)|below\s+(\d+)|less\s+than\s+(\d+)'
        price_match = re.search(price_pattern, query)
        if price_match:
            price = next(g for g in price_match.groups() if g)
            entities['price_range'] = {'max': int(price)}
        
        return entities
    
    def get_autocomplete_suggestions(self, partial_query, max_suggestions=10):
        """Generate autocomplete suggestions"""
        if not partial_query or len(partial_query) < 2:
            return []
        
        partial_query = partial_query.lower()
        suggestions = []
        
        # Search in product names
        for product_name in self.product_names:
            if product_name.lower().startswith(partial_query):
                suggestions.append(product_name)
                if len(suggestions) >= max_suggestions:
                    break
        
        # If not enough, search for contains
        if len(suggestions) < max_suggestions:
            for product_name in self.product_names:
                if partial_query in product_name.lower() and product_name not in suggestions:
                    suggestions.append(product_name)
                    if len(suggestions) >= max_suggestions:
                        break
        
        return suggestions[:max_suggestions]
    
    def build_vocabulary(self, products):
        """Build vocabulary from product catalog"""
        all_text = []
        self.product_names = []
        
        for product in products:
            name = product.get('product_name', '')
            brand = product.get('brand', '')
            
            all_text.append(name)
            all_text.append(brand)
            self.product_names.append(name)
        
        # Tokenize and build vocabulary
        vocab_counter = Counter()
        for text in all_text:
            tokens = self.tokenize(text)
            vocab_counter.update(tokens)
        
        # Store vocabulary
        self.vocabulary = set(vocab_counter.keys())
        
        print(f"Built vocabulary with {len(self.vocabulary)} words and {len(self.product_names)} products")
    
    def semantic_search(self, query, products, top_k=50):
        """Perform semantic search using TF-IDF"""
        try:
            # Build corpus
            corpus = [f"{p.get('product_name', '')} {p.get('brand', '')}" 
                     for p in products]
            
            # Initialize or use existing vectorizer
            if self.tfidf_vectorizer is None:
                self.tfidf_vectorizer = TfidfVectorizer(
                    max_features=500,
                    ngram_range=(1, 2),
                    stop_words='english' if _HAS_NLTK else None
                )
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            else:
                tfidf_matrix = self.tfidf_vectorizer.transform(corpus)
            
            # Transform query
            query_vec = self.tfidf_vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Get top results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    product = products[idx].copy()
                    product['relevance_score'] = float(similarities[idx])
                    results.append(product)
            
            return results
        
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
    
    def analyze_query_intent(self, query):
        """Analyze user intent from query"""
        query_lower = query.lower()
        
        intent = {
            'type': 'product_search',  # default
            'modifiers': []
        }
        
        # Price-sensitive intent
        if any(word in query_lower for word in ['cheap', 'affordable', 'budget', 'under']):
            intent['modifiers'].append('price_sensitive')
        
        # Quality-focused intent
        if any(word in query_lower for word in ['best', 'top', 'premium', 'quality']):
            intent['modifiers'].append('quality_focused')
        
        # Brand-specific intent
        if any(brand in query_lower for brand in self.common_brands):
            intent['modifiers'].append('brand_specific')
        
        # Comparison intent
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'difference']):
            intent['type'] = 'comparison'
        
        return intent
    
    def generate_search_keywords(self, query):
        """Generate optimized search keywords from query"""
        # Preprocess
        cleaned = self.preprocess_text(query)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        #Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = [self.lemmatize(t) for t in tokens]
        
        # Expand with synonyms
        expanded = self.expand_query(' '.join(tokens))
        
        return list(set(expanded))
