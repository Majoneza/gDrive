import inspect
import os
from typing import Any, Callable, Dict, List, Iterable, Optional, TypeVar, Type

T = TypeVar("T")


def splitPath(path: str):
    return os.path.normpath(path).split(os.sep)


class Object(object):
    pass


def list2object(instance: List[Any], obj: Type[Any] = Object) -> List[Any]:
    result: List[Any] = []
    for v in instance:
        if type(v) is dict:
            v = dict2object(v, obj)
        elif type(v) is list:
            v = list2object(v, obj)
        result.append(v)
    return result


def dict2object(instance: Dict[Any, Any], obj: Type[T] = Object) -> T:
    result = obj()
    for k, v in instance.items():
        if type(v) is dict:
            v = dict2object(v, obj)
        elif type(v) is list:
            v = list2object(v, obj)
        setattr(result, k, v)
    return result


def getFunctionVariablesFast(
    function: Callable[..., Any], local_variables: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        k: v
        for k, v in local_variables.items()
        if k in function.__code__.co_varnames and v is not None
    }


def getFunctionName(depth: int = 1):
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


def first(it: Iterable[T]) -> T:
    return next(iter(it))


K = TypeVar("K")
V = TypeVar("V")


def mergeDicts(dicts: Iterable[dict[K, V]]) -> dict[K, V]:
    return first(dicts)
