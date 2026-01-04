# Faculty Deployment Q&A (Viva Voce Prep)

### Q: How does the Price Prediction logic work?
**A:** We use the ARIMA model from the `statsmodels` library. It analyzes the time-series data of a product's price history. It looks for trends (direction) and seasonality (repeating patterns) to forecast the next 7 days. We also use Isolation Forest to detect anomalies (fake discounts).

### Q: What acts as the fallback if live scraping fails?
**A:** The system implements a 'Hybrid Search Pattern'. The `TextSearchService` has a try-catch block. It attempts a live HTTP request to Amazon/Flipkart first. If that times out or returns a 503 (Blocked), it catches the exception and immediately queries our local JSON datasets (`datasets/amazon_products.json`, etc.) to ensure the user always sees results.

### Q: How do you handle image recognition?
**A:** We use a pre-trained **MobileNetV2** model from TensorFlow/Keras. It's a lightweight deep neural network optimized for speed. When you upload an image, we resize it to 224x224 pixels, pass it through the network, and valid the predicted class (e.g., "running shoe") against our product categories.

### Q: How secure is the application?
**A:** We use standard Flask security practices:
- `werkzeug.security` for password hashing (SHA-256).
- `CSFR` protection (simulated for MVP).
- Input sanitization to prevent XSS.
- Environment variables for secrets (in production).

### Q: What is the 'Similarity Score' in your recommendation engine?
**A:** We use **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert product descriptions into vectors. Then we calculate the **Cosine Similarity** between these vectors. If a user likes Product A, we recommend Product B if their vectors are mathematically close (angle near 0).
