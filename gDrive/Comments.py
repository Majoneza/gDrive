from gService import gSubService
from .utils import executeResourceSelf
from gDriveData import Comment, Comments


class gDriveComments(gSubService):
    def create(self, comment: Comment, fileId: str) -> Comment:
        return executeResourceSelf(self, "executeOnlyOnce", body="comment")

    def delete(self, fileId: str, commentId: str) -> None:
        return executeResourceSelf(self, "checkForErrors")

    def get(
        self,
        fileId: str,
        commentId: str,
        includeDeleted: bool | None = None,
    ) -> Comment:
        return executeResourceSelf(self, "execute")

    def list(
        self,
        fileId: str,
        includeDeleted: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        startModifiedTime: str | None = None,
    ) -> Comments.List:
        return executeResourceSelf(self, "execute")

    def update(self, comment: Comment, fileId: str, commentId: str) -> Comment:
        return executeResourceSelf(self, "executeOnlyOnce", body="comment")
