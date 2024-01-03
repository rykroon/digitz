from typing import Tuple, Union
import phonenumbers as pn
from .enums import PhoneNumberType, PhoneNumberFormat
from .interface import PhoneNumberInterface
from .parse import parse


def format_number(num_or_str: Union[PhoneNumberInterface, str], /, format: PhoneNumberFormat) -> str:
    """Return the phone number as a string in the specified format.
    Parameters:
        num_or_str: The phone number.
        fmt: The format to use.

    Returns:
        str: The phone number as a string in the specified format.
    """
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return pn.format_number(num, format)


def get_carrier_name(num_or_str: Union[PhoneNumberInterface, str], /, lang: str = "en") -> str:
    """Return the carrier name of the phone number.
    Parameters:
        num_or_str: The phone number.
        lang: The language to use.

    Returns:
        str: The carrier name of the phone number.
    """
    from phonenumbers.carrier import name_for_number

    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return name_for_number(num, lang)


def get_country_name(num_or_str: Union[PhoneNumberInterface, str], /, lang: str = "en") -> str:
    """Return the country name of the phone number.
    Parameters:
        num_or_str: The phone number.
        lang: The language to use.

    Returns:
        str: The country name of the phone number.
    """
    from phonenumbers.geocoder import country_name_for_number

    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return country_name_for_number(num, lang)


def get_description(num_or_str: Union[PhoneNumberInterface, str], /, lang: str = "en") -> str:
    """Return the description of the phone number.
    Parameters:
        num_or_str: The phone number.
        lang: The language to use.

    Returns:
        str: The description of the phone number.
    """
    from phonenumbers.geocoder import description_for_number

    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return description_for_number(num, lang)


def get_number_type(num_or_str: Union[PhoneNumberInterface, str], /) -> PhoneNumberType:
    """Return the type of phone number.
    Parameters:
        num_or_str: The phone number.

    Returns:
        int: The type of phone number.
    """
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return PhoneNumberType(pn.number_type(num))


def get_region_code(num_or_str: Union[PhoneNumberInterface, str], /) -> str:
    """Return the region code of the phone number.
    Parameters:
        num_or_str: The phone number.

    Returns:
        str: The region code of the phone number.
    """
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return pn.region_code_for_number(num)


def get_timezones(num_or_str: Union[PhoneNumberInterface, str], /) -> Tuple[str, ...]:
    """Return the timezones of the phone number.
    Parameters:
        num_or_str: The phone number.

    Returns:
        list: The timezones of the phone number.
    """
    from phonenumbers.timezone import time_zones_for_number
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return time_zones_for_number(num)


def is_possible_number(num_or_str: Union[PhoneNumberInterface, str], /) -> bool:
    """Return whether the phone number is possible.
    Parameters:
        num_or_str: The phone number.

    Returns:
        bool: Whether the phone number is possible.
    """
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return pn.is_possible_number(num)


def is_valid_number(num_or_str: Union[PhoneNumberInterface, str], /) -> bool:
    """Return whether the phone number is valid.
    Parameters:
        num_or_str: The phone number.

    Returns:
        bool: Whether the phone number is valid.
    """
    num = parse(num_or_str) if isinstance(num_or_str, str) else num_or_str
    return pn.is_valid_number(num)


def to_e164(num_or_str: Union[PhoneNumberInterface, str], /) -> str:
    """Return the phone number in E.164 format.
    Parameters:
        num_or_str: The phone number.

    Returns:
        str: The phone number in E.164 format.
    """
    return format_number(num_or_str, PhoneNumberFormat.E164)


def to_international(num_or_str: Union[PhoneNumberInterface, str], /) -> str:
    """Return the phone number in international format.
    Parameters:
        num_or_str: The phone number.

    Returns:
        str: The phone number in international format.
    """
    return format_number(num_or_str, PhoneNumberFormat.INTERNATIONAL)


def to_national(num_or_str: Union[PhoneNumberInterface, str], /) -> str:
    """Return the phone number in national format.
    Parameters:
        num_or_str: The phone number.

    Returns:
        str: The phone number in national format.
    """
    return format_number(num_or_str, PhoneNumberFormat.NATIONAL)


def to_rfc3966(num_or_str: Union[PhoneNumberInterface, str], /) -> str:
    """Return the phone number in RFC3966 format.
    Parameters:
        num_or_str: The phone number.

    Returns:
        str: The phone number in RFC3966 format.
    """
    return format_number(num_or_str, PhoneNumberFormat.RFC3966)
