"""Singleton using metaclasses"""




# >> Without metaclasses

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class SingleInstanceClass:
    pass


first_instance = SingleInstanceClass()
second_instance = SingleInstanceClass()
print(first_instance is second_instance)
# >> True


















# Using magic method __new__
class Singleton:
    _instances = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class SingleInstanceClass(Singleton):
    ...


first_instance = SingleInstanceClass()
second_instance = SingleInstanceClass()
print(first_instance is second_instance)
# >> True




















# Using metaclasses
class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
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