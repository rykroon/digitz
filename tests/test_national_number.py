import phonenumbers as pn
from digitz import PhoneNumber
from .fixtures import (
    num_can, num_can_pn, num_ita, num_ita_pn, num_mex, num_mex_pn, num_usa, num_usa_pn,
    num_usa_invalid, num_usa_invalid_pn, num_usa_toll_free, num_usa_toll_free_pn
)


def test_national_significant_number(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert num_usa.national_significant_number == pn.national_significant_number(
        num_usa_pn
    )
    assert num_can.national_significant_number == pn.national_significant_number(
        num_can_pn
    )
    assert num_mex.national_significant_number == pn.national_significant_number(
        num_mex_pn
    )
    assert num_ita.national_significant_number == pn.national_significant_number(
        num_ita_pn
    )


def test_national_destination_code_length(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_usa_toll_free: PhoneNumber,
    num_usa_toll_free_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_pn)
    )
    assert (
        num_usa_invalid.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_invalid_pn)
    )
    assert (
        num_usa_toll_free.national_destination_code_length
        == pn.length_of_national_destination_code(num_usa_toll_free_pn)
    )
    assert (
        num_can.national_destination_code_length
        == pn.length_of_national_destination_code(num_can_pn)
    )
    assert (
        num_mex.national_destination_code_length
        == pn.length_of_national_destination_code(num_mex_pn)
    )
    assert (
        num_ita.national_destination_code_length
        == pn.length_of_national_destination_code(num_ita_pn)
    )


def test_national_destination_code(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.national_destination_code
        == pn.national_significant_number(num_usa_pn)[
            : pn.length_of_national_destination_code(num_usa_pn)
        ]
    )
    assert (
        num_usa_invalid.national_destination_code
        == pn.national_significant_number(num_usa_invalid_pn)[
            : pn.length_of_national_destination_code(num_usa_invalid_pn)
        ]
    )
    assert (
        num_can.national_destination_code
        == pn.national_significant_number(num_can_pn)[
            : pn.length_of_national_destination_code(num_can_pn)
        ]
    )
    assert (
        num_mex.national_destination_code
        == pn.national_significant_number(num_mex_pn)[
            : pn.length_of_national_destination_code(num_mex_pn)
        ]
    )
    assert (
        num_ita.national_destination_code
        == pn.national_significant_number(num_ita_pn)[
            : pn.length_of_national_destination_code(num_ita_pn)
        ]
    )


def test_subscriber_number(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_usa_invalid: PhoneNumber,
    num_usa_invalid_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert (
        num_usa.subscriber_number
        == pn.national_significant_number(num_usa_pn)[
            pn.length_of_national_destination_code(num_usa_pn) :
        ]
    )
    assert (
        num_usa_invalid.subscriber_number
        == pn.national_significant_number(num_usa_invalid_pn)[
            pn.length_of_national_destination_code(num_usa_invalid_pn) :
        ]
    )
    assert (
        num_can.subscriber_number
        == pn.national_significant_number(num_can_pn)[
            pn.length_of_national_destination_code(num_can_pn) :
        ]
    )
    assert (
        num_mex.subscriber_number
        == pn.national_significant_number(num_mex_pn)[
            pn.length_of_national_destination_code(num_mex_pn) :
        ]
    )
    assert (
        num_ita.subscriber_number
        == pn.national_significant_number(num_ita_pn)[
            pn.length_of_national_destination_code(num_ita_pn) :
        ]
    )