from gService import gSubService
from gDriveData import About
from .utils import executeResourceSelf


class gDriveAbout(gSubService):
    def get(self) -> About:
        return executeResourceSelf(self)
