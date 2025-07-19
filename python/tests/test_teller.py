import pytest
from unittest.mock import Mock
from tests.fake_catalog import FakeCatalog
from model_objects import Product, ProductUnit, SpecialOfferType, Offer, ProductQuantity
from receipt import Receipt
from teller import Teller
from shopping_cart import ShoppingCart


class TestTeller:
    TOOTHBRUSH = Product("toothbrush", ProductUnit.EACH)
    APPLES = Product("apples", ProductUnit.KILO)
    
    @pytest.fixture
    def teller(self):
        catalog = FakeCatalog()
        catalog.add_product(self.TOOTHBRUSH,0.99)
        catalog.add_product(self.APPLES,1.99)
        return Teller(catalog)
    
    @pytest.fixture
    def cart(self):
        return ShoppingCart()

    def test_valid_creation(self):
        catalog = FakeCatalog()
        teller = Teller(catalog)
        assert teller.catalog == catalog
        assert teller.offers == {}

    @pytest.mark.parametrize("invalid_catalog,expected_error,error_pattern", [
        (None, ValueError, r"catalog cannot be None"),
        ("not_a_catalog", TypeError, r"Invalid catalog type"),
        (123, TypeError, r"Invalid catalog type"),
    ], ids=["none-catalog", "str-catalog", "int-catalog"])
    def test_invalid_creation(self, invalid_catalog, expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            Teller(invalid_catalog)

    def test_add_special_offer(self, teller):
        offer_type = SpecialOfferType.TEN_PERCENT_DISCOUNT
        argument = 10.0
        
        teller.add_special_offer(offer_type, self.TOOTHBRUSH, argument)
        
        assert self.TOOTHBRUSH in teller.offers
        stored_offer = teller.offers[self.TOOTHBRUSH]
        assert stored_offer.offer_type == offer_type
        assert stored_offer.argument == argument
        assert stored_offer.product == self.TOOTHBRUSH
    
    def test_checkout_with_empty_cart_creates_empty_receipt(self, teller, cart):
        receipt = teller.checks_out_articles_from(cart)
        assert isinstance(receipt, Receipt)
        assert len(receipt.items) == 0
        assert len(receipt.discounts) == 0

    def test_checkout_processes_items(self, teller, cart):
        cart.add_item_quantity(self.TOOTHBRUSH, 2)
        cart.add_item_quantity(self.APPLES, 1.5)
        
        receipt = teller.checks_out_articles_from(cart)

        assert len(receipt.items) == 2
        assert receipt.items[0].product == self.TOOTHBRUSH
        assert receipt.items[0].quantity == 2
        assert receipt.items[0].total_price == pytest.approx(1.98)  
        assert receipt.items[1].product == self.APPLES
        assert receipt.items[1].quantity == 1.5
        assert receipt.items[1].total_price == pytest.approx(2.985)
    
