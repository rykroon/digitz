# Why Digitz?

The [phonenumbers](https://pypi.org/project/phonenumbers/) library for Python has long been a trusted solution for phone number validation, formatting, and parsing. While its accuracy and reliability are unquestionable, the library has been slow to embrace modern Python features, often feeling like it's stuck in the past.

`digitz` is a fresh take on phone number handling, designed to bring modern Python features to the world of phone number processing. If you've ever struggled with the verbose syntax or outdated API design of the phonenumbers library, `digitz` is here to change that.

Below are some examples on how digitz improves the developer experience.
___

## Proper Enums

In the `phonenumbers` library there are several classes that behave like enums, but are not actually traditional python enums. They are just classes with class attributes. See the [PhoneNumberType](https://github.com/daviddrysdale/python-phonenumbers/blob/d7fe6c6f1e416797f439beb2ae2bb365360bf340/python/phonenumbers/phonenumberutil.py#L458) class as an example.

In the below code block, `pn.number_type(n)` returns the value `3`. This result does not express any meaning and it is left to the developer to figure out which enum value is associated with the value 3.

```py
>>> import  phonenumbers as pn

>>> n = pn.parse("+18002345678")

>>> pn.number_type(n)
3

>>> pn.PhoneNumberType.TOLL_FREE
3

>>> pn.number_type(n) == pn.PhoneNumberType.TOLL_FREE
True
```

In `digitz`, the PhoneNumber object has a `number_type` property which will return an actual enum. This is much more descriptive than a simple integer. Just like any other python enum you can check the `name` and `value` attributes for more information.

```py
>>> from digitz import PhoneNumber

>>> n = PhoneNumber.parse("+18002345678")

>>> n.number_type
<PhoneNumberType.TOLL_FREE: 3>

>>> n.number_type.name
'TOLL_FREE'

>>> n.number_type.value
3
```

But `digitz` doesn't stop there. If you want to know if a phone number is toll free, then just simply check the `is_toll_free` property. There are additional properties for all of the other phone number types.

```py
>>> n.is_toll_free
True
```
___

## Concise properties over verbose functions.

In `phonenumbers`, aside from the core properties that make up a `PhoneNumber` object, all other information regarding a phone number must be retrieved by calling the appropriate function and passing in the `PhoneNumber` object. Additionally, many of these functions are overly verbose.

```py
>>> import phonenumbers as pn

>>> n = pn.parse("+18002345678")

>>> n.region_code_for_number(n)
'US'

>>> pn.is_valid_number(n)
True

>>> pn.is_number_geographical(n)
False

>>> pn.national_significant_number(n)
'8002345678'

```

With `digitz`, the additional information can be accessed as cached properties or methods on the PhoneNumber object. Aliases are available for any properties whose name is too lengthy.

```py
>>> from digitz import PhoneNumber

>>> n = PhoneNumber.parse("+18002345678")

>>> n.region_code
'US'

>>> n.is_valid
True

>>> n.is_geographical
False

>>> n.national_significant_number
'8002345678'

>>> pn.nsn  # an alias for national_significant_number
'8002345678'
```
___


## Making things easier wherever possible.


### Retrieving the National Destination Code and Subscriber Number.
The `phonenumbers` library puts you through a lot of obstacles to retrieve the National Destination Code (NDC) (Referred to in some countries as the Area Code) as well as the Subscriber Number (the digits after the NDC).

You have to call two functions, one to get the national significant number and another to get the length of the national destination code. You then have to use string slicing to get the national destination code and subscriber number.

This is quite a hassle, especially if you are new to the library and just want to get the area code of a number.

```py
>>> import phonenumbers as pn

>>> n = pn.parse("+18002345678")

>>> nsn = pn.national_significant_number(n)
>>> nsn
'8002345678'

>>> ndc_length = pn.length_of_national_destination_code(n)
>>> ndc_length
3

>>> nsn[:ndc_length]  # ndc
'800'

>>> nsn[ndc_length:]  # subscriber number
'2345678'
```

With `digitz`, getting the NDC and Subscriber Number is a very simple task.
```py
>>> from digitz import PhoneNumber

>>> n = PhoneNumber.parse("+18002345678")

>>> n.national_destination_code
'800'

>>> n.ndc # an alis for national_destination_code
'800'

>>> n.subscriber_number
'2345678'
```
