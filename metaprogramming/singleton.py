"""Singleton using metaclasses"""
from typing import Dict, Type
import functools


# >> Without metaclasses

def singleton(_class: Type[object]) -> object:

    _instances: Dict[type, object] = {}

    @functools.wraps(_class)
    def get_instance(*args, **kwargs) -> object:
        if _class not in _instances:
            _instances[_class] = _class(*args, **kwargs)
        return _instances[_class]

    return get_instance


@singleton
class SingleInstanceClass:
    pass


first_instance = SingleInstanceClass()
second_instance = SingleInstanceClass()
print(first_instance is second_instance)
# >> True


















# Using magic method __new__
class Singleton:
    _instances: Dict[type, 'Singleton'] = {}

    def __new__(cls) -> 'Singleton':
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class SingleInstanceMeta(Singleton):
    ...


first_instance = SingleInstanceMeta()
second_instance = SingleInstanceMeta()
print(first_instance is second_instance)
# >> True




















# Using metaclasses
class Singleton(type):
    _instance: Dict[type, 'Singleton'] = {}

    def __call__(cls, *args, **kwargs) -> 'Singleton':
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]



class SingleInstanceClass(metaclass=Singleton):
    pass


first_instance = SingleInstanceClass()
second_instance = SingleInstanceClass()

print(first_instance is second_instance)
# >> True















# Quiz: What is the sequence of calls there ?

class Metaclass(type):

    def __new__(metacls, cls, bases, classdict):
        print("Meta: __new__")
        return super().__new__(metacls, cls, bases, classdict)

    def __call__(self, *args, **kwargs):
        print('Meta: __call__')
        return super().__call__(*args, **kwargs)


class OriginalClass(metaclass=Metaclass):

    def __new__(cls):
        print('Original: __new__')
        return super().__new__(cls)
    
    def __init__(self) -> None:
        print('Original: __init__')
        pass




# instance = OriginalClass()
# second_instance = OriginalClass()