from gService import gCredentials, gService, executeGDataResource
from .About import gDriveAbout
from .Changes import gDriveChanges
from .Channels import gDriveChannels
from .Drives import gDriveDrives
from .Files import gDriveFiles
from .Permissions import gDrivePermissions
from .Revisions import gDriveRevisions
from .query import FileQueryTerm, SharedDriveQueryTerm


fq = FileQueryTerm
sdq = SharedDriveQueryTerm
execute = executeGDataResource


class Scopes:
    DriveAppdata = "https://www.googleapis.com/auth/drive.appdata"
    DriveAppfolder = "https://www.googleapis.com/auth/drive.appfolder"
    DriveInstall = "https://www.googleapis.com/auth/drive.install"
    DriveFile = "https://www.googleapis.com/auth/drive.file"
    DriveResource = "https://www.googleapis.com/auth/drive.resource"
    DriveAppsReadonly = "https://www.googleapis.com/auth/auth/drive.apps.readonly"
    Drive = "https://www.googleapis.com/auth/drive"
    DriveReadonly = "https://www.googleapis.com/auth/drive.readonly"
    DriveActivity = "https://www.googleapis.com/auth/drive.activity"
    DriveActivityReadonly = "https://www.googleapis.com/auth/drive.activity.readonly"
    DriveMetadata = "https://www.googleapis.com/auth/drive.metadata"
    DriveMetadataReadonly = "https://www.googleapis.com/auth/drive.metadata.readonly"
    DriveScripts = "https://www.googleapis.com/auth/drive.scripts"


class gDrive(gService):
    def __init__(self, credentials: gCredentials):
        super().__init__(credentials, "drive", "v3")
        self.about = gDriveAbout(self._service.about())
        self.changes = gDriveChanges(self._service.changes())
        self.channels = gDriveChannels(self._service.channels())
        self.drives = gDriveDrives(self._service.drives())
        self.files = gDriveFiles(self._service.files())
        self.permissions = gDrivePermissions(self._service.permissions())
        self.revisions = gDriveRevisions(self._service.revisions())
