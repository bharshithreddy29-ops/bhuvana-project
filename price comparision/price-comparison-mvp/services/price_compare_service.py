class PriceCompareService:
    def __init__(self):
        pass

    def compare_prices(self, products):
        """Compare prices and mark the best price for each product."""
        if not products:
            return []

        # Group products by name
        product_groups = {}
        for product in products:
            key = product['product_name'].lower()
            if key not in product_groups:
                product_groups[key] = []
            product_groups[key].append(product)

        # Find best price for each group
        compared_products = []
        for group in product_groups.values():
            # Sort by price ascending
            sorted_group = sorted(group, key=lambda x: x['price'])
            best_price = sorted_group[0]['price']
            
            for product in group:
                product_copy = product.copy()
                product_copy['is_best_price'] = product['price'] == best_price
                compared_products.append(product_copy)

        # Sort all products by price ascending
        compared_products.sort(key=lambda x: x['price'])
        return compared_products

    def get_price_summary(self, products):
        """Get price summary statistics."""
        if not products:
            return {}

        prices = [p['price'] for p in products]
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'total_products': len(products)
        }
