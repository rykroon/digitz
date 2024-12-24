import phonenumbers as pn
import pytest
from digitz import PhoneNumber
from .utils import create_number_list

PHONE_NUMBERS = create_number_list(regions=["US", "CA", "MX", "IT", "GB"])


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_short_nsn_match_extension(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.extension = "1234"

    # is short nsn match is True
    assert (
        num_dg.is_short_nsn_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) == pn.MatchType.SHORT_NSN_MATCH)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_short_nsn_match_leading_zeros(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.italian_leading_zero = not num_pn.italian_leading_zero
    num_pn.number_of_leading_zeros = 1

    num_dg.is_short_nsn_match(num_pn) == (
        pn.is_number_match(num_dg, num_pn) == pn.MatchType.SHORT_NSN_MATCH
    ) == True


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_nsn_match(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.country_code = 0

    # test with object
    assert (
        num_dg.is_nsn_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) == pn.MatchType.NSN_MATCH)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_exact_match_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)

    # test with string
    assert (
        num_dg.is_exact_match(phonenumber)
        == (pn.is_number_match(num_dg, phonenumber) == pn.MatchType.EXACT_MATCH)
        == True
    )

    # test with object
    assert (
        num_dg.is_exact_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) == pn.MatchType.EXACT_MATCH)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_exact_match_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.national_number += 1

    assert (
        num_dg.is_exact_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) == pn.MatchType.EXACT_MATCH)
        == False
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_any_nsn_match_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)

    num_pn_short_nsn = pn.parse(phonenumber)
    num_pn_short_nsn.extension = "1234"

    num_pn_nsn_match = pn.parse(phonenumber)
    num_pn_nsn_match.country_code = 0

    ANY_NSN_MATCH = (pn.MatchType.NSN_MATCH, pn.MatchType.SHORT_NSN_MATCH)

    assert (
        num_dg.is_any_nsn_match(num_pn_short_nsn)
        == (pn.is_number_match(num_dg, num_pn_short_nsn) in ANY_NSN_MATCH)
        == True
    )
    assert (
        num_dg.is_any_nsn_match(num_pn_nsn_match)
        == (pn.is_number_match(num_dg, num_pn_nsn_match) in ANY_NSN_MATCH)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_any_nsn_match_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)

    ANY_NSN_MATCH = (pn.MatchType.NSN_MATCH, pn.MatchType.SHORT_NSN_MATCH)

    # exact match is False
    assert (
        num_dg.is_any_nsn_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) in ANY_NSN_MATCH)
        == False
    )

    # not a match is False
    num_pn.national_number += 1
    assert (
        num_dg.is_any_nsn_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) in ANY_NSN_MATCH)
        == False
    )

    # not a number is False
    assert (
        num_dg.is_any_nsn_match("foobar")
        == (pn.is_number_match(num_dg, "foobar") in ANY_NSN_MATCH)
        == False
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_any_match_true(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)

    num_pn_short_nsn = pn.parse(phonenumber)
    num_pn_short_nsn.extension = "1234"

    num_pn_nsn_match = pn.parse(phonenumber)
    num_pn_nsn_match.country_code = 0

    ANY_MATCH = (
        pn.MatchType.EXACT_MATCH,
        pn.MatchType.NSN_MATCH,
        pn.MatchType.SHORT_NSN_MATCH,
    )

    assert (
        num_dg.is_any_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) in ANY_MATCH)
        == True
    )

    assert (
        num_dg.is_any_match(num_pn_short_nsn)
        == (pn.is_number_match(num_dg, num_pn_short_nsn) in ANY_MATCH)
        == True
    )

    assert (
        num_dg.is_any_match(num_pn_nsn_match)
        == (pn.is_number_match(num_dg, num_pn_nsn_match) in ANY_MATCH)
        == True
    )


@pytest.mark.parametrize("phonenumber", PHONE_NUMBERS)
def test_is_any_match_false(phonenumber: str) -> None:
    num_dg = PhoneNumber.parse(phonenumber)
    num_pn = pn.parse(phonenumber)
    num_pn.national_number += 1

    ANY_MATCH = (
        pn.MatchType.EXACT_MATCH,
        pn.MatchType.NSN_MATCH,
        pn.MatchType.SHORT_NSN_MATCH,
    )

    assert (
        num_dg.is_any_match(num_pn)
        == (pn.is_number_match(num_dg, num_pn) in ANY_MATCH)
        == False
    )
