import pytest
from tests.fake_catalog import FakeCatalog
from model_objects import Product, ProductUnit, SpecialOfferType, Offer, ProductQuantity
from receipt import Receipt
from teller import Teller
from shopping_cart import ShoppingCart


class TestShoppingCart:
    
    @pytest.fixture
    def sample_product(self):
        return Product("toothbrush", ProductUnit.EACH)


    @pytest.fixture
    def sample_catalog(self, sample_product):
        catalog = FakeCatalog()
        catalog.add_product(sample_product, 0.99)
        return catalog


    @pytest.fixture
    def cart(self):
        return ShoppingCart()


    def test_valid_creation(self):
        cart = ShoppingCart()
        assert len(cart.items) == 0
        assert len(cart.product_quantities) == 0

    def test_add_item_in_cart(self,cart, sample_product):
        cart.add_item(sample_product)
        assert len(cart.items) == 1
        assert cart.product_quantities[sample_product] == 1

    def test_add_multiple_items(self, cart):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        apples = Product("apples", ProductUnit.KILO)
        milk = Product("milk", ProductUnit.EACH)
        
        cart.add_item_quantity(toothbrush, 2)
        cart.add_item_quantity(apples, 1.5)
        cart.add_item(milk)  

        assert len(cart.items) == 3
        assert cart.product_quantities[toothbrush] == 2
        assert cart.product_quantities[apples] == 1.5
        assert cart.product_quantities[milk] == 1
        
        assert cart.items[0].product == toothbrush
        assert cart.items[0].quantity == 2
        assert cart.items[1].product == apples
        assert cart.items[1].quantity == 1.5
        assert cart.items[2].product == milk
        assert cart.items[2].quantity == 1

    def test_add_duplicate_item(self, cart, sample_product):
        cart.add_item(sample_product)
        cart.add_item(sample_product)
        assert len(cart.items) == 2
        assert cart.product_quantities[sample_product] == 2

    @pytest.mark.parametrize("product, quantity, expected_error, error_pattern", [
    # Invalid products
    (None, 1, ValueError, r"product cannot be None"),
    
    # Invalid quantities
    (Product("toothbrush", ProductUnit.EACH), 0, ValueError, r"quantity must be positive"),
    (Product("toothbrush", ProductUnit.EACH), -1, ValueError, r"quantity must be positive"),
    (Product("toothbrush", ProductUnit.EACH), "invalid", TypeError, r"quantity must be numeric"),
    
    # Invalid unit product quantities
    (Product("toothbrush", ProductUnit.EACH), 1.5, ValueError, r"quantity must be integer for EACH products"),
    ], ids=[
        "none-product", 
        "zero-quantity", 
        "negative-quantity", 
        "str-quantity",
        "fractional-unit-product"
    ])
    def test_add_invalid_item(self, cart, product, quantity, expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            cart.add_item_quantity(product, quantity)
     

    @pytest.mark.parametrize(
    "receipt, error_pattern",
    [
        (None, r"receipt cannot be None"),
        (123, r"receipt must be Receipt type"),
    ],
    ids=["none-receipt", "wrong-type"]
    )
    def test_handle_offers_with_invalid_receipt(self, cart, sample_catalog, receipt, error_pattern):
        with pytest.raises(ValueError, match=error_pattern):
            cart.handle_offers(receipt, {}, sample_catalog)


    @pytest.mark.parametrize(
    "offers, error_pattern",
    [
        (None, r"offers must be a dictionary"),
        ("invalid", r"offers must be a dictionary"),
    ],
    ids=["none-offers", "non-dict-offers"]
    )
    def test_handle_offers_with_invalid_offers(self, cart, sample_catalog, offers, error_pattern):
        with pytest.raises(ValueError, match=error_pattern):
            cart.handle_offers(Receipt(), offers, sample_catalog)



    @pytest.mark.parametrize(
    "catalog, error_pattern",
    [
        (None, r"catalog cannot be None"),
        (123, r"catalog must implement Catalog interface"),
    ],
    ids=["none-catalog", "wrong-type-int"]
    )
    def test_handle_offers_with_invalid_catalog(self, cart, catalog, error_pattern):
        with pytest.raises(ValueError, match=error_pattern):
            cart.handle_offers(Receipt(), {}, catalog)



    def test_handle_offers_without_offers_added(self, cart, sample_product, sample_catalog):
        receipt = Receipt()
        cart.add_item(sample_product)
        cart.handle_offers(receipt, {}, sample_catalog)
        assert len(receipt.discounts) == 0
        assert len(receipt.items) == 1
    

    @pytest.mark.parametrize("quantity,expected_discount", [
    (1, -0.099),    
    (5, -0.495),
    (10, -0.99),
    (3, -0.297),
    ], ids=["single-item", "five-items", "ten-items", "three-items"])
    def test_ten_percent_discount_creation(self, quantity, expected_discount,
                                        sample_product, sample_catalog):
        cart = ShoppingCart()
        receipt = Receipt()
        cart.add_item_quantity(sample_product, quantity)
        
        offers = {
            sample_product: Offer(
                SpecialOfferType.TEN_PERCENT_DISCOUNT,
                sample_product,
                10.0
            )
        }
        
        cart.handle_offers(receipt, offers, sample_catalog)
        
        assert len(receipt.discounts) == 1
        assert receipt.discounts[0].discount_amount == pytest.approx(expected_discount)



    @pytest.mark.parametrize("quantity,offer_argument,should_apply,expected_amount", [
        # Valid cases
        (2, 1.50, True, -0.48),   
        (4, 1.50, True, -0.96),   
        (3, 1.50, True, -0.48),   
        
        # Invalid case
        (1, 1.50, False, 0),
    ], ids=[
        "exact-2", "exact-4", "3-items",
        "1-item"
    ])
    def test_two_for_amount_discount_creation(self, quantity, offer_argument, should_apply, 
                                           expected_amount, sample_product, sample_catalog):
        cart = ShoppingCart()
        receipt = Receipt()
        cart.add_item_quantity(sample_product, quantity)
    
        offers = {
            sample_product: Offer(
                SpecialOfferType.TWO_FOR_AMOUNT,
                sample_product,
                offer_argument
            )
        }
            
        cart.handle_offers(receipt, offers, sample_catalog)
        
        if should_apply:
            assert len(receipt.discounts) == 1
            assert receipt.discounts[0].discount_amount == pytest.approx(expected_amount)
        else:
            assert len(receipt.discounts) == 0
    

    @pytest.mark.parametrize("quantity,should_apply,expected_amount", [
    # Valid cases 
    (3, True, -0.99),     
    (6, True, -1.98),     
    (4, True, -0.99),
    
    # Invalid case
    (2, False, 0),

    ], ids=[
        "exact-3", "exact-6", "4-items",
        "2-items"
    ])
    def test_three_for_two_discount_creation(self, quantity, should_apply, expected_amount,
                                           sample_product, sample_catalog):
        cart = ShoppingCart()
        receipt = Receipt()
        cart.add_item_quantity(sample_product, quantity)
        
        offers = {
            sample_product: Offer(
                SpecialOfferType.THREE_FOR_TWO,
                sample_product,
                None
            )
        }
        
        cart.handle_offers(receipt, offers, sample_catalog)
        
        if should_apply:
            assert len(receipt.discounts) == 1
            assert receipt.discounts[0].discount_amount == pytest.approx(expected_amount)
        else:
            assert len(receipt.discounts) == 0
    
    
    @pytest.mark.parametrize("quantity,offer_argument,should_apply,expected_amount", [
        # Valid cases
        (5, 3.00, True, -1.95),   
        (10, 3.00, True, -3.90),
        (6, 3.00, True, -1.95),
        
        # Invalid cases
        (4, 3.00, False, 0),
    ], ids=[
        "exact-5", "exact-10", "6-items",
        "4-items"
    ])
    def test_five_for_amount_discount_creation(self, quantity, offer_argument, should_apply,
                                             expected_amount, sample_product, sample_catalog):
        cart = ShoppingCart()
        receipt = Receipt()
        cart.add_item_quantity(sample_product, quantity)
        
        offers = {
            sample_product: Offer(
                SpecialOfferType.FIVE_FOR_AMOUNT,
                sample_product,
                offer_argument
            )
        }
        
        cart.handle_offers(receipt, offers, sample_catalog)
        
        if should_apply:
            assert len(receipt.discounts) == 1
            assert receipt.discounts[0].discount_amount == pytest.approx(expected_amount)
        else:
            assert len(receipt.discounts) == 0