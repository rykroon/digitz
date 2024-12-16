import phonenumbers as pn
from phonenumbers.timezone import time_zones_for_number
from phonenumbers.carrier import name_for_number
from phonenumbers.geocoder import country_name_for_number, description_for_number
import pytest
import pytz

from digitz import PhoneNumber

from .fixtures import (
    USA_EXAMPLE_NUMBER,
    CAN_EXAMPLE_NUMBER,
    MEX_EXAMPLE_NUMBER,
    ITA_EXAMPLE_NUMBER,
)

PHONE_NUMBERS = [
    USA_EXAMPLE_NUMBER,
    CAN_EXAMPLE_NUMBER,
    MEX_EXAMPLE_NUMBER,
    ITA_EXAMPLE_NUMBER,
]


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_timezones(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.timezones == tuple(
        [pytz.timezone(zone) for zone in time_zones_for_number(num_pn)]
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_get_carrier_name(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.get_carrier_name(lang="en") == name_for_number(num_pn, lang="en")


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_get_country_name(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.get_country_name(lang="en") == country_name_for_number(num_pn, lang="en")


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_get_description(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.get_description(lang="en") == description_for_number(num_pn, lang="en")