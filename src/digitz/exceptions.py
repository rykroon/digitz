from phonenumbers import NumberParseException


class InvalidCountryCode(NumberParseException):
    """Raised when the country code is invalid."""
    error_type = NumberParseException.INVALID_COUNTRY_CODE

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class NotANumber(NumberParseException):
    """Raised when the string is not a number."""
    error_type = NumberParseException.NOT_A_NUMBER

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooLong(NumberParseException):
    """Raised when the number is too long."""
    error_type = NumberParseException.TOO_LONG

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooShortAfterIDD(NumberParseException):
    """Raised when the number is too short after IDD."""
    error_type = NumberParseException.TOO_SHORT_AFTER_IDD

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)


class TooShortNsn(NumberParseException):
    """Raised when the number is too short after IDD."""
    error_type = NumberParseException.TOO_SHORT_NSN

    def __init__(self, msg: str):
        super().__init__(self.error_type, msg)
