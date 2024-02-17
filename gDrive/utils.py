import os

FolderMimeType = "application/vnd.google-apps.folder"

def splitPath(path: str) -> list[str]:
    return os.path.normpath(path).split(os.sep)

def processDrivePath(path: str) -> tuple[str, list[str]]:
    split = path.split(":/", maxsplit=1)
    if len(split) == 1:
        split.insert(0, "root")
    return split[0], splitPath(split[1])
