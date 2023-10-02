from gService import gSubService
from .utils import executeResourceSelf
from gDriveData import Revision, Revisions
from typing import Any, Dict


class gDriveRevisions(gSubService):
    def delete(self, fileId: str, revisionId: str):
        return executeResourceSelf(checkError=True)

    def get(
        self, fileId: str, revisionId: str, acknowledgeAbuse: bool | None = None
    ) -> Revision:
        return executeResourceSelf()

    def list(
        self, fileId: str, pageSize: int | None = None, pageToken: str | None = None
    ) -> Revisions.List:
        return executeResourceSelf()

    def update(
        self, revision: Revision | Dict[str, Any], fileId: str, revisionId: str
    ) -> Revision:
        return executeResourceSelf(body="revision")
