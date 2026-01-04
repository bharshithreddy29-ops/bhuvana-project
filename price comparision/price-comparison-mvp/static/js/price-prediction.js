// AI Price Prediction Feature
class PricePrediction {
    constructor() {
        this.init();
    }

    init() {
        this.addPricePredictionToCards();
        this.createPredictionModal();
    }

    addPricePredictionToCards() {
        document.addEventListener('DOMContentLoaded', () => {
            const productCards = document.querySelectorAll('.product-card');
            
            productCards.forEach(card => {
                const priceElement = card.querySelector('.product-price');
                if (priceElement) {
                    const prediction = this.generatePricePrediction(priceElement.textContent);
                    
                    const predictionElement = document.createElement('div');
                    predictionElement.className = 'price-prediction';
                    predictionElement.innerHTML = `
                        <div class="prediction-indicator ${prediction.trend}">
                            <span class="trend-icon">${prediction.icon}</span>
                            <span class="trend-text">${prediction.text}</span>
                        </div>
                        <button class="prediction-details-btn" onclick="pricePrediction.showDetails('${card.dataset.productId || Math.random()}')">
                            📊 Price Forecast
                        </button>
                    `;
                    
                    priceElement.parentNode.insertBefore(predictionElement, priceElement.nextSibling);
                }
            });
        });
    }

    generatePricePrediction(priceText) {
        const price = parseFloat(priceText.replace(/[₹,]/g, ''));
        const random = Math.random();
        
        // Simulate AI prediction based on price range and random factors
        if (price > 50000) {
            // High-value items tend to have more price drops
            if (random > 0.6) {
                return {
                    trend: 'down',
                    icon: '📉',
                    text: 'Price may drop 5-15%',
                    prediction: 'down',
                    confidence: 75 + Math.floor(random * 20)
                };
            } else if (random > 0.3) {
                return {
                    trend: 'stable',
                    icon: '📊',
                    text: 'Price stable',
                    prediction: 'stable',
                    confidence: 80 + Math.floor(random * 15)
                };
            }
        } else if (price > 1000) {
            // Mid-range items
            if (random > 0.7) {
                return {
                    trend: 'up',
                    icon: '📈',
                    text: 'Price may rise 3-8%',
                    prediction: 'up',
                    confidence: 70 + Math.floor(random * 25)
                };
            } else if (random > 0.4) {
                return {
                    trend: 'down',
                    icon: '📉',
                    text: 'Price may drop 2-10%',
                    prediction: 'down',
                    confidence: 65 + Math.floor(random * 30)
                };
            }
        }
        
        // Default stable prediction
        return {
            trend: 'stable',
            icon: '📊',
            text: 'Price stable',
            prediction: 'stable',
            confidence: 85 + Math.floor(random * 10)
        };
    }

    createPredictionModal() {
        const modal = document.createElement('div');
        modal.id = 'prediction-modal';
        modal.innerHTML = `
            <div class="prediction-modal-content">
                <div class="prediction-header">
                    <h3>🤖 AI Price Forecast</h3>
                    <button class="prediction-close">&times;</button>
                </div>
                <div class="prediction-body">
                    <div class="prediction-chart">
                        <canvas id="price-chart" width="400" height="200"></canvas>
                    </div>
                    <div class="prediction-insights">
                        <div class="insight-card">
                            <h4>📊 Current Analysis</h4>
                            <p id="current-analysis">Analyzing market trends...</p>
                        </div>
                        <div class="insight-card">
                            <h4>🔮 7-Day Forecast</h4>
                            <p id="forecast-7day">Generating predictions...</p>
                        </div>
                        <div class="insight-card">
                            <h4>💡 Best Time to Buy</h4>
                            <p id="best-time">Calculating optimal timing...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add CSS for prediction modal
        const style = document.createElement('style');
        style.textContent = `
            .price-prediction {
                margin: 0.5rem 0;
                padding: 0.5rem;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                backdrop-filter: blur(10px);
            }

            .prediction-indicator {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                font-weight: 600;
            }

            .prediction-indicator.up { color: #e74c3c; }
            .prediction-indicator.down { color: #27ae60; }
            .prediction-indicator.stable { color: #f39c12; }

            .prediction-details-btn {
                background: linear-gradient(45deg, #9b59b6, #8e44ad);
                color: white;
                border: none;
                padding: 0.4rem 0.8rem;
                border-radius: 15px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(155, 89, 182, 0.3);
            }

            .prediction-details-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(155, 89, 182, 0.5);
            }

            #prediction-modal {
                display: none;
                position: fixed;
                z-index: 10000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(10px);
            }

            .prediction-modal-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 3% auto;
                padding: 0;
                border-radius: 20px;
                width: 90%;
                max-width: 800px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                animation: modalSlideIn 0.5s ease;
            }

            .prediction-header {
                background: rgba(255,255,255,0.1);
                padding: 1rem 2rem;
                border-radius: 20px 20px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: white;
            }

            .prediction-close {
                background: none;
                border: none;
                color: white;
                font-size: 2rem;
                cursor: pointer;
                padding: 0;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                transition: all 0.3s;
            }

            .prediction-close:hover {
                background: rgba(255,255,255,0.2);
                transform: rotate(90deg);
            }

            .prediction-body {
                padding: 2rem;
                color: white;
            }

            .prediction-chart {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 1rem;
                margin-bottom: 2rem;
                backdrop-filter: blur(10px);
                text-align: center;
            }

            .prediction-insights {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
            }

            .insight-card {
                background: rgba(255,255,255,0.1);
                padding: 1.5rem;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }

            .insight-card h4 {
                margin-bottom: 0.5rem;
                color: #fff;
            }

            .insight-card p {
                color: rgba(255,255,255,0.9);
                line-height: 1.5;
            }

            @media (max-width: 768px) {
                .prediction-insights {
                    grid-template-columns: 1fr;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(modal);

        // Add event listeners
        modal.querySelector('.prediction-close').addEventListener('click', () => {
            modal.style.display = 'none';
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    showDetails(productId) {
        const modal = document.getElementById('prediction-modal');
        modal.style.display = 'block';

        // Simulate AI analysis with realistic delays
        this.simulateAnalysis();
        this.drawPriceChart();
    }

    simulateAnalysis() {
        const analyses = [
            "Market trends show increased demand for this category",
            "Seasonal factors may affect pricing in the coming weeks",
            "Competition analysis suggests price stability",
            "Historical data indicates potential price fluctuation",
            "Supply chain factors may impact future pricing"
        ];

        const forecasts = [
            "Expected 3-7% price decrease within 7 days",
            "Price likely to remain stable for the next week",
            "Potential 2-5% price increase due to demand",
            "Flash sale expected in 3-5 days",
            "Best prices typically occur on weekends"
        ];

        const bestTimes = [
            "Wait 3-5 days for potential price drop",
            "Current price is optimal - buy now",
            "Weekend sales often offer better deals",
            "End of month typically has best prices",
            "Festival season may bring discounts"
        ];

        // Simulate loading with delays
        setTimeout(() => {
            document.getElementById('current-analysis').textContent = 
                analyses[Math.floor(Math.random() * analyses.length)];
        }, 500);

        setTimeout(() => {
            document.getElementById('forecast-7day').textContent = 
                forecasts[Math.floor(Math.random() * forecasts.length)];
        }, 1000);

        setTimeout(() => {
            document.getElementById('best-time').textContent = 
                bestTimes[Math.floor(Math.random() * bestTimes.length)];
        }, 1500);
    }

    drawPriceChart() {
        const canvas = document.getElementById('price-chart');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Generate sample price data
        const days = 7;
        const basePrice = 1000 + Math.random() * 5000;
        const priceData = [];
        
        for (let i = 0; i < days; i++) {
            const variation = (Math.random() - 0.5) * 0.1; // ±10% variation
            priceData.push(basePrice * (1 + variation));
        }

        // Draw chart
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.beginPath();

        const stepX = canvas.width / (days - 1);
        const minPrice = Math.min(...priceData);
        const maxPrice = Math.max(...priceData);
        const priceRange = maxPrice - minPrice || 1;

        priceData.forEach((price, index) => {
            const x = index * stepX;
            const y = canvas.height - ((price - minPrice) / priceRange) * (canvas.height - 40) - 20;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }

            // Draw points
            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, 2 * Math.PI);
            ctx.fill();
        });

        ctx.stroke();

        // Add labels
        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        
        for (let i = 0; i < days; i++) {
            const x = i * stepX;
            ctx.fillText(`Day ${i + 1}`, x, canvas.height - 5);
        }
    }
}

// Initialize Price Prediction
const pricePrediction = new PricePrediction();