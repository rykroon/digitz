import phonenumbers as pn
from phonenumbers import PhoneNumberType as PT
import pytest

from digitz import PhoneNumber
from .utils import create_number_list


REGIONS = ["US", "CA", "MX", "IT", "GB"]
PHONE_NUMBERS = create_number_list(["US", "CA", "MX", "IT", "GB"])

FIXED_LINE_NUMBERS = create_number_list(REGIONS, PT.FIXED_LINE)
MOBILE_NUMBERS = create_number_list(REGIONS, PT.MOBILE)
FIXED_LINE_OR_MOBILE_NUMBERS = create_number_list(REGIONS, PT.FIXED_LINE_OR_MOBILE)
TOLL_FREE_NUMBERS = create_number_list(REGIONS, PT.TOLL_FREE)
PREMIUM_RATE_NUMBERS = create_number_list(REGIONS, PT.PREMIUM_RATE)
SHARED_COST_NUMBERS = create_number_list(REGIONS, PT.SHARED_COST)
VOIP_NUMBERS = create_number_list(REGIONS, PT.VOIP)
PERSONAL_NUMBER_NUMBERS = create_number_list(REGIONS, PT.PERSONAL_NUMBER)
PAGER_NUMBERS = create_number_list(REGIONS, PT.PAGER)
UAN_NUMBERS = create_number_list(REGIONS, PT.UAN)
VOICEMAIL_NUMBERS = create_number_list(REGIONS, PT.VOICEMAIL)


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


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_premium_rate_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        num_dg.is_premium_rate == (pn.number_type(num_pn) == PT.PREMIUM_RATE) == False
    )


@pytest.mark.parametrize("phonenumber", SHARED_COST_NUMBERS)
def test_is_shared_cost_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_shared_cost == (pn.number_type(num_pn) == PT.SHARED_COST) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_shared_cost_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_shared_cost == (pn.number_type(num_pn) == PT.SHARED_COST) == False


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
    assert (
        num_dg.is_personal_number
        == (pn.number_type(num_pn) == PT.PERSONAL_NUMBER)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_personal_number_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert (
        num_dg.is_personal_number
        == (pn.number_type(num_pn) == PT.PERSONAL_NUMBER)
        == False
    )


@pytest.mark.parametrize("phonenumber", PAGER_NUMBERS)
def test_is_pager_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_pager == (pn.number_type(num_pn) == PT.PAGER) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_pager_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_pager == (pn.number_type(num_pn) == PT.PAGER) == False


@pytest.mark.parametrize("phonenumber", UAN_NUMBERS)
def test_is_uan_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_uan == (pn.number_type(num_pn) == PT.UAN) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_uan_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_uan == (pn.number_type(num_pn) == PT.UAN) == False


@pytest.mark.parametrize("phonenumber", VOICEMAIL_NUMBERS)
def test_is_voicemail_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voicemail == (pn.number_type(num_pn) == PT.VOICEMAIL) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_voicemail_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voicemail == (pn.number_type(num_pn) == PT.VOICEMAIL) == False
