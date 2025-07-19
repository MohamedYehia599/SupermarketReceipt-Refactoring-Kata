class OfferContext:
    def __init__(self):
        self.strategies = {
            OfferType.THREE_FOR_TWO: ThreeForTwoStrategy(),
            OfferType.TEN_PERCENT: TenPercentStrategy(),
            OfferType.FIVE_FOR_AMOUNT: BulkDiscountStrategy()
        }
    
    def calculate_discount(self, offer_type, product, quantity,minimum_quantity_apply ,argument=None):
        strategy = self.strategies.get(offer_type)
        return strategy.calculate_discount(product, quantity, argument)
