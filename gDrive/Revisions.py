from gService.gResourceManager import gResourceManager
from .data import Revision, Revisions


class gDriveRevisions(gResourceManager):
    def delete(self, fileId: str, revisionId: str) -> None:
        return self._getResource("checkForErrors")

    def get(
        self, fileId: str, revisionId: str, acknowledgeAbuse: bool | None = None
    ) -> Revision:
        return self._getResource("execute")

    def list(
        self, fileId: str, pageSize: int | None = None, pageToken: str | None = None
    ) -> Revisions.List:
        return self._getResource("execute")

    def update(self, revision: Revision, fileId: str, revisionId: str) -> Revision:
        return self._getResource("executeOnlyOnce", body="revision")
