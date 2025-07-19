import pytest
from model_objects import Product, ProductUnit, Discount

class TestDiscount:
    @pytest.fixture
    def sample_product(self):
        return Product("toothbrush", ProductUnit.EACH)


    def test_valid_creation(self, sample_product):
        discount = Discount(sample_product, "Summer Sale", -1.99)
        assert discount.product == sample_product
        assert discount.description == "Summer Sale"
        assert discount.discount_amount == -1.99




    @pytest.mark.parametrize("description, amount, expected_error, error_pattern", [
    # Invalid Descriptions
    (None, -1.99, ValueError, r"description cannot be None"),
    ("", -1.99, ValueError, r"description cannot be empty"),
    (123, -1.99, TypeError, r"description must be string"),
    
    # Invalid Amounts
    ("Valid", None, TypeError, r"amount cannot be None"),
    ("Valid", "1.99", TypeError, r"amount must be numeric"),
    ("Valid", 0, ValueError, r"amount must be negative"),
    ("Valid", 1.99, ValueError, r"amount must be negative"),
    ], ids=[
        "none-desc", "empty-desc", "non-str-desc",
        "none-amount", "str-amount", "zero-amount", "positive-amount"
    ])
    def test_invalid_discount_attributes(self, sample_product, description, amount, 
                                    expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            Discount(
                product=sample_product,
                description=description,
                discount_amount=amount
            )

    def test_invalid_creation_with_none_product(self):

        with pytest.raises(ValueError, match=r"product cannot be None"):
            Discount(None, "Valid", -1.99)


    def test_large_discount_amount(self, sample_product):
        discount = Discount(sample_product, "Clearance", -9999.99)
        assert discount.discount_amount == -9999.99

