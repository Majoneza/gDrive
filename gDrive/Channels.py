from gService import gSubService
from gDriveData import Channel
from .utils import executeResourceSelf


class gDriveChannels(gSubService):
    def stop(self, channel: Channel) -> None:
        return executeResourceSelf(checkError=True)
