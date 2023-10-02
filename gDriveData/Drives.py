from dataclasses import dataclass
from .base import gData
from gDriveData import Drive
from typing import List as ListType

@dataclass
class List(gData):
    nextPageToken: str
    kind: str
    drives: ListType[Drive]
