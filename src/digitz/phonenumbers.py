# SPDX-FileCopyrightText: 2023-present Ryan Kroon <rykroon.tech@gmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import Optional, Type, TypeVar

import phonenumbers as pn

from digitz.enums import (
    CountryCodeSource, NumberParseErrorType, PhoneNumberFormat,  PhoneNumberType
)
from digitz.exceptions import (
    InvalidCountryCode, NotANumber, TooLong, TooShortAfterIDD, TooShortNsn
)


Self = TypeVar("Self", bound="PhoneNumberMixin")


class PhoneNumberMixin:

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

    def get_number_type(self):
        return PhoneNumberType(pn.number_type(self))

    def get_region_code(self):
        return pn.region_code_for_number(self)

    def is_toll_free(self):
        return self.get_number_type() == PhoneNumberType.TOLL_FREE

    def is_possible(self) -> bool:
        return pn.is_possible_number(self)

    def is_valid(self) -> bool:
        return pn.is_valid_number(self)

    def format(self, format: PhoneNumberFormat):
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
    country_code_source: Optional[CountryCodeSource] = CountryCodeSource.UNSPECIFIED
    preferred_domestic_carrier_code: Optional[str]
