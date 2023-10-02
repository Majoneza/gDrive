import inspect
import os
from typing import Any, Callable, Dict, List, Optional, TypeVar, Type

T = TypeVar("T")


def splitPath(path: str):
    return os.path.normpath(path).split(os.sep)


class Object(object):
    pass


def list2object(obj: List[Any]) -> List[Any]:
    result: List[Any] = []
    for v in obj:
        if type(v) is dict:
            v = dict2object(v)
        elif type(v) is list:
            v = list2object(v)
        result.append(v)
    return result


def dict2object(obj: Dict[Any, Any]) -> Any:
    result = Object()
    for k, v in obj.items():
        if type(v) is dict:
            v = dict2object(v)
        elif type(v) is list:
            v = list2object(v)
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
    keys = list(instance.__annotations__.keys())
    for k in keys:
        v = getattr(instance, k)
        if v is not None:
            setattr(obj, k, v)
    return obj
