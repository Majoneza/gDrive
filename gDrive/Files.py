import os
from gService import gSubService
from gDriveData import Channel, Files, File
from utils import splitPath
from .query import BridgeTerm, FileQueryTerm as fq
from .utils import (
    downloadResourceSelf,
    uploadResourceSelf,
    executeResourceSelf,
)
from googleapiclient.http import MediaDownloadProgress
from io import BufferedWriter
from typing import Any, Dict, List, Generator, overload


class gDriveFiles(gSubService):
    def copy(
        self,
        fileId: str,
        filePath: str,
        fileMetadata: File | Dict[str, Any],
        enforceSingleParent: bool | None = None,
        ignoreDefaultVisibility: bool | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return uploadResourceSelf(
            "filePath", "resumable", joins=["includeLabels"], body="fileMetadata"
        )

    def create(
        self,
        filePath: str,
        fileMetadata: File | Dict[str, Any],
        enforceSingleParent: bool | None = None,
        ignoreDefaultVisibility: bool | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        supportsAllDrives: bool | None = None,
        useContentAsIndexableText: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return uploadResourceSelf(
            "filePath", "resumable", joins=["includeLabels"], body="fileMetadata"
        )

    def delete(self, fileId: str, supportsAllDrives: bool | None = None) -> None:
        return executeResourceSelf(checkError=True)

    def emptyTrash(self, driveId: str | None = None) -> None:
        return executeResourceSelf(checkError=True)

    def export(self, fileId: str, fd: BufferedWriter, mimeType: str | None = None):
        return downloadResourceSelf("fd")

    def generateIds(
        self,
        count: int | None = None,
        space: str | None = None,
        type: str | None = None,
    ) -> Files.GenerateIds:
        return executeResourceSelf()

    @overload
    def get(
        self,
        fileId: str,
        fd: BufferedWriter,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: str | None = None,
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
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
    ) -> File:
        ...

    def get(
        self,
        fileId: str,
        fd: BufferedWriter | None = None,
        acknowledgeAbuse: bool | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
    ):
        if fd is not None:
            return downloadResourceSelf('fd', joins=["includeLabels"])
        else:
            return executeResourceSelf(joins=["includeLabels"])

    def list(
        self,
        corpora: str | None = None,
        driveId: str | None = None,
        includeItemsFromAllDrives: bool | None = None,
        orderBy: List[str] | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        q: str | BridgeTerm | None = None,
        spaces: List[str] | None = None,
        supportsAllDrives: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
    ) -> Files.List:
        return executeResourceSelf(joins=["orderBy", "spaces", "includeLabels"])

    def listLabels(
        self, fileId: str, maxResults: int | None = None, pageToken: str | None = None
    ) -> Files.ListLabels:
        return executeResourceSelf()

    def modifyLabels(
        self, fileId: str, request: Files.ModifyLabelsRequest
    ) -> Files.ModifyLabels:
        return executeResourceSelf()

    def update(
        self,
        fileId: str,
        filePath: str,
        fileMetadata: File | Dict[str, Any],
        addParents: List[str] | None = None,
        keepRevisionForever: bool | None = None,
        ocrLanguage: str | None = None,
        removeParents: List[str] | None = None,
        supportsAllDrives: bool | None = None,
        useContentAsIndexableText: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
        resumable: bool = False,
    ) -> File:
        return uploadResourceSelf(
            "filePath",
            "resumable",
            joins=["addParents", "removeParents", "includeLabels"],
            body="fileMetadata",
        )

    def watch(
        self,
        channel: Channel,
        fileId: str,
        supportsAllDrives: bool | None = None,
        acknowledgeAbuse: bool | None = None,
        includePermissionsForView: str | None = None,
        includeLabels: List[str] | None = None,
    ) -> Channel:
        return executeResourceSelf(joins=["includeLabels"], body="channel")

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
        name: str,
        supportsAllDrives: bool | None = None,
    ) -> None:
        files = self.list(q=f'name = "{name}"').files
        if len(files) != 1:
            raise ValueError(
                "Found multiple files with given name"
                if len(files) > 1
                else "Found no files with given name"
            )
        return self.delete(files[0].id, supportsAllDrives)

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
            file_metadata = {"name": os.path.basename(localPath)}
        else:
            try:
                folderId = self.GetPathId(os.path.dirname(drivePath))
                name = os.path.basename(drivePath)
            except ValueError:
                folderId = self.GetPathId(drivePath)
                name = os.path.basename(localPath)
            file_metadata = {"name": name, "parents": [folderId]}
        return self.create(localPath, file_metadata)