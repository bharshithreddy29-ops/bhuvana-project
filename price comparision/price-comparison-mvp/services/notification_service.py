class NotificationService:
    def __init__(self):
        # For MVP, we'll use print statements or mock email sending
        pass

    def check_price_alerts(self, products, user_alerts):
        """Check if any products trigger price alerts."""
        alerts_triggered = []
        for alert in user_alerts:
            product_name_target = alert['product_name'].lower().strip()
            
            for product in products:
                # Basic matching
                if product_name_target in product['product_name'].lower():
                    
                    condition = alert.get('condition', 'below')  # Default to 'below'
                    threshold = alert['threshold']
                    current_price = product['price']
                    
                    is_triggered = False
                    
                    if condition == 'below':
                        if current_price <= threshold:
                            is_triggered = True
                    elif condition == 'above':
                        if current_price >= threshold:
                            is_triggered = True
                            
                    if is_triggered:
                        alerts_triggered.append({
                            'product': product,
                            'alert': alert,
                            'type': condition
                        })
                        
        return alerts_triggered

    def send_price_alert(self, user_email, product_name, current_price, threshold, condition='below'):
        """Send price alert notification (mock implementation)."""
        if condition == 'above':
            msg_type = "Price INCREASE Alert"
            verb = "risen above"
        else:
            msg_type = "Price DROP Alert"
            verb = "dropped below"
            
        message = f"{msg_type} for {product_name}: Current price ₹{current_price} has {verb} your threshold ₹{threshold}."
        
        # In real implementation, send email
        print(f"📧 Sending email to {user_email}: {message}")
        return True
