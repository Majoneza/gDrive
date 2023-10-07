from .gCredentials import gCredentials
from .gResourceManager import gResourceManager
from googleapiclient.discovery import build
from typing import Any


class gService(gResourceManager):
    def __init__(
        self, credentials: gCredentials, serviceName: str, version: str
    ) -> None:
        if not credentials.isValid():
            raise ValueError("Got invalid credentials")
        resource: Any = build(serviceName, version, credentials=credentials.get())
        super().__init__(resource)
