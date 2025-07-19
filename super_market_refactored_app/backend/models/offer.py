Offer(id, type, argument, is_active)


def calculate_discount(self,product,quantity,offer_min_quantity_to_apply):
    offer_calculator_context = OfferCalculatorContext(self.type)
    offer_calculator_context.calculate_discount(self.type,product,quantity,offer_min_quantity_to_apply,self.argument)

