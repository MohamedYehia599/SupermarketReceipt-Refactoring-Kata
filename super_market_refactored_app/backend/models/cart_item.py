CartItem(id, cart_id, product_id, quantity)

def has_available_offer(self):
    prod_offer = ProductOffer.objects.find(product_id=self.product , min_quantaty <=self.quantity ).
    if prod_offer.offer.is_active:
        return True
    return False

def get_prduct_offer(self):
    return ProductOffer.objects.find(product_id=self.product , min_quantaty <=self.quantity )


