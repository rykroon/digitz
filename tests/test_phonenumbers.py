import pytest

from digitz import PhoneNumberType, PhoneNumber, FrozenPhoneNumber
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


def test_get_country_name_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    num_ca = PhoneNumber.parse(CA_EXAMPLE_NUMBER)
    num_mx = PhoneNumber.parse(MX_EXAMPLE_NUMBER)

    assert num_us.get_country_name() == "United States"
    assert num_ca.get_country_name() == "Canada"
    assert num_mx.get_country_name() == "Mexico"


def test_get_description_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    num_ca = PhoneNumber.parse(CA_EXAMPLE_NUMBER)
    num_mx = PhoneNumber.parse(MX_EXAMPLE_NUMBER)

    assert num_us.get_description() == "New Jersey"
    assert num_ca.get_description() == "New Brunswick"
    assert num_mx.get_description() == "Mexico"


def test_get_number_type_phn():
    num_us = PhoneNumber.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert num_us.get_number_type() == PhoneNumberType.TOLL_FREE


def test_get_region_code_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    num_ca = PhoneNumber.parse(CA_EXAMPLE_NUMBER)
    num_mx = PhoneNumber.parse(MX_EXAMPLE_NUMBER)

    assert num_us.get_region_code() == "US"
    assert num_ca.get_region_code() == "CA"
    assert num_mx.get_region_code() == "MX"


def test_get_timezones_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    num_ca = PhoneNumber.parse(CA_EXAMPLE_NUMBER)
    num_mx = PhoneNumber.parse(MX_EXAMPLE_NUMBER)

    assert num_us.get_timezones() == ("America/New_York",)
    assert num_ca.get_timezones() == ('America/Halifax',)
    assert num_mx.get_timezones() == ('America/Mexico_City', 'America/Tijuana')


def test_is_possible_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.is_possible() is True


def test_is_valid_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.is_valid() is True


def test_is_valid_false_phn():
    num_us = PhoneNumber.parse(US_INVALID_EXAMPLE_NUMBER)
    assert num_us.is_valid() is False


def test_is_toll_free_phn():
    num_us = PhoneNumber.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert num_us.is_toll_free() is True


def test_to_international_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.to_international() == "+1 201-555-0123"


def test_to_national_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.to_national() == "(201) 555-0123"


def test_to_e164_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.to_e164() == "+12015550123"


def test_to_rfc3966_phn():
    num_us = PhoneNumber.parse(US_EXAMPLE_NUMBER)
    assert num_us.to_rfc3966() == "tel:+1-201-555-0123"
