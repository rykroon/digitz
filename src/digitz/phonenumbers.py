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


dataclass_kwargs = {}

if sys.version_info >= (3, 10):
    dataclass_kwargs["slots"] = True


@dataclass(**dataclass_kwargs)
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


@dataclass(frozen=True, **dataclass_kwargs)
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
