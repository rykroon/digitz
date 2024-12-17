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
from .parametrize import create_number_list

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


def test_clear() -> None:
    num_dg = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    with pytest.raises(FrozenInstanceError):
        num_dg.clear()


def test_merge_from() -> None:
    num1 = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    num2 = PhoneNumber.parse(USA_EXAMPLE_NUMBER)
    with pytest.raises(FrozenInstanceError):
        num1.merge_from(num2)
