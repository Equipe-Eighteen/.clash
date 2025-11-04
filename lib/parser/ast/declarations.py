from typing import Optional
from dataclasses import dataclass, field
from lib.parser.ast.base import Node
from lib.parser.ast.statements import Statement, BlockStmt
from lib.parser.ast.expressions import Expression, Identifier
from lib.parser.ast.types import TypeSpecifier

@dataclass(slots=True)
class Declaration(Node):
    pass

@dataclass(slots=True)
class VarDecl(Statement, Declaration):
    name: Identifier
    type_spec: TypeSpecifier
    initializer: Optional[Expression] = None

@dataclass(slots=True)
class FieldDecl(Node):
    name: Identifier
    type_spec: TypeSpecifier

@dataclass(slots=True)
class StructDecl(Declaration):
    name: Identifier
    fields: list[FieldDecl] = field(default_factory=list[FieldDecl])

@dataclass(slots=True)
class ParamDecl(Node):
    name: Identifier
    type_spec: TypeSpecifier

@dataclass(slots=True)
class FuncDecl(Declaration):
    name: Identifier
    return_type: TypeSpecifier
    body: BlockStmt
    params: list[ParamDecl] = field(default_factory=list[ParamDecl])
