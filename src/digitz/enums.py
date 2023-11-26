
from enum import IntEnum
import phonenumbers as pn


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


class PhoneNumberFormat(IntEnum):
    """Enum for phone number formats."""

    E164 = pn.PhoneNumberFormat.E164
    INTERNATIONAL = pn.PhoneNumberFormat.INTERNATIONAL
    NATIONAL = pn.PhoneNumberFormat.NATIONAL
    RFC3966 = pn.PhoneNumberFormat.RFC3966
