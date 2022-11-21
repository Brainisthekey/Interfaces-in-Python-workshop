from typing import (
    Optional,
    Tuple,
    ClassVar,
    Literal,
    Iterator,
    Any,
    OrderedDict as TypedOrderedDict,
)
from types import MappingProxyType
from collections import OrderedDict
from collections import abc



"""
    Ticket Description:

        Why ?
            I want structure(Mapping) where I will be able to store some data

        What ?
            A uniq data structure which will follow two simple rules

        ACs:
            - The data stricture is partially "frozen" - keys/values are not removable
            - Data stricture is restricted to store some specific keys
            - Data should be ordered!
"""


# A Q: bit off topic, but do you know a stricture(mapping) that can't be modified ?

# {'key': 'value'}



















# >> How to create very similar structure to the dict, but not modified

frozendict = MappingProxyType({'key': 'value'})

# frozendict['key'] = 'another_value'
# >>> TypeError: 'mappingproxy' object does not support item assignment

print(frozendict)
print(frozendict['key'])
print(type(frozendict))














# Step 1 >> Let's make the blueprint of our data structure

class FrozenDict(abc.MutableMapping):

    __storage__: TypedOrderedDict = OrderedDict()

    def __init__(self, items: Optional[dict] = None) -> None:
        self.__storage__ = OrderedDict(**items) if items else OrderedDict()

    def __setitem__(self, key: Any, value: Any) -> None:
        ...

    def __getitem__(self, key: Any) -> Any:
        ...

    def __delitem__(self, key: Any) -> None:
        ...

    def __iter__(self) -> Iterator[TypedOrderedDict]:
        ...

    def __len__(self) -> int:
        ...

    def __str__(self) -> str:
        ...





















# Step 2 >> We should restrict our data structure from removing items

class ExceptionDelete(Exception):  # <--------------------new
    """It's frozen a frozen dict, you can't remove keys"""
    ...

class FrozenDict(abc.MutableMapping):

    __storage__: TypedOrderedDict = OrderedDict()

    def __init__(self, items: Optional[dict] = None) -> None:
        self.__storage__ = OrderedDict(**items) if items else OrderedDict()

    def __setitem__(self, key: Any, value: Any) -> None:
        ...

    def __getitem__(self, key: Any) -> Any:
        ...

    def __delitem__(self, key: Any) -> None:
        raise ExceptionDelete("It's a frozen dict, you can't remove keys")  # <--------------------new

    def __iter__(self) -> Iterator[TypedOrderedDict]:
        ...

    def __len__(self) -> int:
        ...

    def __str__(self) -> str:
        ...
























# Step 3 >> And now we should check the key before we actually add it


class ExceptionDelete(Exception):
    """It's frozen a frozen dict, you can't remove keys"""
    ...


class FrozenDict(abc.MutableMapping):


    __keys__ = ('first', 'second') # <--------------------new
    __storage__: TypedOrderedDict = OrderedDict()

    def __init__(self, items: Optional[dict] = None) -> None:
        self.__storage__ = OrderedDict(**items) if items else OrderedDict()

    def __setitem__(self, key, value: Any) -> None: # <--------------------new
        if key not in self.__keys__:
            raise KeyError('The key is not accepted')
        self.__storage__[key] = value

    def __getitem__(self, key) -> Any:
        ...

    def __delitem__(self, key) -> None:
        raise ExceptionDelete("It's a frozen dict, you can't remove keys")

    def __iter__(self) -> Iterator[TypedOrderedDict]:
        ...

    def __len__(self) -> int:
        ...

    def __str__(self) -> str:
        ...
















# Step 4 >> And of course the most painfully part - type annotation ;)

AcceptedKeys = Literal['first', 'second']

class ExceptionDelete(Exception):
    """It's frozen a frozen dict, you can't remove keys"""
    ...


class FrozenDict(abc.MutableMapping):

    __keys__: ClassVar[Tuple[AcceptedKeys, ...]] = ('first', 'second')
    __storage__: TypedOrderedDict = OrderedDict()

    def __init__(self, items: Optional[dict] = None) -> None:
        self.__storage__ = OrderedDict(**items) if items else OrderedDict()

    def __setitem__(self, key: AcceptedKeys, value: Any) -> None:
        if key not in self.__keys__:
            raise KeyError('The key is not accepted')
        self.__storage__[key] = value

    def __getitem__(self, key: AcceptedKeys) -> Any:
        return self.__storage__[key]

    def __delitem__(self, key: AcceptedKeys) -> None:
        raise ExceptionDelete("It's a frozen dict, you can't remove keys")

    def __iter__(self) -> Iterator[TypedOrderedDict]:
        return iter(self.__storage__)

    def __len__(self) -> int:
        return len(self.__storage__)

    def __str__(self) -> str:
        return str(self.__storage__)


frozendict = FrozenDict()
frozendict['first'] = 'first_value'
frozendict['second'] = 'second_value'

# Let's try to delete some key

# del frozendict['first']
# >>> ExceptionDelete("It's a frozen dict, you can't remove keys")

# Let's try to create not allowed key

# frozendict['not_specified'] = 'I really want to create another key :('
# >>> KeyError('The key is not accepted')

# print(frozendict)
