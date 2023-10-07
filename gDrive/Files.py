from gService.gResourceManager import gResourceManager
import os
from .data import Channel, Files, File
from .data.helpers import IncludePermissionsForView, Space
from .utils import splitPath
from .query import BridgeTerm, FileQueryTerm as fq
from googleapiclient.http import MediaDownloadProgress
from io import BufferedWriter
from typing import Any, List, Literal, Generator, overload


GenerateIdsType = Literal["files", "shortcuts"]
ListOrderByItems = Literal[
    "createdTime",
    "folder",
    "modifiedByMeTime",
    "modifiedTime",
    "name",
    "name_natural",
    "quotaBytesUsed",
    "recency",
    "sharedWithMeTime",
    "starred",
    "viewedByMeTime",
]


class gDriveFiles(gResourceManager):
    def copy(
        self,
        fileId: str,
        filePath: str,
        fileMetadata: File,
        enforceSingleParent: bool | None = None,
        ignoreDefaultVisibility: bool | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return self._uploadResource("filePath", "resumable", body="fileMetadata")

    def create(
        self,
        filePath: str,
        fileMetadata: File,
        enforceSingleParent: bool | None = None,
        ignoreDefaultVisibility: bool | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        supportsAllDrives: bool | None = None,
        useContentAsIndexableText: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return self._uploadResource("filePath", "resumable", body="fileMetadata")

    def delete(self, fileId: str, supportsAllDrives: bool | None = None) -> None:
        return self._getResource("checkForErrors")

    def emptyTrash(self, driveId: str | None = None) -> None:
        return self._getResource("checkForErrors")

    def export(self, fileId: str, fd: BufferedWriter, mimeType: str | None = None):
        return self._downloadResource("fd")

    def generateIds(
        self,
        count: int | None = None,
        space: str | None = None,
        type: GenerateIdsType | None = None,
    ) -> Files.GenerateIds:
        return self._getResource("executeOnlyOnce")

    @overload
    def get(
        self,
        fileId: str,
        fd: BufferedWriter,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> Generator[MediaDownloadProgress, Any, None]:
        ...

    @overload
    def get(
        self,
        fileId: str,
        fd: None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> File:
        ...

    def get(
        self,
        fileId: str,
        fd: BufferedWriter | None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ):
        if fd is not None:
            return self._downloadResource("fd")
        else:
            return self._getResource("execute")

    def list(
        self,
        corpora: Literal["user", "domain", "drive", "allDrives"] | None = None,
        driveId: str | None = None,
        includeItemsFromAllDrives: bool | None = None,
        orderBy: List[ListOrderByItems] | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        q: str | BridgeTerm | None = None,
        spaces: List[Space] | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> Files.List:
        return self._getResource("execute")

    def listLabels(
        self, fileId: str, maxResults: int | None = None, pageToken: str | None = None
    ) -> Files.ListLabels:
        return self._getResource("execute")

    def modifyLabels(
        self, request: Files.ModifyLabelsRequest, fileId: str
    ) -> Files.ModifyLabels:
        return self._getResource("executeOnlyOnce", body="request")

    def update(
        self,
        fileId: str,
        filePath: str,
        fileMetadata: File,
        addParents: List[str] | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        removeParents: List[str] | None = None,
        supportsAllDrives: bool | None = None,
        useContentAsIndexableText: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return self._uploadResource(
            "filePath",
            "resumable",
            body="fileMetadata",
        )

    def watch(
        self,
        channel: Channel,
        fileId: str,
        supportsAllDrives: bool | None = None,
        acknowledgeAbuse: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> Channel:
        return self._getResource("executeOnlyOnce", body="channel")

    def GetPathId(self, path: str) -> str:
        parts = splitPath(path)
        fileId = "root"
        for part in parts:
            query = fq().name.Eq(part) & fq().parents.Include(fileId)
            files = self.list(q=query).files
            if len(files) != 1:
                raise ValueError(
                    "Found multiple files with given name"
                    if len(files) > 1
                    else "Found no files with given name"
                )
            fileId = files[0].id
        return fileId

    def Delete(
        self,
        path: str,
        supportsAllDrives: bool | None = None,
    ) -> None:
        fileId = self.GetPathId(path)
        return self.delete(fileId, supportsAllDrives)

    def Download(
        self,
        drivePath: str,
        localPath: str | None = None,
    ):
        fileId = self.GetPathId(drivePath)
        if localPath is not None:
            if os.path.isdir(localPath):
                name = self.get(fileId).name
                path = os.path.join(localPath, name)
            else:
                path = localPath
        else:
            path = self.get(fileId).name
        with open(path, "xb") as file:
            return self.get(fileId, file)

    def Upload(self, localPath: str, drivePath: str | None = None):
        if drivePath is None:
            file_metadata = File(name=os.path.basename(localPath))
        else:
            try:
                folderId = self.GetPathId(os.path.dirname(drivePath))
                name = os.path.basename(drivePath)
            except ValueError:
                folderId = self.GetPathId(drivePath)
                name = os.path.basename(localPath)
            file_metadata = File(name=name, parents=[folderId])
        return self.create(localPath, file_metadata)
