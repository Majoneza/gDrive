from gService.gResourceManager import gResourceManager
from .data import Channel, Changes
from .data.helpers import IncludePermissionsForView, Space
from typing import List


class gDriveChanges(gResourceManager):
    def getStartPageToken(
        self, driveId: str | None = None, supportsAllDrives: bool | None = None
    ) -> Changes.GetStartPageToken:
        return self._getResource("executeOnlyOnce")

    def list(
        self,
        driveId: str,
        includeCorpusRemovals: bool,
        includeItemsFromAllDrives: bool,
        includeRemoved: bool,
        pageSize: int,
        pageToken: str,
        restrictToMyDrive: bool,
        spaces: List[Space],
        supportsAllDrives: bool,
        includePermissionsForView: IncludePermissionsForView,
        includeLabels: List[str],
    ) -> Changes.List:
        return self._getResource("execute")

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
        spaces: List[Space],
        supportsAllDrives: bool,
        includePermissionsForView: IncludePermissionsForView,
        includeLabels: List[str],
    ) -> Channel:
        return self._getResource(
            "executeOnlyOnce",
            body="channel",
        )
