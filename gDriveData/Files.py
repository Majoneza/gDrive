from gService import gDataclass, gList
from .base import File, Label


class List(gDataclass):
    nextPageToken: str
    kind: str
    incompleteSearch: bool
    files: gList[File]


class GenerateIds(gDataclass):
    ids: list[str]
    space: str
    kind: str


class ListLabels(gDataclass):
    labels: gList[Label]
    nextPageToken: str
    kind: str


class ModifyLabels(gDataclass):
    modifiedLabels: gList[Label]
    kind: str


class ModifyLabelsRequest(gDataclass):
    class LabelModification(gDataclass):
        class FieldModification(gDataclass):
            fieldId: str
            kind: str
            setDateValues: list[str]
            setTextValues: list[str]
            setSelectionValues: list[str]
            setIntegerValues: list[str]
            setUserValues: list[str]
            unsetValues: bool

        labelId: str
        fieldModifications: gList[FieldModification]
        removeLabel: bool
        kind: str

    labelModifications: gList[LabelModification]
    kind: str
