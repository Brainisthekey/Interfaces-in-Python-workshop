import os


class ApiClient:

    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")  # <-- dependency
        self.timeout = int(os.getenv("TIMEOUT", 5))  # <-- dependency


class Service:

    def __init__(self) -> None:
        self.api_client = ApiClient()  # <-- dependency


def main() -> None:
    service = Service()  # <-- dependency
    ...


if __name__ == "__main__":
    main()






















# After

import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key  # <-- dependency is injected
        self.timeout = timeout  # <-- dependency is injected


class Service:

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client  # <-- dependency is injected


def main(service: Service) -> None:  # <-- dependency is injected
    ...


if __name__ == "__main__":
    main(
        service=Service(
            api_client=ApiClient(
                api_key=os.getenv("API_KEY"),
                timeout=int(os.getenv("TIMEOUT", 5)),
            ),
        ),
    )




















# Let's use the tool

from dataclasses import dataclass

@dataclass
class User: # <----------------------- new
    id: int
    name: str


class ApiClient:

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key
        self.timeout = timeout
    
    def create_user(self) -> User:  # <----------------------- new
        # Let's assume that we doing something there
        return User(id=1, name='Andrii')


class Service:

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client


def main(service: Service) -> None:
    ...


from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=['config.ini'])

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api.api_key,
        timeout=config.api.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )

@inject
def main(service: Service = Provide[Container.service]) -> None:
    return service.api_client.create_user()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    print(main())  # <-- dependency is injected automatically














    # The best part -> Testing

    class TestApiClient:

        def create_user(self):
            return 'I just override the function!'

    with container.api_client.override(TestApiClient()):
        print(main())  # <-- overridden dependency is injected automatically













# What we are gaining with dependency injection pattern

"""
    1. Flexibility
    2. Testability
    3. Maintainability
"""
