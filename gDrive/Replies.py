from gService import gSubService
from .utils import executeResourceSelf
from gDriveData import Reply, Replies


class gDriveReplies(gSubService):
    def create(self, reply: Reply, fileId: str, commentId: str) -> Reply:
        return executeResourceSelf(self, "executeOnlyOnce", body="reply")

    def delete(self, fileId: str, commentId: str, replyId: str) -> None:
        return executeResourceSelf(self, "checkForErrors")

    def get(
        self,
        fileId: str,
        commentId: str,
        replyId: str,
        includeDeleted: bool | None = None,
    ) -> Reply:
        return executeResourceSelf(self, "execute")

    def list(
        self,
        fileId: str,
        commentId: str,
        includeDeleted: bool | None = None,
        pageSize: int | None = None,
        pageToken: str | None = None,
    ) -> Replies.List:
        return executeResourceSelf(self, "execute")

    def update(self, reply: Reply, fileId: str, commentId: str, replyId: str) -> Reply:
        return executeResourceSelf(self, "executeOnlyOnce", body="reply")
