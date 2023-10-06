from gData import gDataclass, gList
from gDriveData import Reply


class List(gDataclass):
    kind: str
    replies: gList[Reply]
    nextPageToken: str
