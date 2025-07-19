import pytest
from model_objects import Product, ProductUnit , Discount
from receipt import ReceiptItem , Receipt
from receipt_printer import ReceiptPrinter

class TestReceiptPrinter:

    @pytest.fixture
    def sample_item(self):
        return ReceiptItem(Product("Toothbrush", ProductUnit.EACH), 2, 0.99, 1.98)

    def test_print_price_formats_correctly(self):
        printer = ReceiptPrinter()
        assert printer.print_price(0.99) == "0.99"
        assert printer.print_price(1.005) == "1.00"
        assert printer.print_price(0) == "0.00"
        assert printer.print_price(-1.5) == "-1.50"

    @pytest.mark.parametrize("unit, quantity, expected", [
        (ProductUnit.EACH, 3, "3"),
        (ProductUnit.KILO, 1.5, "1.500"),
    ], ids=["each-integer",  "kilo-decimal",])
    def test_print_quantity(self, unit, quantity, expected):
        item = ReceiptItem(Product("test", unit), quantity, 0.0, 0.0)
        assert ReceiptPrinter().print_quantity(item) == expected

    # ---- Test Line Formatting ----

    # @pytest.mark.parametrize("columns, name, price, expected", [
    #     (10, "Apple", "1.99", "Apple  1.99\n"),
    #     (20, "Toothbrush", "0.99", "Toothbrush        0.99\n"),
    #     (30, "A very long product name", "1.99", "A very long product name     1.99\n"),
    # ], ids=["narrow-column", "medium-column", "long-name-truncation"])
    # def test_format_line_with_whitespace(self, columns, name, price, expected):
    #     printer = ReceiptPrinter(columns=columns)
    #     assert printer.format_line_with_whitespace(name, price) == expected

    # ---- Test Receipt Item Printing ----



    def test_print_receipt_item_single_quantity(self):
        item = ReceiptItem(Product("Apple", ProductUnit.EACH), 1, 1.99, 1.99)
        expected = "Apple                          1.99\n"
        assert ReceiptPrinter().print_receipt_item(item) == expected

    def test_print_receipt_item_multi_quantity(self, sample_item):
        expected = (
            "Toothbrush                     1.98\n"
            "  0.99 * 2\n"
        )
        assert ReceiptPrinter().print_receipt_item(sample_item) == expected

 

    @pytest.mark.parametrize("desc, amount, expected_line", [
        ("10% off", -0.099, "10% off (Toothbrush)            -0.10\n"),
        ("2 for 1.50", -0.48, "2 for 1.50 (Toothbrush)                -0.48\n"),
    ], ids=["percent-discount", "absolute-discount"])
    def test_print_discount(self, sample_item, desc, amount, expected_line):
        discount = Discount(sample_item.product, desc, amount)
        assert ReceiptPrinter().print_discount(discount) == expected_line

    # ---- Test Total Line ----

    def test_present_total(self):
        class MockReceipt:
            def total_price(self):
                return 3.97
        
        expected = "Total:                         3.97\n"
        assert ReceiptPrinter().present_total(MockReceipt()) == expected



