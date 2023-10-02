from dataclasses import dataclass
from .base import Change, gData
from typing import List as ListType


@dataclass
class GetStartPageToken(gData):
    startPageToken: str
    kind: str


@dataclass
class List(gData):
    kind: str
    nextPageToken: str
    newStartPageToken: str
    changes: ListType[Change]
