import pytest
from model_objects import Product, SpecialOfferType , Offer , ProductUnit

class TestOffer:

    @pytest.fixture
    def sample_product(self):
        return Product("toothbrush", ProductUnit.EACH)


    @pytest.mark.parametrize("offer_type, argument", [
        (SpecialOfferType.TEN_PERCENT_DISCOUNT, 10.0),
        (SpecialOfferType.THREE_FOR_TWO, 3.0),
        (SpecialOfferType.TWO_FOR_AMOUNT, 5.0),
        (SpecialOfferType.FIVE_FOR_AMOUNT, 7.49),
    ], ids=["percent", "3-for-2", "2-for-amount", "5-for-amount"])
    def test_valid_offer_creation(self, sample_product, offer_type, argument):
        offer = Offer(offer_type, sample_product, argument)
        assert offer.offer_type == offer_type
        assert offer.product == sample_product
        assert offer.argument == argument


    @pytest.mark.parametrize("offer_type, argument, expected_error, error_pattern", [
    # Invalid Offer Types
    (None, 10, ValueError, r"offer_type cannot be None"),
    ("invalid", 10, ValueError, r"Invalid offer type"),
    
    # Invalid Arguments
    (SpecialOfferType.TEN_PERCENT_DISCOUNT, "10", TypeError, r"numeric argument"),
    (SpecialOfferType.TEN_PERCENT_DISCOUNT, -5.0, ValueError, r"positive argument"),
    (SpecialOfferType.TEN_PERCENT_DISCOUNT, None, ValueError, r"argument cannot be None"),
    ], ids=[
        "none-offer-type", "str-offer-type",
        "str-argument", "negative-argument", "none-argument"
    ])
    def test_invalid_offer_attributes(self, sample_product, offer_type, argument, 
                                    expected_error, error_pattern):
        with pytest.raises(expected_error, match=error_pattern):
            Offer(
                offer_type=offer_type,
                product=sample_product,
                argument=argument
            )

    def test_invalid_creation_with_none_product(self):
        with pytest.raises(ValueError, match=r"product cannot be None"):
            Offer(
                offer_type=SpecialOfferType.TEN_PERCENT_DISCOUNT,
                product=None,
                argument=10
            )
