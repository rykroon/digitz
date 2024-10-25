from typing import Optional, Tuple, Union



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


def get_timezones(phn: Union[PhoneNumberInterface, str]) -> Tuple[str, ...]:
    """Returns the timezones of the phone number.

    Returns:
        str: The timezones of the phone number.
    """
    from phonenumbers.timezone import time_zones_for_number

    if isinstance(phn, str):
        phn = parse(phn)

    return time_zones_for_number(phn)

