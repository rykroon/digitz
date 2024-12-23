from phonenumbers import NumberParseException
from .enums import NumberParseErrorType


__all__ = [
    "InvalidCountryCode",
    "NotANumber",
    "TooLong",
    "TooShort",
    "TooShortAfterIDD",
    "TooShortNsn",
]


class InvalidCountryCode(NumberParseException):
    """Raised when the country code is invalid."""

    def __init__(self, msg: str):
        super().__init__(NumberParseErrorType.INVALID_COUNTRY_CODE, msg)


class NotANumber(NumberParseException):
    """Raised when the string is not a number."""

    def __init__(self, msg: str):
        super().__init__(NumberParseErrorType.NOT_A_NUMBER, msg)


class TooLong(NumberParseException):
    """Raised when the number is too long."""

    def __init__(self, msg: str):
        super().__init__(NumberParseErrorType.TOO_LONG, msg)


class TooShort(NumberParseException):
    """Raised when the number is too short."""


class TooShortAfterIDD(TooShort):
    """Raised when the number is too short after International Direct Dialing (IDD)."""

    def __init__(self, msg: str):
        super().__init__(NumberParseErrorType.TOO_SHORT_AFTER_IDD, msg)


class TooShortNsn(TooShort):
    """Raised when the number is shorter than the National Significant Number (NSN)."""

    def __init__(self, msg: str):
        super().__init__(NumberParseErrorType.TOO_SHORT_NSN, msg)
