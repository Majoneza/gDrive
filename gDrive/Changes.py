from gService import gSubService
from gDriveData import Channel, Changes
from .utils import executeResourceSelf
from typing import List


class gDriveChanges(gSubService):
    def getStartPageToken(
        self, driveId: str | None = None, supportsAllDrives: bool | None = None
    ) -> Changes.GetStartPageToken:
        return executeResourceSelf(self)

    def list(
        self,
        driveId: str,
        includeCorpusRemovals: bool,
        includeItemsFromAllDrives: bool,
        includeRemoved: bool,
        pageSize: int,
        pageToken: str,
        restrictToMyDrive: bool,
        spaces: List[str],
        supportsAllDrives: bool,
        includePermissionsForView: str,
        includeLabels: List[str],
    ) -> Changes.List:
        return executeResourceSelf(self, joins=["spaces", "includeLabels"])

    def watch(
        self,
        channel: Channel,
        driveId: str,
        includeCorpusRemovals: bool,
        includeItemsFromAllDrives: bool,
        includeRemoved: bool,
        pageSize: int,
        pageToken: str,
        restrictToMyDrive: bool,
        spaces: List[str],
        supportsAllDrives: bool,
        includePermissionsForView: str,
        includeLabels: List[str],
    ) -> Channel:
        return executeResourceSelf(self, joins=["spaces", "includeLabels"], body="channel")
