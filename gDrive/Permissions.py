from gService import gSubService
from gDriveData import Permission, Permissions
from .utils import executeResourceSelf
from typing import Any, Dict


class gDrivePermissions(gSubService):
    def create(
        self,
        permission: Permission | Dict[str, Any],
        fileId: str,
        emailMessage: str | None = None,
        moveToNewOwnersRoot: bool | None = None,
        sendNotificationEmail: bool | None = None,
        supportsAllDrives: bool | None = None,
        transferOwnership: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return executeResourceSelf(body="permission")

    def delete(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> None:
        return executeResourceSelf(checkError=True)

    def get(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return executeResourceSelf()

    def list(
        self,
        fileId: str,
        pageSize: int | None = None,
        pageToken: str | None = None,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
        includePermissionsForView: str | None = None,
    ) -> Permissions.List:
        return executeResourceSelf()

    def update(
        self,
        permission: Permission | Dict[str, Any],
        fileId: str,
        permissionId: str,
        removeExpiration: bool | None = None,
        supportsAllDrives: bool | None = None,
        transferOwnership: bool | None = None,
        useDomainAdminAccess: bool | None = None
    ) -> Permission:
        return executeResourceSelf(body="permission")
