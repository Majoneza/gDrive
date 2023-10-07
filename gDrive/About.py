from gService.gResourceManager import gResourceManager
from .data import About


class gDriveAbout(gResourceManager):
    def get(self) -> About:
        return self._getResource("execute")
