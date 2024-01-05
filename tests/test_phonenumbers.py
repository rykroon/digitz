import pytest

from digitz import PhoneNumber, PhoneNumberType
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


US_EXAMPLE_NUMBER = "+1 (201) 555-0123"
US_TOLL_FREE_EXAMPLE_NUMBER = "+1 (800) 234-5678"
US_INVALID_EXAMPLE_NUMBER = "+1 (201) 555-012"
CA_EXAMPLE_NUMBER = "+1 (506) 234-5678"
MX_EXAMPLE_NUMBER = "+52 200 123 4567"


def test_parse():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)


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


def test_region_code():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.region_code == "US"

    num = PhoneNumber.parse(CA_EXAMPLE_NUMBER)
    assert num.region_code == "CA"

    num = PhoneNumber.parse(MX_EXAMPLE_NUMBER)
    assert num.region_code == "MX"


def test_number_type():
    num = PhoneNumber.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert num.number_type == PhoneNumberType.TOLL_FREE


def test_is_possible():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.is_possible() is True


def test_is_valid():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.is_valid() is True


def test_is_valid_false():
    num = PhoneNumber.parse(US_INVALID_EXAMPLE_NUMBER)
    assert num.is_valid() is False


def test_is_toll_free():
    num = PhoneNumber.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert num.is_toll_free() is True


def test_str():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert str(num) == "+12015550123"


def test_to_international():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.to_international() == "+1 201-555-0123"


def test_to_national():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.to_national() == "(201) 555-0123"


def test_to_e164():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.to_e164() == "+12015550123"


def test_to_rfc3966():
    num = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num.to_rfc3966() == "tel:+1-201-555-0123"
