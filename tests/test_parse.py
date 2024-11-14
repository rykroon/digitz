import pytest

from digitz import PhoneNumber, FrozenPhoneNumber
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)

US_EXAMPLE_NUMBER = "+1 (201) 555-0123"


def test_parse():
    assert isinstance(PhoneNumber.parse(US_EXAMPLE_NUMBER), PhoneNumber)
    assert isinstance(FrozenPhoneNumber.parse(US_EXAMPLE_NUMBER), FrozenPhoneNumber)


def test_parse_invalid_country_code():
    with pytest.raises(InvalidCountryCode):
        PhoneNumber.parse("+999 (201) 555-0123")


def test_parse_not_a_number():
    with pytest.raises(NotANumber):
        PhoneNumber.parse("foo")


def test_parse_too_long():
    with pytest.raises(TooLong):
        PhoneNumber.parse("+1 (201) 555-0123012301230123")


def test_parse_too_short_after_idd():
    with pytest.raises(TooShortAfterIDD):
        PhoneNumber.parse("011", region="US")


def test_parse_too_short_nsn():
    with pytest.raises(TooShortNsn):
        PhoneNumber.parse("+44 2")