from typing import Union
import phonenumbers as pn

USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"


def create_number_list(
    regions: list[str], types: list[Union[int, None]]
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

    assert len(numbers) > 0, "No example numbers found"
    return tuple(numbers)
