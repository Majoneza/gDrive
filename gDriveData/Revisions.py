from gService import gDataclass
from gDriveData import Revision


class List(gDataclass):
    nextPageToken: str
    kind: str
    revisions: list[Revision]
