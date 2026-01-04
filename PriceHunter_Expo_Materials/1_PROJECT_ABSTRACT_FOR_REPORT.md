# PriceHunter: AI-Powered Price Comparison & Intelligence Platform

## Project Abstract
In the rapidly growing e-commerce landscape, consumers struggle to find the best deals across fragmented platforms. "PriceHunter" is an advanced AI/ML-powered web application that solves this by aggregating real-time product data from Amazon, Flipkart, Myntra, and others. Beyond simple comparison, it utilizes deep learning for image recognition, ARIMA models for price forecasting, and NLP for intelligent search intent analysis.

## Problem Statement
- **Fragmented Pricing:** Prices vary significantly across platforms for identical products.
- **Counterfeit Products:** Users struggle to identify genuine products visually.
- **Timing Dilemma:** Buyers don't know if they should buy now or wait for a price drop.
- **Search Complexity:** Keyword-only searches fail to understand user intent or handle typos.

## Proposed Solution
A unified, intelligent platform providing:
1.  **Cross-Platform Aggregation:** Real-time price scraping and comparison.
2.  **Visual Intelligence:** 3D product previews and image-based search.
3.  **Predictive Analytics:** 7-day price forecasting to recommend optimal buying times.
4.  **Semantic Search:** NLP-driven search engine tolerant of user errors.

## Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript (Responsive)
- **Backend:** Python (Flask 3.0)
- **AI/ML:** 
    - TensorFlow/Keras (MobileNetV2 for Image Recognition)
    - Scikit-learn (Isolation Forest for Anomaly Detection)
    - NLTK (Natural Language Processing)
    - Statsmodels (ARIMA for Time Series Forecasting)
- **Data:** BeautifulSoup4 (Web Scraping), JSON Datasets
- **Tools:** Git, Docker, Gunicorn

## Key Features for Demo
- **Live Search Hybrid Mode:** Failsafe searching using both live scraping and local data.
- **Smart Recommendations:** Collaborative filtering for personalized suggestions.
- **Price Forecasting:** "Buy Now vs. Wait" decision support.
- **Visual Search:** Upload an image to find products.
