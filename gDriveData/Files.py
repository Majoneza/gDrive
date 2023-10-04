from gService import gDataclass
from .base import File, Label


class List(gDataclass):
    nextPageToken: str
    kind: str
    incompleteSearch: bool
    files: list[File]


class GenerateIds(gDataclass):
    ids: list[str]
    space: str
    kind: str


class ListLabels(gDataclass):
    labels: list[Label]
    nextPageToken: str
    kind: str


class ModifyLabels(gDataclass):
    modifiedLabels: list[Label]
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
        fieldModifications: list[FieldModification]
        removeLabel: bool
        kind: str

    labelModifications: list[LabelModification]
    kind: str
