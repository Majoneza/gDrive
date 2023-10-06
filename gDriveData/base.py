from gData import gDataclass, gList
from typing import Any


class User(gDataclass):
    displayName: str
    kind: str
    me: bool
    permissionId: str
    emailAddress: str
    photoLink: str


class ContentRestriction(gDataclass):
    readOnly: bool
    reason: str
    type: str
    restrictingUser: User
    restrictionTime: str
    ownerRestricted: bool


class Label(gDataclass):
    class Field(gDataclass):
        kind: str
        id: str
        valueType: str
        dateString: list[str]
        integer: list[str]
        selection: list[str]
        text: list[str]
        user: gList[User]

    id: str
    revisionId: str
    kind: str
    fields: dict[str, Field]


class About(gDataclass):
    class DriveTheme(gDataclass):
        id: str
        backgroundImageLink: str
        colorRgb: str

    class StorageQuota(gDataclass):
        limit: str
        usageInDrive: str
        usageInDriveTrash: str
        usage: str

    kind: str
    storageQuota: StorageQuota
    driveThemes: gList[DriveTheme]
    canCreateDrives: bool
    importFormats: dict[str, Any]
    exportFormats: dict[str, Any]
    appInstalled: bool
    user: User
    folderColorPalette: list[str]
    maxImportSizes: dict[str, str]
    maxUploadSize: str
    teamDriveThemes: gList[DriveTheme]
    canCreateTeamDrives: bool


class Permission(gDataclass):
    class PermissionDetails(gDataclass):
        permissionType: str
        inheritedFrom: str
        role: str
        inherited: str

    class TeamDrivePermissionDetails(gDataclass):
        teamDrivePermissionType: str
        inheritedFrom: str
        role: str
        inherited: bool

    id: str
    displayName: str
    type: str
    kind: str
    permissionDetails: gList[PermissionDetails]
    photoLink: str
    emailAddress: str
    role: str
    allowFileDiscovery: bool
    domain: str
    expirationTime: str
    teamDrivePermissionDetails: gList[TeamDrivePermissionDetails]
    deleted: bool
    view: str
    pendingOwner: bool


class File(gDataclass):
    class Capabilities(gDataclass):
        canChangeViewersCanCopyContent: bool
        canMoveChildrenOutOfDrive: bool
        canReadDrive: bool
        canEdit: bool
        canCopy: bool
        canComment: bool
        canAddChildren: bool
        canDelete: bool
        canDownload: bool
        canListChildren: bool
        canRemoveChildren: bool
        canRename: bool
        canTrash: bool
        canReadRevisions: bool
        canReadTeamDrive: bool
        canMoveTeamDriveItem: bool
        canChangeCopyRequiresWriterPermission: bool
        canMoveItemIntoTeamDrive: bool
        canUntrash: bool
        canModifyContent: bool
        canMoveItemWithinTeamDrive: bool
        canMoveItemOutOfTeamDrive: bool
        canDeleteChildren: bool
        canMoveChildrenOutOfTeamDrive: bool
        canMoveChildrenWithinTeamDrive: bool
        canTrashChildren: bool
        canMoveItemOutOfDrive: bool
        canAddMyDriveParent: bool
        canRemoveMyDriveParent: bool
        canMoveItemWithinDrive: bool
        canShare: bool
        canMoveChildrenWithinDrive: bool
        canModifyContentRestriction: bool
        canAddFolderFromAnotherDrive: bool
        canChangeSecurityUpdateEnabled: bool
        canAcceptOwnership: bool
        canReadLabels: bool
        canModifyLabels: bool
        canModifyEditorContentRestriction: bool
        canModifyOwnerContentRestriction: bool
        canRemoveContentRestriction: bool

    class ContentHints(gDataclass):
        class Thumbnail(gDataclass):
            image: str
            mimeType: str

        indexableText: str
        thumbnail: Thumbnail

    class ImageMediaMetadata(gDataclass):
        class Location(gDataclass):
            latitude: int
            longitude: int
            altitude: int

        flashUsed: bool
        meteringMode: str
        sensor: str
        exposureMode: str
        colorSpace: str
        whiteBalance: str
        width: int
        height: int
        location: Location
        rotation: int
        time: str
        cameraMake: str
        cameraModel: str
        exposureTime: int
        aperture: int
        focalLength: int
        isoSpeed: int
        exposureBias: int
        maxApertureValue: int
        subjectDistance: int
        lens: str

    class LabelInfo(gDataclass):
        labels: gList[Label]

    class LinkShareMetadata(gDataclass):
        securityUpdateEligible: bool
        securityUpdateEnabled: bool

    class ShortcutDetails(gDataclass):
        targetId: str
        targetMimeType: str
        targetResourceKey: str

    class VideoMediaMetadata(gDataclass):
        width: int
        height: int
        durationMillis: str

    kind: str
    driveId: str
    fileExtension: str
    copyRequiresWriterPermission: bool
    md5Checksum: str
    contentHints: ContentHints
    writersCanShare: bool
    viewedByMe: bool
    mimeType: str
    exportLinks: list[str]
    parents: list[str]
    thumbnailLink: str
    iconLink: str
    shared: bool
    lastModifyingUser: User
    owners: gList[User]
    headRevisionId: str
    sharingUser: User
    webViewLink: str
    webContentLink: str
    size: str
    viewersCanCopyContent: bool
    permissions: gList[Permission]
    hasThumbnail: bool
    spaces: list[str]
    folderColorRgb: str
    id: str
    name: str
    description: str
    starred: bool
    trashed: bool
    explicitlyTrashed: bool
    createdTime: str
    modifiedTime: str
    modifiedByMeTime: str
    viewedByMeTime: str
    sharedWithMeTime: str
    quotaBytesUsed: str
    version: str
    originalFilename: str
    ownedByMe: bool
    fullFileExtension: str
    properties: dict[str, Any]
    appProperties: dict[str, Any]
    isAppAuthorized: bool
    teamDriveId: str
    capabilities: Capabilities
    hasAugmentedPermissions: bool
    trashingUser: User
    thumbnailVersion: str
    trashedTime: str
    modifiedByMe: bool
    permissionIds: list[str]
    imageMediaMetadata: ImageMediaMetadata
    videoMediaMetadata: VideoMediaMetadata
    shortcutDetails: ShortcutDetails
    contentRestrictions: gList[ContentRestriction]
    resourceKey: str
    linkShareMetadata: LinkShareMetadata
    labelInfo: LabelInfo
    sha1Checksum: str
    sha256Checksum: str


class Channel(gDataclass):
    payload: bool
    id: str
    resourceId: str
    resourceUri: str
    token: str
    expiration: str
    type: str
    address: str
    params: dict[str, str]
    kind: str


class Drive(gDataclass):
    class BackgroundImageFile(gDataclass):
        id: str
        xCoordinate: int
        yCoordinate: int
        width: int

    class Capabilities(gDataclass):
        canAddChildren: bool
        canComment: bool
        canCopy: bool
        canDeleteDrive: bool
        canDownload: bool
        canEdit: bool
        canListChildren: bool
        canManageMembers: bool
        canReadRevisions: bool
        canRename: bool
        canRenameDrive: bool
        canChangeDriveBackground: bool
        canShare: bool
        canChangeCopyRequiresWriterPermissionRestriction: bool
        canChangeDomainUsersOnlyRestriction: bool
        canChangeDriveMembersOnlyRestriction: bool
        canChangeSharingFoldersRequiresOrganizerPermissionRestriction: bool
        canResetDriveRestrictions: bool
        canDeleteChildren: bool
        canTrashChildren: bool

    class Restrictions(gDataclass):
        copyRequiresWriterPermission: bool
        domainUsersOnly: bool
        driveMembersOnly: bool
        adminManagedRestrictions: bool
        sharingFoldersRequiresOrganizerPermission: bool

    id: str
    name: str
    colorRgb: str
    kind: str
    backgroundImageLink: str
    capabilities: Capabilities
    themeId: str
    backgroundImageFile: BackgroundImageFile
    createdTime: str
    hidden: bool
    restrictions: Restrictions
    orgUnitId: str


class TeamDrive(gDataclass):
    class Capabilities(gDataclass):
        canAddChildren: bool
        canComment: bool
        canCopy: bool
        canDeleteTeamDrive: bool
        canDownload: bool
        canEdit: bool
        canListChildren: bool
        canManageMembers: bool
        canReadRevisions: bool
        canRemoveChildren: bool
        canRename: bool
        canRenameTeamDrive: bool
        canChangeTeamDriveBackground: bool
        canShare: bool
        canChangeCopyRequiresWriterPermissionRestriction: bool
        canChangeDomainUsersOnlyRestriction: bool
        canChangeTeamMembersOnlyRestriction: bool
        canDeleteChildren: bool
        canTrashChildren: bool

    id: str
    name: str
    colorRgb: str
    kind: str
    backgroundImageLink: str
    capabilities: Capabilities
    themeId: str
    backgroundImageFile: Drive.BackgroundImageFile
    createdTime: str
    hidden: bool
    restrictions: Drive.Restrictions
    orgUnitId: str


class Change(gDataclass):
    kind: str
    removed: bool
    file: File
    fileId: str
    time: str
    driveId: str
    type: str
    teamDriveId: str
    teamDrive: TeamDrive
    changeType: str
    drive: Drive


class Revision(gDataclass):
    id: str
    mimeType: str
    kind: str
    published: bool
    exportLinks: dict[str, str]
    keepForever: bool
    md5Checksum: str
    modifiedTime: str
    publishAuto: bool
    publishedOutsideDomain: bool
    publishedLink: str
    size: str
    originalFilename: str
    lastModifyingUser: User


class Reply(gDataclass):
    id: str
    kind: str
    createdTime: str
    modifiedTime: str
    action: str
    author: User
    deleted: bool
    htmlContent: str
    content: str


class Comment(gDataclass):
    class QuotedFileContent(gDataclass):
        mimeType: str
        value: str

    id: str
    kind: str
    createdTime: str
    modifiedTime: str
    resolved: bool
    anchor: str
    replies: gList[Reply]
    author: User
    deleted: bool
    htmlContent: str
    content: str
    quotedFileContent: QuotedFileContent
