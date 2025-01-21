# digitz

[![PyPI - Version](https://img.shields.io/pypi/v/digitz.svg)](https://pypi.org/project/digitz)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/digitz.svg)](https://pypi.org/project/digitz)

-----

**Table of Contents**

- [Getting Started](#getting-started)
- [Running the tests](#running-the-tests)
- [Built With](built-with)
- [License](#license)
- [Example Usage](#example-usage)

## Getting Started

### Installing

Install digitz using pip.
```console
pip install digitz
```

## Running the tests

The easiest way to run the tests is by using Hatch. You can add the `--cover` argument to see the code coverage. You can add the `--all` argument to run the tests for all supported versions of python.
```console
> hatch test
> hatch test --cover
> hatch test --all
```

## Built With
- [Hatch](https://hatch.pypa.io/latest/) - Python project manager.
- [mkdocstrings](https://mkdocstrings.github.io/) - Static Site Generator for documentation.

## License

`digitz` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Example Usage
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
