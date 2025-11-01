from typing import Optional
from dataclasses import dataclass, field
from lib.parser.ast.base import Node
from lib.parser.ast.expressions import Expression

@dataclass(slots=True)
class Statement(Node):
    pass

@dataclass(slots=True)
class BlockStmt(Statement):
    statements: list[Statement] = field(default_factory=list[Statement])

@dataclass(slots=True)
class ExpressionStmt(Statement):
    expression: Optional[Expression]

@dataclass(slots=True)
class ElifBranch(Node):
    condition: Expression
    body: BlockStmt

@dataclass(slots=True)
class IfStmt(Statement):
    condition: Expression
    then_branch: BlockStmt
    elif_branches: list[ElifBranch] = field(default_factory=list[ElifBranch])
    else_branch: Optional[BlockStmt] = None

@dataclass(slots=True)
class LoopStmt(Statement):
    condition: Expression
    body: BlockStmt

@dataclass(slots=True)
class ReturnStmt(Statement):
    value: Optional[Expression] = None

@dataclass(slots=True)
class BreakStmt(Statement):
    pass

@dataclass(slots=True)
class ContinueStmt(Statement):
    pass