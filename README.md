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

num = PhoneNumber.parse("+1 (201) 555-0123")

num.region_code == "US"
num.is_possible is True
num.national_destination_code == "201"

num.to_e164() == "+12015550123"
num.to_international() == "+1 201-555-0123"
num.to_rfc3966() == "tel:+1-201-555-0123"
```

## License

`digitz` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
