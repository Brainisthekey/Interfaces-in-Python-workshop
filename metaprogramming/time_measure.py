import time
from functools import wraps
from types import FunctionType, MethodType
from timeit import default_timer as timer


# Decorator measuring execution time

def time_measure(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = timer()
        execution_result = func(*args, **kwargs)
        end_time = timer()
        run_time = end_time - start_time
        print(f"Executing {func.__qualname__} took {run_time} seconds.")
        return execution_result

    return wrapper


@time_measure
def simple_function():
    time.sleep(1)


# simple_function()



















# What if we want to measure execution time class methods

class CollectAnalytics:

    @time_measure
    def first_function(self):
        time.sleep(1)

    @time_measure
    def hundredth_function(self):
        time.sleep(1)


# instance = CollectAnalytics()
# instance.first_function()
# instance.hundredth_function()


# >> Question: But what if the we want to decorate all the methods without explicitly using the decorator ?

























# 1. The first one is simply use a decorator factory

import inspect

def class_decorator_time():
    def decorate(cls):
        for name, fn in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, time_measure(fn))
        return cls
    return decorate


@class_decorator_time()
class CollectAnalytics:

    def first_function(self):
        time.sleep(1)

    def hundredth_function(self):
        time.sleep(1)


# instance = CollectAnalytics()
# instance.first_function()
# instance.hundredth_function()



















# 2. Time measuring using metaclasses

class TimeitMeta(type):

    def __new__(metacls, cls, bases, classdict):
        new_cls = super().__new__(metacls, cls, bases, classdict)
        for attribute_name, attribute_functionality in classdict.items():
            # attribute_name: str --> Attribute name
            # attribute_functionality: Any ---> Attribute functionality
            if isinstance(attribute_functionality, (FunctionType, MethodType)):
                setattr(new_cls, attribute_name, time_measure(attribute_functionality))
        return new_cls


class CollectAnalytics(metaclass=TimeitMeta):

    def first_function(self):
        time.sleep(1)

    def hundredth_function(self):
        time.sleep(1)


# inst = CollectAnalytics()
# inst.first_function()
# inst.hundredth_function()