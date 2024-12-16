import phonenumbers as pn
from digitz import PhoneNumber
from .fixtures import (
    num_can, num_can_pn, num_ita, num_ita_pn, num_mex, num_mex_pn, num_usa, num_usa_pn
)



class TestMatch:

    def test_is_no_match(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ):
        # not a match is True
        assert num_usa.is_no_match(num_can_pn) == (
            pn.is_number_match(num_usa, num_can_pn) == pn.MatchType.NO_MATCH
        ) == True
        assert num_can.is_no_match(num_mex_pn) == (
            pn.is_number_match(num_can, num_mex_pn) == pn.MatchType.NO_MATCH
        ) == True
        assert num_mex.is_no_match(num_ita_pn) == (
            pn.is_number_match(num_mex, num_ita_pn) == pn.MatchType.NO_MATCH
        ) == True
        assert num_ita.is_no_match(num_usa_pn) == (
            pn.is_number_match(num_ita, num_usa_pn) == pn.MatchType.NO_MATCH
        ) == True

        # not a match is False
        assert num_usa.is_no_match(num_usa_pn) == (
            pn.is_number_match(num_usa, num_usa_pn) == pn.MatchType.NO_MATCH
        ) == False
        assert num_can.is_no_match(num_can_pn) == (
            pn.is_number_match(num_can, num_can_pn) == pn.MatchType.NO_MATCH
        ) == False
        assert num_mex.is_no_match(num_mex_pn) == (
            pn.is_number_match(num_mex, num_mex_pn) == pn.MatchType.NO_MATCH
        ) == False
        assert num_ita.is_no_match(num_ita_pn) == (
            pn.is_number_match(num_ita, num_ita_pn) == pn.MatchType.NO_MATCH
        ) == False

    def test_is_no_match_strict(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ):
        # not a match (strict) is False
        assert num_usa.is_no_match("not_a_number", strict=True) == (
            pn.is_number_match(num_usa, "not_a_number") == pn.MatchType.NO_MATCH
        ) == False
        assert num_can.is_no_match("not_a_number", strict=True) == (
            pn.is_number_match(num_can, "not_a_number") == pn.MatchType.NO_MATCH
        ) == False
        assert num_mex.is_no_match("not_a_number", strict=True) == (
            pn.is_number_match(num_mex, "not_a_number") == pn.MatchType.NO_MATCH
        ) == False
        assert num_ita.is_no_match("not_a_number", strict=True) == (
            pn.is_number_match(num_ita, "not_a_number") == pn.MatchType.NO_MATCH
        ) == False

    def test_is_short_nsn_match(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ):
        num_usa_ext = num_usa.replace(extension="1234")
        num_can_ext = num_can.replace(extension="1234")
        num_mex_ext = num_mex.replace(extension="1234")
        num_ita_ext = num_ita.replace(extension="1234")

        # is short nsn match due to extension
        assert num_usa_ext.is_short_nsn_match(num_usa_pn) == (
            pn.is_number_match(num_usa_ext, num_usa_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_can_ext.is_short_nsn_match(num_can_pn) == (
            pn.is_number_match(num_can_ext, num_can_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_mex_ext.is_short_nsn_match(num_mex_pn) == (
            pn.is_number_match(num_mex_ext, num_mex_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_ita_ext.is_short_nsn_match(num_ita_pn) == (
            pn.is_number_match(num_ita_ext, num_ita_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True

        # is short nsn match due to leading zeros
        num_usa_lead = num_usa.replace(number_of_leading_zeros=1, italian_leading_zero=True)
        num_can_lead = num_can.replace(number_of_leading_zeros=1, italian_leading_zero=True)
        num_mex_lead = num_mex.replace(number_of_leading_zeros=1, italian_leading_zero=True)
        num_ita_lead = num_ita.replace(number_of_leading_zeros=2)

        assert num_usa_lead.is_short_nsn_match(num_usa_pn) == (
            pn.is_number_match(num_usa_lead, num_usa_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_can_lead.is_short_nsn_match(num_can_pn) == (
            pn.is_number_match(num_can_lead, num_can_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_mex_lead.is_short_nsn_match(num_mex_pn) == (
            pn.is_number_match(num_mex_lead, num_mex_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True
        assert num_ita_lead.is_short_nsn_match(num_ita_pn) == (
            pn.is_number_match(num_ita_lead, num_ita_pn) == pn.MatchType.SHORT_NSN_MATCH
        ) == True

    def test_is_nsn_match(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ):
        num_usa_no_region = num_usa.replace(country_code=0)
        num_can_no_region = num_can.replace(country_code=0)
        num_mex_no_region = num_mex.replace(country_code=0)
        num_ita_no_region = num_ita.replace(country_code=0)

        # is nsn match is True
        assert num_usa_no_region.is_nsn_match(num_usa_pn) == (
            pn.is_number_match(num_usa_no_region, num_usa_pn) == pn.MatchType.NSN_MATCH
        ) == True
        assert num_can_no_region.is_nsn_match(num_can_pn) == (
            pn.is_number_match(num_can_no_region, num_can_pn) == pn.MatchType.NSN_MATCH
        ) == True
        assert num_mex_no_region.is_nsn_match(num_mex_pn) == (
            pn.is_number_match(num_mex_no_region, num_mex_pn) == pn.MatchType.NSN_MATCH
        ) == True
        assert num_ita_no_region.is_nsn_match(num_ita_pn) == (
            pn.is_number_match(num_ita_no_region, num_ita_pn) == pn.MatchType.NSN_MATCH
        ) == True

    def test_is_exact_match(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can: PhoneNumber,
        num_can_pn: pn.PhoneNumber,
        num_mex: PhoneNumber,
        num_mex_pn: pn.PhoneNumber,
        num_ita: PhoneNumber,
        num_ita_pn: pn.PhoneNumber,
    ):
        # is exact match is True
        assert num_usa.is_exact_match(num_usa_pn) == (
            pn.is_number_match(num_usa, num_usa_pn) == pn.MatchType.EXACT_MATCH
        ) == True
        assert num_can.is_exact_match(num_can_pn) == (
            pn.is_number_match(num_can, num_can_pn) == pn.MatchType.EXACT_MATCH
        ) == True
        assert num_mex.is_exact_match(num_mex_pn) == (
            pn.is_number_match(num_mex, num_mex_pn) == pn.MatchType.EXACT_MATCH
        ) == True
        assert num_ita.is_exact_match(num_ita_pn) == (
            pn.is_number_match(num_ita, num_ita_pn) == pn.MatchType.EXACT_MATCH
        ) == True

        # is exact match is False
        assert num_usa.is_exact_match(num_can_pn) == (
            pn.is_number_match(num_usa, num_can_pn) == pn.MatchType.EXACT_MATCH
        ) == False
        assert num_can.is_exact_match(num_mex_pn) == (
            pn.is_number_match(num_can, num_mex_pn) == pn.MatchType.EXACT_MATCH
        ) == False
        assert num_mex.is_exact_match(num_ita_pn) == (
            pn.is_number_match(num_mex, num_ita_pn) == pn.MatchType.EXACT_MATCH
        ) == False
        assert num_ita.is_exact_match(num_usa_pn) == (
            pn.is_number_match(num_ita, num_usa_pn) == pn.MatchType.EXACT_MATCH
        ) == False
    
    def test_is_any_match(
        self,
        num_usa: PhoneNumber,
        num_usa_pn: pn.PhoneNumber,
        num_can_pn: pn.PhoneNumber,
    ):
        num_usa_no_region = num_usa.replace(country_code=0)
        num_usa_ext = num_usa.replace(extension="1234")
        num_usa_lead = num_usa.replace(number_of_leading_zeros=1, italian_leading_zero=True)

        ANY_MATCH = pn.MatchType.EXACT_MATCH, pn.MatchType.NSN_MATCH, pn.MatchType.SHORT_NSN_MATCH

        # is any match is True
        assert num_usa_no_region.is_any_match(num_usa_pn) == (
            pn.is_number_match(num_usa_no_region, num_usa_pn) in ANY_MATCH
        ) == True
        assert num_usa_ext.is_any_match(num_usa_pn) == (
            pn.is_number_match(num_usa_ext, num_usa_pn) in ANY_MATCH
        ) == True
        assert num_usa_lead.is_any_match(num_usa_pn) == (
            pn.is_number_match(num_usa_lead, num_usa_pn) in ANY_MATCH
        ) == True

        # is any match is False
        assert num_usa_no_region.is_any_match(num_can_pn) == (
            pn.is_number_match(num_usa_no_region, num_can_pn) in ANY_MATCH
        ) == False
        assert num_usa_ext.is_any_match(num_can_pn) == (
            pn.is_number_match(num_usa_ext, num_can_pn) in ANY_MATCH
        ) == False
        assert num_usa_lead.is_any_match(num_can_pn) == (
            pn.is_number_match(num_usa_lead, num_can_pn) in ANY_MATCH
        ) == False