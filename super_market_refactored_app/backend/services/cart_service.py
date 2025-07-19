class CartService:
    
    def get_cart(self):
        #this function should return cart
        
    def get_discounts(self):
        item_discounts = {}
        for item in items:
            if item.has_offer():
                product_offer = item.get_product_offer()
                offer = product_offer.offer
                offer_min_quantity = product_offer.get_minimum_quantity
                disc = offer.calculate_discount(item.product,quantity,offer_min_quantity)
                item_discounts[item.id] = disc
        return item_discounts

            

        