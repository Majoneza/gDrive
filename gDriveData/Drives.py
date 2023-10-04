from gService import gDataclass
from gDriveData import Drive


class List(gDataclass):
    nextPageToken: str
    kind: str
    drives: list[Drive]
