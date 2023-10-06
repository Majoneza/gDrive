from gData import gDataclass, gList
from gDriveData import Comment


class List(gDataclass):
    kind: str
    comments: gList[Comment]
    nextPageToken: str
