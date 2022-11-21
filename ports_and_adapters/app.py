from abc import ABC, abstractmethod
from typing import Optional, Any
import uuid
from enum import Enum, IntEnum
from pydantic import BaseModel, PrivateAttr


# Payload and subject used by message broker
received_subject = None
received_payload = None



# >> Step 1: Let's create a Payment model 

class PaymentsStatus(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'

class ProductID(IntEnum):
    KEYBOARD = 1
    MOUSE = 2


class Payments(BaseModel):
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)

    product_id = ProductID
    status: PaymentsStatus
    detail: Optional[str] = None




















# >> Step 2: Interfaces for the Storage and MessageBroker

class BaseStorage(ABC):

    @abstractmethod
    def add(self, model: BaseModel) -> None:
        raise NotImplementedError()

    @abstractmethod
    def remove(self, model: BaseModel) -> None:
        raise NotImplementedError()


class MessageBroker(ABC):

    @abstractmethod
    def publish(self, subject: str, payload: Any) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def subscribe(self, subject: str) -> None:
        raise NotImplementedError()

















# >> Step 3: Implementation a message interfaces

class Nats(MessageBroker):

    def publish(self, subject: str, payload: Any):
        print('Publish message with NATS')
        print('-------------------------')
        global received_subject
        global received_payload
        received_subject = subject
        received_payload = payload
    
    def subscribe(subject: str):
        ...


class ZMQ(MessageBroker):

    def publish(self, subject: str, payload: Any):
        ...
    
    def subscribe(self, subject: str):
        print('ZMQ message broker receive the message')
        print(f'Subject of the message - {received_subject}')
        print(f'Payload - {received_payload}')
        print('-------------------------')












# >> Step 4: Implementation a database interfaces

class MemoryStorage(BaseStorage):

    _memory_storage = []

    def add(self, model: BaseModel):
        self._memory_storage.append(model)
    
    def remove(self, model: BaseModel):
        ...
    
    def __str__(self) -> str:
        return str(self._memory_storage)


class DBStorage(BaseStorage):

    def __init__(self) -> None:
        """Initialize database connection"""
        ...

    def add(self, model):
        ...
    
    def remove(self, model):
        ...












# >> Step 5: Adapters/Transporters

class StorageTransporter:

    def __init__(self, storage: BaseStorage):
        print(f'Adapter/Transporter has been initialized with {type(storage)}')
        print('-------------------------')
        self.storage = storage

    def create(self, model: BaseModel) -> None:
        if isinstance(self.storage, DBStorage):
            # There we basically adapt our data
            ...
        elif isinstance(self.storage, MemoryStorage):
            # There we basically adapt our data\
            print(f'Store value {model} in {type(self.storage)}')
            print('-------------------------')
            self.storage.add(model)

    def delete(self, model: BaseModel) -> None:
        ...


class MessageTransporter:

    def __init__(self, message_broker: MessageBroker) -> None:
        self.message_broker = message_broker

    def send(self, subject, payload):
        if isinstance(self.message_broker, Nats):
            # There adapt our payload
            ...
            self.message_broker.publish(subject, payload)
        elif isinstance(self.message_broker, ZMQ):
            # There adapt our payload
            ...
    
    def listen(self, subject):
        self.message_broker.subscribe(subject)


















# >> Step 6: Check our how it works



# Create payload
payment = Payments(product_id=ProductID.KEYBOARD, status=PaymentsStatus.SUCCESS)

# Send payload using transporter
message_transporter = MessageTransporter(message_broker=Nats())
message_transporter.send('payloads', payment)

# Node which is listening for specific topic subject
message_transporter = MessageTransporter(message_broker=ZMQ())
message_transporter.listen('payloads')


# Once we get the payload we store it somewhere
storage_transporter = StorageTransporter(storage=MemoryStorage())
storage_transporter.create(received_payload)

# Check the results
print(MemoryStorage())