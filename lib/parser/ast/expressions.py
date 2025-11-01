from dataclasses import dataclass, field
from lib.parser.ast.base import Node

@dataclass(slots=True)
class Expression(Node):
    pass

@dataclass(slots=True)
class Identifier(Expression):
    name: str

@dataclass(slots=True)
class IntLiteral(Expression):
    value: int

@dataclass(slots=True)
class FloatLiteral(Expression):
    value: float

@dataclass(slots=True)
class StringLiteral(Expression):
    value: str

@dataclass(slots=True)
class BoolLiteral(Expression):
    value: bool

@dataclass(slots=True)
class LiteralList(Expression):
    elements: list[Expression] = field(default_factory=list[Expression])

@dataclass(slots=True)
class AssignExpr(Expression):
    target: Expression
    value: Expression

@dataclass(slots=True)
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

@dataclass(slots=True)
class UnaryOp(Expression):
    op: str
    right: Expression

@dataclass(slots=True)
class FuncCall(Expression):
    callee: Expression
    arguments: list[Expression] = field(default_factory=list[Expression] )

@dataclass(slots=True)
class MemberAccess(Expression):
    obj: Expression
    member: Identifier

@dataclass(slots=True)
class ArrayAccess(Expression):
    array: Expression
    index: Expression
