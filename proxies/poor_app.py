import httpx
from typing import Optional, TypedDict, List


url = 'https://dog-api.kinduff.com/api/facts'


class ResponseDogs(TypedDict):
    facts: List[str]
    success: bool


class QueryParams(TypedDict):
    number: int


class RequestHeaders(TypedDict):
    api_key: str


class DogsApiClient:

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {}
    ) -> ResponseDogs:
        response: httpx.Response = httpx.get(url, params=params, headers=headers)
        response_data: dict = response.json()
        return ResponseDogs(response_data)


client = DogsApiClient()

# >> 1: I want to get paginated response
result = client.request(url=url, params=QueryParams(number=10))
# print(result)

# >> 2: I want request check user permissions
result = client.request(url=url, headers=RequestHeaders(api_key='some_key'))
# print(result)



















# What if I want to have control of the params and headers


class ValidationError(Exception):
    ...

class NotFound(Exception):
    ...

class PermissionDenied(Exception):
    ...


class DogsApiClient:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(
        self,
        url: str,
        params: Optional[QueryParams] = {},
        headers: Optional[RequestHeaders] = {},
        pagination: bool = False,
        authentication: bool = False
    ) -> ResponseDogs:

        if pagination:
            if not isinstance(params.get('number'), int) or params.get('number') not in range(1, 100):
                raise ValidationError('Wrong pagination value has been requested')
        if authentication:
            if headers.get('api_key') != self.api_key:
                raise PermissionDenied(403, 'Permission Denied')
                # Q: Is that Exception correct ?

        response: httpx.Response = httpx.get(url, params=params)
        response_data: dict = response.json()
        return ResponseDogs(response_data)


client = DogsApiClient(api_key='super_secret')

# >> 1: I want request response with pagination
# result = client.request(url=url, params=QueryParams(number=10))
# print(result)

# >> 2: I want request check user permissions
# result = client.request(url=url, headers=RequestHeaders(api_key='super_secret'))
# print(result)

