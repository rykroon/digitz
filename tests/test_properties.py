import phonenumbers as pn
from phonenumbers import PhoneNumberType as PT
import pytest
from digitz import PhoneNumber
from .utils import create_number_list


REGIONS = ("US", "CA", "MX", "IT", "GB")
PHONE_NUMBERS = create_number_list(regions=REGIONS, types=[None])
FIXED_LINE_NUMBERS = create_number_list(regions=REGIONS, types=[PT.FIXED_LINE])
MOBILE_NUMBERS = create_number_list(regions=REGIONS, types=[PT.MOBILE])
FIXED_LINE_OR_MOBILE_NUMBERS = create_number_list(
    regions=REGIONS, types=[PT.FIXED_LINE_OR_MOBILE]
)
TOLL_FREE_NUMBERS = create_number_list(regions=REGIONS, types=[PT.TOLL_FREE])
PREMIUM_RATE_NUMBERS = create_number_list(regions=REGIONS, types=[PT.PREMIUM_RATE])
VOIP_NUMBERS = create_number_list(regions=REGIONS, types=[PT.VOIP])
PERSONAL_NUMBER_NUMBERS = create_number_list(regions=REGIONS, types=[PT.PERSONAL_NUMBER])
INVALID_NUMBERS = create_number_list(regions=REGIONS, types=[PT.UNKNOWN])


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_significant_number(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.national_significant_number == pn.national_significant_number(num_pn)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_destination_code_length(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        num_dg.national_destination_code_length
        == pn.length_of_national_destination_code(num_pn)
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_national_destination_code(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        num_dg.national_destination_code
        == pn.national_significant_number(num_pn)[
            : pn.length_of_national_destination_code(num_pn)
        ]
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_subscriber_number(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        num_dg.subscriber_number
        == pn.national_significant_number(num_pn)[
            pn.length_of_national_destination_code(num_pn) :
        ]
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_possible_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_possible == pn.is_possible_number(num_pn) == True


# @pytest.mark.parametrize("phonenumber", INVALID_NUMBERS)
# def test_is_possible_false(phonenumber: str) -> None:
#     num_dg = PhoneNumber.parse(phonenumber)
#     num_pn = pn.parse(phonenumber)
#     assert num_dg.is_possible == pn.is_possible_number(num_pn) == False


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_valid_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_valid == pn.is_valid_number(num_pn) == True


@pytest.mark.parametrize("phonenumber", INVALID_NUMBERS)
def test_is_valid_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_valid == pn.is_valid_number(num_pn) == False


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_number_type(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.number_type == pn.number_type(num_pn)


@pytest.mark.parametrize("phonenumber", FIXED_LINE_NUMBERS)
def test_is_fixed_line_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        (num_dg.is_fixed_line or num_dg.is_fixed_line_or_mobile)
        == (pn.number_type(num_pn) in (PT.FIXED_LINE, PT.FIXED_LINE_OR_MOBILE))
        == True
    )


@pytest.mark.parametrize("phonenumber", MOBILE_NUMBERS)
def test_is_mobile_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        (num_dg.is_mobile or num_dg.is_fixed_line_or_mobile)
        == (pn.number_type(num_pn) in (PT.MOBILE, PT.FIXED_LINE_OR_MOBILE))
        == True
    )


@pytest.mark.parametrize("phonenumber", FIXED_LINE_OR_MOBILE_NUMBERS)
def test_is_fixed_line_or_mobile_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        (num_dg.is_fixed_line_or_mobile or num_dg.is_fixed_line or num_dg.is_mobile)
        == (
            pn.number_type(num_pn)
            in (PT.FIXED_LINE_OR_MOBILE, PT.FIXED_LINE, PT.MOBILE)
        )
        == True
    )


@pytest.mark.parametrize("phonenumber", TOLL_FREE_NUMBERS)
def test_is_toll_free_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_toll_free == (pn.number_type(num_pn) == PT.TOLL_FREE) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_toll_free_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_toll_free == (pn.number_type(num_pn) == PT.TOLL_FREE) == False


@pytest.mark.parametrize("phonenumber", PREMIUM_RATE_NUMBERS)
def test_is_premium_rate_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_premium_rate == (pn.number_type(num_pn) == PT.PREMIUM_RATE) == True


@pytest.mark.parametrize("phonenumber", VOIP_NUMBERS)
def test_is_voip_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voip == (pn.number_type(num_pn) == PT.VOIP) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_voip_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voip == (pn.number_type(num_pn) == PT.VOIP) == False

@pytest.mark.parametrize("phonenumber", PERSONAL_NUMBER_NUMBERS)
def test_is_personal_number_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_personal_number == (pn.number_type(num_pn) == PT.PERSONAL_NUMBER) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_region_code(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.region_code == pn.region_code_for_number(num_pn)


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_geographical(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_geographical == pn.is_number_geographical(num_pn)
