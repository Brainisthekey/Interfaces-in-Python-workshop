"""Class that can't be subclassed"""


class BlockSubclassing(type):

    def __new__(metacls, cls, bases, classdict):
        if metacls in map(type, bases):
                raise RuntimeError(
                    f"Subclassing a class that has "
                    + f"{metacls.__name__} metaclass is prohibited"
                )
        return super().__new__(metacls, cls, bases, classdict)


class UniqClass(metaclass=BlockSubclassing):
    ...

class Example(UniqClass):
    pass

# >> RuntimeError: Subclassing a class that has BlockSubclassing metaclass is prohibited










# >> Question: What value stored in the magic variable __bases__

class ExampleClass:
    ...

print(ExampleClass.__base__)
print(ExampleClass.__bases__)
















"""Multiple inheritance is blocked"""

class BlockMultipleInheritance(type):

    def __new__(metacls, cls, bases, classdict):
        if len(bases) > 1:
            raise RuntimeError("Inherited multiple base classes!")
        return super().__new__(metacls, cls, bases, classdict)


class Base(metaclass=BlockMultipleInheritance):
    pass


# no error is raised
class A(Base):
    pass


# no error is raised
class B(Base):
    pass


# This will raise an error!
class C(A, B):
    pass


# >> RuntimeError: Inherited multiple base classes!