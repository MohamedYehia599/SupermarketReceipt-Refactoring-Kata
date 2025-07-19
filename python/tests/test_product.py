import pytest
from model_objects import Product, ProductUnit

class TestProduct:

    def test_valid_creation(self):
        product = Product("toothbrush", ProductUnit.EACH)
        assert product.name == "toothbrush"
        assert product.unit == ProductUnit.EACH


    def test_product_equality(self):
        p1 = Product("toothbrush", ProductUnit.EACH)
        p2 = Product("toothbrush", ProductUnit.EACH)
        assert p1 == p2



    @pytest.mark.parametrize("name, unit, expected_error, error_pattern", [
        # Invalid names
        (None, ProductUnit.EACH, ValueError, r"name cannot be None"),
        ("", ProductUnit.EACH, ValueError, r"name cannot be empty"),
        (" ", ProductUnit.EACH, ValueError, r"name cannot be whitespace"),
        (123, ProductUnit.EACH, TypeError, r"name must be string"),
        
        # Invalid units
        ("apple", None, ValueError, r"unit cannot be None"),
        ("apple", "invalid_unit", ValueError, r"unit must be ProductUnit"),
        
        # Edge case
        ("A"*101, ProductUnit.EACH, ValueError, r"name too long"),  # If length limit exists
    ], ids=[
        "none-name", "empty-name", "whitespace-name", "non-str-name",
        "none-unit", "str-unit",
        "long-name"
    ])
    def test_invalid_creation(self, name, unit, expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            Product(name, unit)