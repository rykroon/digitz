# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
import sys
from typing import NamedTuple, Optional, Protocol

from .enums import CountryCodeSource


class PhoneNumberInterface(Protocol):
    """Interface for PhoneNumber."""

    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]


if sys.version_info >= (3, 10):

    @dataclass(slots=True)
    class SlottedPhoneNumber:
        """A phone number."""
        country_code: int = 0
        national_number: int = 0
        extension: Optional[str] = None
        italian_leading_zero: Optional[bool] = None
        number_of_leading_zeros: Optional[int] = None
        raw_input: Optional[str] = None
        country_code_source: Optional[CountryCodeSource] = CountryCodeSource.UNSPECIFIED
        preferred_domestic_carrier_code: Optional[str] = None

else:

    class SlottedPhoneNumber:
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

        def __init__(
            self,
            country_code: int = 0,
            national_number: int = 0,
            extension: Optional[str] = None,
            italian_leading_zero: Optional[bool] = None,
            number_of_leading_zeros: Optional[int] = None,
            raw_input: Optional[str] = None,
            country_code_source: Optional[CountryCodeSource] = CountryCodeSource.UNSPECIFIED,
            preferred_domestic_carrier_code: Optional[str] = None
        ) -> None:
            self.country_code = country_code
            self.national_number = national_number
            self.extension = extension
            self.italian_leading_zero = italian_leading_zero
            self.number_of_leading_zeros = number_of_leading_zeros
            self.raw_input = raw_input
            self.country_code_source = country_code_source
            self.preferred_domestic_carrier_code = preferred_domestic_carrier_code


@dataclass
class PhoneNumber:
    """A phone number."""

    country_code: int = 0
    national_number: int = 0
    extension: Optional[str] = None
    italian_leading_zero: Optional[bool] = None
    number_of_leading_zeros: Optional[int] = None
    raw_input: Optional[str] = None
    country_code_source: Optional[CountryCodeSource] = CountryCodeSource.UNSPECIFIED
    preferred_domestic_carrier_code: Optional[str] = None


@dataclass(frozen=True)
class FrozenPhoneNumber:
    """A frozen phone number."""

    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]


class PhoneNumberTuple(NamedTuple):
    """A phone number as a tuple."""

    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]
