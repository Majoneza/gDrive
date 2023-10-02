from gService import gResource
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from io import BufferedWriter
from utils import dict2object, removeNones, getFunctionName, getFunctionVariables
from typing import Any, Dict, Iterable


def downloadMedia(fd: BufferedWriter, request: gResource):
    downloader = MediaIoBaseDownload(fd, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        yield status


def moveToKwargsBody(kwargs: Dict[str, Any], name: str):
    kwargs["body"] = kwargs[name]
    del kwargs[name]


def joinKwargs(kwargs: Dict[str, Any], variables: Iterable[str]):
    for v in variables:
        if v in kwargs:
            kwargs[v] = ",".join(kwargs[v])


def removeNonesKwargs(kwargs: Dict[str, Any], name: str):
    kwargs[name] = removeNones(kwargs[name])


def getResourceSelf(
    functionName: str,
    kwargs: Dict[str, Any],
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
) -> gResource:
    joinKwargs(kwargs, joins)
    if body is not None:
        kwargs["body"] = removeNones(kwargs[body])
        del kwargs[body]
    resource = getattr(kwargs["self"], resourceVariableName)
    del kwargs["self"]
    return getattr(resource, functionName)(**kwargs)


def executeResourceSelf(
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    checkError: bool = False,
    depth: int = 1,
) -> Any:
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    data = getResourceSelf(name, kwargs, joins, body, resourceVariableName).execute()
    if checkError and len(data) != 0:
        raise Exception(data)
    else:
        return dict2object(data)


def uploadResourceSelf(
    filePathKey: str,
    resumableKey: str,
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
) -> Any:
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    filePath: str = kwargs[filePathKey]
    resumable: bool = kwargs[resumableKey]
    del kwargs[filePathKey]
    del kwargs[resumableKey]
    media = MediaFileUpload(filePath, resumable=resumable)
    kwargs["media_body"] = media
    data = getResourceSelf(name, kwargs, joins, body, resourceVariableName).execute()
    return dict2object(data)


def downloadResourceSelf(
    fdKey: str,
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
) -> Any:
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    fd: BufferedWriter = kwargs[fdKey]
    del kwargs[fdKey]
    request = getResourceSelf(
        f"{name}_media", kwargs, joins, body, resourceVariableName
    )
    downloader = MediaIoBaseDownload(fd, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        yield status
