from dataclasses import is_dataclass
from typing import Any, Optional, Tuple, Type, TypeVar, Union

import phonenumbers as pn

from .enums import (
    CountryCodeSource,
    NumberParseErrorType,
    PhoneNumberType,
    PhoneNumberFormat,
)
from .phonenumbers import PhoneNumber, PhoneNumberInterface, SlottedPhoneNumber
from .exceptions import (
    InvalidCountryCode,
    NotANumber,
    TooLong,
    TooShortAfterIDD,
    TooShortNsn,
)


T = TypeVar("T", bound=PhoneNumberInterface)


def parse(
    number: str,
    /,
    *,
    region: Optional[str] = None,
    keep_raw_input: bool = False,
    numcls: Type[T] = PhoneNumber,
) -> T:
    is_immutable = (
        issubclass(numcls, tuple)
        or is_dataclass(numcls)
        and numcls.__dataclass_params__.frozen is True
    )
    # If numcls is immutable, then we need to use a mutable object to parse the number.
    numobj = numcls() if not is_immutable else SlottedPhoneNumber()

    try:
        numobj = pn.parse(
            number, region=region, keep_raw_input=keep_raw_input, numobj=numobj
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

    # Convert the country_code_source attribute to a CountryCodeSource enum.
    numobj.country_code_source = CountryCodeSource(numobj.country_code_source)

    if type(numobj) == numcls:
        return numobj

    # If the type of numobj is not the same as numcls, then we need to create a new
    # object of type numcls and copy the attributes of numobj to it.
    return numcls(
        country_code=numobj.country_code,
        national_number=numobj.national_number,
        extension=numobj.extension,
        italian_leading_zero=numobj.italian_leading_zero,
        number_of_leading_zeros=numobj.number_of_leading_zeros,
        raw_input=numobj.raw_input,
        country_code_source=numobj.country_code_source,
        preferred_domestic_carrier_code=numobj.preferred_domestic_carrier_code,
    )


def get_country_name(
    phn: Union[PhoneNumberInterface, str], lang: str = "en"
) -> Optional[str]:
    """Returns the country name of the phone number.

    Returns:
        str: The country name of the phone number.
    """
    from phonenumbers.geocoder import country_name_for_number

    if isinstance(phn, str):
        phn = parse(phn)

    return country_name_for_number(phn, lang)


def get_description(
    phn: Union[PhoneNumberInterface, str], lang: str = "en"
) -> Optional[str]:
    """Returns the description of the phone number.

    Returns:
        str: The description of the phone number.
    """
    from phonenumbers.geocoder import description_for_number

    if isinstance(phn, str):
        phn = parse(phn)

    return description_for_number(phn, lang)


def get_number_type(phn: Union[PhoneNumberInterface, str]) -> PhoneNumberType:
    """Returns the phone number type.

    Returns:
        The type of phone number.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return PhoneNumberType(pn.number_type(phn))


def get_region_code(phn: Union[PhoneNumberInterface, str]) -> Optional[str]:
    """Returns the region code of the phone number.

    Returns:
        str: The region code of the phone number.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return pn.region_code_for_number(phn)


def get_timezones(phn: Union[PhoneNumberInterface, str]) -> Tuple[str, ...]:
    """Returns the timezones of the phone number.

    Returns:
        str: The timezones of the phone number.
    """
    from phonenumbers.timezone import time_zones_for_number

    if isinstance(phn, str):
        phn = parse(phn)

    return time_zones_for_number(phn)


def is_toll_free(phn: Union[PhoneNumberInterface, str]) -> bool:
    """Returns whether the phone number is toll free.

    Returns:
        bool: Whether the phone number is toll free.
    """

    return get_number_type(phn) == PhoneNumberType.TOLL_FREE


def is_possible(phn: Union[PhoneNumberInterface, str]) -> bool:
    """Returns whether the phone number is possible.

    Returns:
        bool: Whether the phone number is possible.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return pn.is_possible_number(phn)


def is_valid(phn: Union[PhoneNumberInterface, str]) -> bool:
    """Returns whether the phone number is valid.

    Returns:
        bool: Whether the phone number is valid.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return pn.is_valid_number(phn)


def format(phn: Union[PhoneNumberInterface, str], format: PhoneNumberFormat) -> str:
    """Returns the phone number as a string in the specified format.

    Parameters:
        format: The format to use.

    Returns:
        str: The phone number in the specified format.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return pn.format_number(phn, format)


def to_e164(phn: Union[PhoneNumberInterface, str]) -> str:
    """Returns the phone number in E.164 format.

    Returns:
        str: The phone number in E.164 format.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return format(phn, PhoneNumberFormat.E164)


def to_international(phn: PhoneNumberInterface) -> str:
    """Returns the phone number in international format.

    Returns:
        str: The phone number in international format.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return format(phn, PhoneNumberFormat.INTERNATIONAL)


def to_national(phn: PhoneNumberInterface) -> str:
    """Returns the phone number in national format.

    Returns:
        str: The phone number in national format.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return format(phn, PhoneNumberFormat.NATIONAL)


def to_rfc3966(phn: PhoneNumberInterface) -> str:
    """Returns the phone number in RFC3966 format.

    Returns:
        str: The phone number in RFC3966 format.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return format(phn, PhoneNumberFormat.RFC3966)


def to_tuple(
    phn: Union[PhoneNumberInterface, str]
) -> Tuple[
    int,
    int,
    Optional[str],
    Optional[bool],
    Optional[int],
    Optional[str],
    Optional[int],
    Optional[str],
]:
    """Returns the phone number as a tuple.

    Returns:
        tuple: The phone number as a tuple.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return (
        phn.country_code,
        phn.national_number,
        phn.extension,
        phn.italian_leading_zero,
        phn.number_of_leading_zeros,
        phn.raw_input,
        phn.country_code_source,
        phn.preferred_domestic_carrier_code,
    )


def to_dict(phn: Union[PhoneNumberInterface, str]) -> dict[str, Any]:
    """Returns the phone number as a dictionary.

    Returns:
        dict: The phone number as a dictionary.
    """
    if isinstance(phn, str):
        phn = parse(phn)

    return {
        "country_code": phn.country_code,
        "national_number": phn.national_number,
        "extension": phn.extension,
        "italian_leading_zero": phn.italian_leading_zero,
        "number_of_leading_zeros": phn.number_of_leading_zeros,
        "raw_input": phn.raw_input,
        "country_code_source": phn.country_code_source,
        "preferred_domestic_carrier_code": phn.preferred_domestic_carrier_code,
    }


def is_phone_number_object(obj: Any) -> bool:
    """Check if an object is a PhoneNumber."""
    return (
        hasattr(obj, "country_code")
        and hasattr(obj, "national_number")
        and hasattr(obj, "extension")
        and hasattr(obj, "italian_leading_zero")
        and hasattr(obj, "number_of_leading_zeros")
        and hasattr(obj, "raw_input")
        and hasattr(obj, "country_code_source")
        and hasattr(obj, "preferred_domestic_carrier_code")
    )


def is_equal_phone_number(p1: PhoneNumberInterface, p2: PhoneNumberInterface) -> bool:
    """Check if two PhoneNumber objects are equal."""
    return (
        p1.country_code == p2.country_code
        and p1.national_number == p2.national_number
        and p1.extension == p2.extension
        and p1.italian_leading_zero == p2.italian_leading_zero
        and p1.number_of_leading_zeros == p2.number_of_leading_zeros
        and p1.raw_input == p2.raw_input
        and p1.country_code_source == p2.country_code_source
        and p1.preferred_domestic_carrier_code == p2.preferred_domestic_carrier_code
    )
