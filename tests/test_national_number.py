import phonenumbers as pn
import pytest
from digitz import PhoneNumber
from .parametrize import create_number_list


PHONE_NUMBERS = create_number_list(regions=["US", "CA", "MX", "IT", "GB"], types=[None])


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_significant_number(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.national_significant_number == pn.national_significant_number(num_pn)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_destination_code_length(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.national_destination_code_length == pn.length_of_national_destination_code(num_pn)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_destination_code(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.national_destination_code == pn.national_significant_number(num_pn)[:pn.length_of_national_destination_code(num_pn)]


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_subscriber_number(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.subscriber_number == pn.national_significant_number(num_pn)[pn.length_of_national_destination_code(num_pn):]