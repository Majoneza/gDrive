from gService.gData import gDataclass, gList
from .base import Revision


class List(gDataclass):
    nextPageToken: str
    kind: str
    revisions: gList[Revision]
