from gService.gResourceManager import gResourceManager
from .data import Channel


class gDriveChannels(gResourceManager):
    def stop(self, channel: Channel) -> None:
        return self._getResource("checkForErrors", body="channel")
