from dataclasses import FrozenInstanceError
import pytest

from digitz import PhoneNumber
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)
import phonenumbers as pn
from phonenumbers.carrier import name_for_number
from phonenumbers.geocoder import country_name_for_number, description_for_number
from phonenumbers.timezone import time_zones_for_number


USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"
CAN_EXAMPLE_NUMBER = "+1 506-234-5678"
MEX_EXAMPLE_NUMBER = "+52 200 123 4567"
ITA_EXAMPLE_NUMBER = "+39 02 1234 5678"

USA_TOLL_FREE_EXAMPLE_NUMBER = "+1 800-234-5678"
USA_VOIP_EXAMPLE_NUMBER = "+1 305-209-0123"
USA_INVALID_EXAMPLE_NUMBER = "+1 201555012"


@pytest.fixture
def num_usa() -> PhoneNumber:
    return PhoneNumber.parse(USA_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_pn() -> pn.PhoneNumber:
    return pn.parse(USA_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_toll_free() -> PhoneNumber:
    return PhoneNumber.parse(USA_TOLL_FREE_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_toll_free_pn() -> pn.PhoneNumber:
    return pn.parse(USA_TOLL_FREE_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_voip() -> PhoneNumber:
    return PhoneNumber.parse(USA_VOIP_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_voip_pn() -> pn.PhoneNumber:
    return pn.parse(USA_VOIP_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_invalid() -> PhoneNumber:
    return PhoneNumber.parse(USA_INVALID_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_invalid_pn() -> pn.PhoneNumber:
    return pn.parse(USA_INVALID_EXAMPLE_NUMBER)


@pytest.fixture
def num_can() -> PhoneNumber:
    return PhoneNumber.parse(CAN_EXAMPLE_NUMBER)


@pytest.fixture
def num_can_pn() -> pn.PhoneNumber:
    return pn.parse(CAN_EXAMPLE_NUMBER)


@pytest.fixture
def num_mex() -> PhoneNumber:
    return PhoneNumber.parse(MEX_EXAMPLE_NUMBER)


@pytest.fixture
def num_mex_pn() -> pn.PhoneNumber:
    return pn.parse(MEX_EXAMPLE_NUMBER)


@pytest.fixture
def num_ita() -> PhoneNumber:
    return PhoneNumber.parse(ITA_EXAMPLE_NUMBER)


@pytest.fixture
def num_ita_pn() -> pn.PhoneNumber:
    return pn.parse(ITA_EXAMPLE_NUMBER)


class TestParse:
    def test_success(self) -> None:
        assert isinstance(PhoneNumber.parse(USA_EXAMPLE_NUMBER), PhoneNumber)

    def test_invalid_country_code(self) -> None:
        with pytest.raises(InvalidCountryCode):
            PhoneNumber.parse("+999 (201) 555-0123")

    def test_not_a_number(self) -> None:
        with pytest.raises(NotANumber):
            PhoneNumber.parse("foo")

    def test_too_long(self) -> None:
        with pytest.raises(TooLong):
            PhoneNumber.parse("+1 (201) 555-0123012301230123")

    def test_too_short_after_idd(self) -> None:
        with pytest.raises(TooShortAfterIDD):
            PhoneNumber.parse("011", region="US")

    def test_too_short_nsn(self) -> None:
        with pytest.raises(TooShortNsn):
            PhoneNumber.parse("+44 2")


def test_national_significant_number(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.national_significant_number == pn.national_significant_number(
        num_usa_pn
    )
    assert num_can.national_significant_number == pn.national_significant_number(
        num_can_pn
    )
    assert num_mex.national_significant_number == pn.national_significant_number(
        num_mex_pn
    )
    assert num_ita.national_significant_number == pn.national_significant_number(
        num_ita_pn
    )


def test_national_destination_code_length(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_pn)
    )
    assert (
        num_usa_invalid.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_invalid_pn)
    )
    assert (
        num_usa_toll_free.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_toll_free_pn)
    )
    assert (
        num_can.national_destination_code_length
        == pn.length_of_national_destination_code(num_can_pn)
    )
    assert (
        num_mex.national_destination_code_length
        == pn.length_of_national_destination_code(num_mex_pn)
    )
    assert (
        num_ita.national_destination_code_length
        == pn.length_of_national_destination_code(num_ita_pn)
    )


def test_national_destination_code(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.national_destination_code
        == pn.national_significant_number(num_usa_pn)[
            : pn.length_of_national_destination_code(num_usa_pn)
        ]
    )
    assert (
        num_usa_invalid.national_destination_code
        == pn.national_significant_number(num_usa_invalid_pn)[
            : pn.length_of_national_destination_code(num_usa_invalid_pn)
        ]
    )
    assert (
        num_can.national_destination_code
        == pn.national_significant_number(num_can_pn)[
            : pn.length_of_national_destination_code(num_can_pn)
        ]
    )
    assert (
        num_mex.national_destination_code
        == pn.national_significant_number(num_mex_pn)[
            : pn.length_of_national_destination_code(num_mex_pn)
        ]
    )
    assert (
        num_ita.national_destination_code
        == pn.national_significant_number(num_ita_pn)[
            : pn.length_of_national_destination_code(num_ita_pn)
        ]
    )


def test_subscriber_number(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.subscriber_number
        == pn.national_significant_number(num_usa_pn)[
            pn.length_of_national_destination_code(num_usa_pn) :
        ]
    )
    assert (
        num_usa_invalid.subscriber_number
        == pn.national_significant_number(num_usa_invalid_pn)[
            pn.length_of_national_destination_code(num_usa_invalid_pn) :
        ]
    )
    assert (
        num_can.subscriber_number
        == pn.national_significant_number(num_can_pn)[
            pn.length_of_national_destination_code(num_can_pn) :
        ]
    )
    assert (
        num_mex.subscriber_number
        == pn.national_significant_number(num_mex_pn)[
            pn.length_of_national_destination_code(num_mex_pn) :
        ]
    )
    assert (
        num_ita.subscriber_number
        == pn.national_significant_number(num_ita_pn)[
            pn.length_of_national_destination_code(num_ita_pn) :
        ]
    )


def test_number_type(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_usa_voip: PhoneNumber,
    num_usa_voip_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.number_type == pn.number_type(num_usa_pn)
    assert num_usa_toll_free.number_type == pn.number_type(num_usa_toll_free_pn)
    assert num_usa_voip.number_type == pn.number_type(num_usa_voip_pn)
    assert num_usa_invalid.number_type == pn.number_type(num_usa_invalid_pn)
    assert num_can.number_type == pn.number_type(num_can_pn)
    assert num_mex.number_type == pn.number_type(num_mex_pn)
    assert num_ita.number_type == pn.number_type(num_ita_pn)


def test_region_code(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.region_code == pn.region_code_for_number(num_usa_pn)
    assert num_usa_invalid.region_code == pn.region_code_for_number(num_usa_invalid_pn)
    assert num_can.region_code == pn.region_code_for_number(num_can_pn)
    assert num_mex.region_code == pn.region_code_for_number(num_mex_pn)
    assert num_ita.region_code == pn.region_code_for_number(num_ita_pn)


def test_timezones(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.timezones == time_zones_for_number(num_usa_pn)
    assert num_usa_toll_free.timezones == time_zones_for_number(num_usa_toll_free_pn)
    assert num_can.timezones == time_zones_for_number(num_can_pn)
    assert num_mex.timezones == time_zones_for_number(num_mex_pn)
    assert num_ita.timezones == time_zones_for_number(num_ita_pn)


def test_get_carrier_name(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.get_carrier_name(lang="en") == name_for_number(num_usa_pn, lang="en")
    assert num_can.get_carrier_name(lang="en") == name_for_number(num_can_pn, lang="en")
    assert num_mex.get_carrier_name(lang="en") == name_for_number(num_mex_pn, lang="en")
    assert num_ita.get_carrier_name(lang="en") == name_for_number(num_ita_pn, lang="en")


def test_get_country_name(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.get_country_name(lang="en") == country_name_for_number(
        num_usa_pn, lang="en"
    )
    assert num_can.get_country_name(lang="en") == country_name_for_number(
        num_can_pn, lang="en"
    )
    assert num_mex.get_country_name(lang="en") == country_name_for_number(
        num_mex_pn, lang="en"
    )
    assert num_ita.get_country_name(lang="en") == country_name_for_number(
        num_ita_pn, lang="en"
    )


def test_get_description(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.get_description(lang="en") == description_for_number(
        num_usa_pn, lang="en"
    )
    assert num_can.get_description(lang="en") == description_for_number(
        num_can_pn, lang="en"
    )
    assert num_mex.get_description(lang="en") == description_for_number(
        num_mex_pn, lang="en"
    )
    assert num_ita.get_description(lang="en") == description_for_number(
        num_ita_pn, lang="en"
    )


def test_is_geographical(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.is_geographical == pn.is_number_geographical(num_usa_pn)
    assert num_usa_toll_free.is_geographical == pn.is_number_geographical(
        num_usa_toll_free_pn
    )
    assert num_can.is_geographical == pn.is_number_geographical(num_can_pn)
    assert num_mex.is_geographical == pn.is_number_geographical(num_mex_pn)
    assert num_ita.is_geographical == pn.is_number_geographical(num_ita_pn)


def test_is_possible(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.is_possible == pn.is_possible_number(num_usa_pn)
    assert num_usa_toll_free.is_possible == pn.is_possible_number(num_usa_toll_free_pn)
    assert num_usa_invalid.is_possible == pn.is_possible_number(num_usa_invalid_pn)
    assert num_can.is_possible == pn.is_possible_number(num_can_pn)
    assert num_mex.is_possible == pn.is_possible_number(num_mex_pn)
    assert num_ita.is_possible == pn.is_possible_number(num_ita_pn)


def test_is_valid(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.is_valid == pn.is_valid_number(num_usa_pn)
    assert num_usa_toll_free.is_valid == pn.is_valid_number(num_usa_toll_free_pn)
    assert num_usa_invalid.is_valid == pn.is_valid_number(num_usa_invalid_pn)
    assert num_can.is_valid == pn.is_valid_number(num_can_pn)
    assert num_mex.is_valid == pn.is_valid_number(num_mex_pn)
    assert num_ita.is_valid == pn.is_valid_number(num_ita_pn)


def test_is_toll_free(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
) -> None:
    assert num_usa_toll_free.is_toll_free == (
        pn.number_type(num_usa_toll_free_pn) == pn.PhoneNumberType.TOLL_FREE
    )
    assert num_usa.is_toll_free == (
        pn.number_type(num_usa_pn) == pn.PhoneNumberType.TOLL_FREE
    )


def test_is_voip(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_voip: PhoneNumber,
    num_usa_voip_pn: pn.PhoneNumber,
) -> None:
    assert num_usa_voip.is_voip == (
        pn.number_type(num_usa_voip_pn) == pn.PhoneNumberType.VOIP
    )
    assert num_usa.is_voip == (pn.number_type(num_usa_pn) == pn.PhoneNumberType.VOIP)


def test_is_match(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.get_match_type(num_usa_pn) == pn.is_number_match(num_usa, num_usa_pn)
    assert num_can.get_match_type(num_can_pn) == pn.is_number_match(num_can, num_can_pn)
    assert num_mex.get_match_type(num_mex_pn) == pn.is_number_match(num_mex, num_mex_pn)
    assert num_ita.get_match_type(num_ita_pn) == pn.is_number_match(num_ita, num_ita_pn)


class TestFormat:

    def test_to_international(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_international() == pn.format_number(
            num_usa_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_can.to_international() == pn.format_number(
            num_can_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_mex.to_international() == pn.format_number(
            num_mex_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_ita.to_international() == pn.format_number(
            num_ita_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )

    def test_to_national(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_national() == pn.format_number(num_usa_pn, pn.PhoneNumberFormat.NATIONAL)
        assert num_can.to_national() == pn.format_number(num_can_pn, pn.PhoneNumberFormat.NATIONAL)
        assert num_mex.to_national() == pn.format_number(num_mex_pn, pn.PhoneNumberFormat.NATIONAL)
        assert num_ita.to_national() == pn.format_number(num_ita_pn, pn.PhoneNumberFormat.NATIONAL)

    def test_e164_format(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_e164() == pn.format_number(num_usa_pn, pn.PhoneNumberFormat.E164)
        assert num_can.to_e164() == pn.format_number(num_can_pn, pn.PhoneNumberFormat.E164)
        assert num_mex.to_e164() == pn.format_number(num_mex_pn, pn.PhoneNumberFormat.E164)
        assert num_ita.to_e164() == pn.format_number(num_ita_pn, pn.PhoneNumberFormat.E164)

    def test_to_rfc3966(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_rfc3966() == pn.format_number(num_usa_pn, pn.PhoneNumberFormat.RFC3966)
        assert num_can.to_rfc3966() == pn.format_number(num_can_pn, pn.PhoneNumberFormat.RFC3966)
        assert num_mex.to_rfc3966() == pn.format_number(num_mex_pn, pn.PhoneNumberFormat.RFC3966)
        assert num_ita.to_rfc3966() == pn.format_number(num_ita_pn, pn.PhoneNumberFormat.RFC3966)


class TestReplace:
    def test_country_code(self, num_usa: PhoneNumber) -> None:
        num = num_usa.replace(country_code=44)
        assert num.country_code == 44

    def test_national_number(self, num_usa: PhoneNumber) -> None:
        num = num_usa.replace(national_number=8002345678)
        assert num.national_number == 8002345678

    def test_extension(self, num_usa: PhoneNumber) -> None:
        num = num_usa.replace(extension="1234")
        assert num.extension == "1234"

    def test_leading_italian_zero(self, num_usa: PhoneNumber) -> None:
        num = num_usa.replace(italian_leading_zero=True)
        assert num.italian_leading_zero is True

    def test_number_of_leading_zeros(self, num_usa: PhoneNumber) -> None:
        num = num_usa.replace(number_of_leading_zeros=1)
        assert num.number_of_leading_zeros == 1


def test_clear(num_usa: PhoneNumber) -> None:
    with pytest.raises(FrozenInstanceError):
        num_usa.clear()


def test_merge_from(num_usa: PhoneNumber, num_can: PhoneNumber) -> None:
    with pytest.raises(FrozenInstanceError):
        num_usa.merge_from(num_can)
