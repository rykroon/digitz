from phonenumbers import NumberParseException


"""
Note: Fix __init__ method for these exceptions so that they do not
require an error_type
"""


class InvalidCountryCode(NumberParseException):
    """Raised when the country code is invalid."""
    pass


class NotANumber(NumberParseException):
    """Raised when the string is not a number."""
    pass


class TooLong(NumberParseException):
    """Raised when the number is too long."""
    pass


class TooShortAfterIDD(NumberParseException):
    """Raised when the number is too short after IDD."""
    pass


class TooShortNsn(NumberParseException):
    """Raised when the number is too short after IDD."""
    pass
