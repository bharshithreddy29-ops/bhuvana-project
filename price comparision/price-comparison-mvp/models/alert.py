# Simple Alert model for file-based storage
class Alert:
    def __init__(self, id, user_id, product_name, threshold_price, condition='below'):
        self.id = id
        self.user_id = user_id
        self.product_name = product_name
        self.threshold_price = threshold_price
        self.condition = condition  # 'below' or 'above'

    def __repr__(self):
        return f'<Alert {self.product_name} - ₹{self.threshold_price}>'
