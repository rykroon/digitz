import phonenumbers as pn
import pytest
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
def test_str(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert str(num_dg) == pn.format_number(num_pn, pn.PhoneNumberFormat.E164)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_international(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.to_international() == pn.format_number(
        num_pn, pn.PhoneNumberFormat.INTERNATIONAL
    )

@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_national(phonenumber) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.to_national() == pn.format_number(
        num_pn, pn.PhoneNumberFormat.NATIONAL
    )

@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_e164_format(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.to_e164() == pn.format_number(
        num_pn, pn.PhoneNumberFormat.E164
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_rfc3966(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.to_rfc3966() == pn.format_number(
        num_pn, pn.PhoneNumberFormat.RFC3966
    )
