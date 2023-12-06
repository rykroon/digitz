# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from functools import cached_property
from typing import Optional
import phonenumbers as pn

from .enums import CountryCodeSource, PhoneNumberFormat, PhoneNumberType
from .parse import parse


@dataclass(repr=False, eq=False, frozen=True)
class PhoneNumber(pn.PhoneNumber):
    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]

    @classmethod
    def parse(
        cls,
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
        result = parse(number, region=region, keep_raw_input=keep_raw_input)
        return cls(
            country_code=result.country_code,
            national_number=result.national_number,
            extension=result.extension,
            italian_leading_zero=result.italian_leading_zero,
            number_of_leading_zeros=result.number_of_leading_zeros,
            raw_input=result.raw_input,
            country_code_source=result.country_code_source,
            preferred_domestic_carrier_code=result.preferred_domestic_carrier_code,
        )

    @cached_property
    def region_code(self) -> str:
        """Return the region code of the phone number.

        Returns:
            str: The region code of the phone number.
        """
        return pn.region_code_for_number(self)

    @cached_property
    def number_type(self) -> PhoneNumberType:
        """Return the type of phone number.

        Returns:
            The type of phone number.
        """
        return PhoneNumberType(pn.number_type(self))

    def get_country_name(self, lang: str = "en") -> str:
        """Return the country name of the phone number.
        Parameters:
            lang: The language to use.
        Returns:
            The country name of the phone number.
        """
        from phonenumbers.geocoder import country_name_for_number

        return country_name_for_number(self, lang)

    def get_description(self, lang: str = "en") -> str:
        """Return the description of the phone number.
        Parameters:
            lang: The language to use.
        Returns:
            The description of the phone number.
        """
        from phonenumbers.geocoder import description_for_number

        return description_for_number(self, lang)

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
        return self.number_type == PhoneNumberType.TOLL_FREE

    def format(self, format: PhoneNumberFormat) -> str:
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
        return self.format(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Return the phone number in international format.

        Returns:
            str: The phone number in international format.
        """
        return self.format(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Return the phone number in national format.

        Returns:
            str: The phone number in national format.
        """
        return self.format(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Return the phone number in RFC3966 format.

        Returns:
            str: The phone number in RFC3966 format.
        """
        return self.format(PhoneNumberFormat.RFC3966)

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
        return f"<{self.__class__.__name__}: {self.to_international()}>"
