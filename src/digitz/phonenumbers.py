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


Self = TypeVar("Self", bound="PhoneNumber")


@dataclass(frozen=True)
class PhoneNumber(pn.PhoneNumber):
    country_code: int
    national_number: int
    extension: str = ""
    italian_leading_zero: bool = False
    number_of_leading_zeros: int = 1
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

        if numobj.country_code is None:
            numobj.country_code = 0

        if numobj.national_number is None:
            numobj.national_number = 0

        if numobj.extension is None:
            numobj.extension = ""

        if numobj.italian_leading_zero is None:
            numobj.italian_leading_zero = False

        if numobj.number_of_leading_zeros is None:
            numobj.number_of_leading_zeros = 1

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

    @property
    def national_destination_code(self) -> str:
        return self.national_significant_number[:self.national_destination_code_length]

    @property
    def subscriber_number(self) -> str:
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

    @property
    def is_toll_free(self) -> bool:
        return self.number_type == PhoneNumberType.TOLL_FREE

    @property
    def is_voip(self) -> bool:
        return self.number_type == PhoneNumberType.VOIP

    def is_number_match(self, other: Union[str, pn.PhoneNumber], /) -> int:
        # this function returns an enum that needs to be interpreted.
        return pn.is_number_match(self, other)

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

    def replace(
        self: Self,
        *,
        country_code: Optional[int] = None,
        national_number: Optional[int] = None,
        extension: Optional[str] = None,
        italian_leading_zero: Optional[bool] = None,
        number_of_leading_zeros: Optional[int] = None,
    ) -> Self:
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
