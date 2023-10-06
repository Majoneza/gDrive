from gService import gResource
from gData import gData, gDataclass
from googleapiclient.http import (
    MediaIoBaseDownload,
    MediaFileUpload,
    MediaDownloadProgress,
)
from io import BufferedWriter
from utils import (
    object2dict,
    getFunctionName,
    getFunctionVariables,
    getFunctionReturnType,
)
from typing import Any, cast, Dict, Literal, Generator


def downloadMedia(
    fd: BufferedWriter, request: gResource
) -> Generator[MediaDownloadProgress, Any, None]:
    downloader = MediaIoBaseDownload(fd, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        yield status


def moveToKwargsBody(kwargs: Dict[str, Any], name: str):
    kwargs["body"] = kwargs[name]
    del kwargs[name]


def convertKwargs(kwargs: dict[str, Any]):
    for k, v in kwargs.items():
        if type(v).__base__ is gDataclass:
            kwargs[k] = object2dict(v, gDataclass)
        elif type(v) is list:
            kwargs[k] = ",".join(cast(list[Any], v))


def prepareResourceSelf(
    functionName: str,
    kwargs: dict[str, Any],
    body: str | None = None,
    resourceVariableName: str = "_resource",
) -> tuple[gResource, dict[str, Any]]:
    convertKwargs(kwargs)
    if body is not None:
        moveToKwargsBody(kwargs, body)
    resource = getattr(kwargs["self"], resourceVariableName)
    del kwargs["self"]
    return getattr(resource, functionName), kwargs


def executeResourceSelf(
    module: object,
    executionPolicy: Literal["execute", "executeOnlyOnce", "checkForErrors"],
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
) -> Any:
    variableClass = getFunctionReturnType(module, depth + 1)
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    resource, kwargs = prepareResourceSelf(name, kwargs, body, resourceVariableName)
    if executionPolicy == "checkForErrors":
        data = resource(**kwargs).execute()
        if len(data) != 0:
            raise Exception(data)
    else:
        return gData(
            variableClass, resource, kwargs, executionPolicy == "executeOnlyOnce"
        )


def uploadResourceSelf(
    module: object,
    filePathKey: str,
    resumableKey: str,
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
    resource, kwargs = prepareResourceSelf(name, kwargs, body, resourceVariableName)
    return gData(variableClass, resource, kwargs, onlyExecuteOnce=True)


def downloadResourceSelf(
    fdKey: str,
    body: str | None = None,
    resourceVariableName: str = "_resource",
    depth: int = 1,
):
    name = getFunctionName(depth + 1)
    kwargs = getFunctionVariables(depth + 1)
    fd: BufferedWriter = kwargs[fdKey]
    del kwargs[fdKey]
    resource, kwargs = prepareResourceSelf(
        f"{name}_media", kwargs, body, resourceVariableName
    )
    return downloadMedia(fd, resource(**kwargs))
