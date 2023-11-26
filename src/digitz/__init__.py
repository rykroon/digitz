# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT

import phonenumbers as pn

from .enums import PhoneNumberFormat, PhoneNumberType
from .exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


class PhoneNumber(pn.PhoneNumber):

    @classmethod
    def from_string(cls, string: str) -> "PhoneNumber":
        """Parse a phone number from a string.

        Args:
            string: The string to parse.

        Returns:
            A PhoneNumber object.
        """
        try:
            return pn.parse(string, numobj=cls())

        except pn.NumberParseException as e:
            if e.error_type == pn.NumberParseException.INVALID_COUNTRY_CODE:
                raise InvalidCountryCode(e._msg) from e
            elif e.error_type == pn.NumberParseException.NOT_A_NUMBER:
                raise NotANumber(e._msg) from e
            elif e.error_type == pn.NumberParseException.TOO_LONG:
                raise TooLong(e._msg) from e
            elif e.error_type == pn.NumberParseException.TOO_SHORT_AFTER_IDD:
                raise TooShortAfterIDD(e._msg) from e
            elif e.error_type == pn.NumberParseException.TOO_SHORT_NSN:
                raise TooShortNsn(e._msg) from e
            else:
                raise

    @property
    def region_code(self) -> str:
        """Return the region code of the phone number.

        Returns:
            str: The region code of the phone number.
        """
        return pn.region_code_for_country_code(self.country_code)

    def get_country_name(self, lang="en") -> str:
        """Return the country name of the phone number.
        Parameters:
            lang: The language to use.
        Returns:
            The country name of the phone number.
        """
        from phonenumbers.geocoder import country_name_for_number
        return country_name_for_number(self, lang)

    def get_description(self, lang="en") -> str:
        """Return the description of the phone number.
        Parameters:
            lang: The language to use.
        Returns:
            The description of the phone number.
        """
        from phonenumbers.geocoder import description_for_number
        return description_for_number(self, lang)

    @property
    def number_type(self) -> PhoneNumberType:
        """Return the type of phone number.

        Returns:
            The type of phone number.
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
        return self.number_type is PhoneNumberType.TOLL_FREE

    def to_string(self, format: PhoneNumberFormat = PhoneNumberFormat.E164) -> str:
        """Return the phone number as a string in the specified format.

        Parameters:
            format: The format to use.

        Returns:
            str: The phone number in the specified format.
        """
        return pn.format_number(self, format)

    def to_e164(self) -> str:
        """Return the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return self.to_string(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Return the phone number in international format.

        Returns:
            str: The phone number in international format.
        """
        return self.to_string(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Return the phone number in national format.

        Returns:
            str: The phone number in national format.
        """
        return self.to_string(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Return the phone number in RFC3966 format.

        Returns:
            str: The phone number in RFC3966 format.
        """
        return self.to_string(PhoneNumberFormat.RFC3966)

    def __str__(self) -> str:
        """Return the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return self.to_e164()

    def __repr__(self) -> str:
        """Return the phone number in International format.

        Returns:
            str: The phone number in International format.
        """
        return f"<PhoneNumber: {self.to_international()}>"
