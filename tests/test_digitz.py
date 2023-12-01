from digitz import PhoneNumber, PhoneNumberType
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)

import pytest


def test_parse():
    num = PhoneNumber.parse("+1 (202) 555-0192")


def test_parse_invalid_country_code():
    with pytest.raises(InvalidCountryCode):
        PhoneNumber.parse("+999 (202) 555-0192")


def test_parse_not_a_number():
    with pytest.raises(NotANumber):
        PhoneNumber.parse("foo")


def test_parse_too_long():
    with pytest.raises(TooLong):
        PhoneNumber.parse("+1 (202) 555-01923456789012345678901234567890")


# def test_parse_too_short_after_idd():
#     with pytest.raises(TooShortAfterIDD):
#         PhoneNumber.parse("+1 (202) 555-0192")


def test_parse_too_short_nsn():
    with pytest.raises(TooShortNsn):
        PhoneNumber.parse("+44 2")


def test_region_code():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.region_code == "US"

    num = PhoneNumber.parse("+1 (204) 555-0192")
    assert num.region_code == "CA"

    num = PhoneNumber.parse("+52 55 1234 5678")
    assert num.region_code == "MX"


# def test_get_country_name():
#     num = PhoneNumber.parse("+1 (202) 555-0192")
#     assert num.get_country_name() == "United States"


# def test_get_country_name_fr():
#     num = PhoneNumber.parse("+1 (202) 555-0192")
#     assert num.get_country_name("fr") == "États-Unis"


# def test_get_description():
#     num = PhoneNumber.parse("+1 (202) 555-0192")
#     assert num.get_description() == "Washington, DC"


def test_number_type():
    num = PhoneNumber.parse("+1 (800) 555-0192")
    assert num.number_type == PhoneNumberType.TOLL_FREE


def test_is_possible():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.is_possible() is True


def test_is_possible_false():
    num = PhoneNumber.parse("+ (123) 456-7890")
    assert num.is_possible() is False


def test_is_valid():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.is_valid() is True


def test_is_valid_false():
    num = PhoneNumber.parse("+ (123) 456-7890")
    assert num.is_valid() is False


def test_is_toll_free():
    num = PhoneNumber.parse("+1 (800) 555-0192")
    assert num.is_toll_free() is True


def test_repr():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert repr(num) == "<PhoneNumber: +1 202-555-0192>"


def test_str():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert str(num) == "+12025550192"


def test_to_international():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.to_international() == "+1 202-555-0192"


def test_to_national():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.to_national() == "(202) 555-0192"


def test_to_e164():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.to_e164() == "+12025550192"


def test_to_rfc3966():
    num = PhoneNumber.parse("+1 (202) 555-0192")
    assert num.to_rfc3966() == "tel:+1-202-555-0192"
