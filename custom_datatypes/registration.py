"""
The implementation of custom or abstract data types
Documentation link:
    https://docs.python.org/3.10/library/collections.abc.html?highlight=collections%20abc#collections-abstract-base-classes
    from _collections_abc import ...  <=== NOT FOR DEVELOPER USAGE
"""
from collections import abc
from datetime import datetime
from pydantic import BaseModel, EmailStr, PrivateAttr
from typing import Any, List, ClassVar, Iterator, Protocol, TypeVar, Type
from itertools import groupby


"""
    Ticket Description:

        Why ?
            We want to prepare data about newly registered users for further dispatch

        What ?
            Separate service which is responsible for validation/store info about Users
        
        ACs:
            - There should be an option to add/remove user from the list
            - We are able to check if User present on the list
            - We can check how many potential emails would be send
            - Duplicates should be excluded from the list
        
        Bonus points:
            - What in case if there is a different name of the User, but the same email ?
                Would we send 2 emails for each name respectively?
            - Generic solution/data structure that can be reused in the future
"""









# Step 1: Create model


class RegistrationUserForm(BaseModel):

    username: str
    email: EmailStr # https://github.com/JoshData/python-email-validator

















# Step 2: Example of input data


first_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
second_user = RegistrationUserForm(username='Mateusz', email='another@gmail.com')



















# Step 3: Where to store ?

# example_set: set[RegistrationUserForm] = {first_user, second_user}
# >> TypeError: unhashable type: 'RegistrationUserForm'

example_list: list[RegistrationUserForm] = [first_user, second_user]
















# >> Step 4, Custom Data Type ?

class UniqList(abc.MutableSet):

    _storage: list = []



















# >> Step 5, There should be an option to add/remove user from the list ?

class UniqList(abc.MutableSet):

    _storage: list = []

    def add(self, item: Any) -> None:  # <-------------new
        self._storage.append(item)

    def discard(self, item: Any) -> None:  # <-------------new
        try:
            self._storage.remove(item)
        except ValueError:
            pass





















# >> Step 6, We should be able to check if User present in the list

class UniqList(abc.MutableSet):

    _storage: list = []

    def add(self, item: Any) -> None:
        self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __contains__(self, item: Any) -> bool:  # <-------------new
        return item in self._storage






















# >> Step 7, We can check how many potential emails would be send ?

class UniqList(abc.MutableSet):

    _storage: list = []

    def add(self, item: Any) -> None:
        self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __len__(self) -> int:  # <-------------new
        return len(self._storage)

















# >> Step 8, Duplicates should be excluded from the list

class UniqList(abc.MutableSet):

    _storage: List[Any] = []

    def add(self, item: Any) -> None:
        if item not in self._storage:  # <-------------new
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __len__(self) -> int:
        return len(self._storage)










# >> Step 9, Let's make the result human-readable and make object iterable

class UniqList(abc.MutableSet):

    _storage: List[Any] = []

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator: # <-------------new
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: Any) -> None:
        if item not in self._storage:
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __str__(self) -> str: # <-------------new
        return str(self._storage)



first_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
second_user = RegistrationUserForm(username='Mateusz', email='another@gmail.com')

duplicate_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')


uniq_users = UniqList()
uniq_users.add(first_user)
uniq_users.add(second_user)
uniq_users.add(duplicate_user)

# print(uniq_users)

second_data_type = UniqList()
# print(second_data_type)

# We have one critical issue with that code :(






















# >> Step 9, Possible fix

class UniqList(abc.MutableSet):

    _storage: list = None

    def __init__(self) -> None: # <-------------new
        self._storage = list()

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: Any) -> None:
        if item not in self._storage:
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __str__(self) -> str:
        return str(self._storage)



















# >> Step 10, What else ? Bonus points
# Bonus points:
#   - What in case if there are different names of the User, but the same emails ?
#       Would we send 2 emails for each name respectively?
#   - Generic solution/data structure that can be reused in the future


class UniqList(abc.MutableSet):

    _storage: list = None

    def __init__(self) -> None:
        self._storage = list()

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: Any) -> None:
        if item not in self._storage:
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __str__(self) -> str:
        return str(self._storage)


first_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
second_user = RegistrationUserForm(username='Mateusz', email='another@gmail.com')

duplicate_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
same_email_user = RegistrationUserForm(username='Oh sorry I made a mistake in my name first time', email='some@gmail.com')


uniq_users = UniqList()
uniq_users.add(first_user)
uniq_users.add(second_user)
uniq_users.add(duplicate_user)
uniq_users.add(same_email_user)

# print(uniq_users)


# Any ideas how to resolve to save a bit of resources and don't send email second time ?




























# >> Step 11, Solve problem with same email address, but another name

class RegistrationUserForm(BaseModel):

    username: str
    email: EmailStr

    _created_at: datetime = PrivateAttr(default_factory=datetime.now)  # <-------------new


test_user = RegistrationUserForm(username='Andrii', email='test@gmail.com')
# >>> username='Andrii' email='test@gmail.com'

test_user._created_at
# >>> 2022-11-09 21:01:27.994017


class UniqList(abc.MutableSet):

    _storage: list = None

    def __init__(self) -> None:
        self._storage = list()

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: Any) -> None:
        if item not in self._storage:
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass
    
    def get_uniq_registrations(self) -> list:  # <-------------new
        sorted_storage = sorted(self._storage, key=lambda x: (x.email, x._created_at))
        result = [list(g)[-1] for _, g in groupby(sorted_storage, key=lambda x: x.email)]
        return result

    def __str__(self) -> str:
        return str(self._storage)


first_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
second_user = RegistrationUserForm(username='Mateusz', email='another@gmail.com')

duplicate_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
same_email_user = RegistrationUserForm(username='Oh sorry I made a mistake in my name first time', email='some@gmail.com')


uniq_users = UniqList()
uniq_users.add(first_user)
uniq_users.add(second_user)
uniq_users.add(duplicate_user)
uniq_users.add(same_email_user)

print(uniq_users.get_uniq_registrations())





















# >> Step 12, What about the second point, generic solution ?

class ModelException(Exception):  # <-------------new
    """The wrong type exception"""
    ...


class UniqList(abc.MutableSet):

    _storage: list = None
    _model: ClassVar[Type[BaseModel]] = BaseModel  # <-------------new
    # https://docs.python.org/3/library/typing.html#typing.Type

    def __init__(self) -> None:
        self._storage = list()

    def __contains__(self, item: Any) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: Any) -> None:
        if isinstance(item, self._model):  # <-------------new
            raise ModelException('The wrong Pydantic model exception') 
        if item not in self._storage:
            self._storage.append(item)

    def discard(self, item: Any) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __str__(self) -> str:
        return str(self._storage)



class UserRegistration(UniqList):  # <-------------new

    _storage: ClassVar[List[RegistrationUserForm]] = []
    _model: ClassVar[Type[RegistrationUserForm]] = RegistrationUserForm

    def get_uniq_registrations(self) -> List[RegistrationUserForm]:
        sorted_storage: List[RegistrationUserForm] = sorted(self._storage, key=lambda x: (x.email, x._created_at))
        result: List[RegistrationUserForm] = [list(g)[-1] for _, g in groupby(sorted_storage, key=lambda x: x.email)]
        return result


# Any other model
class EventModel(BaseModel): ...


# Custom register for that events
class EventsRegistration(UniqList):

    _storage: ClassVar[List[EventModel]] = []
    _model: ClassVar[Type[EventModel]] = EventModel

    def custom_logic_with_storage_goes_there(self):
        ...


























# >> Step 12, Improvements! ?

PydanticModelClass = TypeVar('PydanticModelClass', bound=BaseModel, covariant=True)
PydanticModelType = TypeVar('PydanticModelType', bound=BaseModel)
class PydanticModel(Protocol[PydanticModelClass]): ...


class ModelException(Exception):
    """The wrong type exception"""
    ...


class RegistrationUserForm(BaseModel):

    username: str
    email: EmailStr

    _created_at: datetime = PrivateAttr(default_factory=datetime.now)


class UniqList(abc.MutableSet):

    _storage: ClassVar[List[PydanticModel]] = []
    _model: ClassVar[Type[BaseModel]] = BaseModel

    def __init__(self) -> None:
        self._storage = list()

    def __contains__(self, item: PydanticModelType) -> bool:
        return item in self._storage

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def add(self, item: PydanticModelType) -> None:
        if not isinstance(item, self._model):
            raise ModelException('The wrong Pydantic model exception')
        if item not in self._storage and isinstance(item, self._model):
            self._storage.append(item)

    def discard(self, item: PydanticModelType) -> None:
        try:
            self._storage.remove(item)
        except ValueError:
            pass

    def __str__(self) -> str:
        return str(self._storage)


class UserRegistration(UniqList):

    _storage: ClassVar[List[RegistrationUserForm]] = []
    _model: ClassVar[Type[RegistrationUserForm]] = RegistrationUserForm

    def get_uniq_registrations(self) -> List[RegistrationUserForm]:
        sorted_storage: List[RegistrationUserForm] = sorted(self._storage, key=lambda x: (x.email, x._created_at))
        result: List[RegistrationUserForm] = [list(g)[-1] for _, g in groupby(sorted_storage, key=lambda x: x.email)]
        return result


# Register users
first_user = RegistrationUserForm(username='Andrii', email='some@gmail.com')
second_user = RegistrationUserForm(username='Mateusz', email='another@gmail.com')
duplicated_user = RegistrationUserForm(username='Andrii', email='some@gmail.com') 
same_email_user = RegistrationUserForm(username='Oh sorry I made a mistake in my name first time', email='some@gmail.com')


# Create container
Container = UserRegistration()
Container.add(first_user)
Container.add(second_user)
Container.add(duplicated_user)
Container.add(same_email_user)

result = Container.get_uniq_registrations()
# print(result)