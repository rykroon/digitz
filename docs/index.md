# Digitz

Python phone numbers made easy.


### Installation
```
pip install digitz
```


### Quick Example
```
from digitz import PhoneNumber

num = PhoneNumber.parse("+1 (202) 555-1234")
num.to_e164() == "+12025551234"
num.to_international() == "+1 202-555-1234"
num.to_rfc3966() == "tel:+1-202-555-1234"

num.region_code == "US"
num.get_country_name() == "United States"
num.get_country_name(lang="es") == "Estados Unidos"

```
