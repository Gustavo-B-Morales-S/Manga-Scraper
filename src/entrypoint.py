# Native Libraries
from typing import Iterable, List, Literal

# Third-Party Libraries
from trio import run

# Local Modules
from src.core.requester import (
    RequestContext,
    RequestStrategy,
    SimpleRequestStrategy,
)


def fetch(
    base_url: str = '',
    paths: Iterable[str] | List[Literal['/']] = ['/'],
    request_strategy: RequestStrategy = SimpleRequestStrategy(),
) -> None:
    """
    This function performs asynchronous HTTP requests to multiple paths
    under the given `base_url` and stores the responses in a local directory.
    It uses the provided request strategy to determine who requests are handled.

    Args:
        base_url (str): The base URL for all HTTP requests.
        paths (Iterable[str] | List[Literal['/']], optional): The endpoint paths
                                                              for requests. Defaults to ['/'] if not specified.
        request_strategy (RequestStrategy, optional): The strategy used for managing HTTP requests,
                                                       e.g., `SimpleRequestStrategy`
                                                       or    `PaginatedRequestStrategy`.
                                                       Defaults to `SimpleRequestStrategy`.
    """
    return run(
        request_strategy.fetch, RequestContext(base_url=base_url, paths=paths)
    )
