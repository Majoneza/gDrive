from gService.gData import gDataclass, gList
from .base import Drive


class List(gDataclass):
    nextPageToken: str
    kind: str
    drives: gList[Drive]
