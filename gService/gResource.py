from googleapiclient.discovery import Resource
from typing import Any, Self


class gResource(Resource):
    def execute(self, *args: Any) -> Any:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        ...

    def __getattribute__(self, __name: str) -> Self:
        ...
