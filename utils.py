import inspect
import os
from typing import Any, Callable, cast, Dict, List, Iterable, Optional, TypeVar, Type

T = TypeVar("T")


def splitPath(path: str) -> list[str]:
    return os.path.normpath(path).split(os.sep)


class Object(object):
    pass


def dictsIterable2objectList(
    instance: Iterable[Any], obj: Type[Any] = Object
) -> List[Any]:
    result: List[Any] = []
    for v in instance:
        if type(v) is dict:
            v = dict2object(cast(dict[Any, Any], v), obj)
        elif type(v) is list or type(v) is tuple:
            v = dictsIterable2objectList(cast(Iterable[Any], v), obj)
        result.append(v)
    return result


def dict2object(instance: Dict[Any, Any], obj: Type[T] = Object) -> T:
    result = obj()
    for k, v in instance.items():
        if type(v) is dict:
            v = dict2object(cast(dict[Any, Any], v), obj)
        elif type(v) is list or type(v) is tuple:
            v = dictsIterable2objectList(cast(Iterable[Any], v), obj)
        setattr(result, k, v)
    return result


def objectsIterable2dictsList(
    lst: Iterable[object], base: Type[Any] = Object
) -> List[Any]:
    result: list[Any] = []
    for v in lst:
        if type(v).__base__ is base:
            v = object2dict(v, base)
        elif type(v) is list or type(v) is tuple:
            v = objectsIterable2dictsList(cast(Iterable[Any], v), base)
        result.append(v)
    return result


def object2dict(obj: object, base: Type[Any] = Object) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for k, v in obj.__dict__.items():
        if type(v).__base__ is base:
            v = object2dict(v, base)
        elif type(v) is list or type(v) is tuple:
            v = objectsIterable2dictsList(cast(Iterable[Any], v), base)
        result[k] = v
    return result


def getFunctionVariablesFast(
    function: Callable[..., Any], local_variables: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        k: v
        for k, v in local_variables.items()
        if k in function.__code__.co_varnames and v is not None
    }


def getFunctionName(depth: int = 1) -> str:
    return inspect.stack()[depth].function


def getFunctionRef(module: object, depth: int = 1) -> Callable[..., Any]:
    name = getFunctionName(depth + 1)
    return getattr(module, name)


def getFunctionReturnType(module: object, depth: int = 1) -> Any:
    ref = getFunctionRef(module, depth + 1)
    return ref.__annotations__["return"]


def getFunctionVariables(depth: int = 1) -> Dict[str, Any]:
    frame = inspect.stack()[depth].frame
    code = frame.f_code
    return {
        k: v
        for k, v in frame.f_locals.items()
        if k in code.co_varnames and v is not None
    }


def getFunctionVariablesSelf(depth: int = 1) -> Dict[str, Any]:
    return {k: v for k, v in getFunctionVariables(depth + 1).items() if k != "self"}


def optional(cls: Type[T]) -> Type[T]:
    annotations = {}
    for k, v in cls.__annotations__.items():
        annotations[k] = Optional[v]
        setattr(cls, k, None)
    cls.__annotations__ = annotations
    return cls


def removeNones(instance: object) -> Object:
    obj = Object()
    for k in instance.__dict__.keys():
        v = getattr(instance, k)
        if v is not None:
            setattr(obj, k, v)
    return obj


def resolveVariableName(cls: Type[T]) -> Type[T]:
    for variableName in cls.__annotations__:
        setattr(cls, variableName, variableName)
    return cls


def resolveVariableInheritancePath(
    cls: Type[T], previous: str | None = None
) -> Type[T]:
    if previous is None:
        previous = cls.__name__
    for variableName, variableType in cls.__annotations__.items():
        if variableType.__base__ is cls.__base__:
            value = resolveVariableInheritancePath(
                variableType, previous + "." + variableType.__name__
            )
            setattr(cls, variableName, value)
        else:
            setattr(cls, variableName, previous + "." + variableName)
    return cls


def mergeDicts(dicts: Iterable[dict[Any, Any]]) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for d in dicts:
        for k, v in d.items():
            if type(v) is dict:
                if k not in result:
                    result[k] = []
                result[k].append(v)
            else:
                if k in result:
                    raise RuntimeError(f"Unable to merge dicts, failed on key: {k}")
                result[k] = v
    for k, v in result.items():
        if type(v) is list:
            result[k] = mergeDicts(cast(list[Any], v))
    return result
