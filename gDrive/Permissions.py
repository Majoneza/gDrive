from gService import gSubService
from gDriveData import Permission, Permissions, IncludePermissionsForView
from .utils import executeResourceSelf


class gDrivePermissions(gSubService):
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
        return executeResourceSelf(self, "executeOnlyOnce", body="permission")

    def delete(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> None:
        return executeResourceSelf(self, "checkForErrors")

    def get(
        self,
        fileId: str,
        permissionId: str,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
    ) -> Permission:
        return executeResourceSelf(self, "execute")

    def list(
        self,
        fileId: str,
        pageSize: int | None = None,
        pageToken: str | None = None,
        supportsAllDrives: bool | None = None,
        useDomainAdminAccess: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
    ) -> Permissions.List:
        return executeResourceSelf(self, "execute")

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
        return executeResourceSelf(self, "executeOnlyOnce", body="permission")
