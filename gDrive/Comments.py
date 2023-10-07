from gService.gResourceManager import gResourceManager
import datetime
from .data import Comment, Comments


class gDriveComments(gResourceManager):
    def create(self, comment: Comment, fileId: str) -> Comment:
        return self._getResource("executeOnlyOnce", body="comment")

    def delete(self, fileId: str, commentId: str) -> None:
        return self._getResource("checkForErrors")

    def get(
        self,
        fileId: str,
        commentId: str,
        includeDeleted: bool | None = None,
    ) -> Comment:
        return self._getResource("execute")

    def list(
        self,
        fileId: str,
        includeDeleted: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
        startModifiedTime: datetime.datetime | None = None,
    ) -> Comments.List:
        return self._getResource("execute")

    def update(self, comment: Comment, fileId: str, commentId: str) -> Comment:
        return self._getResource("executeOnlyOnce", body="comment")
