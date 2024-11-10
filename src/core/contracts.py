# Native Libraries
from dataclasses import dataclass
from typing import Iterable


class BaseClass:
    def to_dict(self):
        return self.__dict__

@dataclass(frozen=True)
class RequestContext(BaseClass):
    base_url: str
    paths: Iterable[str]
