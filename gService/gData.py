from .gResource import gResource
from itertools import chain, count
from abc import abstractmethod
from .utils import mergeDicts
from typing import (
    Any,
    cast,
    Generic,
    Iterable,
    Self,
    Tuple,
    TypeVar,
    Type,
    Union,
    get_origin,
    get_args,
)


class gDataclassMetaclass(type):
    def __getattr__(self, name: str) -> str:
        return name


class gDataclass(metaclass=gDataclassMetaclass):
    def getFields(self, *fields: Any) -> Self:
        raise NotImplementedError()

    def __init__(self, *args: Tuple[Any, Any], **kwargs: Any) -> None:
        super().__init__()
        for k, v in chain(args, kwargs.items()):
            if k not in self.__annotations__:
                raise ValueError(f"Invalid variable name: {k}")
            if type(v) is not self.__annotations__[k]:
                raise TypeError(f"Invalid type: {type(v).__name__}, of variable '{k}'")
            setattr(self, k, v)


T = TypeVar("T", bound=gDataclass)
K = TypeVar("K", str, int)
V = TypeVar("V", bound=gDataclass)


class gList(gDataclass, Generic[T]):
    @abstractmethod
    def __contains__(self, obj: object) -> bool:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        ...


class gDict(gDataclass, Generic[K, V]):
    @abstractmethod
    def __contains__(self, key: object) -> bool:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __getitem__(self, key: K) -> V:
        ...

    @abstractmethod
    def keys(self) -> list[K]:
        ...

    @abstractmethod
    def values(self) -> list[V]:
        ...

    def get(self, key: K, default: V) -> V:
        if key not in self:
            return default
        return self[key]

    def items(self) -> list[tuple[K, V]]:
        return list(zip(self.keys(), self.values()))


FieldDictStr = dict[str, Union["FieldsDict", None]]
FieldDictInt = dict[int, "FieldsDict"]
FieldDictNone = dict[None, "FieldsDict"]
FieldsDict = FieldDictStr | FieldDictInt | FieldDictNone


class gBaseData(Generic[T]):
    @abstractmethod
    def setData(self, data: Any) -> None:
        ...

    @abstractmethod
    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        ...

    def __init__(self, variableName: str, variableClass: Type[T]) -> None:
        super().__init__()
        self._variableName = variableName
        self._variableClass = variableClass
        self._setupVariables()

    def _setupVariables(self) -> None:
        for k, v in self._getVariableItemTypes().items():
            origin = get_origin(v)
            if origin is not None:
                if origin is gList or origin is gDict:
                    itemType = get_args(v)[0]
                    if not issubclass(itemType, gDataclass):
                        continue
                    data = gListData(k, itemType, self)
                    setattr(self, k, data)
                elif origin is gDict:
                    valueType = get_args(v)[1]
                    if not issubclass(valueType, gDataclass):
                        continue
                    data = cast(
                        gDictData[Any, gDataclass], gDictData(k, valueType, self)
                    )
                    setattr(self, k, data)
                elif issubclass(origin, gDataclass):
                    objdata = gObjectData(k, v, self)
                    setattr(self, k, objdata)
            elif issubclass(v, gDataclass):
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

    def _getAttributeWrapperSafe(self, name: str) -> Union["gBaseData[T]", None]:
        if name in self.__dict__:
            variable = self.__dict__[name]
            if isinstance(variable, gBaseData):
                return cast(gBaseData[Any], variable)
        return None

    def _getMissingFields(self, fields: Iterable[Any]) -> list[Any]:
        for field in fields:
            if not self._hasVariableAttribute(field):
                raise ValueError(f"Invalid field name: {field}")
        return [field for field in fields if not self._hasAttributeUnchecked(field)]

    def getFieldNames(self, fields: Iterable[str] | None = None) -> FieldsDict:
        result: FieldDictStr = {}
        if fields is None:
            fields = self._getVariableItemTypes().keys()
        for field in fields:
            variable = self._getAttributeWrapperSafe(field)
            if variable is not None:
                result[field] = variable.getFieldNames()
                continue
            result[field] = None
        return result


class gBaseObjectData(Generic[T], gBaseData[T], gDataclass):
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
        for k, v in cast(dict[Any, Any], data).items():
            variable = self._getAttributeWrapperSafe(k)
            if variable is not None:
                variable.setData(v)
                continue
            setattr(self, k, v)

    def getFields(self, *fields: Any) -> Self:
        missingFields = self._getMissingFields(fields)
        if len(missingFields) != 0:
            self.getFieldsDict(self.getFieldNames(missingFields))
        return self


class gObjectData(Generic[T], gBaseObjectData[T]):
    def __init__(
        self, variableName: str, variableClass: Type[T], previous: gBaseData[Any]
    ) -> None:
        super().__init__(variableName, variableClass)
        self._previous = previous

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        self._previous.getFieldsDict({self._variableName: fields})


class gDictItemData(Generic[K, V], gBaseObjectData[V]):
    def __init__(
        self,
        variableName: str,
        variableClass: Type[V],
        previous: "gBaseDictData[K, V]",
        key: K,
    ) -> None:
        super().__init__(variableName, variableClass)
        self._previous = previous
        self._key = key

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        if fields is None:
            raise ValueError("Invalid fields format")
        self._previous.getFieldsDict(cast(FieldsDict, {self._key: fields}))


class gBaseDictData(Generic[K, V], gBaseData[V], gDict[K, gDictItemData[K, V]]):
    @abstractmethod
    def _setData(self, data: Any) -> None:
        ...

    def __init__(
        self, valueName: str, valueClass: Type[V], previous: gBaseData[Any]
    ) -> None:
        super().__init__(valueName, valueClass)
        self._items: dict[K, gDictItemData[K, V]] = {}
        self._previous = previous
        self._hasData = False

    def __contains__(self, obj: object) -> bool:
        if not isinstance(obj, self._variableClass):
            return False
        if not self._hasData:
            self.getFieldsDict(self.getFieldNames())
        return obj in self._items.values()

    def __len__(self) -> int:
        if not self._hasData:
            self.getFieldsDict(None)
        return len(self._items)

    def keys(self) -> list[K]:
        return list(self._items.keys())

    def values(self) -> list[gDictItemData[K, V]]:
        return list(self._items.values())

    def setData(self, data: Any) -> None:
        self._hasData = True
        self._setData(data)

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        self._previous.getFieldsDict({self._variableName: fields})

    def getFields(self, *fields: Any) -> Self:
        missingFields = self._getMissingFields(fields)
        if len(missingFields) != 0:
            self.getFieldsDict({None: self.getFieldNames(missingFields)})
        return self


class gListData(Generic[T], gBaseDictData[int, T]):
    def _getItem(self, index: int) -> gDictItemData[int, T]:
        if index not in self._items:
            self._items[index] = gDictItemData(
                self._variableName, self._variableClass, self, index
            )
        return self._items[index]

    def __getitem__(self, index: int) -> gDictItemData[int, T]:
        if self._hasData and index >= len(self):
            raise IndexError()
        return self._getItem(index)

    def _setData(self, data: Any) -> None:
        if type(data) is not list:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for list class: {self._variableClass.__name__}"
            )
        for i, v in zip(count(), cast(list[Any], data)):
            self._getItem(i).setData(v)


class gDictData(Generic[K, V], gBaseDictData[K, V]):
    def _getItem(self, key: K) -> gDictItemData[K, V]:
        if not self._hasData:
            self.getFieldsDict(None)
        if key not in self._items:
            raise KeyError()
        return self._items[key]

    def __getitem__(self, key: K) -> gDictItemData[K, V]:
        return self._getItem(key)

    def _setData(self, data: Any) -> None:
        if type(data) is not dict:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for dict class: {self._variableClass.__name__}"
            )
        for k, v in cast(dict[Any, Any], data):
            self._getItem(k).setData(v)


class gData(Generic[T], gBaseObjectData[T]):
    def __init__(
        self,
        variableClass: Type[T],
        resource: gResource,
        kwargs: dict[str, Any] = {},
        executeOnlyOnce: bool = False,
    ) -> None:
        super().__init__(variableClass.__name__, variableClass)
        self._resource = resource
        self._kwargs = kwargs
        self._executeOnlyOnce = executeOnlyOnce
        self._executed = False

    @staticmethod
    def _convertFieldsToGoogleFormat(fields: FieldsDict) -> Any:
        if all(type(k) is int for k in fields):
            merged = mergeDicts(cast(Iterable[FieldDictInt], fields.values()))
            return __class__._convertFieldsToGoogleFormat(merged)
        fieldsFormat: list[Any] = []
        for k, v in fields.items():
            if v is None:
                fieldsFormat.append(k)
            else:
                value = __class__._convertFieldsToGoogleFormat(v)
                if k is None:
                    fieldsFormat.append(value)
                else:
                    fieldsFormat.append(f"{k}({value})")
        return ",".join(fieldsFormat)

    def _execute(self, fields: str) -> None:
        if self._executeOnlyOnce and self._executed:
            raise RuntimeError("This resource cannot be called twice")
        self._executed = True
        data = self._resource(**self._kwargs, fields=fields).execute()
        self.setData(data)

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        if fields is not None:
            googleFields = self._convertFieldsToGoogleFormat(fields)
        else:
            googleFields = ""
        self._execute(googleFields)

    def execute(self) -> None:
        self._execute("")


def executeGDataResource(dataclass: gDataclass) -> None:
    if type(dataclass) is not gData:
        raise TypeError(
            f"Invalid given type: {type(dataclass).__name__}, is it top level?"
        )
    dataclass.execute()
