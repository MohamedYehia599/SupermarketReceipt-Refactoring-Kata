import pytest
from model_objects import Product, ProductUnit
from receipt import ReceiptItem

class TestReceiptItem:
    @pytest.fixture
    def sample_product(self):
        return Product("toothbrush", ProductUnit.EACH)


    def test_creation_with_valid_values(self, sample_product):
        item = ReceiptItem(
            product=sample_product,
            quantity=2,
            price=0.99,
            total_price=1.98
        )
        
        assert item.product == sample_product
        assert item.quantity == 2
        assert item.price == 0.99
        assert item.total_price == 1.98

    def test_total_price_mismatch(self, sample_product):
        with pytest.raises(ValueError, match=r"total_price must equal quantity \* price"):
            ReceiptItem(sample_product, 2, 0.99, 1.50)  
    
    
    @pytest.mark.parametrize("quantity, price, total_price", [
        (1, 1.50, 1.50),      
        (1000, 0.01, 10.00),  
        (1, 0.0, 0.0),
    ], ids=["single", "bulk", "free"])
    def test_various_valid_combinations(self, sample_product, quantity, price, total_price):
        item = ReceiptItem(sample_product, quantity, price, total_price)
        assert item.total_price == total_price



    @pytest.mark.parametrize("quantity, price, total_price, expected_error, error_pattern", [
    # Invalid quantities
    (-1, 0.99, -0.99, ValueError, r"quantity must be >= 0"),
    (None, 0.99, 0.99, TypeError, r"quantity must be positive"),
    (0, 0.99, 0.99, TypeError, r"quantity must be positive"),
    ("two", 0.99, 1.98, TypeError, r"quantity must be numeric"),
    
    # Invalid prices
    (2, -0.99, -1.98, ValueError, r"price must be >= 0"),
    (2, None, 1.98, TypeError, r"price must be numeric"),
    (2, "free", 1.98, TypeError, r"price must be numeric"),
    
    # Invalid total prices
    (2, 0.99, None, TypeError, r"total_price must be numeric"),
    (2, 0.99, "two", TypeError, r"total_price must be numeric"),
    ], ids=[
        "neg-qty", "none-qty", "zero-qty", "str-qty",
        "neg-price", "none-price", "str-price",
        "none-total", "str-total"
    ])
    def test_invalid_attributes(self, sample_product, quantity, price, total_price,
                            expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            ReceiptItem(
                product=sample_product,
                quantity=quantity,
                price=price,
                total_price=total_price
        )

    def test_invalid_creation_with_none_product(self):
        with pytest.raises(TypeError, match=r"product cannot be None"):
            ReceiptItem(None, 1, 1.0, 1.0)




    