from dataclasses import dataclass
from .base import gData, File, Label
from typing import List as ListType


@dataclass
class List(gData):
    nextPageToken: str
    kind: str
    incompleteSearch: bool
    files: ListType[File]


@dataclass
class GenerateIds(gData):
    ids: ListType[str]
    space: str
    kind: str


@dataclass
class ListLabels(gData):
    labels: ListType[Label]
    nextPageToken: str
    kind: str


@dataclass
class ModifyLabels(gData):
    modifiedLabels: ListType[Label]
    kind: str


@dataclass
class ModifyLabelsRequest(gData):
    @dataclass
    class LabelModification(gData):
        @dataclass
        class FieldModification(gData):
            fieldId: str
            kind: str
            setDateValues: ListType[str]
            setTextValues: ListType[str]
            setSelectionValues: ListType[str]
            setIntegerValues: ListType[str]
            setUserValues: ListType[str]
            unsetValues: bool

        labelId: str
        fieldModifications: ListType[FieldModification]
        removeLabel: bool
        kind: str

    labelModifications: ListType[LabelModification]
    kind: str
