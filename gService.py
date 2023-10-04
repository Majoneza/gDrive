from gCredentials import gCredentials
from itertools import chain, count
from googleapiclient.discovery import build, Resource
from abc import ABCMeta, abstractmethod
from utils import mergeDicts
from typing import Any, Generic, Self, Tuple, TypeVar, Type, Union
from types import TracebackType


T = TypeVar("T")


class gResource(Resource):
    def execute(self, *args: Any) -> Any:
        ...

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        ...

    def __getattribute__(self, __name: str) -> Self:
        ...


class gFields:
    def getFields(self, *fields: Any) -> Self:
        raise NotImplementedError()


FieldDictStr = dict[str, Union["FieldDictStr", None]]
FieldsDict = dict[str, Union["FieldsDict", None]] | dict[int, "FieldsDict"]


class gBaseData(Generic[T], gFields, metaclass=ABCMeta):
    def __init__(self, variableName: str, variableClass: Type[T]):
        self._variableName = variableName
        self._variableClass = variableClass
        self._setupVariables()

    def _setupVariables(self):
        for k, v in self._getVariableItemTypes().items():
            if hasattr(v, "__origin__") and v.__origin__ is list:
                typeArg = v.__args__[0]
                if typeArg.__base__ is not self._variableClass.__base__:
                    continue
                listdata = gListData(k, typeArg, self)
                setattr(self, k, listdata)
            elif v.__base__ is self._variableClass.__base__:
                objdata = gObjectData(k, v, self)
                setattr(self, k, objdata)

    def _getVariableItemTypes(self) -> dict[str, Any]:
        return self._variableClass.__annotations__

    def _hasVariableAttribute(self, name: str) -> bool:
        return name in self._variableClass.__annotations__

    def _hasAttributeUnchecked(self, name: str) -> bool:
        return name in self.__dict__

    def _getAttributeUnchecked(self, name: str) -> Any:
        return self.__dict__[name]

    def _getAttributeWrapper(self, name: str) -> Union["gBaseData[T]", None]:
        if name in self.__dict__:
            variable = self.__dict__[name]
            if type(variable) is gObjectData or type(variable) is gListData:
                return variable
        return None

    def getFieldNames(self) -> FieldDictStr:
        result: FieldDictStr = {}
        for k in self._getVariableItemTypes():
            variable = self._getAttributeWrapper(k)
            if variable is not None:
                result[k] = variable.getFieldNames()
                continue
            result[k] = None
        return result

    @abstractmethod
    def setData(self, data: Any) -> None:
        ...

    @abstractmethod
    def getFieldsDict(self, fields: FieldsDict) -> None:
        ...


class gBaseObjectData(Generic[T], gBaseData[T], metaclass=ABCMeta):
    def __getattr__(self, name: str) -> Any:
        if not self._hasVariableAttribute(name):
            raise AttributeError()
        self.getFieldsDict({name: None})
        if not self._hasAttributeUnchecked(name):
            raise RuntimeError(f"Unable to fetch requested resource: {name}")
        return self._getAttributeUnchecked(name)

    def setData(self, data: Any) -> None:
        if type(data) is not dict:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for object class: {self._variableClass.__name__}"
            )
        k: Any
        v: Any
        for k, v in data.items():
            variable = self._getAttributeWrapper(k)
            if variable is not None:
                variable.setData(v)
                continue
            setattr(self, k, v)

    def getFields(self, *fields: Any) -> Self:
        for field in fields:
            if not self._hasVariableAttribute(field):
                raise ValueError(f"Invalid field name: {field}")
        self.getFieldsDict(
            {k: v for k, v in self.getFieldNames().items() if k in fields}
        )
        return self


class gObjectData(Generic[T], gBaseObjectData[T]):
    def __init__(
        self, variableName: str, variableClass: Type[T], previous: gBaseData[Any]
    ):
        super().__init__(variableName, variableClass)
        self._previous = previous

    def getFieldsDict(self, fields: FieldsDict) -> None:
        self._previous.getFieldsDict({self._variableName: fields})


class gListItemData(Generic[T], gBaseObjectData[T]):
    def __init__(
        self,
        variableName: str,
        variableClass: Type[T],
        previous: "gListData[Any]",
        index: int,
    ):
        super().__init__(variableName, variableClass)
        self._previous = previous
        self._index = index

    def getFieldsDict(self, fields: FieldsDict) -> None:
        self._previous.getFieldsDict({self._index: fields})


class gListData(Generic[T], gBaseData[T]):
    def __init__(self, itemName: str, itemClass: Type[T], previous: gBaseData[Any]):
        super().__init__(itemName, itemClass)
        self._items: dict[int, gListItemData[T]] = {}
        self._previous = previous
        self._hasData = False

    def _getItem(self, index: int) -> gListItemData[T]:
        if index not in self._items:
            self._items[index] = gListItemData(
                self._variableName, self._variableClass, self, index
            )
        return self._items[index]

    def __len__(self) -> int:
        if not self._hasData:
            # FIXME: Field selection produces error
            self.getFieldsDict({})
        return len(self._items)

    def __getitem__(self, index: int) -> gListItemData[T]:
        if self._hasData and index >= len(self):
            raise IndexError()
        return self._getItem(index)

    def setData(self, data: Any) -> None:
        if type(data) is not list:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for list class: {self._variableClass.__name__}"
            )
        self._hasData = True
        v: Any
        for i, v in zip(count(), data):
            self._getItem(i).setData(v)

    def getFieldsDict(self, fields: FieldsDict) -> None:
        self._previous.getFieldsDict({self._variableName: fields})


class gData(Generic[T], gBaseObjectData[T]):
    def __init__(
        self,
        variableClass: Type[T],
        resource: gResource,
        kwargs: dict[str, Any] = {},
    ) -> None:
        super().__init__(variableClass.__name__, variableClass)
        self._resource = resource
        self._kwargs = kwargs

    @staticmethod
    def _convertFieldsToGoogleFormat(fields: FieldsDict) -> Any:
        if len(fields) == 0:
            return None
        if all(type(k) is int for k in fields):
            merged = mergeDicts(fields.values())
            return __class__._convertFieldsToGoogleFormat(merged)
        fieldsFormat: list[Any] = []
        for k, v in fields.items():
            if v is None:
                fieldsFormat.append(k)
            else:
                value = __class__._convertFieldsToGoogleFormat(v)
                fieldsFormat.append(f"{k}({value})")
        return ",".join(fieldsFormat)

    def getFieldsDict(self, fields: FieldsDict) -> None:
        print("... Fetching resources ...")
        googleFields = self._convertFieldsToGoogleFormat(fields)
        data = self._resource(**self._kwargs, fields=googleFields).execute()
        self.setData(data)


class gDataclassMetaclass(type):
    def __getattr__(self, name: str):
        return name


class gDataclass(gFields, metaclass=gDataclassMetaclass):
    def __init__(self, *args: Tuple[Any, Any], **kwargs: Any):
        super().__init__()
        for k, v in chain(args, kwargs.items()):
            if k not in self.__annotations__:
                raise ValueError(f"Invalid variable name: {k}")
            if type(v) is not self.__annotations__[k]:
                raise TypeError(f"Invalid type: {type(v).__name__}, of variable '{k}'")
            setattr(self, k, v)


class gSubService:
    _resource: gResource

    def __init__(self, resource: gResource):
        self._resource = resource


class gService:
    _service: gResource

    def __init__(self, credentials: gCredentials, serviceName: str, version: str):
        if not credentials.update():
            raise ValueError("Unable to acquire credentials")
        self._service = build(serviceName, version, credentials=credentials.get())

    def __enter__(self):
        self._service.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self._service.__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        self._service.close()
