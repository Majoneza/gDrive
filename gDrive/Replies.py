from gService.gResourceManager import gResourceManager
from .data import Reply, Replies


class gDriveReplies(gResourceManager):
    def create(self, reply: Reply, fileId: str, commentId: str) -> Reply:
        return self._getResource("executeOnlyOnce", body="reply")

    def delete(self, fileId: str, commentId: str, replyId: str) -> None:
        return self._getResource("checkForErrors")

    def get(
        self,
        fileId: str,
        commentId: str,
        replyId: str,
        includeDeleted: bool | None = None,
    ) -> Reply:
        return self._getResource("execute")

    def list(
        self,
        fileId: str,
        commentId: str,
        includeDeleted: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
    ) -> Replies.List:
        return self._getResource("execute")

    def update(self, reply: Reply, fileId: str, commentId: str, replyId: str) -> Reply:
        return self._getResource("executeOnlyOnce", body="reply")
