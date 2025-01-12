from enum import IntEnum
import phonenumbers as pn


__all__ = [
    "CountryCodeSource",
    "MatchType",
    "NumberParseErrorType",
    "PhoneNumberFormat",
    "PhoneNumberType",
]


class CountryCodeSource(IntEnum):
    """Enum for phone number country code sources.
    
    Attributes:
        UNSPECIFIED: Country code source is unspecified.
        FROM_NUMBER_WITH_PLUS_SIGN: Country code was extracted from number with a leading '+' sign.
        FROM_NUMBER_WITH_IDD: Country code was extracted from number with an IDD prefix.
        FROM_NUMBER_WITHOUT_PLUS_SIGN: Country code was extracted from number without a leading '+' sign.
        FROM_DEFAULT_COUNTRY: Country code was extracted from number with a default country code.
    """

    UNSPECIFIED = pn.CountryCodeSource.UNSPECIFIED
    FROM_NUMBER_WITH_PLUS_SIGN = pn.CountryCodeSource.FROM_NUMBER_WITH_PLUS_SIGN
    FROM_NUMBER_WITH_IDD = pn.CountryCodeSource.FROM_NUMBER_WITH_IDD
    FROM_NUMBER_WITHOUT_PLUS_SIGN = pn.CountryCodeSource.FROM_NUMBER_WITHOUT_PLUS_SIGN
    FROM_DEFAULT_COUNTRY = pn.CountryCodeSource.FROM_DEFAULT_COUNTRY


class MatchType(IntEnum):
    """Enum for phone number match types.
    
    Attributes:
        EXACT_MATCH: Exact match.
        NOT_A_NUMBER: Number is not a number.
        NO_MATCH: No match.
        NSN_MATCH: National significant number match.
        SHORT_NSN_MATCH: Short national significant number match.
    """

    EXACT_MATCH = pn.MatchType.EXACT_MATCH
    NOT_A_NUMBER = pn.MatchType.NOT_A_NUMBER
    NO_MATCH = pn.MatchType.NO_MATCH
    NSN_MATCH = pn.MatchType.NSN_MATCH
    SHORT_NSN_MATCH = pn.MatchType.SHORT_NSN_MATCH


class NumberParseErrorType(IntEnum):
    """Enum for phone number parsing error types.
    
    Attributes:
        INVALID_COUNTRY_CODE: Invalid country code.
        NOT_A_NUMBER: Number is not a number.
        TOO_SHORT_AFTER_IDD: Number is too short after IDD.
        TOO_SHORT_NSN: Number is too short.
        TOO_LONG: Number is too long.
    """

    INVALID_COUNTRY_CODE = pn.NumberParseException.INVALID_COUNTRY_CODE
    NOT_A_NUMBER = pn.NumberParseException.NOT_A_NUMBER
    TOO_SHORT_AFTER_IDD = pn.NumberParseException.TOO_SHORT_AFTER_IDD
    TOO_SHORT_NSN = pn.NumberParseException.TOO_SHORT_NSN
    TOO_LONG = pn.NumberParseException.TOO_LONG


class PhoneNumberFormat(IntEnum):
    """Enum for phone number formats.
    
    Attributes:
        E164: E.164 format.
        INTERNATIONAL: International format.
        NATIONAL: National format.
        RFC3966: RFC 3966 format.
    """

    E164 = pn.PhoneNumberFormat.E164
    INTERNATIONAL = pn.PhoneNumberFormat.INTERNATIONAL
    NATIONAL = pn.PhoneNumberFormat.NATIONAL
    RFC3966 = pn.PhoneNumberFormat.RFC3966


class PhoneNumberType(IntEnum):
    """Enum for phone number types.
    
    Attributes:
        FIXED_LINE: Fixed line.
        MOBILE: Mobile.
        FIXED_LINE_OR_MOBILE: Fixed line or mobile.
        TOLL_FREE: Toll free.
        PREMIUM_RATE: Premium rate.
        SHARED_COST: Shared cost.
        VOIP: Voice over IP.
        PERSONAL_NUMBER: Personal number.
        PAGER: Pager.
        UAN: Universal access number.
        VOICEMAIL: Voicemail.
        UNKNOWN: Unknown.
    """

    FIXED_LINE = pn.PhoneNumberType.FIXED_LINE
    MOBILE = pn.PhoneNumberType.MOBILE
    FIXED_LINE_OR_MOBILE = pn.PhoneNumberType.FIXED_LINE_OR_MOBILE
    TOLL_FREE = pn.PhoneNumberType.TOLL_FREE
    PREMIUM_RATE = pn.PhoneNumberType.PREMIUM_RATE
    SHARED_COST = pn.PhoneNumberType.SHARED_COST
    VOIP = pn.PhoneNumberType.VOIP
    PERSONAL_NUMBER = pn.PhoneNumberType.PERSONAL_NUMBER
    PAGER = pn.PhoneNumberType.PAGER
    UAN = pn.PhoneNumberType.UAN
    VOICEMAIL = pn.PhoneNumberType.VOICEMAIL
    UNKNOWN = pn.PhoneNumberType.UNKNOWN
