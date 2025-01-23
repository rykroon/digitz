# digitz

[![PyPI - Version](https://img.shields.io/pypi/v/digitz.svg)](https://pypi.org/project/digitz)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/digitz.svg)](https://pypi.org/project/digitz)
[![codecov](https://codecov.io/github/rykroon/digitz/graph/badge.svg?token=XMEHBWSYHD)](https://codecov.io/github/rykroon/digitz)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/digitz.svg)](https://pypi.org/project/digitz)

-----

## What is it?

digitz is a phone number parsing, validating, and formatting library built on top of [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers). The goal of digitz is to bring a modern Python developer experience to working with phone numbers.

## Table of Contents

- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Running the tests](#running-the-tests)
- [License](#license)
- [Example Usage](#example-usage)

## Getting Started

### Installing

Install digitz using pip.
```console
pip install digitz
```

## Documentation

The official documentation can be found [here](https://digitz.rykroon.com)

## Running the tests

It is recommended to run the tests using hatch.
```console
hatch test
```

## License

`digitz` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Example Usage

```python
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
