from gService.gData import gDataclass, gList
from .base import Change


class GetStartPageToken(gDataclass):
    startPageToken: str
    kind: str


class List(gDataclass):
    kind: str
    nextPageToken: str
    newStartPageToken: str
    changes: gList[Change]
