import pytest

from digitz import PhoneNumber
from digitz.enums import PhoneNumberFormat, PhoneNumberType
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)

from digitz.undefined import Undefined


US_EXAMPLE_NUMBER = "+1 (201) 555-0123"


@pytest.fixture
def num_usa() -> PhoneNumber:
    return PhoneNumber.parse(US_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_toll_free():
    return PhoneNumber.parse("+1 (800) 234-5678")


@pytest.fixture
def num_usa_voip():
    return PhoneNumber.parse("+1 (305) 209-0123")


@pytest.fixture
def num_usa_invalid():
    return PhoneNumber.parse("+1 (201) 555-012")


@pytest.fixture
def num_can():
    return PhoneNumber.parse("+1 (506) 234-5678")


@pytest.fixture
def num_mex():
    return PhoneNumber.parse("+52 200 123 4567")


def test_parse():
    assert isinstance(PhoneNumber.parse(US_EXAMPLE_NUMBER), PhoneNumber)


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


def test_national_significant_number(num_usa: PhoneNumber):
    assert num_usa.national_significant_number == "2015550123"


def test_national_destination_code_length(
    num_usa: PhoneNumber, num_usa_invalid: PhoneNumber, num_mex: PhoneNumber
):
    assert num_usa.national_destination_code_length == 3
    assert num_usa_invalid.national_destination_code_length == 0
    assert num_mex.national_destination_code_length == 3


def test_national_destination_code(
    num_usa: PhoneNumber, num_usa_invalid: PhoneNumber, num_mex: PhoneNumber
):
    assert num_usa.national_destination_code == "201"
    assert num_usa_invalid.national_destination_code == ""
    assert num_mex.national_destination_code == "200"


def test_subscriber_number(num_usa: PhoneNumber):
    assert num_usa.subscriber_number == "5550123"


def test_number_type(num_usa: PhoneNumber):
    assert num_usa.number_type == PhoneNumberType.FIXED_LINE_OR_MOBILE


def test_region_code(num_usa: PhoneNumber, num_can: PhoneNumber, num_mex: PhoneNumber):
    assert num_usa.region_code == "US"
    assert num_can.region_code == "CA"
    assert num_mex.region_code == "MX"


def test_timezones(num_usa: PhoneNumber, num_can: PhoneNumber, num_mex: PhoneNumber):
    assert num_usa.timezones == ("America/New_York",)
    assert num_can.timezones == ('America/Halifax',)
    assert num_mex.timezones == ('America/Mexico_City', 'America/Tijuana')


def test_get_carrier_name(
    num_usa: PhoneNumber, num_can: PhoneNumber, num_mex: PhoneNumber
):
    assert num_usa.get_carrier_name(lang="en") == ""
    assert num_can.get_carrier_name(lang="en") == ""
    assert num_mex.get_carrier_name(lang="en") == ""


def test_get_country_name(
    num_usa: PhoneNumber, num_can: PhoneNumber, num_mex: PhoneNumber
):
    assert num_usa.get_country_name(lang="en") == "United States"
    assert num_can.get_country_name(lang="en") == "Canada"
    assert num_mex.get_country_name(lang="en") == "Mexico"


def test_get_description(
    num_usa: PhoneNumber, num_can: PhoneNumber, num_mex: PhoneNumber
):
    assert num_usa.get_description(lang="en") == "New Jersey"
    assert num_can.get_description(lang="en") == "New Brunswick"
    assert num_mex.get_description(lang="en") == "Mexico"


def test_is_geographical(num_usa: PhoneNumber, num_usa_toll_free: PhoneNumber):
    assert num_usa.is_geographical is True
    assert num_usa_toll_free.is_geographical is False


def test_is_possible(num_usa: PhoneNumber, num_usa_invalid: PhoneNumber):
    assert num_usa.is_possible is True
    assert num_usa_invalid.is_possible is False


def test_is_valid(num_usa: PhoneNumber, num_usa_invalid: PhoneNumber):
    assert num_usa.is_valid is True
    assert num_usa_invalid.is_valid is False


def test_is_toll_free(num_usa: PhoneNumber, num_usa_toll_free: PhoneNumber):
    assert num_usa_toll_free.is_toll_free is True
    assert num_usa.is_toll_free is False


def test_is_voip(num_usa: PhoneNumber, num_usa_voip: PhoneNumber):
    assert num_usa_voip.is_voip is True
    assert num_usa.is_voip is False


def test_format(num_usa: PhoneNumber):
    assert num_usa.format(format=PhoneNumberFormat.E164) == "+12015550123"


def test_to_international(num_usa: PhoneNumber):
    assert num_usa.to_international() == "+1 201-555-0123"


def test_to_national(num_usa: PhoneNumber):
    assert num_usa.to_national() == "(201) 555-0123"


def test_e164_format(num_usa: PhoneNumber):
    assert num_usa.to_e164() == "+12015550123"


def test_to_rfc3966(num_usa: PhoneNumber):
    assert num_usa.to_rfc3966() == "tel:+1-201-555-0123"


def test_replace_country_code(num_usa: PhoneNumber):
    num = num_usa.replace(country_code=44)
    assert num.country_code == 44


def test_replace_national_number(num_usa: PhoneNumber):
    num = num_usa.replace(national_number=8002345678)
    assert num.national_number == 8002345678


def test_replace_extension(num_usa: PhoneNumber):
    num = num_usa.replace(extension="1234")
    assert num.extension == "1234"


def test_replace_leading_italian_zero(num_usa: PhoneNumber):
    num = num_usa.replace(italian_leading_zero=True)
    assert num.italian_leading_zero is True


def test_replace_number_of_leading_zeros(num_usa: PhoneNumber):
    num = num_usa.replace(number_of_leading_zeros=1)
    assert num.number_of_leading_zeros == 1


def test_undefined():
    assert bool(Undefined) is False
    assert repr(Undefined) == "Undefined"
