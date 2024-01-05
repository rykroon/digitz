from phonenumbers import NumberParseException
from .enums import NumberParseErrorType


class InvalidCountryCode(NumberParseException):
    """Raised when the country code is invalid."""

    error_type = NumberParseErrorType.INVALID_COUNTRY_CODE

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class NotANumber(NumberParseException):
    """Raised when the string is not a number."""

    error_type = NumberParseErrorType.NOT_A_NUMBER

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooLong(NumberParseException):
    """Raised when the number is too long."""

    error_type = NumberParseErrorType.TOO_LONG

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooShort(NumberParseException):
    """Raised when the number is too short."""


class TooShortAfterIDD(TooShort):
    """Raised when the number is too short after International Direct Dialing (IDD)."""

    error_type = NumberParseErrorType.TOO_SHORT_AFTER_IDD

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooShortNsn(TooShort):
    """Raised when the number is shorter than the National Significant Number (NSN)."""

    error_type = NumberParseErrorType.TOO_SHORT_NSN

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)
