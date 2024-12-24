import phonenumbers as pn
import pytest
from digitz import PhoneNumber

from .utils import create_number_list


PHONE_NUMBERS = create_number_list(regions=["US", "CA", "MX", "IT", "GB"])


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
    assert num_dg.to_e164() == pn.format_number(num_pn, pn.PhoneNumberFormat.E164)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_rfc3966(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.to_rfc3966() == pn.format_number(num_pn, pn.PhoneNumberFormat.RFC3966)
