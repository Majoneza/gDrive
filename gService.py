from gCredentials import gCredentials
from googleapiclient.discovery import build, Resource
from typing import Any, Self
from types import TracebackType


class gResource(Resource):
    def execute(self, *args: Any) -> Any:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        ...

    def __getattribute__(self, __name: str) -> Self:
        ...


class gSubService:
    _resource: gResource

    def __init__(self, resource: gResource) -> None:
        self._resource = resource


class gService:
    _service: gResource

    def __init__(
        self, credentials: gCredentials, serviceName: str, version: str
    ) -> None:
        if not credentials.isValid():
            raise ValueError("Got invalid credentials")
        self._service = build(serviceName, version, credentials=credentials.get())

    def __enter__(self) -> Self:
        self._service.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._service.__exit__(exc_type, exc_val, exc_tb)

    def close(self) -> None:
        self._service.close()
