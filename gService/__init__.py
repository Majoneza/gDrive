from .gCredentials import gCredentials
from .gResourceManager import gResourceManager
from googleapiclient.discovery import build
from typing import Any


class gService(gResourceManager):
    def __init__(
        self, credentials: gCredentials, serviceName: str, version: str
    ) -> None:
        c = credentials.getStoredCredentials()
        if c is not None:
            resource: Any = build(serviceName, version, credentials=c)
        else:
            k = credentials.getStoredKey()
            if k is None:
                raise ValueError("Got invalid credentials")
            resource: Any = build(serviceName, version, developerKey=k)
        super().__init__(resource)
