import pytest
from model_objects import Product, ProductQuantity, ProductUnit

class TestProductQuantity:

    @pytest.fixture
    def unit_product(self):
        return Product("toothbrush", ProductUnit.EACH)
    
    @pytest.fixture
    def weighted_product(self):
        return Product("apples", ProductUnit.KILO)


    @pytest.mark.parametrize("product_fixture, quantity", [
        ("unit_product", 3),          # Integer for unit product
        ("weighted_product", 0.75),   # Float for weighted product
        ("weighted_product", 1_000_000),  # Large quantity
    ], ids=["unit-int", "weighted-float", "large-qty"])
    def test_valid_creation(self, product_fixture, quantity, request):
        product = request.getfixturevalue(product_fixture)
        pq = ProductQuantity(product, quantity)
        assert pq.product == product
        assert pq.quantity == quantity


    @pytest.mark.parametrize("product_fixture, quantity, expected_error, error_pattern", [
        # Invalid Unit product quantity
        ("unit_product", 1.5, ValueError, r"whole number for EACH products"),
        ("weighted_product", -1, ValueError, r"positive quantity"),
        ("unit_product", 0, ValueError, r"positive quantity"),
        
        # Invalid Quantity 
        ("unit_product", None, TypeError, r"quantity cannot be None"),
        ("unit_product", "two", TypeError, r"numeric type"),
        
        # Invalid Product 
        (None, 1, ValueError, r"product cannot be None"),
    ], ids=[
        "unit-float", "unit-negative", "unit-zero",
        "none-qty", "str-qty",
        "none-product"
    ])
    def test_invalid_creation(self, product_fixture, quantity, expected_error, error_pattern, request):
        product = request.getfixturevalue(product_fixture) if product_fixture else None
        with pytest.raises(expected_error, match=error_pattern):
            ProductQuantity(product, quantity)


    


    
