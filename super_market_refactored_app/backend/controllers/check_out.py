class CheckoutController:
    def __init__(self, cart_service, receipt_service):
        self.cart_service = cart_service
        self.receipt_service = receipt_service
    
    def checkout(self, cart_id):
        cart = self.cart_service.get_cart(cart_id)
        item_discounts = self.cart_service.get_discounts(cart)  # Move logic here
        receipt = self.receipt_service.generate(cart, item_discounts)
        return Response(receipt.to_dict())