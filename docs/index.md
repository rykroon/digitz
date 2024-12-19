# Digitz

Python phone numbers made easy.


### Installation
```
pip install digitz
```


### Quick Example
```
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
