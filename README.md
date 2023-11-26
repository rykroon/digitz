# digitz

[![PyPI - Version](https://img.shields.io/pypi/v/digitz.svg)](https://pypi.org/project/digitz)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/digitz.svg)](https://pypi.org/project/digitz)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install digitz
```

## Quickstart
```
from digitz import PhoneNumber

num = PhoneNumber.from_string("+1 (202) 555-1234")
num.to_e164() == "+12025551234"
num.to_international() == "+1 202-555-1234"
num.to_rfc3966() == "tel:+1-202-555-1234"

num.region_code == "US"
num.get_country_name() == "United States"
num.get_country_name(lang="es") == "Estados Unidos"

```

## License

`digitz` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
