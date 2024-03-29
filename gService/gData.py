from .gResource import gResource
from itertools import chain, count
from abc import abstractmethod
from .utils import mergeDicts, swapDict, isSubclassOrigin
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
    @classmethod
    def allFields(cls, depth: int = 0) -> Self:
        if depth == 0:
            return cls(*cls.__annotations__.keys())
        result = {}
        for k, v in cls.__annotations__.items():
            if isSubclassOrigin(v, gDataclass):
                result[k] = cast(gDataclass, v).allFields(depth - 1)
            else:
                result[k] = v()
        return cls(**result)

    @abstractmethod
    def getFields(self, *fields: Any) -> Self: ...

    def __init__(self, *args: Tuple[Any, Any] | Any, **kwargs: Any) -> None:
        super().__init__()
        if len(args) > 0:
            result: list[tuple[Any, Any]] = []
            swapped_annotations = swapDict(self.__annotations__)
            for arg in args:
                if isinstance(arg, gDataclass):
                    argType = type(arg)
                    if argType not in swapped_annotations:
                        raise ValueError(
                            f'Unable to find field with type "{argType.__name__}"'
                        )
                    name = swapped_annotations[argType]
                    result.append((name, arg))
                elif type(arg) is str:
                    if arg not in self.__annotations__:
                        raise ValueError(f'Unable to find field with name "{arg}"')
                    default_value = self.__annotations__[arg]()
                    result.append((arg, default_value))
                elif type(arg) is tuple:
                    result.append(cast(tuple[Any, Any], arg))
                else:
                    raise TypeError(f"Invalid argument type: {type(arg).__name__}")
            args = tuple(result)
        for k, v in chain(args, kwargs.items()):
            if k not in self.__annotations__:
                raise ValueError(f"Invalid variable name: {k}")
            if type(v) is not self.__annotations__[k] and type(v) is not get_origin(
                self.__annotations__[k]
            ):
                raise TypeError(
                    f"Invalid type: {type(v).__name__}, of variable '{k}', required type: {self.__annotations__[k].__name__}"
                )
            setattr(self, k, v)


T = TypeVar("T", bound=gDataclass)
K = TypeVar("K", str, int)
V = TypeVar("V", bound=gDataclass)


class gList(Generic[T]):
    @abstractmethod
    def __contains__(self, obj: T) -> bool: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __getitem__(self, index: int) -> T: ...

    @abstractmethod
    def getFields(self, *fields: Any) -> Self: ...


class gDict(Generic[K, V]):
    @abstractmethod
    def __contains__(self, key: K) -> bool: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __getitem__(self, key: K) -> V: ...

    @abstractmethod
    def keys(self) -> list[K]: ...

    @abstractmethod
    def values(self) -> list[V]: ...

    @abstractmethod
    def items(self) -> list[tuple[K, V]]: ...

    @abstractmethod
    def getFields(self, *fields: Any) -> Self: ...


FieldDictStr = dict[str, Union["FieldsDict", None]]
FieldDictInt = dict[int, "FieldsDict"]
FieldDictNone = dict[None, "FieldsDict"]
FieldsDict = FieldDictStr | FieldDictInt | FieldDictNone


class gBaseData(Generic[T]):
    @abstractmethod
    def setData(self, data: Any) -> None: ...

    @abstractmethod
    def getFieldsDict(self, fields: FieldsDict | None) -> None: ...

    def __init__(self, variableName: str, variableClass: Type[T]) -> None:
        super().__init__()
        self._variableName = variableName
        self._variableClass = variableClass

    def _getVariableItemTypes(self) -> dict[str, Any]:
        return self._variableClass.__annotations__

    def _hasVariableAttribute(self, name: str) -> bool:
        return name in self._variableClass.__annotations__

    def _hasAttribute(self, name: str) -> bool:
        return name in self.__dict__

    def _getAttributeUnchecked(self, name: str) -> Any:
        return self.__dict__[name]

    def _getAttributeWrapperSafe(self, name: str) -> Union["gBaseData[T]", None]:
        if self._hasAttribute(name):
            variable = self._getAttributeUnchecked(name)
            if isinstance(variable, gBaseData):
                return cast(gBaseData[Any], variable)
        return None

    def _createDataclassFromFields(self, fields: Tuple[Any, ...]) -> gDataclass:
        if len(fields) == 0:
            return self._variableClass.allFields()
        return self._variableClass(*fields)

    def getMissingFields(self, comparison: gDataclass) -> FieldsDict:
        result: FieldDictStr = {}
        for field in comparison.__dict__:
            if not self._hasVariableAttribute(field):
                raise ValueError(
                    f'Invalid field name "{field}" for class "{self._variableClass.__name__}"'
                )
            value = getattr(comparison, field)
            if isinstance(value, gDataclass):
                gBaseDataVariable = self._getAttributeWrapperSafe(field)
                if gBaseDataVariable is None:
                    raise ValueError(
                        f'Unable to find attribute with name "{field}" for class "{self._variableClass.__name__}"'
                    )
                missingFields = gBaseDataVariable.getMissingFields(value)
                if len(missingFields) > 0:
                    result[field] = missingFields
            elif not self._hasAttribute(field):
                result[field] = None
        return result


class gBaseObjectData(Generic[T], gBaseData[T], gDataclass):
    def __init__(self, variableName: str, variableClass: type[T]) -> None:
        super().__init__(variableName, variableClass)
        self._setupVariables()

    def __repr__(self) -> str:
        return (
            self._variableClass.__qualname__
            + "("
            + ", ".join(
                [
                    k + "=" + repr(self._getAttributeUnchecked(k))
                    for k in self._getVariableItemTypes()
                    if self._hasAttribute(k)
                ]
            )
            + ")"
        )

    def __getattr__(self, name: str) -> Any:
        if not self._hasVariableAttribute(name):
            raise AttributeError()
        self.getFieldsDict({name: None})
        if not self._hasAttribute(name):
            raise RuntimeError(f"Unable to fetch requested resource: {name}")
        return self._getAttributeUnchecked(name)

    def _setupVariables(self) -> None:
        for k, v in self._getVariableItemTypes().items():
            origin = get_origin(v)
            if origin is not None:
                if origin is gList:
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
        missingFields = self.getMissingFields(self._createDataclassFromFields(fields))
        if len(missingFields) > 0:
            self.getFieldsDict(missingFields)
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
        key: K | None,
    ) -> None:
        super().__init__(variableName, variableClass)
        self._previous = previous
        self._key = key

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        if fields is None:
            raise ValueError("Invalid fields format")
        self._previous.getFieldsDict(cast(FieldsDict, {self._key: fields}))


class gBaseDictData(Generic[K, V], gBaseData[V]):
    @abstractmethod
    def _setData(self, data: Any) -> None: ...

    def __init__(
        self, valueName: str, valueClass: Type[V], previous: gBaseData[Any]
    ) -> None:
        super().__init__(valueName, valueClass)
        self._dummy_item = gDictItemData(
            self._variableName, self._variableClass, self, None
        )
        self._items: dict[K, gDictItemData[K, V]] = {}
        self._previous = previous
        self._hasData = False

    def __len__(self) -> int:
        if not self._hasData:
            self.getFieldsDict(None)
        return len(self._items)

    def __getitem__(self, key: K) -> gDictItemData[K, V]:
        if self._hasData and key not in self._items:
            raise IndexError()
        return self._getItem(key)

    def _getItem(self, key: K) -> gDictItemData[K, V]:
        if key not in self._items:
            self._items[key] = gDictItemData(
                self._variableName, self._variableClass, self, key
            )
        return self._items[key]

    def setData(self, data: Any) -> None:
        self._hasData = True
        self._setData(data)

    def getFieldsDict(self, fields: FieldsDict | None) -> None:
        self._previous.getFieldsDict({self._variableName: fields})

    def getFields(self, *fields: Any) -> Self:
        self._dummy_item.getFields(*fields)
        return self


class gListData(Generic[T], gBaseDictData[int, T]):
    def __repr__(self) -> str:
        return (
            self._variableClass.__qualname__
            + "["
            + ", ".join([repr(v) for v in self._items.values()])
            + "]"
        )

    def __contains__(self, obj: T) -> bool:
        if not self._hasData:
            self.getFieldsDict(None)
        return obj in self._items.values()

    def _setData(self, data: Any) -> None:
        if type(data) is not list:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for list class: {self._variableClass.__name__}"
            )
        for i, v in zip(count(), cast(list[Any], data)):
            self._getItem(i).setData(v)


class gDictData(Generic[K, V], gBaseDictData[K, V]):
    def __repr__(self) -> str:
        return (
            self._variableClass.__qualname__
            + "{"
            + ", ".join([repr(k) + ": " + repr(v) for k, v in self._items.items()])
            + "}"
        )

    def __contains__(self, obj: K) -> bool:
        if not self._hasData:
            self.getFieldsDict(None)
        return obj in self._items

    def _setData(self, data: Any) -> None:
        if type(data) is not dict:
            raise RuntimeError(
                f"Received invalid data type {type(data).__name__} for dict class: {self._variableClass.__name__}"
            )
        for k, v in cast(dict[Any, Any], data):
            self._getItem(k).setData(v)

    def keys(self) -> list[K]:
        if not self._hasData:
            self.getFieldsDict(None)
        return list(self._items.keys())

    def values(self) -> list[gDictItemData[K, V]]:
        if not self._hasData:
            self.getFieldsDict(None)
        return list(self._items.values())

    def items(self) -> list[tuple[K, gDictItemData[K, V]]]:
        return list(zip(self.keys(), self.values()))


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
