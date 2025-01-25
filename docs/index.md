# Digitz

`digitz` is a phone number parsing, validating, and formatting library built on top of [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers). The goal of digitz is to bring a modern Python developer experience to working with phone numbers.


### Installation
Install digitz using pip.
```console
pip install digitz
```

### Quick Example
```py
>>> from digitz import PhoneNumber

>>> num = PhoneNumber.parse("+1 (201) 555-0123")

>>> num.region_code
'US'

>>> num.is_possible
True

>>> num.national_destination_code
'201'

>>> num.to_e164()
'+12015550123'

>>> num.to_national()
'(201) 555-0123'

>>> num.to_international()
'+1 201-555-0123'
```
