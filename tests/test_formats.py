import phonenumbers as pn
from digitz import PhoneNumber
from .fixtures import (
    num_can, num_can_pn, num_ita, num_ita_pn, num_mex, num_mex_pn, num_usa, num_usa_pn
)

def test_str(
    num_usa: PhoneNumber,
    num_usa_pn: pn.PhoneNumber,
    num_can: PhoneNumber,
    num_can_pn: pn.PhoneNumber,
    num_mex: PhoneNumber,
    num_mex_pn: pn.PhoneNumber,
    num_ita: PhoneNumber,
    num_ita_pn: pn.PhoneNumber,
) -> None:
    assert str(num_usa) == pn.format_number(num_usa_pn, pn.PhoneNumberFormat.E164)
    assert str(num_can) == pn.format_number(num_can_pn, pn.PhoneNumberFormat.E164)
    assert str(num_mex) == pn.format_number(num_mex_pn, pn.PhoneNumberFormat.E164)
    assert str(num_ita) == pn.format_number(num_ita_pn, pn.PhoneNumberFormat.E164)


class TestFormat:
    def test_to_international(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_international() == pn.format_number(
            num_usa_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_can.to_international() == pn.format_number(
            num_can_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_mex.to_international() == pn.format_number(
            num_mex_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )
        assert num_ita.to_international() == pn.format_number(
            num_ita_pn, pn.PhoneNumberFormat.INTERNATIONAL
        )

    def test_to_national(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_national() == pn.format_number(
            num_usa_pn, pn.PhoneNumberFormat.NATIONAL
        )
        assert num_can.to_national() == pn.format_number(
            num_can_pn, pn.PhoneNumberFormat.NATIONAL
        )
        assert num_mex.to_national() == pn.format_number(
            num_mex_pn, pn.PhoneNumberFormat.NATIONAL
        )
        assert num_ita.to_national() == pn.format_number(
            num_ita_pn, pn.PhoneNumberFormat.NATIONAL
        )

    def test_e164_format(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_e164() == pn.format_number(
            num_usa_pn, pn.PhoneNumberFormat.E164
        )
        assert num_can.to_e164() == pn.format_number(
            num_can_pn, pn.PhoneNumberFormat.E164
        )
        assert num_mex.to_e164() == pn.format_number(
            num_mex_pn, pn.PhoneNumberFormat.E164
        )
        assert num_ita.to_e164() == pn.format_number(
            num_ita_pn, pn.PhoneNumberFormat.E164
        )

    def test_to_rfc3966(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ) -> None:
        assert num_usa.to_rfc3966() == pn.format_number(
            num_usa_pn, pn.PhoneNumberFormat.RFC3966
        )
        assert num_can.to_rfc3966() == pn.format_number(
            num_can_pn, pn.PhoneNumberFormat.RFC3966
        )
        assert num_mex.to_rfc3966() == pn.format_number(
            num_mex_pn, pn.PhoneNumberFormat.RFC3966
        )
        assert num_ita.to_rfc3966() == pn.format_number(
            num_ita_pn, pn.PhoneNumberFormat.RFC3966
        )