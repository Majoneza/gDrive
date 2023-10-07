from gService import gCredentials, gService
from gService.gData import executeGDataResource
from .About import gDriveAbout
from .Changes import gDriveChanges
from .Channels import gDriveChannels
from .Comments import gDriveComments
from .Drives import gDriveDrives
from .Files import gDriveFiles
from .Permissions import gDrivePermissions
from .Replies import gDriveReplies
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
        self.about = gDriveAbout(self._resource.about())
        self.changes = gDriveChanges(self._resource.changes())
        self.channels = gDriveChannels(self._resource.channels())
        self.comments = gDriveComments(self._resource.comments())
        self.drives = gDriveDrives(self._resource.drives())
        self.files = gDriveFiles(self._resource.files())
        self.permissions = gDrivePermissions(self._resource.permissions())
        self.replies = gDriveReplies(self._resource.replies())
        self.revisions = gDriveRevisions(self._resource.revisions())
