from gData import gDataclass, gList
from gDriveData import Permission


class List(gDataclass):
    nextPageToken: str
    kind: str
    permissions: gList[Permission]
