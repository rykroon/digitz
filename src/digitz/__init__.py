# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from enum import Enum
import phonenumbers as pn

from .exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


class PhoneNumberType(Enum):
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


class PhoneNumber(pn.PhoneNumber):

    @property
    def region_code(self) -> str:
        """Return the region code of the phone number.

        Returns:
            str: The region code of the phone number.
        """
        return pn.region_code_for_country_code(self.country_code)

    @property
    def type(self) -> str:
        """Return the type of phone number.

        Returns:
            str: The type of phone number.
        """
        return PhoneNumberType(pn.number_type(self))

    def is_possible(self) -> bool:
        """Return whether the phone number is possible.

        Returns:
            bool: Whether the phone number is possible.
        """
        return pn.is_possible_number(self)

    def is_valid(self) -> bool:
        """Return whether the phone number is valid.

        Returns:
            bool: Whether the phone number is valid.
        """
        return pn.is_valid_number(self)

    def is_toll_free(self) -> bool:
        """Return whether the phone number is toll free.

        Returns:
            bool: Whether the phone number is toll free.
        """
        return self.type is PhoneNumberType.TOLL_FREE

    def to_e164(self) -> str:
        """Return the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return pn.format_number(self, pn.PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Return the phone number in international format.

        Returns:
            str: The phone number in international format.
        """
        return pn.format_number(self, pn.PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Return the phone number in national format.

        Returns:
            str: The phone number in national format.
        """
        return pn.format_number(self, pn.PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Return the phone number in RFC3966 format.

        Returns:
            str: The phone number in RFC3966 format.
        """
        return pn.format_number(self, pn.PhoneNumberFormat.RFC3966)

    def __str__(self) -> str:
        """Return the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return self.to_e164()

    def __repr__(self) -> str:
        """Return the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return f"<PhoneNumber {self.to_e164()}>"


def parse(string: str) -> str:
    """Parse a phone number from a string.

    Args:
        string (str): The string to parse.

    Returns:
        str: The parsed phone number.
    """
    try:
        obj = PhoneNumber()
        obj.merge_from(pn.parse(string))
        return obj

    except pn.NumberParseException as e:
        if e.error_type == pn.NumberParseException.INVALID_COUNTRY_CODE:
            raise InvalidCountryCode from e
        elif e.error_type == pn.NumberParseException.NOT_A_NUMBER:
            raise NotANumber from e
        elif e.error_type == pn.NumberParseException.TOO_LONG:
            raise TooLong from e
        elif e.error_type == pn.NumberParseException.TOO_SHORT_AFTER_IDD:
            raise TooShortAfterIDD from e
        elif e.error_type == pn.NumberParseException.TOO_SHORT_NSN:
            raise TooShortNsn from e
        else:
            raise
