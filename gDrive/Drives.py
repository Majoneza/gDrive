import uuid
from gService import gSubService
from gDriveData import Drive, Drives
from .query import BridgeTerm
from .utils import executeResourceSelf
from typing import Any, Dict


class gDriveDrives(gSubService):
    def create(
        self, drive: Drive | Dict[str, Any], requestId: str = str(uuid.uuid4())
    ) -> Drive:
        return executeResourceSelf(body="drive")

    def delete(
        self,
        driveId: str,
        useDomainAdminAccess: bool | None = None,
        allowItemDeletion: bool | None = None,
    ) -> None:
        return executeResourceSelf(checkError=True)

    def get(self, driveId: str, useDomainAdminAccess: bool | None = None) -> Drive:
        return executeResourceSelf()

    def hide(self, driveId: str) -> Drive:
        return executeResourceSelf()

    def list(
        self,
        pageSize: int | None = None,
        pageToken: str | None = None,
        q: str | BridgeTerm | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Drives.List:
        return executeResourceSelf()

    def unhide(self, driveId: str) -> Drive:
        return executeResourceSelf()

    def update(
        self,
        drive: Drive | Dict[str, Any],
        driveId: str,
        useDomainAdminAccess: bool | None = None,
    ) -> Drive:
        return executeResourceSelf(body="drive")
