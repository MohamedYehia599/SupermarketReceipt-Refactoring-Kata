import pytest
from approvaltests import verify
from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter

class TestSupermarket:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.cart = ShoppingCart()
        
        # Add test products
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.catalog.add_product(self.toothbrush, 0.99)
        self.apples = Product("apples", ProductUnit.KILO)
        self.catalog.add_product(self.apples, 1.99)
        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.49)

    def test_empty_cart(self):
        receipt = self.teller.checks_out_articles_from(self.cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_two_normal_items(self):
        self.cart.add_item(self.toothbrush)
        self.cart.add_item(self.rice)
        receipt = self.teller.checks_out_articles_from(self.cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))

    def test_buy_two_get_one_free(self):
        self.cart.add_item(self.toothbrush)
        self.cart.add_item(self.toothbrush)
        self.cart.add_item(self.toothbrush)
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO,
            self.toothbrush,
            self.catalog.unit_price(self.toothbrush)
        )
        receipt = self.teller.checks_out_articles_from(self.cart)
        verify(ReceiptPrinter(40).print_receipt(receipt))