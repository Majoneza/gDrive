from gService import gDataclass
from gDriveData import Permission


class List(gDataclass):
    nextPageToken: str
    kind: str
    permissions: list[Permission]
