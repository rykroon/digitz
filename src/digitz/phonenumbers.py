# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, field
from functools import lru_cache, cached_property
from typing import Optional, Tuple, Type, TypeVar, Union

import phonenumbers as pn

from digitz.enums import (
    CountryCodeSource, NumberParseErrorType, PhoneNumberFormat,  PhoneNumberType
)
from digitz.exceptions import (
    InvalidCountryCode, NotANumber, TooLong, TooShortAfterIDD, TooShortNsn
)
from digitz.undefined import Undefined, UndefinedType


Self = TypeVar("Self", bound="PhoneNumber")


"""
Ideas
- Might need to do additional thinking on whether or not compatibility of the Java port is necesary.

"""


@dataclass(frozen=True)
class PhoneNumber(pn.PhoneNumber):
    country_code: int = 0
    national_number: int = 0
    extension: Optional[str] = None
    italian_leading_zero: Optional[bool] = None
    number_of_leading_zeros: Optional[int] = None

    # non-essential fields.
    raw_input: Optional[str] = field(default=None, repr=False)
    country_code_source: CountryCodeSource = CountryCodeSource.UNSPECIFIED
    preferred_domestic_carrier_code: Optional[str] = None

    @classmethod
    def parse(
        cls: Type[Self],
        number: str,
        /, *,
        region: Optional[str] = None,
        keep_raw_input: bool = False
    ) -> Self:
        try:
            numobj = pn.parse(
                number, region=region, keep_raw_input=keep_raw_input
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

    @cached_property
    def national_destination_code_length(self) -> int:
        return pn.length_of_national_destination_code(self)

    @cached_property
    def national_significant_number(self) -> str:
        return pn.national_significant_number(self)

    @cached_property
    def national_destination_code(self) -> str:
        return self.national_significant_number[:self.national_destination_code_length]

    @cached_property
    def subscriber_number(self):
        return self.national_significant_number[self.national_destination_code_length:]

    @cached_property
    def number_type(self) -> PhoneNumberType:
        return PhoneNumberType(pn.number_type(self))

    @cached_property
    def region_code(self) -> Optional[str]:
        return pn.region_code_for_number(self)

    @cached_property
    def timezones(self) -> Tuple[str, ...]:
        from phonenumbers.timezone import time_zones_for_number
        return time_zones_for_number(self)

    @cached_property
    def is_geographical(self) -> bool:
        return pn.is_number_geographical(self)

    @cached_property
    def is_possible(self) -> bool:
        return pn.is_possible_number(self)

    @cached_property
    def is_valid(self) -> bool:
        return pn.is_valid_number(self)

    @cached_property
    def is_toll_free(self) -> bool:
        return self.number_type == PhoneNumberType.TOLL_FREE

    @cached_property
    def is_voip(self) -> bool:
        return self.number_type == PhoneNumberType.VOIP

    @lru_cache
    def get_carrier_name(self, lang: str) -> str:
        from phonenumbers.carrier import name_for_number
        return name_for_number(self, lang=lang)

    @lru_cache
    def get_country_name(self, lang: str) -> str:
        from phonenumbers.geocoder import country_name_for_number
        return country_name_for_number(self, lang=lang)

    @lru_cache
    def get_description(self, lang: str) -> str:
        from phonenumbers.geocoder import description_for_number
        return description_for_number(self, lang=lang)

    @lru_cache
    def format(self, format: PhoneNumberFormat) -> str:
        return pn.format_number(self, format)

    def to_e164(self) -> str:
        return self.format(PhoneNumberFormat.E164)

    def to_international(self) -> str:
        return self.format(PhoneNumberFormat.INTERNATIONAL)

    def to_national(self) -> str:
        return self.format(PhoneNumberFormat.NATIONAL)

    def to_rfc3966(self) -> str:
        return self.format(PhoneNumberFormat.RFC3966)

    def clear(self):
        ...

    def merge_from(self):
        ...

    def replace(
        self: Self,
        *,
        country_code: Union[int, UndefinedType] = Undefined,
        national_number: Union[int, UndefinedType] = Undefined,
        extension: Union[Optional[str], UndefinedType] = Undefined,
        italian_leading_zero: Union[bool, UndefinedType] = Undefined,
        number_of_leading_zeros: Union[Optional[int], UndefinedType] = Undefined,
    ) -> Self:
        if country_code is Undefined:
            country_code = self.country_code

        if national_number is Undefined:
            national_number = self.national_number

        if extension is Undefined:
            extension = self.extension

        if italian_leading_zero is Undefined:
            italian_leading_zero = self.italian_leading_zero

        if number_of_leading_zeros is Undefined:
            number_of_leading_zeros = self.number_of_leading_zeros

        return type(self)(
            country_code=country_code,
            national_number=national_number,
            extension=extension,
            italian_leading_zero=italian_leading_zero,
            number_of_leading_zeros=number_of_leading_zeros,
        )
