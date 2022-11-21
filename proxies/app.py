import httpx
from abc import ABC, abstractmethod
from typing import Optional, TypedDict, List


url = 'https://dog-api.kinduff.com/api/facts'


class ValidationError(Exception):
    ...

class NotFound(Exception):
    ...

class PermissionDenied(Exception):
    ...


class ResponseDogs(TypedDict):
    facts: List[str]
    success: bool


class QueryParams(TypedDict):
    number: int


class RequestHeaders(TypedDict):
    api_key: str


class ApiClient(ABC):

    @abstractmethod
    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {}
    ) -> ResponseDogs:
        raise NotImplementedError()























class ApiDogsPublic(ApiClient):

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {}
    ) -> ResponseDogs:
        response: httpx.Response = httpx.get(url, params=params, headers=headers)
        response_data: dict = response.json()
        return ResponseDogs(response_data)



class ApiDogsPaginated(ApiClient):
    
    def __init__(self, api_client: ApiDogsPublic) -> None:
        self.api_client = api_client

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {}
    ) -> ResponseDogs:
        if self._has_valid_pagination(params):
            return self.api_client.request(url, params)

    def _has_valid_pagination(self, params: Optional[QueryParams] = {}) -> bool:
        if not isinstance(params.get('number'), int) or params.get('number') not in range(1, 100):
            raise ValidationError('Wrong pagination value has been requested')
        return True


class ApiDogsRestricted(ApiClient):

    def __init__(self, api_client: ApiDogsPublic, api_key: str) -> None:
        self.api_client = api_client
        self.api_key = api_key

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {}
    ) -> ResponseDogs:
        if self._is_request_authorized(headers):
            return self.api_client.request(url, headers)
    
    def _is_request_authorized(self, headers: Optional[RequestHeaders] = {}) -> bool:
        if headers.get('api_key') != self.api_key:
            raise NotFound('Not Found')
        return True


client = ApiDogsPaginated(ApiDogsPublic())
# print(client.request(url, {'number': 'wrong_text'}))
# print(client.request(url, {'number': 101}))
# print(client.request(url, {'number': 0}))
# >> Wrong pagination value has been requested

# print(client.request(url, params=QueryParams(number=10)))


# client = ApiDogsRestricted(ApiDogsPublic(), api_key='super_secret')
# print(client.request(url, headers=RequestHeaders(api_key='super_secret')))
