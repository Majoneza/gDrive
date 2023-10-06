import uuid
from gService import gSubService
from gDriveData import Drive, Drives
from .query import BridgeTerm
from .utils import executeResourceSelf


class gDriveDrives(gSubService):
    def create(self, drive: Drive, requestId: str = str(uuid.uuid4())) -> Drive:
        return executeResourceSelf(self, "executeOnlyOnce", body="drive")

    def delete(
        self,
        driveId: str,
        useDomainAdminAccess: bool | None = None,
        allowItemDeletion: bool | None = None,
    ) -> None:
        return executeResourceSelf(self, "checkForErrors")

    def get(self, driveId: str, useDomainAdminAccess: bool | None = None) -> Drive:
        return executeResourceSelf(self, "execute")

    def hide(self, driveId: str) -> Drive:
        return executeResourceSelf(self, "executeOnlyOnce")

    def list(
        self,
        pageSize: int | None = None,
        pageToken: str | None = None,
        q: str | BridgeTerm | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Drives.List:
        return executeResourceSelf(self, "execute")

    def unhide(self, driveId: str) -> Drive:
        return executeResourceSelf(self, "executeOnlyOnce")

    def update(
        self,
        drive: Drive,
        driveId: str,
        useDomainAdminAccess: bool | None = None,
    ) -> Drive:
        return executeResourceSelf(self, "executeOnlyOnce", body="drive")
