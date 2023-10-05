from gService import gDataclass, gList
from gDriveData import Revision


class List(gDataclass):
    nextPageToken: str
    kind: str
    revisions: gList[Revision]
