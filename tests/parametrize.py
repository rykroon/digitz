import pytest
import phonenumbers as pn
from digitz import PhoneNumber


def create_number_list(
    regions: list[str], types: list[pn.PhoneNumberType | None]
) -> tuple[str, ...]:
    """
    Create a list of example numbers for the given regions and types.
    """
    numbers = []
    for region in regions:
        for type_ in types:
            if type_ is None:
                numobj = pn.example_number(region)
            elif type_ == pn.PhoneNumberType.UNKNOWN:
                numobj = pn.invalid_example_number(region)
            else:
                numobj = pn.example_number_for_type(region, type_)

            if numobj is None:
                continue

            number = pn.format_number(numobj, pn.PhoneNumberFormat.E164)
            if number not in numbers:
                numbers.append(number)

    return tuple(numbers)


USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"
CAN_EXAMPLE_NUMBER = "+1 506-234-5678"
MEX_EXAMPLE_NUMBER = "+52 200 123 4567"
ITA_EXAMPLE_NUMBER = "+39 02 1234 5678"

USA_FIXED_LINE_EXAMPLE_NUMBER = "+1 201-555-0123"
USA_MOBILE_EXAMPLE_NUMBER = "+1 201-555-0123"
USA_TOLL_FREE_EXAMPLE_NUMBER = "+1 800-234-5678"
USA_VOIP_EXAMPLE_NUMBER = "+1 305-209-0123"
USA_INVALID_EXAMPLE_NUMBER = "+1 201555012"
