# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, field
from functools import lru_cache, cached_property
from typing import Any, Dict, Optional, Tuple, Type, TypeVar, Union

import phonenumbers as pn
from zoneinfo import ZoneInfo

from digitz.enums import (
    CountryCodeSource,
    MatchType,
    NumberParseErrorType,
    PhoneNumberFormat,
    PhoneNumberType,
)

PhoneNumberTuple = Tuple[
    int,
    int,
    Optional[str],
    bool,
    Optional[int],
    Optional[str],
    Union[CountryCodeSource, int],
    Optional[str],
]


class _MISSING_TYPE:
    pass


MISSING = _MISSING_TYPE()


Self = TypeVar("Self", bound="PhoneNumber")


@dataclass(frozen=True)
class PhoneNumber(pn.PhoneNumber):
    """
    A dataclass representing a phone number.

    Parameters:
        country_code: The country code of the phone number.
        national_number: The national number of the phone number.
        extension: The extension of the phone number.
        italian_leading_zero: Whether the phone number has an Italian leading zero.
        number_of_leading_zeros: The number of leading zeros in the phone number.
        raw_input: The raw input of the phone number.
        country_code_source: The source of the country code.
        preferred_domestic_carrier_code: The preferred domestic
    """

    country_code: int
    national_number: int
    extension: Optional[str] = None
    italian_leading_zero: bool = False
    number_of_leading_zeros: Optional[int] = None
    raw_input: Optional[str] = field(default=None, repr=False)
    country_code_source: CountryCodeSource = CountryCodeSource.UNSPECIFIED
    preferred_domestic_carrier_code: Optional[str] = None

    @classmethod
    def parse(
        cls: Type[Self],
        number: str,
        /,
        *,
        region: Optional[str] = None,
        keep_raw_input: bool = False,
    ) -> Self:
        """Attempts to parse a string and return a new PhoneNumber object.

        Parameters:
            number: The phone number to parse.
            region: The region code the phone number is expected to be from.
            keep_raw_input: Whether to keep the raw input of the phone number.

        Raises:
            NumberParseException: If the phone number cannot be parsed.

        Returns:
            A new PhoneNumber object.
        """
        try:
            numobj = pn.parse(number, region=region, keep_raw_input=keep_raw_input)

        except pn.NumberParseException as e:
            e.error_type = NumberParseErrorType(e.error_type)
            raise e

        return cls(
            country_code=numobj.country_code or 0,
            national_number=numobj.national_number or 0,
            extension=numobj.extension,
            italian_leading_zero=bool(numobj.italian_leading_zero),
            number_of_leading_zeros=numobj.number_of_leading_zeros,
            raw_input=numobj.raw_input,
            country_code_source=CountryCodeSource(numobj.country_code_source),
            preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
        )

    @classmethod
    def example_number(
        cls: Type[Self],
        region: str,
        number_type: PhoneNumberType = PhoneNumberType.FIXED_LINE,
    ) -> Optional[Self]:
        """Returns an example phone number for the specified region and number type.

        Parameters:
            region: The region code of the phone number.
            number_type: The type of phone number.

        Returns:
            An example phone number for the specified region and number type.
        """
        numobj = pn.example_number_for_type(region, number_type)
        if numobj is None:
            return None

        return cls(
            country_code=numobj.country_code or 0,
            national_number=numobj.national_number or 0,
            extension=numobj.extension,
            italian_leading_zero=bool(numobj.italian_leading_zero),
            number_of_leading_zeros=numobj.number_of_leading_zeros,
            raw_input=numobj.raw_input,
            country_code_source=CountryCodeSource(numobj.country_code_source),
            preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
        )

    def __getstate__(self) -> PhoneNumberTuple:
        return (
            self.country_code,
            self.national_number,
            self.extension,
            self.italian_leading_zero,
            self.number_of_leading_zeros,
            self.raw_input,
            self.country_code_source.value,
            self.preferred_domestic_carrier_code,
        )

    def __setstate__(self, state: PhoneNumberTuple) -> None:
        self.__dict__.update(
            {
                "country_code": state[0],
                "national_number": state[1],
                "extension": state[2],
                "italian_leading_zero": state[3],
                "number_of_leading_zeros": state[4],
                "raw_input": state[5],
                "country_code_source": CountryCodeSource(state[6]),
                "preferred_domestic_carrier_code": state[7],
            }
        )

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __str__(self) -> str:
        """Returns the E.164 representation of the phone number."""
        return self.to_e164()

    # ~~~ national number related properties ~~~
    @cached_property
    def national_destination_code_length(self) -> int:
        """Returns the length of the national destination code."""
        return pn.length_of_national_destination_code(self)

    @property
    def ndc_length(self) -> int:
        """An alias for the national_destination_code_length property."""
        return self.national_destination_code_length

    @cached_property
    def national_significant_number(self) -> str:
        """Returns the national significant number."""
        return pn.national_significant_number(self)

    @property
    def nsn(self) -> str:
        """An alias for the national_significant_number property."""
        return self.national_significant_number

    @property
    def national_destination_code(self) -> str:
        """Returns the national destination code."""
        return self.national_significant_number[: self.national_destination_code_length]

    @property
    def ndc(self) -> str:
        """An alias for the national_destination_code property."""
        return self.national_destination_code

    @property
    def subscriber_number(self) -> str:
        """Returns the subscriber number."""
        return self.national_significant_number[self.national_destination_code_length :]

    # ~~~ region related properties ~~~
    @cached_property
    def region_code(self) -> Optional[str]:
        """Returns the region code of the phone number."""
        return pn.region_code_for_number(self)

    @cached_property
    def is_geographical(self) -> bool:
        """Returns True if the phone number has a geographical association."""
        return pn.is_number_geographical(self)

    @cached_property
    def is_nanpa_country(self) -> bool:
        """Returns True if the phone number is from a NANPA country."""
        if self.region_code is None:
            return False  # pragma: no cover
        return pn.is_nanpa_country(self.region_code)

    # ~~~ phone number validity properties ~~~
    @cached_property
    def is_possible(self) -> bool:
        """Returns True if the phone number is possible."""
        return pn.is_possible_number(self)

    @cached_property
    def is_valid(self) -> bool:
        """Returns True if the phone number is of a valid pattern."""
        if self.region_code is None:
            return False
        return pn.is_valid_number_for_region(self, self.region_code)

    # ~~~ Number type properties ~~~
    @cached_property
    def number_type(self) -> PhoneNumberType:
        """Returns the type of a valid phone number."""
        return PhoneNumberType(pn.number_type(self))

    @property
    def is_fixed_line(self) -> bool:
        """Returns whether the phone number type is fixed line."""
        return self.number_type == PhoneNumberType.FIXED_LINE

    @property
    def is_mobile(self) -> bool:
        """Returns whether the phone number type is mobile."""
        return self.number_type == PhoneNumberType.MOBILE

    @property
    def is_fixed_line_or_mobile(self) -> bool:
        """Returns whether the phone number type is fixed line or mobile."""
        return self.number_type == PhoneNumberType.FIXED_LINE_OR_MOBILE

    @property
    def is_toll_free(self) -> bool:
        """Returns whether the phone number type is toll free."""
        return self.number_type == PhoneNumberType.TOLL_FREE

    @property
    def is_premium_rate(self) -> bool:
        """Returns whether the phone number type is premium rate."""
        return self.number_type == PhoneNumberType.PREMIUM_RATE

    @property
    def is_shared_cost(self) -> bool:
        """Returns whether the phone number type is shared cost."""
        return self.number_type == PhoneNumberType.SHARED_COST

    @property
    def is_voip(self) -> bool:
        """Returns whether the phone number type is voip."""
        return self.number_type == PhoneNumberType.VOIP

    @property
    def is_personal_number(self) -> bool:
        """Returns whether the phone number type is personal number."""
        return self.number_type == PhoneNumberType.PERSONAL_NUMBER

    @property
    def is_pager(self) -> bool:
        """Returns whether the phone number type is pager."""
        return self.number_type == PhoneNumberType.PAGER

    @property
    def is_uan(self) -> bool:
        """Returns whether the phone number type is a universal access number."""
        return self.number_type == PhoneNumberType.UAN

    @property
    def is_voicemail(self) -> bool:
        """Returns whether the phone number type is a voicemail access number."""
        return self.number_type == PhoneNumberType.VOICEMAIL

    @cached_property
    def timezones(self) -> Tuple[ZoneInfo, ...]:
        """Returns the timezones of the phone number."""
        from phonenumbers.timezone import time_zones_for_number

        return tuple([ZoneInfo(zone) for zone in time_zones_for_number(self)])

    # ~~~ Match type methods ~~~
    def match(self, other: Union[str, pn.PhoneNumber], /) -> MatchType:
        """Returns the match type of the phone number.

        Parameters:
            other: The other phone number to compare.

        Returns:
            The match type of the phone number.
        """
        return MatchType(pn.is_number_match(self, other))

    def is_short_nsn_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Returns True if the other phone number is a short NSN match."""
        return self.match(other) == MatchType.SHORT_NSN_MATCH

    def is_nsn_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Returns True if the other phone number is a NSN match."""
        return self.match(other) == MatchType.NSN_MATCH

    def is_exact_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Returns True if the other phone number is an exact match."""
        return self.match(other) == MatchType.EXACT_MATCH

    def is_any_nsn_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Returns True if the other phone number is any NSN match."""
        return self.match(other) in (MatchType.SHORT_NSN_MATCH, MatchType.NSN_MATCH)

    def is_any_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Returns True if the other phone number is any match."""
        return self.match(other) in (
            MatchType.EXACT_MATCH,
            MatchType.NSN_MATCH,
            MatchType.SHORT_NSN_MATCH,
        )

    # ~~~ Carrier and country name methods ~~~
    @lru_cache
    def get_carrier_name(self, lang: str) -> str:
        """Returns the carrier name of the phone number.

        Parameters:
            lang: The language to use.

        Returns:
            The carrier name of the phone number.
        """
        from phonenumbers.carrier import name_for_number

        return name_for_number(self, lang=lang)

    @lru_cache
    def get_country_name(self, lang: str) -> str:
        """Returns the country name of the phone number.

        Parameters:
            lang: The language to use.

        Returns:
            The country name of the phone number.
        """
        from phonenumbers.geocoder import country_name_for_number

        return country_name_for_number(self, lang=lang)

    @lru_cache
    def get_description(self, lang: str) -> str:
        """Returns the description of the phone number.

        Parameters:
            lang: The language to use.

        Returns:
            The description of the phone number.
        """
        from phonenumbers.geocoder import description_for_number

        return description_for_number(self, lang=lang)

    # ~~~ Formatting methods ~~~
    @lru_cache
    def format(self, format: PhoneNumberFormat) -> str:
        """Returns the string representation of the phone number in the specified format.

        Parameters:
            format: The format to use.

        Returns:
            The string representation of the phone number.
        """
        return pn.format_number(self, format)

    def to_e164(self) -> str:
        """Returns the E.164 representation of the phone number."""
        return self.format(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Returns the international representation of the phone number."""
        return self.format(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Returns the national representation of the phone number."""
        return self.format(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Returns the RFC3966 representation of the phone number."""
        return self.format(PhoneNumberFormat.RFC3966)

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the phone number."""
        return {
            "country_code": self.country_code,
            "national_number": self.national_number,
            "extension": self.extension,
            "italian_leading_zero": self.italian_leading_zero,
            "number_of_leading_zeros": self.number_of_leading_zeros,
            "raw_input": self.raw_input,
            "country_code_source": self.country_code_source,
            "preferred_domestic_carrier_code": self.preferred_domestic_carrier_code,
        }

    def to_tuple(self) -> PhoneNumberTuple:
        """Returns a tuple representation of the phone number."""
        return (
            self.country_code,
            self.national_number,
            self.extension,
            self.italian_leading_zero,
            self.number_of_leading_zeros,
            self.raw_input,
            self.country_code_source,
            self.preferred_domestic_carrier_code,
        )

    def replace(
        self: Self,
        *,
        country_code: Union[int, _MISSING_TYPE] = MISSING,
        national_number: Union[int, _MISSING_TYPE] = MISSING,
        extension: Union[Optional[str], _MISSING_TYPE] = MISSING,
        italian_leading_zero: Union[bool, _MISSING_TYPE] = MISSING,
        number_of_leading_zeros: Union[Optional[int], _MISSING_TYPE] = MISSING,
    ) -> Self:
        """Returns a new phone number with the specified attributes replaced.

        Parameters:
            country_code: The country code of the phone number.
            national_number: The national number of the phone number.
            extension: The extension of the phone number.
            italian_leading_zero: Whether the phone number has an Italian leading zero.
            number_of_leading_zeros: The number of leading zeros in the phone number.

        Returns:
            A new PhoneNumber object
        """
        if isinstance(country_code, _MISSING_TYPE):
            country_code = self.country_code

        if isinstance(national_number, _MISSING_TYPE):
            national_number = self.national_number

        if isinstance(extension, _MISSING_TYPE):
            extension = self.extension

        if isinstance(italian_leading_zero, _MISSING_TYPE):
            italian_leading_zero = self.italian_leading_zero

        if isinstance(number_of_leading_zeros, _MISSING_TYPE):
            number_of_leading_zeros = self.number_of_leading_zeros

        return type(self)(
            country_code=country_code,
            national_number=national_number,
            extension=extension,
            italian_leading_zero=italian_leading_zero,
            number_of_leading_zeros=number_of_leading_zeros,
        )
