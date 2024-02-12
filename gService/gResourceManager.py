from .gResource import gResource
from .gData import gData, gDataclass
import datetime
from googleapiclient.http import (
    MediaIoBaseDownload,
    MediaFileUpload,
    MediaDownloadProgress,
)
from io import BufferedWriter
from .utils import (
    object2dict,
    removeNonesDict,
    getFunctionName,
    getFunctionVariables,
    getOverloadedFunctionReturnTypeAndVariables,
)
from typing import Any, cast, Dict, Literal, Generator, Self
from types import TracebackType


class gResourceManager:
    _resource: gResource

    def __init__(self, resource: gResource) -> None:
        self._resource = resource

    @staticmethod
    def _downloadMedia(
        fd: BufferedWriter, request: gResource
    ) -> Generator[MediaDownloadProgress, Any, None]:
        downloader = MediaIoBaseDownload(fd, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            yield status

    @staticmethod
    def _moveToKwargsBody(kwargs: Dict[str, Any], name: str):
        kwargs["body"] = kwargs[name]
        del kwargs[name]

    @staticmethod
    def _convertKwargs(kwargs: dict[str, Any]):
        for k, v in kwargs.items():
            if isinstance(v, gDataclass):
                kwargs[k] = object2dict(v, gDataclass)
            elif type(v) is list:
                kwargs[k] = ",".join(cast(list[Any], v))
            elif type(v) is datetime.datetime:
                kwargs[k] = v.isoformat()

    @classmethod
    def _prepareKwargs(
        cls,
        kwargs: dict[str, Any],
        body: str | None,
    ) -> None:
        cls._convertKwargs(kwargs)
        if body is not None:
            cls._moveToKwargsBody(kwargs, body)
        del kwargs["self"]

    def _getRawResource(self, depth: int = 1, suffix: str = ""):
        name = getFunctionName(depth + 1)
        return getattr(self._resource, name + suffix)

    def _getResource(
        self,
        executionPolicy: Literal["execute", "executeOnlyOnce", "checkForErrors"],
        body: str | None = None,
        depth: int = 1,
    ) -> Any:
        variableClass, kwargs = getOverloadedFunctionReturnTypeAndVariables(
            self, depth + 1
        )
        kwargs = removeNonesDict(kwargs)
        self._prepareKwargs(kwargs, body)
        resource = self._getRawResource(depth + 1)
        if executionPolicy == "checkForErrors":
            data = resource(**kwargs).execute()
            if len(data) != 0:
                raise Exception(data)
        else:
            return gData(
                variableClass, resource, kwargs, executionPolicy == "executeOnlyOnce"
            )

    def _uploadResource(
        self,
        filePathKey: str,
        resumableKey: str,
        body: str | None = None,
        depth: int = 1,
    ) -> Any:
        variableClass, kwargs = getOverloadedFunctionReturnTypeAndVariables(
            self, depth + 1
        )
        kwargs = removeNonesDict(kwargs)
        filePath: str = kwargs[filePathKey]
        resumable: bool = kwargs[resumableKey]
        del kwargs[filePathKey]
        del kwargs[resumableKey]
        media = MediaFileUpload(filePath, resumable=resumable)
        kwargs["media_body"] = media
        self._prepareKwargs(kwargs, body)
        resource = self._getRawResource(depth + 1)
        return gData(variableClass, resource, kwargs, executeOnlyOnce=True)

    def _downloadResource(
        self,
        fdKey: str,
        body: str | None = None,
        depth: int = 1,
    ):
        kwargs = removeNonesDict(getFunctionVariables(depth + 1))
        fd: BufferedWriter = kwargs[fdKey]
        del kwargs[fdKey]
        self._prepareKwargs(kwargs, body)
        resource = self._getRawResource(depth + 1, suffix="_media")
        return self._downloadMedia(fd, resource(**kwargs))

    def __enter__(self) -> Self:
        self._resource.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._resource.__exit__(exc_type, exc_val, exc_tb)

    def close(self) -> None:
        self._resource.close()
