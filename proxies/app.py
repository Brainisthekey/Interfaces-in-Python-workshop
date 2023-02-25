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
    facts: Optional[List[str]]
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
        params: Optional[QueryParams] = None,
        headers: Optional[RequestHeaders] = None
    ) -> ResponseDogs:
        raise NotImplementedError()























class ApiDogsPublic(ApiClient):

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = None,
        headers: Optional[RequestHeaders] = None
    ) -> ResponseDogs:
        response: httpx.Response = httpx.get(url, params=params, headers=headers)
        response_data: dict = response.json()
        return ResponseDogs(facts=response_data['facts']['facts'], success=True)


















class ApiDogsPaginated(ApiClient):
    
    def __init__(self, api_client: ApiDogsPublic) -> None:
        self.api_client = api_client

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = None,
        headers: Optional[RequestHeaders] = None
    ) -> ResponseDogs:
        if params and self._has_valid_pagination(params):
            return self.api_client.request(url=url, params=params)
        return ResponseDogs(facts=[], success=False)

    def _has_valid_pagination(self, params: QueryParams) -> bool:
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
        params: Optional[QueryParams] = None,
        headers: Optional[RequestHeaders] = None
    ) -> ResponseDogs:
        if headers and self._is_request_authorized(headers):
            return self.api_client.request(url=url, headers=headers)
        return ResponseDogs(facts=[], success=False)

    def _is_request_authorized(self, headers: RequestHeaders) -> bool:
        if headers.get('api_key') != self.api_key:
            raise NotFound('Not Found')
        return True


client = ApiDogsPaginated(ApiDogsPublic())
# print(client.request(url, {'number': 'wrong_text'}))
# print(client.request(url, {'number': 101}))
# print(client.request(url, {'number': 0}))
# >> Wrong pagination value has been requested

print(client.request(url, params=QueryParams(number=10)))


# client = ApiDogsRestricted(ApiDogsPublic(), api_key='super_secret')
# print(client.request(url, headers=RequestHeaders(api_key='super_secret')))
