from gService.gData import gDataclass, gList
from .base import Comment


class List(gDataclass):
    kind: str
    comments: gList[Comment]
    nextPageToken: str
