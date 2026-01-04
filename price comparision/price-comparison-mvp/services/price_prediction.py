"""
Price Prediction and Intelligence Service
Forecasts price trends, detects anomalies, and provides pricing insights
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import IsolationForest, RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    import joblib
    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False
    print("scikit-learn not available. Using basic price analysis.")

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    _HAS_STATSMODELS = True
except ImportError:
    _HAS_STATSMODELS = False
    print("statsmodels not available. Using simple forecasting.")


class PricePredictionService:
    """ML-based price prediction and analysis"""
    
    def __init__(self):
        self.price_history = defaultdict(list)  # product_id -> price history
        self.scaler = StandardScaler() if _HAS_SKLEARN else None
        self.prediction_model = None
    
    def add_price_point(self, product_id, price, timestamp=None, platform=None):
        """Add a price point to history"""
        if timestamp is None:
            timestamp = datetime.now()
        
        self.price_history[product_id].append({
            'price': price,
            'timestamp': timestamp,
            'platform': platform
        })
    
    def load_price_history(self, history_file):
        """Load price history from file"""
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for product_id, history in data.items():
                        for point in history:
                            point['timestamp'] = datetime.fromisoformat(point['timestamp'])
                        self.price_history[product_id] = history
                print(f"Loaded price history for {len(self.price_history)} products")
        except Exception as e:
            print(f"Error loading price history: {e}")
    
    def save_price_history(self, history_file):
        """Save price history to file"""
        try:
            # Convert to JSON-serializable format
            data = {}
            for product_id, history in self.price_history.items():
                data[product_id] = [
                    {
                        'price': point['price'],
                        'timestamp': point['timestamp'].isoformat(),
                        'platform': point['platform']
                    }
                    for point in history
                ]
            
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Saved price history for {len(self.price_history)} products")
        except Exception as e:
            print(f"Error saving price history: {e}")
    
    def predict_future_price(self, product_id, days_ahead=7):
        """Predict future prices using time series analysis"""
        if product_id not in self.price_history:
            return None
        
        history = self.price_history[product_id]
        if len(history) < 7:  # Need minimum data points
            return self.simple_forecast(history, days_ahead)
        
        # Extract prices and timestamps
        df = pd.DataFrame(history)
        df = df.sort_values('timestamp')
        prices = df['price'].values
        
        # Use ARIMA if available
        if _HAS_STATSMODELS and len(prices) >= 14:
            try:
                model = ARIMA(prices, order=(1, 1, 1))
                fitted_model = model.fit()
                forecast = fitted_model.forecast(steps=days_ahead)
                
                return {
                    'predictions': forecast.tolist(),
                    'current_price': float(prices[-1]),
                    'predicted_change': float(forecast[-1] - prices[-1]),
                    'method': 'ARIMA',
                    'confidence': 0.75
                }
            except Exception as e:
                print(f"ARIMA failed: {e}, using simple forecast")
                return self.simple_forecast(history, days_ahead)
        else:
            return self.simple_forecast(history, days_ahead)
    
    def simple_forecast(self, history, days_ahead):
        """Simple moving average forecast"""
        if not history:
            return None
        
        prices = [p['price'] for p in history]
        current_price = prices[-1]
        
        # Calculate trend
        if len(prices) >= 3:
            recent_prices = prices[-7:] if len(prices) >= 7 else prices
            trend = (recent_prices[-1] - recent_prices[0]) / len(recent_prices)
        else:
            trend = 0
        
        # Forecast
        predictions = []
        for i in range(1, days_ahead + 1):
            predicted_price = current_price + (trend * i)
            predictions.append(max(0, predicted_price))  # Ensure non-negative
        
        return {
            'predictions': predictions,
            'current_price': current_price,
            'predicted_change': predictions[-1] - current_price,
            'method': 'moving_average',
            'confidence': 0.5
        }
    
    def detect_price_anomalies(self, product_id):
        """Detect unusual price changes"""
        if product_id not in self.price_history:
            return []
        
        history = self.price_history[product_id]
        if len(history) < 10:  # Need minimum data points for Isolation Forest
            # Use statistical method for small datasets
            prices = np.array([p['price'] for p in history]).reshape(-1, 1)
            return self.statistical_anomaly_detection(prices, history)
        
        prices = np.array([p['price'] for p in history]).reshape(-1, 1)
        
        # Use Isolation Forest if available and enough data
        if _HAS_SKLEARN and len(prices) >= 10:
            try:
                # Create a fresh detector for this dataset
                detector = IsolationForest(contamination=0.1, random_state=42)
                predictions = detector.fit_predict(prices)
                anomalies = []
                
                for i, pred in enumerate(predictions):
                    if pred == -1:  # Anomaly detected
                        anomalies.append({
                            'index': i,
                            'price': float(prices[i][0]),
                            'timestamp': history[i]['timestamp'].isoformat(),
                            'type': 'anomaly'
                        })
                
                return anomalies
            except Exception as e:
                print(f"Anomaly detection failed: {e}")
        
        # Fallback: statistical method
        return self.statistical_anomaly_detection(prices, history)
    
    def statistical_anomaly_detection(self, prices, history):
        """Detect anomalies using statistical methods"""
        mean_price = np.mean(prices)
        std_price = np.std(prices)
        
        anomalies = []
        for i, price in enumerate(prices):
            z_score = abs((price - mean_price) / (std_price + 1e-7))
            
            if z_score > 2.5:  # More than 2.5 standard deviations
                anomalies.append({
                    'index': i,
                    'price': float(price[0]),
                    'timestamp': history[i]['timestamp'].isoformat(),
                    'z_score': float(z_score),
                    'type': 'statistical_anomaly'
                })
        
        return anomalies
    
    def calculate_price_drop_probability(self, product_id):
        """Calculate probability of price drop"""
        if product_id not in self.price_history:
            return 0.0
        
        history = self.price_history[product_id]
        if len(history) < 5:
            return 0.5  # Neutral probability
        
        # Analyze recent trend
        prices = [p['price'] for p in history]
        recent_prices = prices[-10:] if len(prices) >= 10 else prices
        
        # Calculate drops
        drops = 0
        increases = 0
        
        for i in range(1, len(recent_prices)):
            if recent_prices[i] < recent_prices[i-1]:
                drops += 1
            elif recent_prices[i] > recent_prices[i-1]:
                increases += 1
        
        total_changes = drops + increases
        if total_changes == 0:
            return 0.5
        
        probability = drops / total_changes
        
        return probability
    
    def get_optimal_buy_time(self, product_id, days_to_analyze=30):
        """Recommend optimal time to buy based on price patterns"""
        if product_id not in self.price_history:
            return {'recommendation': 'insufficient_data'}
        
        history = self.price_history[product_id]
        if len(history) < 7:
            return {'recommendation': 'buy_now', 'reason': 'Limited price history'}
        
        # Get current price
        current_price = history[-1]['price']
        
        # Get price prediction
        prediction = self.predict_future_price(product_id, days_ahead=7)
        
        if prediction:
            predicted_price = prediction['predictions'][-1]
            predicted_change = prediction['predicted_change']
            
            # Decision logic
            if predicted_change < -50:  # Significant drop expected
                return {
                    'recommendation': 'wait',
                    'reason': f'Price expected to drop by ₹{abs(predicted_change):.2f}',
                    'wait_days': 5,
                    'expected_price': predicted_price
                }
            elif predicted_change > 50:  # Price likely to increase
                return {
                    'recommendation': 'buy_now',
                    'reason': f'Price expected to increase by ₹{predicted_change:.2f}',
                    'current_price': current_price
                }
            else:
                return {
                    'recommendation': 'neutral',
                    'reason': 'Price expected to remain stable',
                    'current_price': current_price
                }
        
        return {'recommendation': 'buy_now', 'reason': 'Unable to predict trends'}
    
    def analyze_price_trends(self, product_id):
        """Comprehensive price trend analysis"""
        if product_id not in self.price_history:
            return None
        
        history = self.price_history[product_id]
        if len(history) < 2:
            return None
        
        prices = [p['price'] for p in history]
        timestamps = [p['timestamp'] for p in history]
        
        # Basic statistics
        analysis = {
            'current_price': prices[-1],
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': np.mean(prices),
            'std_dev': np.std(prices),
            'price_range': max(prices) - min(prices),
            'data_points': len(prices),
        }
        
        # Trend direction
        if len(prices) >= 3:
            recent = prices[-5:] if len(prices) >= 5 else prices
            if recent[-1] < recent[0]:
                analysis['trend'] = 'decreasing'
            elif recent[-1] > recent[0]:
                analysis['trend'] = 'increasing'
            else:
                analysis['trend'] = 'stable'
        
        # Volatility
        if len(prices) >= 3:
            price_changes = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
            analysis['volatility'] = np.mean(price_changes)
            analysis['is_volatile'] = analysis['volatility'] > (0.1 * analysis['avg_price'])
        
        # Price drop from max
        if prices[-1] < max(prices):
            analysis['discount_from_max'] = max(prices) - prices[-1]
            analysis['discount_percentage'] = (analysis['discount_from_max'] / max(prices)) * 100
        
        return analysis
    
    def get_price_insights(self, products):
        """Generate pricing insights across multiple products"""
        insights = {
            'best_deals': [],
            'price_drops': [],
            'trending_up': [],
            'volatile_products': []
        }
        
        for product in products:
            product_id = product.get('product_name', '') + '_' + product.get('platform', '')
            
            # Simulate some history for demo (in production, use real data)
            current_price = product.get('price', 0)
            
            analysis = self.analyze_price_trends(product_id)
            
            # Identify patterns (for demo purposes)
            if current_price > 0:
                # Random classification for demo
                import random
                category = random.choice(['deal', 'drop', 'trending', 'volatile', 'normal'])
                
                if category == 'deal':
                    insights['best_deals'].append(product)
                elif category == 'drop':
                    insights['price_drops'].append(product)
                elif category == 'trending':
                    insights['trending_up'].append(product)
                elif category == 'volatile':
                    insights['volatile_products'].append(product)
        
        return insights
