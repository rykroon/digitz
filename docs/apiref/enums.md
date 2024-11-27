# Enums

::: digitz.enums.CountryCodeSource
    options:
        members:
        - UNSPECIFIED
        - FROM_NUMBER_WITH_PLUS_SIGN
        - FROM_NUMBER_WITH_IDD
        - FROM_NUMBER_WITHOUT_PLUS_SIGN
        - FROM_DEFAULT_COUNTR

::: digitz.enums.MatchType
    options:
        members:
        - EXACT_MATCH
        - NOT_A_NUMBER
        - NO_MATCH
        - NSN_MATCH
        - SHORT_NSN_MATCH

::: digitz.enums.NumberParseErrorType
    options:
        members:
        - INVALID_COUNTRY_CODE
        - NOT_A_NUMBER
        - TOO_SHORT_AFTER_IDD
        - TOO_SHORT_NSN
        - TOO_LONG

::: digitz.enums.PhoneNumberFormat
    options:
        members:
        - E164
        - INTERNATIONAL
        - NATIONAL
        - RFC3966

::: digitz.enums.PhoneNumberType
    options:
        members:
        - FIXED_LINE
        - MOBILE
        - FIXED_LINE_OR_MOBILE
        - TOLL_FREE
        - PREMIUM_RATE
        - SHARED_COST
        - VOIP
        - PERSONAL_NUMBER
        - PAGER
        - UAN
        - VOICEMAIL
        - UNKNOWN
