# Walkthrough

## The PhoneNumber class.
At the core of `digitz` is the `PhoneNumber` class, which is implemented as an immutable (frozen) dataclass. This design prevents state changes, guaranteeing that cached properties always remain accurate and consistent.

## Creating a PhoneNumber instance.
There are a few different ways to create a new `PhoneNumber` instance.

- Parsing a string.
- Retrieiving an example number.
- Creating a new instance from an existing instance.

### Parsing a string.
The `PhoneNumber` class provides a `parse()` class method, enabling the creation of a new PhoneNumber instance from a raw string. A `NumberParseException` is raised if the string cannot be parsed.

```python
>>> from digitz import PhoneNumber

>>> num = PhoneNumber.parse("+12015550123")
```

### Retrieving an Example Number
The `PhoneNumber` class includes an `example_number()` class method, allowing you to generate a new PhoneNumber object for a specified region code and an optional phone number type.

```py
>>> from digitz import PhoneNumber

>>> num = PhoneNumber.example_number("US")
```

### Creating a new PhoneNumber from an already existing instance.
The `PhoneNumber` class includes a `replace()` method, which allows you to create a new instance of the class with specified attributes replaced. This method aligns with the immutable nature of the class, ensuring that any modifications result in a new object rather than altering the existing one.

```py
>>> from digitz import PhoneNumber

>>> num = PhoneNumber.parse("+12015550123")

>>> new_num = num.replace(country_code=44)

>>> new_num.country_code
44

>>> num.country_code
1
```

## Seamless E.164 String Conversion
The `__str__` method of the PhoneNumber class returns the phone number as an E.164-formatted string. This design ensures seamless integration with ORMs, allowing phone number objects to be automatically converted into strings and stored in databases in the standardized E.164 format, promoting consistency and compatibility across systems.
