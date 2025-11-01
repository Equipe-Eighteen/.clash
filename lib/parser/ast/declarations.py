from typing import Optional
from dataclasses import dataclass, field
from lib.parser.ast.base import Node
from lib.parser.ast.expressions import Expression, Identifier
from lib.parser.ast.statements import BlockStmt, Statement

@dataclass(slots=True)
class Declaration(Node):
    pass

@dataclass(slots=True)
class TypeSpecifier(Node):
    base_type_name: str
    array_level: int = 0

@dataclass(slots=True)
class ParamDecl(Node):
    type_spec: TypeSpecifier
    name: Identifier

@dataclass(slots=True)
class InitDeclarator(Node):
    name: Identifier
    initializer: Optional[Expression] = None

@dataclass(slots=True)
class VarDecl(Statement, Declaration):
    type_spec: TypeSpecifier
    declarators: list[InitDeclarator]

@dataclass(slots=True)
class StructDecl(Declaration):
    name: Identifier
    fields: Optional[list[VarDecl]] = None

@dataclass(slots=True)
class FuncDecl(Declaration):
    return_type: TypeSpecifier
    name: Identifier
    body: BlockStmt
    params: list[ParamDecl] = field(default_factory=list[ParamDecl])

@dataclass(slots=True)
class MethodDecl(Declaration):
    return_type: TypeSpecifier
    receiver: ParamDecl
    name: Identifier
    body: BlockStmt
    params: list[ParamDecl] = field(default_factory=list[ParamDecl])