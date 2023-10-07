from gService.gResourceManager import gResourceManager
from .data import Permission, Permissions
from .data.helpers import IncludePermissionsForView


class gDrivePermissions(gResourceManager):
    def create(
        self,
        permission: Permission,
        fileId: str,
        emailMessage: str | None = None,
        moveToNewOwnersRoot: bool | None = None,
        sendNotificationEmail: bool | None = None,
        supportsAllDrives: bool | None = None,
        transferOwnership: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return self._getResource("executeOnlyOnce", body="permission")

    def delete(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> None:
        return self._getResource("checkForErrors")

    def get(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return self._getResource("execute")

    def list(
        self,
        fileId: str,
        pageSize: int | None = None,
        pageToken: str | None = None,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
    ) -> Permissions.List:
        return self._getResource("execute")

    def update(
        self,
        permission: Permission,
        fileId: str,
        permissionId: str,
        removeExpiration: bool | None = None,
        supportsAllDrives: bool | None = None,
        transferOwnership: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return self._getResource("executeOnlyOnce", body="permission")
