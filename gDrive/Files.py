from gService.gResourceManager import gResourceManager
import os
from .data import Channel, Files, File
from .data.helpers import IncludePermissionsForView, Space
from .utils import FolderMimeType, processDrivePath
from .query import BridgeTerm, FileQueryTerm as fq
from googleapiclient.http import MediaDownloadProgress
from io import BufferedWriter
from typing import Any, List, Literal, Generator, overload, Union


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
TreeResult = dict[tuple[str, str], Union["TreeResult", None]]


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
    ) -> Generator[MediaDownloadProgress, Any, None]: ...

    @overload
    def get(
        self,
        fileId: str,
        fd: None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ) -> File: ...

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

    def GetDrivePathId(self, drivePath: str) -> str:
        fileId, parts = processDrivePath(drivePath)
        for part in parts:
            query = fq().name.Eq(part) & fq().parents.Include(fileId)
            files = self.list(q=query).files.getFields(File.id)
            if len(files) != 1:
                raise ValueError(
                    "Found multiple files with given name"
                    if len(files) > 1
                    else "Found no files with given name"
                )
            fileId = files[0].id
        return fileId

    def TreeId(self, folderId: str) -> TreeResult:
        query = fq().parents.Include(folderId)
        files = self.list(q=query).files.getFields(File.id, File.name, File.mimeType)
        result: TreeResult = {}
        for file in files:
            key = (file.id, file.name)
            if file.mimeType == FolderMimeType:
                result[key] = self.TreeId(file.id)
            else:
                result[key] = None
        return result

    def Tree(self, drivePath: str) -> TreeResult:
        folderId = self.GetDrivePathId(drivePath)
        return self.TreeId(folderId)

    def Delete(
        self,
        drivePath: str,
        supportsAllDrives: bool | None = None,
    ) -> None:
        fileId = self.GetDrivePathId(drivePath)
        return self.delete(fileId, supportsAllDrives)

    def DownloadId(
        self,
        fileId: str,
        localPath: str | None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ):
        if localPath is not None:
            if os.path.isdir(localPath):
                path = os.path.join(localPath, self.get(fileId).name)
            else:
                path = localPath
        else:
            path = self.get(fileId).name
        with open(path, "xb") as file:
            getGenerator = self.get(
                fileId,
                file,
                acknowledgeAbuse,
                supportsAllDrives,
                includePermissionsForView,
                includeLabels,
            )
            for progress in getGenerator:
                yield progress

    def Download(
        self,
        drivePath: str,
        localPath: str | None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: IncludePermissionsForView | None = None,
        includeLabels: List[str] | None = None,
    ):
        fileId = self.GetDrivePathId(drivePath)
        return self.DownloadId(
            fileId,
            localPath,
            acknowledgeAbuse,
            supportsAllDrives,
            includePermissionsForView,
            includeLabels,
        )

    def _DownloadTree(self, tree: TreeResult, localFolderPath: str):
        result: list[tuple[str, Generator[MediaDownloadProgress, Any, None]]] = []
        for key, value in tree.items():
            path = os.path.join(localFolderPath, key[1])
            if value is None:
                result.append((path, self.DownloadId(key[0], path)))
            else:
                os.mkdir(path)
                result.extend(self._DownloadTree(value, path))
        return result

    def DownloadFolderId(self, folderId: str, localPath: str | None = None):
        if localPath is not None:
            if not os.path.isdir(localPath):
                os.makedirs(localPath)
        else:
            localPath = os.curdir
        return self._DownloadTree(self.TreeId(folderId), localPath)

    def DownloadFolder(self, drivePath: str, localPath: str | None = None):
        return self.DownloadFolderId(self.GetDrivePathId(drivePath), localPath)
