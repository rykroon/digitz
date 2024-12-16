from dataclasses import FrozenInstanceError
import pytest

from digitz import PhoneNumber, parse
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
import pytz

from .fixtures import (
    num_can,
    num_can_pn,
    num_ita,
    num_ita_pn,
    num_mex,
    num_mex_pn,
    num_usa,
    num_usa_pn,
    num_usa_invalid,
    num_usa_invalid_pn,
    num_usa_toll_free,
    num_usa_toll_free_pn,
    num_usa_voip,
    num_usa_voip_pn,
)

USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"


class TestParse:
    def test_success(self) -> None:
        assert isinstance(PhoneNumber.parse(USA_EXAMPLE_NUMBER), PhoneNumber)

    def test_invalid_country_code(self) -> None:
        with pytest.raises(InvalidCountryCode):
            parse("+999 (201) 555-0123")

    def test_not_a_number(self) -> None:
        with pytest.raises(NotANumber):
            parse("foo")

    def test_too_long(self) -> None:
        with pytest.raises(TooLong):
            parse("+1 (201) 555-0123012301230123")

    def test_too_short_after_idd(self) -> None:
        with pytest.raises(TooShortAfterIDD):
            parse("011", region="US")

    def test_too_short_nsn(self) -> None:
        with pytest.raises(TooShortNsn):
            PhoneNumber.parse("+44 2")


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
    assert num_usa.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_usa_pn)]
    )
    assert num_usa_toll_free.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_usa_toll_free_pn)]
    )
    assert num_can.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_can_pn)]
    )
    assert num_mex.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_mex_pn)]
    )
    assert num_ita.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_ita_pn)]
    )


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


class TestPhoneNumberType:
    def test_is_toll_free(
        self,
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
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_usa_voip: PhoneNumber,
        num_usa_voip_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa_voip.is_voip == (
            pn.number_type(num_usa_voip_pn) == pn.PhoneNumberType.VOIP
        )
        assert num_usa.is_voip == (pn.number_type(num_usa_pn) == pn.PhoneNumberType.VOIP)


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
