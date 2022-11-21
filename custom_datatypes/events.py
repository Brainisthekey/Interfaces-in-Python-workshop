import uuid
from collections import abc, defaultdict
from enum import Enum
from functools import lru_cache
from typing import DefaultDict, List, Optional
from pydantic import BaseModel, PrivateAttr


"""
    Ticket Description:

        Why ?
            We want to store "events" that comes from different resources

        What ?
            Each event should have the next criteria:
            - status
            - type
            - detail(In case of errors)
        
        ACs:
            - There should be the only source of truth
            - Stored events can't be deleted
            - Each event should have a uniq identifier
            - There should be a way to filter out events by types AND statuses

        Bonus points:
            - There should be a way to cache events!
"""





























# >> Step 1: Let's create our Event model

class EvenStatus(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    UNKNOWN = 'UNKNOWN'


class EventType(Enum):
    SCHEDULER = 'SCHEDULER'
    DATABASE = 'DATABASE'
    REACTOR = 'REACTOR'


class Event(BaseModel):
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)

    status: EvenStatus
    type: EventType
    detail: Optional[str] = None

    class Config:
        frozen = True  # Event can't be modified







































# >> Step 2: Let's create a storage for the events stored by specific type

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __new__(cls):
        cls._storage = list()









































# >> Step 3: We can add events and get the amount of events by type

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __new__(cls):
        cls._storage = list()

    def append(self, value: Event) -> None:  # <--------------------new
        self._storage.append(value)

    def count(self, value: EventType) -> int:
        return len(list(filter(lambda x: x.type == value, self._storage)))  # <--------------------new






























# >> Step 4: We should be able to filter event by type

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __new__(cls):
        cls._storage = list()

    def append(self, value: Event) -> None:
        self._storage.append(value)

    def count(self, value: EventType) -> int:
        return len(list(filter(lambda x: x.type == value, self._storage)))

    def __getitem__(self, event_type: EventType) -> List[Event]:  # <--------------------new
        if not isinstance(event_type, EventType):
            raise TypeError('The wrong type of key, it should EventType')
        return [item for item in self._storage if item.type == event_type]































# >> Step 5: Fill required magic methods to be able initialize our type

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __new__(cls):
        cls._storage = list()

    def append(self, value: Event) -> None:
        if not isinstance(value, Event):
            raise TypeError('The wrong type of event, it should Event') 
        self._storage.append(value)

    def count(self, value: EventType) -> int:
        return len(list(filter(lambda x: x.type == value, self._storage)))

    def __getitem__(self, event_type: EventType) -> List[Event]:
        if not isinstance(event_type, EventType):
            raise TypeError('The wrong type of key, it should EventType')
        return [item for item in self._storage if item.type == event_type]

    def __len__(self) -> int: # <--------------------new
        return len(self._storage)
    
    def __hash__(self) -> int: # <--------------------new
        return hash(len(self._storage))

    def __str__(self) -> str: # <--------------------new
        return str(self._storage)


storage = EventContainer()

first_event = Event(status=EvenStatus.SUCCESS, type=EventType.REACTOR)
second_event = Event(status=EvenStatus.ERROR, type=EventType.DATABASE, detail='Duplicate user ID')

storage.append(first_event)
storage.append(second_event)

# print(storage[EventType.DATABASE])
# print(storage.count(EventType.DATABASE))
# print(storage[EventType.SCHEDULER])
# print(storage.count([EventType.SCHEDULER]))



# Question: Is it possible to cache values ?
# For example if we don't have that match events






































# >> Step 7: Adding cache mechanism
# Example could be that we have multiple services that periodically asks about the events

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __init__(self):
        self._storage = list()

    def append(self, value: Event) -> None:
        if not isinstance(value, Event):
            raise TypeError('The wrong type of event, it should Event') 
        self._storage.append(value)

    @lru_cache  # <--------------------new
    def count(self, value: EventType) -> int:
        return len(list(filter(lambda x: x.type == value, self._storage)))

    @lru_cache  # <--------------------new
    def __getitem__(self, event_type: EventType) -> List[Event]:
        if not isinstance(event_type, EventType):
            raise TypeError('The wrong type of key, it should EventType')
        print('I am generating the list for you!')
        return [item for item in self._storage if item.type == event_type]

    def __len__(self) -> int:
        return len(self._storage)
    
    def __hash__(self) -> int:
        return hash(len(self._storage))

    def __str__(self) -> str:
        return str(self._storage)


storage = EventContainer()

first_event = Event(status=EvenStatus.SUCCESS, type=EventType.REACTOR)
second_event = Event(status=EvenStatus.ERROR, type=EventType.DATABASE, detail='Duplicate user ID')

storage.append(first_event)
storage.append(second_event)

# print(storage[EventType.REACTOR])
# print(storage[EventType.REACTOR])
# print(storage[EventType.REACTOR])
# print(storage[EventType.DATABASE])




































# >> Step 8: Let's create another data structure which will store events based on statuses

"""
{
    EvenStatus.SUCCESS: [Event, Event],
    EvenStatus.ERROR: [Event],
    EvenStatus.UNKNOWN: [Event, Event, Event],
}
"""

class EventStorage(abc.Mapping):

    _storage: DefaultDict[EvenStatus, EventContainer] = defaultdict(EventContainer)































# >> Step 9: Let's implement required methods

class EventStorage(abc.Mapping):

    _storage: DefaultDict[EvenStatus, EventContainer] = defaultdict(EventContainer)

    def __getitem__(self, key: EvenStatus) -> EventContainer: # <--------------------new
        if not isinstance(key, EvenStatus):
            raise TypeError('The wrong type of key, it should EventStatus')
        return self._storage.get(key, EventContainer())

    def __setitem__(self, key: EvenStatus, value: Event) -> None: # <--------------------new
        if not isinstance(key, EvenStatus) or not isinstance(value, Event):
            raise TypeError('The wrong type key or value, it should be EventStatus and Event respectively')
        self._storage[key].append(value)

    def __iter__(self) -> abc.Iterator: # <--------------------new
        return iter(self._storage)

    def __len__(self) -> int: # <--------------------new
        return len(self._storage)

    def __contains__(self, key) -> bool: # <--------------------new
        return key in self._storage

































# >> Step 10: Let's put things together and see how it works

class EventContainer(abc.Sequence):

    _storage: List[Event] = []

    def __init__(self):
        self._storage = list()

    def append(self, value: Event) -> None:
        if not isinstance(value, Event):
            raise TypeError('The wrong type of event, it should Event') 
        self._storage.append(value)

    @lru_cache
    def count(self, value: EventType) -> int:
        return len(list(filter(lambda x: x.type == value, self._storage)))

    @lru_cache
    def __getitem__(self, event_type: EventType) -> List[Event]:
        if not isinstance(event_type, EventType):
            raise TypeError('The wrong type of key, it should EventType')
        return [item for item in self._storage if item.type == event_type]

    def __len__(self) -> int:
        return len(self._storage)
    
    def __hash__(self) -> int:
        return hash(len(self._storage))

    def __str__(self) -> str:
        return str(self._storage)


class EventStorage(abc.Mapping):

    _storage: DefaultDict[EvenStatus, EventContainer] = defaultdict(EventContainer)

    def __getitem__(self, key: EvenStatus) -> EventContainer:
        if not isinstance(key, EvenStatus):
            raise TypeError('The wrong type of key, it should EventStatus')
        return self._storage.get(key, EventContainer())

    def __setitem__(self, key: EvenStatus, value: Event) -> None:
        if not isinstance(key, EvenStatus) or not isinstance(value, Event):
            raise TypeError('The wrong type key or value, it should be EventStatus and Event respectively')
        self._storage[key].append(value)

    def __iter__(self) -> abc.Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def __contains__(self, key) -> bool:
        return key in self._storage
    
    def __str__(self) -> str:
        return str(self._storage)



storage = EventStorage()

first_event = Event(status=EvenStatus.SUCCESS, type=EventType.REACTOR)
second_event = Event(status=EvenStatus.ERROR, type=EventType.DATABASE, detail='Duplicate user ID')
third_event = Event(status=EvenStatus.UNKNOWN, type=EventType.SCHEDULER, detail='Exception during handling error')

storage[first_event.status] = first_event
storage[second_event.status] = second_event
storage[third_event.status] = third_event

# print(storage[EvenStatus.ERROR])
# print(storage[EvenStatus.SUCCESS][EventType.REACTOR])
# print(storage[EvenStatus.UNKNOWN][EventType.SCHEDULER])


# second_storage = EventStorage()
# print(second_storage[EvenStatus.ERROR][EventType.DATABASE])

