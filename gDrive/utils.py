from gService import gResource, gData
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from io import BufferedWriter
from utils import (
    removeNones,
    getFunctionName,
    getFunctionVariables,
    getFunctionReturnType,
)
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


def joinKwargs(kwargs: dict[str, Any], variables: Iterable[str]):
    for v in variables:
        if v in kwargs:
            kwargs[v] = ",".join(kwargs[v])


def removeNonesKwargs(kwargs: dict[str, Any], name: str):
    kwargs[name] = removeNones(kwargs[name])


def prepareResourceSelf(
    functionName: str,
    kwargs: dict[str, Any],
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
) -> tuple[gResource, dict[str, Any]]:
    joinKwargs(kwargs, joins)
    if body is not None:
        moveToKwargsBody(kwargs, body)
    resource = getattr(kwargs["self"], resourceVariableName)
    del kwargs["self"]
    return getattr(resource, functionName), kwargs


def executeResourceSelf(
    module: object,
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    checkError: bool = False,
    depth: int = 1,
) -> Any:
    variableClass = getFunctionReturnType(module, depth + 1)
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    resource, kwargs = prepareResourceSelf(
        name, kwargs, joins, body, resourceVariableName
    )
    if checkError:
        data = resource(**kwargs).execute()
        if len(data) != 0:
            raise Exception(data)
    else:
        return gData(variableClass, resource, kwargs)


def uploadResourceSelf(
    module: object,
    filePathKey: str,
    resumableKey: str,
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
) -> Any:
    variableClass = getFunctionReturnType(module, depth + 1)
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    filePath: str = kwargs[filePathKey]
    resumable: bool = kwargs[resumableKey]
    del kwargs[filePathKey]
    del kwargs[resumableKey]
    media = MediaFileUpload(filePath, resumable=resumable)
    kwargs["media_body"] = media
    resource, kwargs = prepareResourceSelf(
        name, kwargs, joins, body, resourceVariableName
    )
    return gData(variableClass, resource, kwargs)


def downloadResourceSelf(
    fdKey: str,
    joins: Iterable[str] = [],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
):
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    fd: BufferedWriter = kwargs[fdKey]
    del kwargs[fdKey]
    resource, kwargs = prepareResourceSelf(
        f"{name}_media", kwargs, joins, body, resourceVariableName
    )
    return downloadMedia(fd, resource(**kwargs))
