from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import Config
from data_sources.source_manager import SourceManager
from services.text_search_service import TextSearchService
from services.image_service_simple import ImageService
from services.image_recognition import ImageRecognitionService
from services.nlp_service import NLPService
from services.price_prediction import PricePredictionService
from services.recommendation_engine import RecommendationEngine
from services.price_compare_service import PriceCompareService
from services.notification_service import NotificationService
from models.user import User
from models.alert import Alert

app = Flask(__name__)
app.config.from_object(Config)

# In-memory stores for MVP
alerts_store = []
users_store = []
wishlist_store = []
recent_searches = []
_next_alert_id = 1
_next_user_id = 1
_next_wishlist_id = 1

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize services
source_manager = SourceManager()

# Initialize search with live scraping enabled (hybrid mode)
try:
    from search_config import ENABLE_LIVE_SCRAPING
    text_search_service = TextSearchService(use_live_scraping=ENABLE_LIVE_SCRAPING)
    print(f"🔍 Search mode: {'HYBRID (Live + Datasets)' if ENABLE_LIVE_SCRAPING else 'Datasets Only'}")
except ImportError:
    text_search_service = TextSearchService(use_live_scraping=True)
    print("🔍 Search mode: HYBRID (Live + Datasets)")

image_service = ImageService()
price_compare_service = PriceCompareService()
notification_service = NotificationService()

# Initialize AI/ML services
image_recognition_service = ImageRecognitionService()
nlp_service = NLPService()
price_prediction_service = PricePredictionService()
recommendation_engine = RecommendationEngine()

print("✓ AI/ML services initialized successfully!")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Homepage with search interface."""
    return render_template('realistic-index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('auth/login.html')
        
        # Find user
        user = next((u for u in users_store if u['username'] == username), None)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    global users_store, _next_user_id
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html')
        
        # Check if user exists
        if any(u['username'] == username for u in users_store):
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        
        if any(u['email'] == email for u in users_store):
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        # Create user
        user = {
            'id': _next_user_id,
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password)
        }
        users_store.append(user)
        _next_user_id += 1
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    user_alerts = [a for a in alerts_store if a.get('user_id') == session['user_id']]
    user_wishlist = [w for w in wishlist_store if w.get('user_id') == session['user_id']]
    user_searches = [s for s in recent_searches if s.get('user_id') == session['user_id']][-5:]
    
    return render_template('dashboard.html', 
                         alerts=user_alerts,
                         wishlist=user_wishlist,
                         recent_searches=user_searches)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Text-based product search."""
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if not query:
            flash('Please enter a search query.', 'error')
            return redirect(url_for('index'))

        try:
            # Save search history if user is logged in
            if 'user_id' in session:
                recent_searches.append({
                    'user_id': session['user_id'],
                    'query': query,
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                })
            
            # Perform search
            results = text_search_service.search_products(query)

            # Compare prices across platforms
            if results:
                comparison_results = price_compare_service.compare_prices(results)
                return render_template('realistic-search-results.html',
                                     query=query,
                                     results=comparison_results)
            else:
                return render_template('realistic-search-results.html',
                                     query=query,
                                     results=[],
                                     message="No products found matching your search.")

        except Exception as e:
            app.logger.error(f"Search error: {e}")
            flash('An error occurred during search. Please try again.', 'error')
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Image upload and search."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Process image and search
                processed_path = image_service.process_image(filepath)
                results = image_service.search_by_image(processed_path)

                # Compare prices
                if results:
                    comparison_results = price_compare_service.compare_prices(results)
                    return render_template('search_results.html',
                                         query=f"Image: {filename}",
                                         results=comparison_results,
                                         image_path=processed_path)
                else:
                    return render_template('search_results.html',
                                         query=f"Image: {filename}",
                                         results=[],
                                         message="No products found matching the uploaded image.")

            except Exception as e:
                app.logger.error(f"Image processing error: {e}")
                flash('An error occurred while processing the image. Please try again.', 'error')
                return redirect(request.url)

    return render_template('upload.html')

@app.route('/results')
def results():
    """Display search results (alternative route)."""
    return render_template('search_results.html')

@app.route('/alerts', methods=['GET', 'POST'])
@login_required
def alerts():
    """Price alert setup."""
    global alerts_store, _next_alert_id
    
    if request.method == 'POST':
        # Deletion path
        delete_id = request.form.get('delete_alert_id')
        if delete_id:
            try:
                delete_id = int(delete_id)
                alerts_store = [a for a in alerts_store if a['id'] != delete_id or a.get('user_id') != session['user_id']]
                flash('Alert deleted.', 'success')
            except Exception as e:
                app.logger.error(f"Alert delete error: {e}")
                flash('Could not delete alert.', 'error')
            return redirect(url_for('alerts'))

        # Create new alert
        product_name = request.form.get('product_name', '').strip()
        email = request.form.get('email', '').strip()
        threshold = request.form.get('threshold')
        condition = request.form.get('condition', 'below')  # default to below
        
        try:
            threshold_val = float(threshold)
        except Exception:
            threshold_val = None

        if not all([product_name, threshold_val is not None]):
            flash('Please fill in product name and threshold.', 'error')
            return redirect(request.url)

        try:
            alert = {
                'id': _next_alert_id, 
                'user_id': session['user_id'],
                'product_name': product_name, 
                'email': email or session.get('email', ''), 
                'threshold': threshold_val,
                'condition': condition
            }
            alerts_store.append(alert)
            _next_alert_id += 1
            flash('Price alert set successfully!', 'success')
            return redirect(url_for('alerts'))
        except Exception as e:
            app.logger.error(f"Alert setup error: {e}")
            flash('An error occurred while setting up the alert.', 'error')
            return redirect(request.url)

    user_alerts = [a for a in alerts_store if a.get('user_id') == session['user_id']]
    return render_template('alerts.html', alerts=user_alerts)

@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    """User wishlist management."""
    global wishlist_store, _next_wishlist_id
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            product_name = request.form.get('product_name', '').strip()
            platform = request.form.get('platform', '').strip()
            price = request.form.get('price')
            image_url = request.form.get('image_url', '')
            
            if product_name and platform:
                wishlist_item = {
                    'id': _next_wishlist_id,
                    'user_id': session['user_id'],
                    'product_name': product_name,
                    'platform': platform,
                    'price': float(price) if price else 0,
                    'image_url': image_url,
                    'added_date': __import__('datetime').datetime.now().isoformat()
                }
                wishlist_store.append(wishlist_item)
                _next_wishlist_id += 1
                flash('Product added to wishlist!', 'success')
        
        elif action == 'remove':
            item_id = request.form.get('item_id')
            if item_id:
                wishlist_store = [w for w in wishlist_store if w['id'] != int(item_id) or w.get('user_id') != session['user_id']]
                flash('Product removed from wishlist.', 'info')
    
    user_wishlist = [w for w in wishlist_store if w.get('user_id') == session['user_id']]
    return render_template('wishlist.html', wishlist=user_wishlist)

@app.route('/categories')
def categories():
    """Product categories page."""
    categories = {
        'Groceries': {
            'items': ['milk', 'bread', 'rice', 'oil', 'sugar', 'noodles', 'chips', 'beverages'],
            'count': '2000+',
            'icon': '🛒'
        },
        'Electronics': {
            'items': ['phones', 'laptops', 'headphones', 'tablets', 'cameras', 'tvs', 'watches'],
            'count': '5000+',
            'icon': '📱'
        },
        'Fashion': {
            'items': ['shoes', 'jeans', 'tshirts', 'dresses', 'jackets', 'sneakers', 'accessories'],
            'count': '8000+',
            'icon': '👕'
        },
        'Home & Kitchen': {
            'items': ['furniture', 'appliances', 'cookware', 'decor', 'storage', 'lighting'],
            'count': '3000+',
            'icon': '🏠'
        },
        'Beauty': {
            'items': ['skincare', 'makeup', 'perfumes', 'haircare', 'personal care', 'wellness'],
            'count': '4000+',
            'icon': '💄'
        },
        'Sports': {
            'items': ['fitness equipment', 'outdoor gear', 'sports accessories', 'supplements'],
            'count': '1500+',
            'icon': '⚽'
        }
    }
    return render_template('realistic-categories.html', categories=categories)

@app.route('/category/<category_name>')
def category_products(category_name):
    """Products by category."""
    # Get products for this category
    category_datasets = {
        'groceries': ['blinkit', 'zepto', 'instamart', 'bigbasket'],
        'electronics': ['amazon', 'flipkart', 'electronics_amazon'],
        'fashion': ['myntra', 'ajio', 'fashion_myntra'],
        'home': ['home_kitchen'],
        'homekitchen': ['home_kitchen'],
        'beauty': ['nykaa', 'beauty_nykaa'],
        'sports': ['sports_fitness']
    }
    
    datasets = category_datasets.get(category_name.lower(), [])
    all_results = []
    
    # Load products from category-specific datasets
    for dataset in datasets:
        try:
            products = source_manager.load_products(dataset)
            for product in products:
                product['platform'] = dataset
                all_results.append(product)
        except Exception as e:
            print(f"Error loading {dataset}: {e}")
    
    # If no specific datasets, fall back to keyword search
    if not all_results:
        category_keywords = {
            'groceries': ['milk', 'bread', 'rice', 'oil', 'sugar', 'noodles', 'chips'],
            'electronics': ['phone', 'laptop', 'headphones', 'tablet', 'camera', 'tv'],
            'fashion': ['shoes', 'jeans', 'tshirt', 'dress', 'jacket', 'sneakers'],
            'home': ['furniture', 'appliances', 'cookware', 'decor'],
            'beauty': ['skincare', 'makeup', 'perfume', 'haircare'],
            'sports': ['fitness', 'outdoor', 'sports']
        }
        
        keywords = category_keywords.get(category_name.lower(), [])
        for keyword in keywords:
            results = text_search_service.search_products(keyword)
            all_results.extend(results)
    
    # Remove duplicates and compare prices
    unique_results = []
    seen = set()
    for product in all_results:
        key = (product['product_name'], product.get('platform', 'unknown'))
        if key not in seen:
            seen.add(key)
            unique_results.append(product)
    
    comparison_results = price_compare_service.compare_prices(unique_results)
    
    return render_template('category_products.html', 
                         category=category_name.title(),
                         results=comparison_results)


@app.route('/redirect/<platform>/<path:product_name>')
def redirect_to_platform(platform, product_name):
    """Redirect users to the actual platform website."""
    # Platform URLs mapping
    platform_urls = {
        'amazon': 'https://www.amazon.in/s?k={}',
        'flipkart': 'https://www.flipkart.com/search?q={}',
        'myntra': 'https://www.myntra.com/{}',
        'blinkit': 'https://blinkit.com/s/?q={}',
        'zepto': 'https://www.zepto.com/search?query={}',
        'bigbasket': 'https://www.bigbasket.com/ps/?q={}',
        'ajio': 'https://www.ajio.com/search/?text={}',
        'meesho': 'https://www.meesho.com/s/p/{}',
        'shopsy': 'https://www.shopsy.in/search?q={}',
        'nykaa': 'https://www.nykaa.com/search/result/?q={}',
        'instamart': 'https://www.swiggy.com/instamart/search?custom_back=true&query={}',
        'electronics_amazon': 'https://www.amazon.in/s?k={}',
        'fashion_myntra': 'https://www.myntra.com/{}',
        'home_kitchen': 'https://www.amazon.in/s?k={}',
        'beauty_nykaa': 'https://www.nykaa.com/search/result/?q={}',
        'sports_fitness': 'https://www.amazon.in/s?k={}'
    }
    
    # Get the base URL for the platform
    base_url = platform_urls.get(platform.lower())
    
    if not base_url:
        flash(f'Platform {platform} not supported yet.', 'error')
        return redirect(url_for('index'))
    
    # Format the product name for URL
    formatted_product = product_name.replace(' ', '%20')
    redirect_url = base_url.format(formatted_product)
    
    # Track the redirect for analytics
    if 'user_id' in session:
        # In a real app, you'd log this to analytics
        print(f"User {session['user_id']} redirected to {platform} for {product_name}")
    
    # For direct redirect (if 'direct' parameter is passed)
    if request.args.get('direct') == 'true':
        return redirect(redirect_url)
    
    # Show confirmation page with auto-redirect
    return render_template('redirect_confirmation.html', 
                         platform=platform,
                         product_name=product_name,
                         redirect_url=redirect_url)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'features': ['text_search', 'image_search', 'price_alerts']
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon if present, otherwise return empty response."""
    favicon_path = os.path.join(app.static_folder or 'static', 'images', 'favicon.ico')
    if os.path.exists(favicon_path):
        from flask import send_file
        return send_file(favicon_path)
    return ('', 204)

@app.route('/api/search')
def api_search():
    """API endpoint for product search."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400

    try:
        results = text_search_service.search_products(query)
        comparison_results = price_compare_service.compare_prices(results)
        return jsonify({
            'query': query,
            'results': comparison_results,
            'count': len(comparison_results)
        })
    except Exception as e:
        app.logger.error(f"API search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

# ========================
# AI/ML-Powered API Endpoints
# ========================

@app.route('/api/visual-search', methods=['POST'])
def api_visual_search():
    """AI-powered visual search using image recognition"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save uploaded image
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Classify product using AI
        classification = image_recognition_service.classify_product(filepath)
        
        # Extract features and find similar products
        all_products = source_manager.get_all_products()
        keywords = classification.get('category', 'general').split()
        
        # Search using extracted keywords
        results = []
        for keyword in keywords:
            results.extend(text_search_service.search_products(keyword))
        
        # Remove duplicates
        unique_results = list({(p['product_name'], p.get('platform', '')): p for p in results}.values())
        
        # Compare prices
        comparison_results = price_compare_service.compare_prices(unique_results[:50])
        
        return jsonify({
            'classification': classification,
            'results': comparison_results,
            'count': len(comparison_results)
        })
    
    except Exception as e:
        app.logger.error(f"Visual search error: {e}")
        return jsonify({'error': 'Visual search failed'}), 500

@app.route('/api/smart-search')
def api_smart_search():
    """NLP-powered smart search with query understanding"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        # Build vocabulary if not already done
        if not nlp_service.vocabulary:
            all_products = source_manager.get_all_products()
            nlp_service.build_vocabulary(all_products)
        
        # Analyze query intent
        intent = nlp_service.analyze_query_intent(query)
        
        # Correct spelling
        corrected_query = nlp_service.correct_query(query)
        
        # Extract entities
        entities = nlp_service.extract_entities(corrected_query)
        
        # Expand query with synonyms
        expanded_keywords = nlp_service.generate_search_keywords(corrected_query)
        
        # Perform search with expanded keywords
        all_results = []
        for keyword in expanded_keywords[:5]:  # Limit to top 5 keywords
            results = text_search_service.search_products(keyword)
            all_results.extend(results)
        
        # Remove duplicates
        unique_results = list({(p['product_name'], p.get('platform', '')): p for p in all_results}.values())
        
        # Semantic ranking
        all_products = source_manager.get_all_products()
        semantic_results = nlp_service.semantic_search(corrected_query, all_products, top_k=50)
        
        # Combine and deduplicate
        final_results = semantic_results if semantic_results else unique_results[:50]
        
        # Compare prices
        comparison_results = price_compare_service.compare_prices(final_results)
        
        return jsonify({
            'original_query': query,
            'corrected_query': corrected_query if corrected_query != query else None,
            'intent': intent,
            'entities': entities,
            'results': comparison_results,
            'count': len(comparison_results)
        })
    
    except Exception as e:
        app.logger.error(f"Smart search error: {e}")
        return jsonify({'error': 'Smart search failed'}), 500

@app.route('/api/autocomplete')
def api_autocomplete():
    """AI-powered autocomplete suggestions"""
    partial_query = request.args.get('q', '').strip()
    if not partial_query or len(partial_query) < 2:
        return jsonify({'suggestions': []})
    
    try:
        # Build vocabulary if needed
        if not nlp_service.product_names:
            all_products = source_manager.get_all_products()
            nlp_service.build_vocabulary(all_products)
        
        suggestions = nlp_service.get_autocomplete_suggestions(partial_query, max_suggestions=10)
        
        return jsonify({'suggestions': suggestions})
    
    except Exception as e:
        app.logger.error(f"Autocomplete error: {e}")
        return jsonify({'suggestions': []})

@app.route('/api/recommendations')
def api_recommendations():
    """Get personalized product recommendations"""
    user_id = session.get('user_id', 'guest')
    
    try:
        # Build item features if not done
        all_products = source_manager.get_all_products()
        if not recommendation_engine.products_catalog:
            recommendation_engine.build_item_features(all_products)
            recommendation_engine.compute_item_similarity()
        
        # Get personalized recommendations
        recommendations = recommendation_engine.get_personalized_recommendations(
            user_id, top_k=20
        )
        
        # If no personalized recommendations, get trending
        if not recommendations:
            recommendations = recommendation_engine.get_trending_products(top_k=20)
        
        return jsonify({
            'recommendations': recommendations,
            'count': len(recommendations),
            'personalized': user_id != 'guest'
        })
    
    except Exception as e:
        app.logger.error(f"Recommendations error: {e}")
        return jsonify({'error': 'Recommendations failed'}), 500

@app.route('/api/similar-products')
def api_similar_products():
    """Find similar products based on a given product"""
    product_name = request.args.get('product')
    platform = request.args.get('platform')
    
    if not product_name:
        return jsonify({'error': 'Product parameter required'}), 400
    
    try:
        # Find the product
        all_products = source_manager.get_all_products()
        product = next(
            (p for p in all_products 
             if p.get('product_name') == product_name and 
             (not platform or p.get('platform') == platform)),
            None
        )
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Build features if needed
        if not recommendation_engine.products_catalog:
            recommendation_engine.build_item_features(all_products)
            recommendation_engine.compute_item_similarity()
        
        # Get similar products
        similar = recommendation_engine.get_similar_products(product, top_k=15)
        
        return jsonify({
            'product': product,
            'similar_products': similar,
            'count': len(similar)
        })
    
    except Exception as e:
        app.logger.error(f"Similar products error: {e}")
        return jsonify({'error': 'Failed to find similar products'}), 500

@app.route('/api/predict-price')
def api_predict_price():
    """Predict future price for a product"""
    product_name = request.args.get('product')
    platform = request.args.get('platform')
    days_ahead = int(request.args.get('days', 7))
    
    if not product_name:
        return jsonify({'error': 'Product parameter required'}), 400
    
    try:
        product_id = f"{product_name}_{platform}" if platform else product_name
        
        # Get prediction
        prediction = price_prediction_service.predict_future_price(product_id, days_ahead)
        
        # Get trend analysis
        analysis = price_prediction_service.analyze_price_trends(product_id)
        
        # Get optimal buy time
        buy_recommendation = price_prediction_service.get_optimal_buy_time(product_id)
        
        return jsonify({
            'product': product_name,
            'platform': platform,
            'prediction': prediction,
            'analysis': analysis,
            'buy_recommendation': buy_recommendation
        })
    
    except Exception as e:
        app.logger.error(f"Price prediction error: {e}")
        return jsonify({'error': 'Price prediction failed'}), 500

@app.route('/api/price-insights')
def api_price_insights():
    """Get comprehensive price insights across products"""
    try:
        all_products = source_manager.get_all_products()
        insights = price_prediction_service.get_price_insights(all_products[:100])  # Sample
        
        return jsonify(insights)
    
    except Exception as e:
        app.logger.error(f"Price insights error: {e}")
        return jsonify({'error': 'Failed to generate insights'}), 500

@app.route('/api/trending')
def api_trending():
    """Get trending products"""
    limit = int(request.args.get('limit', 20))
    
    try:
        all_products = source_manager.get_all_products()
        
        # Build features if needed
        if not recommendation_engine.products_catalog:
            recommendation_engine.build_item_features(all_products)
        
        trending = recommendation_engine.get_trending_products(top_k=limit)
        
        return jsonify({
            'trending': trending,
            'count': len(trending)
        })
    
    except Exception as e:
        app.logger.error(f"Trending products error: {e}")
        return jsonify({'error': 'Failed to get trending products'}), 500

@app.route('/api/track-interaction', methods=['POST'])
def api_track_interaction():
    """Track user interaction for better recommendations"""
    user_id = session.get('user_id', 'guest')
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        product = data.get('product')
        interaction_type = data.get('type', 'view')  # view, click, search, wishlist
        weight = float(data.get('weight', 1.0))
        
        if product:
            recommendation_engine.add_interaction(user_id, product, interaction_type, weight)
        
        return jsonify({'success': True})
    
    except Exception as e:
        app.logger.error(f"Track interaction error: {e}")
        return jsonify({'error': 'Failed to track interaction'}), 500

def allowed_file(filename):
    """Check if file extension is allowed."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
