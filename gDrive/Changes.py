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
        driveId: str | None = None,
        includeCorpusRemovals: bool | None = None,
        includeItemsFromAllDrives: bool | None = None,
        includeRemoved: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        restrictToMyDrive: bool | None = None,
        spaces: List[Space] | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> Changes.List:
        return self._getResource("execute")

    def watch(
        self,
        channel: Channel,
        driveId: str | None = None,
        includeCorpusRemovals: bool | None = None,
        includeItemsFromAllDrives: bool | None = None,
        includeRemoved: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        restrictToMyDrive: bool | None = None,
        spaces: List[Space] | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> Channel:
        return self._getResource(
            "executeOnlyOnce",
            body="channel",
        )
