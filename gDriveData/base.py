from gService import gData
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class User(gData):
    displayName: str
    kind: str
    me: bool
    permissionId: str
    emailAddress: str
    photoLink: str


@dataclass
class ContentRestriction(gData):
    readOnly: bool
    reason: str
    type: str
    restrictingUser: User
    restrictionTime: str
    ownerRestricted: bool


@dataclass
class Label(gData):
    @dataclass
    class Field(gData):
        kind: str
        id: str
        valueType: str
        dateString: List[str]
        integer: List[str]
        selection: List[str]
        text: List[str]
        user: List[User]

    id: str
    revisionId: str
    kind: str
    fields: Dict[str, Field]


@dataclass
class Permission(gData):
    @dataclass
    class PermissionDetails(gData):
        permissionType: str
        inheritedFrom: str
        role: str
        inherited: str

    @dataclass
    class TeamDrivePermissionDetails(gData):
        teamDrivePermissionType: str
        inheritedFrom: str
        role: str
        inherited: bool

    id: str
    displayName: str
    type: str
    kind: str
    permissionDetails: List[PermissionDetails]
    photoLink: str
    emailAddress: str
    role: str
    allowFileDiscovery: bool
    domain: str
    expirationTime: str
    teamDrivePermissionDetails: List[TeamDrivePermissionDetails]
    deleted: bool
    view: str
    pendingOwner: bool


@dataclass
class File(gData):
    @dataclass
    class Capabilities(gData):
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

    @dataclass
    class ContentHints(gData):
        @dataclass
        class Thumbnail(gData):
            image: str
            mimeType: str

        indexableText: str
        thumbnail: Thumbnail

    @dataclass
    class ImageMediaMetadata(gData):
        @dataclass
        class Location(gData):
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

    @dataclass
    class LabelInfo(gData):
        labels: List[Label]

    @dataclass
    class LinkShareMetadata(gData):
        securityUpdateEligible: bool
        securityUpdateEnabled: bool

    @dataclass
    class ShortcutDetails(gData):
        targetId: str
        targetMimeType: str
        targetResourceKey: str

    @dataclass
    class VideoMediaMetadata(gData):
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
    exportLinks: List[str]
    parents: List[str]
    thumbnailLink: str
    iconLink: str
    shared: bool
    lastModifyingUser: User
    owners: List[User]
    headRevisionId: str
    sharingUser: User
    webViewLink: str
    webContentLink: str
    size: str
    viewersCanCopyContent: bool
    permissions: List[Permission]
    hasThumbnail: bool
    spaces: List[str]
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
    properties: Dict[str, Any]
    appProperties: Dict[str, Any]
    isAppAuthorized: bool
    teamDriveId: str
    capabilities: Capabilities
    hasAugmentedPermissions: bool
    trashingUser: User
    thumbnailVersion: str
    trashedTime: str
    modifiedByMe: bool
    permissionIds: List[str]
    imageMediaMetadata: ImageMediaMetadata
    videoMediaMetadata: VideoMediaMetadata
    shortcutDetails: ShortcutDetails
    contentRestrictions: List[ContentRestriction]
    resourceKey: str
    linkShareMetadata: LinkShareMetadata
    labelInfo: LabelInfo
    sha1Checksum: str
    sha256Checksum: str


@dataclass
class About(gData):
    @dataclass
    class DriveTheme(gData):
        id: str
        backgroundImageLink: str
        colorRgb: str

    @dataclass
    class StorageQuota(gData):
        limit: str
        usageInDrive: str
        usageInDriveTrash: str
        usage: str

    kind: str
    storageQuota: StorageQuota
    driveThemes: List[DriveTheme]
    canCreateDrives: bool
    importFormats: Dict[str, Any]
    exportFormats: Dict[str, Any]
    appInstalled: bool
    user: User
    folderColorPalette: List[str]
    maxImportSizes: Dict[str, str]
    maxUploadSize: str
    teamDriveThemes: List[DriveTheme]
    canCreateTeamDrives: bool


@dataclass
class Channel(gData):
    payload: bool
    id: str
    resourceId: str
    resourceUri: str
    token: str
    expiration: str
    type: str
    address: str
    params: Dict[str, str]
    kind: str


@dataclass
class Drive(gData):
    @dataclass
    class BackgroundImageFile(gData):
        id: str
        xCoordinate: int
        yCoordinate: int
        width: int

    @dataclass
    class Capabilities(gData):
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

    @dataclass
    class Restrictions(gData):
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


@dataclass
class TeamDrive(gData):
    @dataclass
    class Capabilities(gData):
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


@dataclass
class Change(gData):
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


@dataclass
class Revision(gData):
    id: str
    mimeType: str
    kind: str
    published: bool
    exportLinks: Dict[str, str]
    keepForever: bool
    md5Checksum: str
    modifiedTime: str
    publishAuto: bool
    publishedOutsideDomain: bool
    publishedLink: str
    size: str
    originalFilename: str
    lastModifyingUser: User
