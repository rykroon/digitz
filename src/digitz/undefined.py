from functools import cache
from typing import Final


class UndefinedType:

    __slots__ = ()

    @cache
    def __new__(cls):
        return super().__new__(cls)

    def __bool__(self) -> bool:
        return False
    
    def __repr__(self) -> str:
        return "Undefined"


Undefined: Final[UndefinedType] = UndefinedType()
