"""
Configuration for Live Product Search
Choose between different data sources
"""

# DATA SOURCE CONFIGURATION
# Options: 'dataset', 'scraper', 'api', 'hybrid'
DATA_SOURCE_MODE = 'hybrid'  # Use both live scraping and local datasets

# LIVE SCRAPING SETTINGS
ENABLE_LIVE_SCRAPING = True
SCRAPING_TIMEOUT = 15  # seconds
MAX_PRODUCTS_PER_PLATFORM = 10

# Platforms to scrape (when live scraping is enabled)
SCRAPING_PLATFORMS = {
    'amazon': True,
    'flipkart': True,
    'myntra': False,  # Set to True for fashion items
}

# FALLBACK SETTINGS
# If live scraping fails, fallback to local datasets
USE_DATASET_FALLBACK = True

# RATE LIMITING
# Delay between requests to avoid blocking (seconds)
REQUEST_DELAY = 2

# USER AGENT ROTATION
ROTATE_USER_AGENTS = True

# CACHING
# Cache scraped results to reduce API calls
ENABLE_CACHING = True
CACHE_DURATION = 3600  # 1 hour in seconds

# API KEYS (for future API integration)
# Get these from respective platforms
API_KEYS = {
    'amazon': '',  # Amazon Product Advertising API
    'flipkart': '',  # Flipkart Affiliate API
    'myntra': '',
}

# DATASET SETTINGS
DATASET_DIR = 'datasets'

# SEARCH SETTINGS
DEFAULT_MAX_RESULTS = 50
ENABLE_NLP = True  #Enable AI-powered search enhancements
ENABLE_PRICE_PREDICTION = True
ENABLE_RECOMMENDATIONS = True

# DEBUGGING
DEBUG_MODE = True  # Print detailed logs
LOG_SCRAPING = True  # Log scraping attempts
