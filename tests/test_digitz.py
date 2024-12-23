from dataclasses import FrozenInstanceError
import phonenumbers as pn
import pytest

from digitz import PhoneNumber, parse
from digitz.enums import PhoneNumberType
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)
from .utils import create_number_list

PHONE_NUMBERS = create_number_list(regions=["US", "CA", "MX", "IT", "GB"], types=[None])


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


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
class TestReplace:
    def test_country_code(self, phonenumber: str) -> None:
        num1 = PhoneNumber.parse(phonenumber)
        num2 = num1.replace(country_code=44)
        assert num2.country_code == 44

    def test_national_number(self, phonenumber: str) -> None:
        num1 = PhoneNumber.parse(phonenumber)
        num2 = num1.replace(national_number=8002345678)
        assert num2.national_number == 8002345678

    def test_extension(self, phonenumber: str) -> None:
        num1 = PhoneNumber.parse(phonenumber)
        num2 = num1.replace(extension="1234")
        assert num2.extension == "1234"

    def test_leading_italian_zero(self, phonenumber: str) -> None:
        num1 = PhoneNumber.parse(phonenumber)
        num2 = num1.replace(italian_leading_zero=True)
        assert num2.italian_leading_zero is True

    def test_number_of_leading_zeros(self, phonenumber: str) -> None:
        num1 = PhoneNumber.parse(phonenumber)
        num2 = num1.replace(number_of_leading_zeros=1)
        assert num2.number_of_leading_zeros == 1


@pytest.mark.parametrize("region", ["US", "CA", "MX", "IT", "GB"])
@pytest.mark.parametrize("type", list(PhoneNumberType))
def test_example_number(region: str, type: PhoneNumberType) -> None:
    assert PhoneNumber.example_number(region, type) == pn.example_number_for_type(region, type)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_eq_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg == num_pn
    assert num_pn == num_dg


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_eq_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.national_number += 1

    assert num_dg != num_pn
    assert num_pn != num_dg


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_dict(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)

    assert num_dg.to_dict() == {
        "country_code": num_dg.country_code,
        "national_number": num_dg.national_number,
        "extension": num_dg.extension,
        "italian_leading_zero": num_dg.italian_leading_zero,
        "number_of_leading_zeros": num_dg.number_of_leading_zeros,
        "raw_input": num_dg.raw_input,
        "country_code_source": num_dg.country_code_source,
        "preferred_domestic_carrier_code": num_dg.preferred_domestic_carrier_code,
    }


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_to_tuple(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    assert num_dg.to_tuple() == (
        num_dg.country_code,
        num_dg.national_number,
        num_dg.extension,
        num_dg.italian_leading_zero,
        num_dg.number_of_leading_zeros,
        num_dg.raw_input,
        num_dg.country_code_source,
        num_dg.preferred_domestic_carrier_code,
    )


def test_clear() -> None:
    num_dg = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    with pytest.raises(FrozenInstanceError):
        num_dg.clear()


def test_merge_from() -> None:
    num1 = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    num2 = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    with pytest.raises(FrozenInstanceError):
        num1.merge_from(num2)
