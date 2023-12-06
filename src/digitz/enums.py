from enum import IntEnum
import phonenumbers as pn


class CountryCodeSource(IntEnum):
    """Enum for phone number country code sources."""

    UNSPECIFIED = pn.CountryCodeSource.UNSPECIFIED
    FROM_NUMBER_WITH_PLUS_SIGN = pn.CountryCodeSource.FROM_NUMBER_WITH_PLUS_SIGN
    FROM_NUMBER_WITH_IDD = pn.CountryCodeSource.FROM_NUMBER_WITH_IDD
    FROM_NUMBER_WITHOUT_PLUS_SIGN = pn.CountryCodeSource.FROM_NUMBER_WITHOUT_PLUS_SIGN
    FROM_DEFAULT_COUNTRY = pn.CountryCodeSource.FROM_DEFAULT_COUNTRY


class NumberParseErrorType(IntEnum):
    """Enum for phone number parsing error types."""

    INVALID_COUNTRY_CODE = pn.NumberParseException.INVALID_COUNTRY_CODE
    NOT_A_NUMBER = pn.NumberParseException.NOT_A_NUMBER
    TOO_SHORT_AFTER_IDD = pn.NumberParseException.TOO_SHORT_AFTER_IDD
    TOO_SHORT_NSN = pn.NumberParseException.TOO_SHORT_NSN
    TOO_LONG = pn.NumberParseException.TOO_LONG


class PhoneNumberFormat(IntEnum):
    """Enum for phone number formats."""

    E164 = pn.PhoneNumberFormat.E164
    INTERNATIONAL = pn.PhoneNumberFormat.INTERNATIONAL
    NATIONAL = pn.PhoneNumberFormat.NATIONAL
    RFC3966 = pn.PhoneNumberFormat.RFC3966


class PhoneNumberType(IntEnum):
    """Enum for phone number types."""

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
