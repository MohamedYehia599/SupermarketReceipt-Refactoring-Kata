import pytest
from model_objects import Product, ProductUnit , Discount
from receipt import Receipt, ReceiptItem

class TestReceipt:
    @pytest.fixture
    def receipt(self):
        return Receipt()
    
    @pytest.fixture
    def sample_product(self):
        return Product("toothbrush", ProductUnit.EACH)

    @pytest.fixture
    def one_toothbrush_ten_percent_discount(self,sample_product):
        return Discount(sample_product," 10 % OFF",- 0.099)
                                        

    def test_empty_receipt(self,receipt):
        assert receipt.total_price() == 0
        assert len(receipt.items) == 0
        assert len(receipt.discounts) == 0

    def test_receipt_add_product_without_discount(self,receipt,sample_product):
        receipt.add_product(sample_product,2,0.99,1.98)
        assert receipt.total_price() == 1.98
        assert len(receipt.items) == 1
        assert len(receipt.discounts) == 0
    
    
    def test_total_amount_float_precision(self, receipt, sample_product):
        receipt.add_product(sample_product, 3, 0.33, 0.99)
        assert receipt.total_price() == pytest.approx(0.99)
    
    def test_receipt_add_multiple_products(self, receipt, sample_product):
        receipt.add_product(
            product=sample_product,
            quantity=2,
            price=0.99,
            total_price=1.98
        )
        

        apples = Product("apples", ProductUnit.KILO)
        receipt.add_product(
            product=apples,
            quantity=1.5,
            price=1.99,
            total_price=2.99
        )
        
        assert len(receipt.items) == 2
        assert receipt.total_price() == pytest.approx(4.97)
        

    def test_receipt_item_values(self,receipt, sample_product):
        receipt.add_product(sample_product,2,0.99,1.98)
        item = receipt.items[0]
        assert item.product == sample_product
        assert item.quantity == 2
        assert item.price == 0.99
        assert item.total_price == 1.98

    def test_receipt_add_product_with_discount(self,receipt,sample_product,one_toothbrush_ten_percent_discount):
        receipt.add_product(sample_product,1,0.99,0.99)
        receipt.add_discount(one_toothbrush_ten_percent_discount)
        assert receipt.total_price() == 0.891
        assert len(receipt.items) == 1
        assert len(receipt.discounts) == 1

    
    def test_add_zero_quantity_product(self,receipt, sample_product):
        receipt.add_product(sample_product, 0, 0.99, 0)
        assert receipt.total_price() == 0
        assert len(receipt.items) == 1

    def test_total_amount_with_positive_discount(self, receipt, sample_product):
        invalid_discount = Discount(sample_product, "Invalid", 0.50)
        receipt.add_product(sample_product, 1, 0.99, 0.99)
        receipt.add_discount(invalid_discount)
        assert receipt.total_price() == 0.49
    
    def test_total_amount_with_discount_exceeds_total(self, receipt, sample_product):
        receipt.add_product(sample_product, 1, 0.99, 0.99)
        receipt.add_discount(Discount(sample_product, "Huge Discount", -1.50))
        assert receipt.total_price() == 0.0

    def test_duplicate_products(self, receipt, sample_product):
        receipt.add_product(sample_product, 1, 0.99, 0.99)
        receipt.add_product(sample_product, 1, 0.99, 0.99)
        assert len(receipt.items) == 1
        assert receipt.items[0].quantity == 2 
        assert receipt.total_price() == pytest.approx(1.98)

    def test_add_negative_price_product(self,receipt, sample_product):
        with pytest.raises(ValueError,match="price must be positive"):
            receipt.add_product(sample_product, 1, -0.99, -0.99)

    
    def test_add_negative_quantity_product(self,receipt, sample_product):
        with pytest.raises(ValueError,match="quantity must be positive"):
            receipt.add_product(sample_product, -1, 0.99, -0.99)

    def test_discount_on_non_existent_product(self, receipt, sample_product, one_toothbrush_ten_percent_discount):
        with pytest.raises(ValueError, match="Cannot apply discount: product not in receipt"):
            receipt.add_discount(one_toothbrush_ten_percent_discount)

    def test_multiple_discounts_same_product(self,receipt, sample_product):
        #unclear business case but we will assume its right
        receipt.add_product(sample_product, 5, 0.99, 4.95)
        receipt.add_discount(Discount(sample_product, "Bulk", -1.00))
        receipt.add_discount(Discount(sample_product, "Sale", -0.50))
        assert receipt.total_price() == pytest.approx(3.45)
        assert len(receipt.discounts) == 2
        

