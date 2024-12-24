from typing import Union
import phonenumbers as pn

USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"


def create_number_list(
    regions: list[str], number_type: int = pn.PhoneNumberType.FIXED_LINE
) -> tuple[str, ...]:
    """
    Create a list of example numbers for the given regions and types.
    """
    numbers = []
    for region in regions:
        if number_type == pn.PhoneNumberType.UNKNOWN:
            numobj = pn.invalid_example_number(region)
        else:
            numobj = pn.example_number_for_type(region, number_type)

        if numobj is None:
            continue

        number = pn.format_number(numobj, pn.PhoneNumberFormat.E164)
        if number not in numbers:
            numbers.append(number)

    assert len(numbers) > 0, "No example numbers found"
    return tuple(numbers)
