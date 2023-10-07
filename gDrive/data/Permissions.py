from gService.gData import gDataclass, gList
from .base import Permission


class List(gDataclass):
    nextPageToken: str
    kind: str
    permissions: gList[Permission]
