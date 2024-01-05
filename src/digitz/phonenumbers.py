# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from functools import cached_property
from typing import Optional, Type, TypeVar

import phonenumbers as pn

from .enums import (
    CountryCodeSource,
    PhoneNumberFormat,
    PhoneNumberType,
    NumberParseErrorType,
)
from .exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


class PhoneNumber(pn.PhoneNumber):
    __slots__ = (
        "country_code",
        "national_number",
        "extension",
        "italian_leading_zero",
        "number_of_leading_zeros",
        "raw_input",
        "country_code_source",
        "preferred_domestic_carrier_code",
    )

    @classmethod
    def parse(
        cls: Type["PhoneNumber"],
        number: str,
        /,
        *,
        region: Optional[str] = None,
        keep_raw_input: bool = False,
    ) -> "PhoneNumber":
        """Parse a phone number.

        Parameters:
            number: The phone number to parse.
            region: The region to assume for phone numbers without an international prefix.
            keep_raw_input: Whether to keep the raw input.

        Returns:
            PhoneNumber: The parsed phone number.
        """
        try:
            numobj = pn.parse(
                number, region=region, keep_raw_input=keep_raw_input, numobj=cls()
            )

        except pn.NumberParseException as e:
            if e.error_type == NumberParseErrorType.INVALID_COUNTRY_CODE:
                raise InvalidCountryCode(e._msg) from e

            elif e.error_type == NumberParseErrorType.NOT_A_NUMBER:
                raise NotANumber(e._msg) from e

            elif e.error_type == NumberParseErrorType.TOO_LONG:
                raise TooLong(e._msg) from e

            elif e.error_type == NumberParseErrorType.TOO_SHORT_AFTER_IDD:
                raise TooShortAfterIDD(e._msg) from e

            elif e.error_type == NumberParseErrorType.TOO_SHORT_NSN:
                raise TooShortNsn(e._msg) from e

            else:
                raise e

        numobj.country_code_source = CountryCodeSource(numobj.country_code_source)
        assert isinstance(numobj, cls)
        return numobj

    @cached_property
    def region_code(self) -> Optional[str]:
        """Returns the region code of the phone number.

        Returns:
            str: The region code of the phone number.
        """
        return pn.region_code_for_number(self)

    @cached_property
    def number_type(self) -> PhoneNumberType:
        """Returns the phone number type.

        Returns:
            The type of phone number.
        """
        return PhoneNumberType(pn.number_type(self))

    def is_possible(self) -> bool:
        """Returns whether the phone number is possible.

        Returns:
            bool: Whether the phone number is possible.
        """
        return pn.is_possible_number(self)

    def is_valid(self) -> bool:
        """Returns whether the phone number is valid.

        Returns:
            bool: Whether the phone number is valid.
        """
        return pn.is_valid_number(self)

    def is_toll_free(self) -> bool:
        """Returns whether the phone number is toll free.

        Returns:
            bool: Whether the phone number is toll free.
        """
        return self.number_type == PhoneNumberType.TOLL_FREE

    def format(self, format: PhoneNumberFormat) -> str:
        """Returns the phone number as a string in the specified format.

        Parameters:
            format: The format to use.

        Returns:
            str: The phone number in the specified format.
        """
        return pn.format_number(self, format)

    def to_e164(self) -> str:
        """Returns the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return self.format(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Returns the phone number in international format.

        Returns:
            str: The phone number in international format.
        """
        return self.format(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Returns the phone number in national format.

        Returns:
            str: The phone number in national format.
        """
        return self.format(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Returns the phone number in RFC3966 format.

        Returns:
            str: The phone number in RFC3966 format.
        """
        return self.format(PhoneNumberFormat.RFC3966)

    def __str__(self) -> str:
        """Returns the phone number in E.164 format.

        Returns:
            str: The phone number in E.164 format.
        """
        return self.to_e164()
