from gService import gSubService
from .utils import executeResourceSelf
from gDriveData import Revision, Revisions


class gDriveRevisions(gSubService):
    def delete(self, fileId: str, revisionId: str) -> None:
        return executeResourceSelf(self, "checkForErrors")

    def get(
        self, fileId: str, revisionId: str, acknowledgeAbuse: bool | None = None
    ) -> Revision:
        return executeResourceSelf(self, "execute")

    def list(
        self, fileId: str, pageSize: int | None = None, pageToken: str | None = None
    ) -> Revisions.List:
        return executeResourceSelf(self, "execute")

    def update(self, revision: Revision, fileId: str, revisionId: str) -> Revision:
        return executeResourceSelf(self, "executeOnlyOnce", body="revision")
