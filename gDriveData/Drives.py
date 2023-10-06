from gData import gDataclass, gList
from gDriveData import Drive


class List(gDataclass):
    nextPageToken: str
    kind: str
    drives: gList[Drive]
