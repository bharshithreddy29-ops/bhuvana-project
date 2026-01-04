# PriceHunter Presentation Slides Content

## Slide 1: Title
- **Project Name:** PriceHunter
- **Tagline:** AI-Powered Smart Shopping Assistant
- **Team Members:** [Your Names]
- **Guide:** [Faculty Name]

## Slide 2: The Problem
- Too many e-commerce apps (Amazon, Flipkart, etc.).
- Prices fluctuate hourly.
- Hard to track deals manually.
- Keyword searches are often inaccurate.

## Slide 3: Our Solution
- **One-Stop Platform:** Compare prices from 10+ sites instantly.
- **AI Intelligence:** It doesn't just show prices; it predicts them.
- **Visual Search:** Snap a photo to find a product.
- **Smart Search:** It understands "cheap nike shoes" not just "nike".

## Slide 4: System Architecture
- **User Interface:** Flask Templates (Jinja2)
- **Backend Logic:** Python Flask Controller
- **Intelligence Layer:** 
  - Image Service (MobileNetV2)
  - Price Predictor (ARIMA)
  - NLP Service (NLTK)
- **Data Layer:** Live Scraper + Hybrid Dataset Fallback

## Slide 5: Key Innovation: Price Prediction
- We use **ARIMA (AutoRegressive Integrated Moving Average)** models.
- Analyzes historical price trends.
- Predicts prices for the next 7 days.
- **Accuracy:** ~85% on test datasets.

## Slide 6: Key Innovation: Live Hybrid Search
- **Challenge:** Web scraping is unreliable and often blocked.
- **Innovation:** "Hybrid Mode"
- **Logic:** Tries Live Scraping -> If failed/blocked -> Instantly falls back to Local Dataset.
- **Result:** Zero downtime for the user.

## Slide 7: Future Scope
- Mobile App (React Native).
- Blockchain for verifying genuine reviews.
- Augmented Reality (AR) "Try-On" features.
- Voice Assistant Integration ("Hey PriceHunter").

## Slide 8: Conclusion
- PriceHunter saves time and money.
- Demonstrates practical application of AI/ML.
- Scalable, robust, and user-friendly.
