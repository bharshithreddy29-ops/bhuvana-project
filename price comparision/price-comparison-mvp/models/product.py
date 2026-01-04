# Simple Product model for file-based storage
class Product:
    def __init__(self, id, name, brand, price, platform, image_url=None):
        self.id = id
        self.name = name
        self.brand = brand
        self.price = price
        self.platform = platform
        self.image_url = image_url

    def __repr__(self):
        return f'<Product {self.name} - {self.platform}>'
