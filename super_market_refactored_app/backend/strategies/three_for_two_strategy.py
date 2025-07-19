class ThreeForTwoStrategy:
    def calculate_discount(self, unit_price, quantity, min_quantity, _=None):
        if quantity < min_quantity:
            return 0
        
        full_price = quantity * unit_price
        paid_items = (quantity // 3) * 2 + (quantity % 3)
        discounted_price = paid_items * unit_price
        
        return full_price - discounted_price