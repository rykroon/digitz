import phonenumbers as pn
import pytest
from digitz import PhoneNumber
from .parametrize import create_number_list


REGIONS = ("US", "CA", "MX", "IT", "GB")
PHONE_NUMBERS = create_number_list(regions=REGIONS, types=[None])
INVALID_NUMBERS = create_number_list(regions=REGIONS, types=[pn.PhoneNumberType.UNKNOWN])
TOLL_FREE_NUMBERS = create_number_list(regions=REGIONS, types=[pn.PhoneNumberType.TOLL_FREE])
VOIP_NUMBERS = create_number_list(regions=REGIONS, types=[pn.PhoneNumberType.VOIP])


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


@pytest.mark.parametrize("phonenumber", TOLL_FREE_NUMBERS)
def test_is_toll_free_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_toll_free == (pn.number_type(num_pn) == pn.PhoneNumberType.TOLL_FREE) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_toll_free_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_toll_free == (pn.number_type(num_pn) == pn.PhoneNumberType.TOLL_FREE) == False


@pytest.mark.parametrize("phonenumber", VOIP_NUMBERS)
def test_is_voip_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voip == (pn.number_type(num_pn) == pn.PhoneNumberType.VOIP) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_voip_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    assert num_dg.is_voip == (pn.number_type(num_pn) == pn.PhoneNumberType.VOIP) == False


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
