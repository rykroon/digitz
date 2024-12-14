# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, field
from functools import lru_cache, cached_property, wraps
from typing import Optional, Tuple, Type, TypeVar, Union

import phonenumbers as pn
import pytz
from pytz.tzinfo import BaseTzInfo

from digitz.enums import (
    CountryCodeSource,
    MatchType,
    NumberParseErrorType,
    PhoneNumberFormat,
    PhoneNumberType,
)
from digitz.exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


Self = TypeVar("Self", bound="PhoneNumber")


def number_type_property(phone_number_type: PhoneNumberType) -> property:
    """Return a property that returns whether the phone number is of the given type."""

    def fget(self: Self) -> bool:
        return self.number_type == phone_number_type

    return property(
        fget=fget,
        doc=f"Return whether the phone number type is {phone_number_type.name.lower()}."
    )


@dataclass(frozen=True)
class PhoneNumber(pn.PhoneNumber):
    """A dataclass representing a phone number."""

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
        """Parse a phone number."""
        try:
            numobj = pn.parse(number, region=region, keep_raw_input=keep_raw_input)

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
                raise e  # pragma: no cover

        # Set default values for country_code and national_number
        # to avoid type checking errors
        if numobj.country_code is None:
            numobj.country_code = 0  # pragma: no cover

        if numobj.national_number is None:
            numobj.national_number = 0  # pragma: no cover

        return cls(
            country_code=numobj.country_code,
            national_number=numobj.national_number,
            extension=numobj.extension,
            italian_leading_zero=bool(numobj.italian_leading_zero),
            number_of_leading_zeros=numobj.number_of_leading_zeros,
            raw_input=numobj.raw_input,
            country_code_source=CountryCodeSource(numobj.country_code_source),
            preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
        )

    def __str__(self) -> str:
        """Return the E.164 representation of the phone number."""
        return self.to_e164()

    @cached_property
    def national_destination_code_length(self) -> int:
        """Return the length of the national destination code."""
        return pn.length_of_national_destination_code(self)

    @cached_property
    def national_significant_number(self) -> str:
        """Return the national significant number."""
        return pn.national_significant_number(self)

    @property
    def national_destination_code(self) -> str:
        """Return the national destination code."""
        return self.national_significant_number[: self.national_destination_code_length]

    @property
    def subscriber_number(self) -> str:
        """Return the subscriber number."""
        return self.national_significant_number[self.national_destination_code_length :]

    @cached_property
    def number_type(self) -> PhoneNumberType:
        """Return the type of the phone number."""
        return PhoneNumberType(pn.number_type(self))

    @cached_property
    def region_code(self) -> Optional[str]:
        """Return the region code of the phone number."""
        return pn.region_code_for_number(self)

    @cached_property
    def timezones(self) -> Tuple[BaseTzInfo, ...]:
        """Return the timezones of the phone number."""
        from phonenumbers.timezone import time_zones_for_number

        return tuple([pytz.timezone(zone) for zone in time_zones_for_number(self)])

    @cached_property
    def is_geographical(self) -> bool:
        """Return whether the phone number is geographical."""
        return pn.is_number_geographical(self)

    @cached_property
    def is_possible(self) -> bool:
        """Return whether the phone number is possible."""
        return pn.is_possible_number(self)

    @cached_property
    def is_valid(self) -> bool:
        """Return whether the phone number is valid."""
        return pn.is_valid_number(self)

    # Number type properties
    is_fixed_line = number_type_property(PhoneNumberType.FIXED_LINE)
    is_mobile = number_type_property(PhoneNumberType.MOBILE)
    is_fixed_line_or_mobile = number_type_property(PhoneNumberType.FIXED_LINE_OR_MOBILE)
    is_toll_free = number_type_property(PhoneNumberType.TOLL_FREE)
    is_premium_rate = number_type_property(PhoneNumberType.PREMIUM_RATE)
    is_shared_cost = number_type_property(PhoneNumberType.SHARED_COST)
    is_voip = number_type_property(PhoneNumberType.VOIP)
    is_personal_number = number_type_property(PhoneNumberType.PERSONAL_NUMBER)
    is_pager = number_type_property(PhoneNumberType.PAGER)
    is_uan = number_type_property(PhoneNumberType.UAN)
    is_voicemail = number_type_property(PhoneNumberType.VOICEMAIL)
    is_unknown = number_type_property(PhoneNumberType.UNKNOWN)

    def match(self, other: Union[str, pn.PhoneNumber], /) -> MatchType:
        """Return the match type of the phone number."""
        return MatchType(pn.is_number_match(self, other))

    def is_no_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Return whether the phone number is no match."""
        return self.match(other) == MatchType.NO_MATCH

    def is_short_nsn_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Return whether the phone number is a short NSN match."""
        return self.match(other) == MatchType.SHORT_NSN_MATCH

    def is_nsn_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Return whether the phone number is a NSN match."""
        return self.match(other) == MatchType.NSN_MATCH

    def is_exact_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Return whether the phone number is an exact match."""
        return self.match(other) == MatchType.EXACT_MATCH

    def is_any_match(self, other: Union[str, pn.PhoneNumber], /) -> bool:
        """Return whether the phone number is any match."""
        return (
            self.is_exact_match(other)
            or self.is_nsn_match(other)
            or self.is_short_nsn_match(other)
        )

    @lru_cache
    def get_carrier_name(self, lang: str) -> str:
        """Return the carrier name of the phone number."""
        from phonenumbers.carrier import name_for_number

        return name_for_number(self, lang=lang)

    @lru_cache
    def get_country_name(self, lang: str) -> str:
        """Return the country name of the phone number."""
        from phonenumbers.geocoder import country_name_for_number

        return country_name_for_number(self, lang=lang)

    @lru_cache
    def get_description(self, lang: str) -> str:
        """Return the description of the phone number."""
        from phonenumbers.geocoder import description_for_number

        return description_for_number(self, lang=lang)

    @lru_cache
    def format(self, format: PhoneNumberFormat) -> str:
        """Return the formatted phone number."""
        return pn.format_number(self, format)

    def to_e164(self) -> str:
        """Return the E.164 representation of the phone number."""
        return self.format(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        """Return the international representation of the phone number."""
        return self.format(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        """Return the national representation of the phone number."""
        return self.format(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        """Return the RFC3966 representation of the phone number."""
        return self.format(PhoneNumberFormat.RFC3966)

    def replace(
        self: Self,
        *,
        country_code: Optional[int] = None,
        national_number: Optional[int] = None,
        extension: Optional[str] = None,
        italian_leading_zero: Optional[bool] = None,
        number_of_leading_zeros: Optional[int] = None,
    ) -> Self:
        """Return a new phone number with the specified attributes replaced."""
        if country_code is None:
            country_code = self.country_code

        if national_number is None:
            national_number = self.national_number

        if extension is None:
            extension = self.extension

        if italian_leading_zero is None:
            italian_leading_zero = self.italian_leading_zero

        if number_of_leading_zeros is None:
            number_of_leading_zeros = self.number_of_leading_zeros

        return type(self)(
            country_code=country_code,
            national_number=national_number,
            extension=extension,
            italian_leading_zero=italian_leading_zero,
            number_of_leading_zeros=number_of_leading_zeros,
        )
