from gService.gResourceManager import gResourceManager
import uuid
from .data import Drive, Drives
from .query import BridgeTerm


class gDriveDrives(gResourceManager):
    def create(self, drive: Drive, requestId: str = str(uuid.uuid4())) -> Drive:
        return self._getResource("executeOnlyOnce", body="drive")

    def delete(
        self,
        driveId: str,
        useDomainAdminAccess: bool | None = None,
        allowItemDeletion: bool | None = None,
    ) -> None:
        return self._getResource("checkForErrors")

    def get(self, driveId: str, useDomainAdminAccess: bool | None = None) -> Drive:
        return self._getResource("execute")

    def hide(self, driveId: str) -> Drive:
        return self._getResource("executeOnlyOnce")

    def list(
        self,
        pageSize: int | None = None,
        pageToken: str | None = None,
        q: str | BridgeTerm | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Drives.List:
        return self._getResource("execute")

    def unhide(self, driveId: str) -> Drive:
        return self._getResource("executeOnlyOnce")

    def update(
        self,
        drive: Drive,
        driveId: str,
        useDomainAdminAccess: bool | None = None,
    ) -> Drive:
        return self._getResource("executeOnlyOnce", body="drive")
