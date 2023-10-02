import datetime
from typing import Any, Callable, Generic, Literal, TypeVar

T = TypeVar("T")


class QueryTerm:
    @staticmethod
    def Not(q: "BridgeTerm") -> "BridgeTerm":
        return BridgeTerm(f"not ({q})")

    def __call__(self, queryTerm: str) -> "AllOperators[Any]":
        return AllOperators(queryTerm)

    def __getattr__(self, __name: str) -> Any:
        vartype = self.__annotations__[__name]
        return vartype(__name)


class BridgeTerm:
    def __init__(self, value: str):
        self._value = value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return self.__str__()

    def __invert__(self) -> "BridgeTerm":
        return QueryTerm.Not(self)

    def __and__(self, q: "BridgeTerm") -> "BridgeTerm":
        return self.And(q)

    def __or__(self, q: "BridgeTerm") -> "BridgeTerm":
        return self.Or(q)

    def _and_or(self, op: Literal["and", "or"], *q: "BridgeTerm") -> "BridgeTerm":
        terms = map(lambda x: f"({x})", (self, *q))
        return BridgeTerm(f" {op} ".join(terms))

    def And(self, *q: "BridgeTerm") -> "BridgeTerm":
        return self._and_or("and", *q)

    def Or(self, *q: "BridgeTerm") -> "BridgeTerm":
        return self._and_or("or", *q)
    

class NotAValue:
    pass


class Operator:
    def __init__(self, queryTerm: str):
        self._queryTerm = queryTerm

    @staticmethod
    def _processValue(value: Any) -> str:
        if type(value) is str:
            return value
        elif type(value) is int:
            return str(value)
        elif type(value) is bool:
            return "true" if value else "false"
        elif type(value) is datetime.datetime:
            return value.isoformat()
        raise TypeError("Invalid value type: " + type(value).__name__)

    def __getattr__(self, operator: str) -> Any:
        pFunction = getattr(self, f"_{operator}")

        def func(value: Any = NotAValue):
            if value is NotAValue:
                return BridgeTerm(pFunction())
            pValue = Operator._processValue(value)
            return BridgeTerm(pFunction(pValue))

        return func


class ContainsOperator(Operator, Generic[T]):
    Contains: Callable[[T], BridgeTerm]

    def _Contains(self, value: str) -> str:
        return f"{self._queryTerm} contains '{value}'"


class IncludeOperator(Operator, Generic[T]):
    Include: Callable[[T], BridgeTerm]

    def _Include(self, value: str) -> str:
        return f"'{value}' in {self._queryTerm}"


class HasOperator(Operator, Generic[T]):
    Has: Callable[[T], BridgeTerm]

    def _Has(self, value: str) -> str:
        return f"{self._queryTerm} has {value}"


class EqOperator(Operator, Generic[T]):
    def __eq__(self, value: Any) -> bool:
        raise NotImplementedError()

    def __ne__(self, value: Any) -> bool:
        raise NotImplementedError()

    Eq: Callable[[T], BridgeTerm]

    Neq: Callable[[T], BridgeTerm]

    def _Eq(self, value: str) -> str:
        return f"{self._queryTerm} = '{value}'"

    def _Neq(self, value: str) -> str:
        return f"{self._queryTerm} != '{value}'"


class OrderOperator(Operator, Generic[T]):
    __gt__: Callable[[T], BridgeTerm]

    __ge__: Callable[[T], BridgeTerm]

    __lt__: Callable[[T], BridgeTerm]

    __le__: Callable[[T], BridgeTerm]

    Gt: Callable[[T], BridgeTerm]

    Geq: Callable[[T], BridgeTerm]

    Lt: Callable[[T], BridgeTerm]

    Leq: Callable[[T], BridgeTerm]

    def ___gt__(self, value: str) -> str:
        return self._Gt(value)

    def ___ge__(self, value: str) -> str:
        return self._Geq(value)

    def ___lt__(self, value: str) -> str:
        return self._Lt(value)

    def ___le__(self, value: str) -> str:
        return self._Leq(value)

    def _Gt(self, value: str) -> str:
        return f"{self._queryTerm} > '{value}'"

    def _Geq(self, value: str) -> str:
        return f"{self._queryTerm} >= '{value}'"

    def _Lt(self, value: str) -> str:
        return f"{self._queryTerm} < '{value}'"

    def _Leq(self, value: str) -> str:
        return f"{self._queryTerm} <= '{value}'"


class IsNullOperator(Operator, Generic[T]):
    IsNull: Callable[[], BridgeTerm]

    IsNotNull: Callable[[], BridgeTerm]

    def _IsNull(self) -> str:
        return f"{self._queryTerm} is null"

    def _IsNotNull(self) -> str:
        return f"{self._queryTerm} is not null"


class StartsWithOperator(Operator, Generic[T]):
    StartsWith: Callable[[T], BridgeTerm]

    def _StartsWith(self, value: str) -> str:
        return f"{self._queryTerm} starts with '{value}'"


class ContainsEqOperators(Generic[T], ContainsOperator[T], EqOperator[T]):
    pass


class EqOrderOperators(Generic[T], EqOperator[T], OrderOperator[T]):
    pass


class AllOperators(
    Generic[T],
    ContainsOperator[T],
    IncludeOperator[T],
    HasOperator[T],
    EqOperator[T],
    OrderOperator[T],
    IsNullOperator[T],
    StartsWithOperator[T],
):
    pass


class FileQueryTerm(QueryTerm):
    name: ContainsEqOperators[str]

    fullText: ContainsOperator[str]

    mimeType: ContainsEqOperators[str]

    modifiedTime: EqOrderOperators[datetime.datetime]

    viewedByMeTime: EqOrderOperators[datetime.datetime]

    trashed: EqOperator[bool]

    starred: EqOperator[bool]

    parents: IncludeOperator[str]

    owners: IncludeOperator[str]

    writers: IncludeOperator[str]

    readers: IncludeOperator[str]

    labels: IncludeOperator[str]

    sharedWithMe: EqOperator[bool]

    createdTime: EqOrderOperators[datetime.datetime]

    properties: HasOperator[str]

    appProperties: HasOperator[str]

    visibility: EqOperator[
        Literal[
            "anyoneCanFind",
            "anyoneWithLink",
            "domainCanFind",
            "domainWithLink",
            "limited",
        ]
    ]


class SharedDriveQueryTerm(QueryTerm):
    createdTime: EqOrderOperators[datetime.datetime]

    hidden: EqOperator[bool]

    memberCount: EqOrderOperators[int]

    name: ContainsEqOperators[str]

    organizerCount: EqOrderOperators[int]

    orgUnitId: EqOperator[str]
