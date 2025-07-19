class ReceiptService:
    def generate(self, cart, item_discounts):
        receipt = Receipt()
        for item in cart.items:
            discount = item_discounts.get(item.id)
            receipt.add_item(item.product, item.quantity, item.product.price,item.product.price - discount)
            receipt.add_discount(discount)