from gService.gData import gDataclass, gList
from .base import Reply


class List(gDataclass):
    kind: str
    replies: gList[Reply]
    nextPageToken: str
