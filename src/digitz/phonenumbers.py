# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from functools import lru_cache, cached_property
from typing import Optional, Tuple, Type, TypeVar

import phonenumbers as pn

from digitz.enums import (
    CountryCodeSource, NumberParseErrorType, PhoneNumberFormat,  PhoneNumberType
)
from digitz.exceptions import (
    InvalidCountryCode, NotANumber, TooLong, TooShortAfterIDD, TooShortNsn
)


Self = TypeVar("Self", bound="PhoneNumberMixin")


class PhoneNumberMixin(pn.PhoneNumber):
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
            italian_leading_zero=numobj.italian_leading_zero,
            number_of_leading_zeros=numobj.number_of_leading_zeros,
            raw_input=numobj.raw_input,
            country_code_source=CountryCodeSource(numobj.country_code_source),
            preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
        )

    @property
    def national_destination_code_length(self) -> int:
        return pn.length_of_national_destination_code(self)

    @property
    def national_significant_number(self) -> str:
        return pn.national_significant_number(self)

    @property
    def national_destination_code(self) -> str:
        return self.national_significant_number[:self.national_destination_code_length]

    @property
    def number_type(self) -> PhoneNumberType:
        return PhoneNumberType(pn.number_type(self))

    @property
    def region_code(self) -> Optional[str]:
        return pn.region_code_for_number(self)

    @property
    def timezones(self) -> Tuple[str, ...]:
        from phonenumbers.timezone import time_zones_for_number
        return time_zones_for_number(self)

    def is_possible(self) -> bool:
        return pn.is_possible_number(self)

    def is_valid(self) -> bool:
        return pn.is_valid_number(self)

    def is_toll_free(self) -> bool:
        return self.number_type == PhoneNumberType.TOLL_FREE

    def is_voip(self) -> bool:
        return self.number_type == PhoneNumberType.VOIP

    def get_carrier_name(self, lang: str) -> str:
        from phonenumbers.carrier import name_for_number
        return name_for_number(self, lang=lang)

    def get_country_name(self, lang: str) -> str:
        from phonenumbers.geocoder import country_name_for_number
        return country_name_for_number(self, lang=lang)

    def get_description(self, lang: str) -> str:
        from phonenumbers.geocoder import description_for_number
        return description_for_number(self, lang=lang)

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


@dataclass
class PhoneNumber(PhoneNumberMixin):
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
class FrozenPhoneNumber(PhoneNumberMixin):
    """A frozen phone number."""

    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]

    @cached_property
    def national_destination_code_length(self) -> int:
        return super().national_destination_code_length

    @cached_property
    def national_significant_number(self) -> str:
        return super().national_significant_number

    @cached_property
    def number_type(self) -> PhoneNumberType:
        return super().number_type

    @cached_property
    def region_code(self) -> Optional[str]:
        return super().region_code

    @cached_property
    def timezones(self) -> Tuple[str, ...]:
        return super().timezones

    @lru_cache
    def is_possible(self) -> bool:
        return super().is_possible()

    @lru_cache
    def is_valid(self) -> bool:
        return super().is_valid()

    @lru_cache
    def get_carrier_name(self, lang: str) -> str:
        return super().get_carrier_name(lang=lang)

    @lru_cache
    def get_country_name(self, lang: str) -> str:
        return super().get_country_name(lang=lang)

    @lru_cache
    def get_description(self, lang: str) -> str:
        return super().get_description(lang=lang)

    @lru_cache
    def format(self, format: PhoneNumberFormat) -> str:
        return super().format(format=format)
