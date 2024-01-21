import pytest

import digitz as dg
from digitz import PhoneNumberType
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
    assert isinstance(dg.parse(US_EXAMPLE_NUMBER), dg.PhoneNumber)
    assert isinstance(dg.parse(US_EXAMPLE_NUMBER, numcls=dg.FrozenPhoneNumber), dg.FrozenPhoneNumber)
    assert isinstance(dg.parse(US_EXAMPLE_NUMBER, numcls=dg.PhoneNumberTuple), dg.PhoneNumberTuple)


def test_parse_invalid_country_code():
    with pytest.raises(InvalidCountryCode):
        dg.parse("+999 (201) 555-0123")


def test_parse_not_a_number():
    with pytest.raises(NotANumber):
        dg.parse("foo")


def test_parse_too_long():
    with pytest.raises(TooLong):
        dg.parse("+1 (201) 555-0123012301230123")


def test_parse_too_short_after_idd():
    with pytest.raises(TooShortAfterIDD):
        dg.parse("011", region="US")


def test_parse_too_short_nsn():
    with pytest.raises(TooShortNsn):
        dg.parse("+44 2")


def test_get_country_name_str():
    assert dg.get_country_name(US_EXAMPLE_NUMBER) == "United States"
    assert dg.get_country_name(CA_EXAMPLE_NUMBER) == "Canada"
    assert dg.get_country_name(MX_EXAMPLE_NUMBER) == "Mexico"


def test_get_country_name_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    num_ca = dg.parse(CA_EXAMPLE_NUMBER)
    num_mx = dg.parse(MX_EXAMPLE_NUMBER)

    assert dg.get_country_name(num_us) == "United States"
    assert dg.get_country_name(num_ca) == "Canada"
    assert dg.get_country_name(num_mx) == "Mexico"


def test_get_description_str():
    assert dg.get_description(US_EXAMPLE_NUMBER) == "New Jersey"
    assert dg.get_description(CA_EXAMPLE_NUMBER) == "New Brunswick"
    assert dg.get_description(MX_EXAMPLE_NUMBER) == "Mexico"


def test_get_description_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    num_ca = dg.parse(CA_EXAMPLE_NUMBER)
    num_mx = dg.parse(MX_EXAMPLE_NUMBER)

    assert dg.get_description(num_us) == "New Jersey"
    assert dg.get_description(num_ca) == "New Brunswick"
    assert dg.get_description(num_mx) == "Mexico"


def test_get_number_type_str():
    assert dg.get_number_type(US_TOLL_FREE_EXAMPLE_NUMBER) == PhoneNumberType.TOLL_FREE


def test_get_number_type_phn():
    num_us = dg.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert dg.get_number_type(num_us) == PhoneNumberType.TOLL_FREE


def test_get_region_code_str():
    assert dg.get_region_code(US_EXAMPLE_NUMBER) == "US"
    assert dg.get_region_code(CA_EXAMPLE_NUMBER) == "CA"
    assert dg.get_region_code(MX_EXAMPLE_NUMBER) == "MX"


def test_get_region_code_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    num_ca = dg.parse(CA_EXAMPLE_NUMBER)
    num_mx = dg.parse(MX_EXAMPLE_NUMBER)

    assert dg.get_region_code(num_us) == "US"
    assert dg.get_region_code(num_ca) == "CA"
    assert dg.get_region_code(num_mx) == "MX"


def test_get_timezones_str():
    assert dg.get_timezones(US_EXAMPLE_NUMBER) == ("America/New_York",)
    assert dg.get_timezones(CA_EXAMPLE_NUMBER) == ('America/Halifax',)
    assert dg.get_timezones(MX_EXAMPLE_NUMBER) == ('America/Mexico_City', 'America/Tijuana')


def test_get_timezones_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    num_ca = dg.parse(CA_EXAMPLE_NUMBER)
    num_mx = dg.parse(MX_EXAMPLE_NUMBER)

    assert dg.get_timezones(num_us) == ("America/New_York",)
    assert dg.get_timezones(num_ca) == ('America/Halifax',)
    assert dg.get_timezones(num_mx) == ('America/Mexico_City', 'America/Tijuana')


def test_is_possible_str():
    assert dg.is_possible(US_EXAMPLE_NUMBER) is True


def test_is_possible_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.is_possible(num_us) is True


def test_is_valid_str():
    assert dg.is_valid(US_EXAMPLE_NUMBER) is True


def test_is_valid_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.is_valid(num_us) is True


def test_is_valid_false_str():
    assert dg.is_valid(US_INVALID_EXAMPLE_NUMBER) is False


def test_is_valid_false_phn():
    num_us = dg.parse(US_INVALID_EXAMPLE_NUMBER)
    assert dg.is_valid(num_us) is False


def test_is_toll_free_str():
    assert dg.is_toll_free(US_TOLL_FREE_EXAMPLE_NUMBER) is True


def test_is_toll_free_phn():
    num_us = dg.parse(US_TOLL_FREE_EXAMPLE_NUMBER)
    assert dg.is_toll_free(num_us) is True


def test_to_international_str():
    assert dg.to_international(US_EXAMPLE_NUMBER) == "+1 201-555-0123"


def test_to_international_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_international(num_us) == "+1 201-555-0123"


def test_to_national_str():
    assert dg.to_national(US_EXAMPLE_NUMBER) == "(201) 555-0123"


def test_to_national_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_national(num_us) == "(201) 555-0123"


def test_to_e164_str():
    assert dg.to_e164(US_EXAMPLE_NUMBER) == "+12015550123"


def test_to_e164_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_e164(num_us) == "+12015550123"


def test_to_rfc3966_str():
    assert dg.to_rfc3966(US_EXAMPLE_NUMBER) == "tel:+1-201-555-0123"


def test_to_rfc3966_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_rfc3966(num_us) == "tel:+1-201-555-0123"


def to_tuple_str():
    assert dg.to_tuple(US_EXAMPLE_NUMBER) == (
        1,
        201,
        5550123,
        None,
        None,
        None,
        None,
        None,
    )


def to_tuple_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_tuple(num_us) == (
        1,
        201,
        5550123,
        None,
        None,
        None,
        None,
        None,
    )


def to_dict_str():
    assert dg.to_dict(US_EXAMPLE_NUMBER) == {
        "country_code": 1,
        "national_number": 2015550123,
        "extension": None,
        "italian_leading_zero": None,
        "number_of_leading_zeros": None,
        "raw_input": None,
        "country_code_source": None,
        "preferred_domestic_carrier_code": None,
    }


def to_dict_phn():
    num_us = dg.parse(US_EXAMPLE_NUMBER)
    assert dg.to_dict(num_us) == {
        "country_code": 1,
        "national_number": 2015550123,
        "extension": None,
        "italian_leading_zero": None,
        "number_of_leading_zeros": None,
        "raw_input": None,
        "country_code_source": None,
        "preferred_domestic_carrier_code": None,
    }
