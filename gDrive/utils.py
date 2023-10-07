import os

def splitPath(path: str) -> list[str]:
    return os.path.normpath(path).split(os.sep)
