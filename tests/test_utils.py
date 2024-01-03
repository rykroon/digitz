from digitz import parse, PhoneNumberType
from digitz.utils import (
    get_carrier_name,
    get_country_name,
    get_description,
    get_number_type,
    get_region_code,
    get_timezones,
    is_possible_number,
    is_valid_number,
    to_e164,
    to_international,
    to_national,
    to_rfc3966,
)


# def test_get_country_name():
#     assert get_country_name("+1 (202) 555-0192") == "United States"
#     numtup = parse("+1 (202) 555-0192")
#     assert get_country_name(numtup) == "United States"


# def test_get_country_name_fr():
#     assert get_country_name("+1 (202) 555-0192", "fr") == "États-Unis"
#     numtup = parse("+1 (202) 555-0192")
#     assert get_country_name(numtup, "fr") == "États-Unis"


# def test_get_description():
#     assert get_description("+1 (202) 555-0192") == "Washington, DC"
#     numtup = parse("+1 (202) 555-0192")
#     assert get_description(numtup) == "Washington, DC"

# def test_get_carrier_name():
#     assert get_carrier_name("+1 (202) 555-0192") == ""
#     numtup = parse("+1 (202) 555-0192")
#     assert get_carrier_name(numtup) == ""


def test_get_number_type():
    assert get_number_type("+1 (800) 555-0192") == PhoneNumberType.TOLL_FREE
    numtup = parse("+1 (800) 555-0192")
    assert get_number_type(numtup) == PhoneNumberType.TOLL_FREE


def get_region_code():
    assert get_region_code("+1 (202) 555-0192") == "US"
    numtup = parse("+1 (202) 555-0192")
    assert get_region_code(numtup) == "US"


def test_is_possible_number():
    assert is_possible_number("+1 (202) 555-0192") is True
    numtup = parse("+1 (202) 555-0192")
    assert is_possible_number(numtup) is True


def test_is_valid_number():
    assert is_valid_number("+1 (202) 555-0192") is True
    numtup = parse("+1 (202) 555-0192")
    assert is_valid_number(numtup) is True


def test_get_timezones():
    assert get_timezones("+1 (202) 555-0192") == ("America/New_York",)
    numtup = parse("+1 (202) 555-0192")
    assert get_timezones(numtup) == ("America/New_York",)


def test_to_e164():
    assert to_e164("+1 (202) 555-0192") == "+12025550192"
    numtup = parse("+1 (202) 555-0192")
    assert to_e164(numtup) == "+12025550192"


def test_to_international():
    assert to_international("+1 (202) 555-0192") == "+1 202-555-0192"
    numtup = parse("+1 (202) 555-0192")
    assert to_international(numtup) == "+1 202-555-0192"


def test_to_national():
    assert to_national("+1 (202) 555-0192") == "(202) 555-0192"
    numtup = parse("+1 (202) 555-0192")
    assert to_national(numtup) == "(202) 555-0192"


def test_to_rfc3966():
    assert to_rfc3966("+1 (202) 555-0192") == "tel:+1-202-555-0192"
    numtup = parse("+1 (202) 555-0192")
    assert to_rfc3966(numtup) == "tel:+1-202-555-0192"
