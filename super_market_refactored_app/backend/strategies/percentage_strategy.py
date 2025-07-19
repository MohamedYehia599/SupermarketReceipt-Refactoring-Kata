class PercentageDiscountStrategy:
    def calculate_discount(self, unit_price, quantity, min_quantity, percentage):
        if quantity < min_quantity:
            return 0
            
        full_price = quantity * unit_price
        return full_price * (percentage / 100)