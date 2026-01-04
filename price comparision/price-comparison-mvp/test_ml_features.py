"""
Comprehensive Test Suite for AI/ML Features
Tests image recognition, NLP, price prediction, and recommendations
"""
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.image_recognition import ImageRecognitionService
from services.nlp_service import NLPService
from services.price_prediction import PricePredictionService
from services.recommendation_engine import RecommendationEngine
from data_sources.source_manager import SourceManager

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60 + "\n")

def test_image_recognition():
    """Test image recognition service"""
    print_section("Testing Image Recognition Service")
    
    service = ImageRecognitionService()
    print(f"✓ Service initialized")
    print(f"  Model loaded: {service.model_loaded}")
    
    # Test with a sample image (if exists)
    test_images = [
        'static/images/uploads/test.jpg',
        'static/images/product1.jpg',
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f"\nTesting with {img_path}...")
            result = service.classify_product(img_path)
            print(f"  Category: {result.get('category')}")
            print(f"  Confidence: {result.get('confidence'):.2f}")
            
            # Test color extraction
            colors = service.extract_color_palette(img_path, num_colors=3)
            if colors:
                print(f"  Dominant colors: {[c['hex'] for c in colors[:3]]}")
            
            # Test quality detection
            quality = service.detect_image_quality(img_path)
            if quality:
                print(f"  Image quality: {quality.get('overall_quality')}")
            break
    else:
        print("  No test images found - using fallback classification")
        result = service.fallback_classification("test_phone.jpg")
        print(f"  Fallback category: {result.get('category')}")

def test_nlp_service():
    """Test NLP service"""
    print_section("Testing NLP Service")
    
    service = NLPService()
    print("✓ Service initialized")
    
    # Load products for vocabulary
    source_manager = SourceManager()
    all_products = source_manager.get_all_products()
    print(f"  Loaded {len(all_products)} products")
    
    # Build vocabulary
    service.build_vocabulary(all_products)
    print(f"  Built vocabulary with {len(service.vocabulary)} words")
    
    # Test queries
    test_queries = [
        "nike sheos under 2000",  # Typo
        "best laptop for students",
        "amul milk 1 liter",
        "cheap headphones"
    ]
    
    print("\nTesting query processing:")
    for query in test_queries:
        print(f"\nOriginal: '{query}'")
        
        # Correct spelling
        corrected = service.correct_query(query)
        if corrected != query:
            print(f"  Corrected: '{corrected}'")
        
        # Extract entities
        entities = service.extract_entities(query)
        print(f"  Entities: {entities}")
        
        # Analyze intent
        intent = service.analyze_query_intent(query)
        print(f"  Intent: {intent}")
        
        # Generate keywords
        keywords = service.generate_search_keywords(query)
        print(f"  Keywords: {keywords[:5]}")
    
    # Test autocomplete
    print("\n\nTesting autocomplete:")
    for partial in ["ni", "lap", "mil"]:
        suggestions = service.get_autocomplete_suggestions(partial)
        print(f"  '{partial}' -> {suggestions[:3]}")

def test_price_prediction():
    """Test price prediction service"""
    print_section("Testing Price Prediction Service")
    
    service = PricePredictionService()
    print("✓ Service initialized")
    
    # Add some sample price history
    from datetime import datetime, timedelta
    
    product_id = "test_product_amazon"
    base_price = 1000
    
    print(f"\nAdding sample price history for '{product_id}'...")
    for i in range(30):
        date = datetime.now() - timedelta(days=30-i)
        # Simulate price variation
        price = base_price + (i % 7) * 10 - 20
        service.add_price_point(product_id, price, date, 'amazon')
    
    print(f"  Added {len(service.price_history[product_id])} price points")
    
    # Test prediction
    print("\nTesting price prediction:")
    prediction = service.predict_future_price(product_id, days_ahead=7)
    if prediction:
        print(f"  Current price: ₹{prediction['current_price']:.2f}")
        print(f"  Predicted change: ₹{prediction['predicted_change']:.2f}")
        print(f"  Method: {prediction['method']}")
        print(f"  Future prices: {[f'₹{p:.2f}' for p in prediction['predictions'][:3]]}")
    
    # Test anomaly detection
    print("\nTesting anomaly detection:")
    anomalies = service.detect_price_anomalies(product_id)
    print(f"  Found {len(anomalies)} anomalies")
    
    # Test trend analysis
    print("\nTesting trend analysis:")
    analysis = service.analyze_price_trends(product_id)
    if analysis:
        print(f"  Min price: ₹{analysis['min_price']:.2f}")
        print(f"  Max price: ₹{analysis['max_price']:.2f}")
        print(f"  Avg price: ₹{analysis['avg_price']:.2f}")
        print(f"  Trend: {analysis.get('trend', 'unknown')}")
    
    # Test buy recommendation
    print("\nTesting buy recommendation:")
    recommendation = service.get_optimal_buy_time(product_id)
    print(f"  Recommendation: {recommendation['recommendation']}")
    print(f"  Reason: {recommendation['reason']}")

def test_recommendations():
    """Test recommendation engine"""
    print_section("Testing Recommendation Engine")
    
    engine = RecommendationEngine()
    print("✓ Service initialized")
    
    # Load products
    source_manager = SourceManager()
    all_products = source_manager.get_all_products()
    print(f"  Loaded {len(all_products)} products")
    
    # Build features
    print("\nBuilding item features...")
    engine.build_item_features(all_products)
    print(f"  Built features for {len(engine.product_features)} products")
    
    # Compute similarity
    print("\nComputing item similarity...")
    engine.compute_item_similarity()
    print("  ✓ Similarity matrix computed")
    
    # Test similar products
    if all_products:
        test_product = all_products[0]
        print(f"\nFinding products similar to '{test_product.get('product_name')}'...")
        similar = engine.get_similar_products(test_product, top_k=5)
        print(f"  Found {len(similar)} similar products:")
        for i, prod in enumerate(similar[:3], 1):
            print(f"    {i}. {prod.get('product_name')} (score: {prod.get('similarity_score', 0):.2f})")
    
    # Test personalized recommendations
    print("\nTesting personalized recommendations:")
    user_id = "test_user_123"
    
    # Simulate user interactions
    print(f"  Adding user interactions for '{user_id}'...")
    for product in all_products[:5]:
        engine.add_interaction(user_id, product, 'view', 1.0)
    
    recommendations = engine.get_personalized_recommendations(user_id, top_k=10)
    print(f"  Generated {len(recommendations)} recommendations:")
    for i, prod in enumerate(recommendations[:3], 1):
        print(f"    {i}. {prod.get('product_name')} (score: {prod.get('recommendation_score', 0):.2f})")
    
    # Test trending products
    print("\nTesting trending products:")
    trending = engine.get_trending_products(top_k=5)
    print(f"  Found {len(trending)} trending products:")
    for i, prod in enumerate(trending[:3], 1):
        print(f"    {i}. {prod.get('product_name')}")

def test_integration():
    """Test integration between services"""
    print_section("Testing Service Integration")
    
    # Initialize all services
    image_service = ImageRecognitionService()
    nlp_service = NLPService()
    price_service = PricePredictionService()
    recommendation_engine = RecommendationEngine()
    source_manager = SourceManager()
    
    print("✓ All services initialized")
    
    # Load data
    all_products = source_manager.get_all_products()
    print(f"✓ Loaded {len(all_products)} products from datasets")
    
    # Build vocabularies and features
    nlp_service.build_vocabulary(all_products)
    recommendation_engine.build_item_features(all_products)
    recommendation_engine.compute_item_similarity()
    
    print("✓ Built vocabularies and features")
    print("\nIntegration test completed successfully!")

def run_all_tests():
    """Run all tests"""
    print("\n" + "*"*60)
    print(" AI/ML FEATURE TEST SUITE")
    print("*"*60)
    
    try:
        test_image_recognition()
        test_nlp_service()
        test_price_prediction()
        test_recommendations()
        test_integration()
        
        print("\n" + "="*60)
        print(" ✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
        return True
    
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
