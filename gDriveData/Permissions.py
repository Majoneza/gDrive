from dataclasses import dataclass
from .base import gData
from gDriveData import Permission
from typing import List as ListType

@dataclass
class List(gData):
    nextPageToken: str
    kind: str
    permissions: ListType[Permission]
