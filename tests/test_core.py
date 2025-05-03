import pytest
from formatting_module.core import format_phone_number, format_currency


def test_format_phone_number_10_digits():
    assert format_phone_number("1234567890") == "(123) 456-7890"

def test_format_phone_number_11_digits_with_1():
    assert format_phone_number("1-234-567-8901") == "+1 (234) 567-8901"

@pytest.mark.parametrize("bad", ["1234", "abcdefghij"])
def test_format_phone_number_errors(bad):
    with pytest.raises(ValueError):
        format_phone_number(bad)

def test_format_currency_positive():
    assert format_currency(1234.5) == "$1,234.50"

def test_format_currency_negative():
    assert format_currency(-99.9, symbol="€") == "-€99.90"

