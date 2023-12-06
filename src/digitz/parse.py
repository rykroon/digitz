from typing import NamedTuple, Optional

import phonenumbers as pn

from .enums import NumberParseErrorType, CountryCodeSource
from .exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


class PhoneNumberTuple(NamedTuple):
    country_code: int
    national_number: int
    extension: Optional[str]
    italian_leading_zero: Optional[bool]
    number_of_leading_zeros: Optional[int]
    raw_input: Optional[str]
    country_code_source: Optional[CountryCodeSource]
    preferred_domestic_carrier_code: Optional[str]


def parse(
    number: str, /, *, region: Optional[str] = None, keep_raw_input: bool = False
) -> PhoneNumberTuple:
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
            raise
    else:
        return PhoneNumberTuple(
            country_code=numobj.country_code,
            national_number=numobj.national_number,
            extension=numobj.extension,
            italian_leading_zero=numobj.italian_leading_zero,
            number_of_leading_zeros=numobj.number_of_leading_zeros,
            raw_input=numobj.raw_input,
            country_code_source=CountryCodeSource(numobj.country_code_source),
            preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
        )
