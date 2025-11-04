from dataclasses import dataclass
from lib.parser.ast.base import Node

@dataclass(slots=True)
class TypeSpecifier(Node):
    pass

@dataclass(slots=True)
class BaseType(TypeSpecifier):
    name: str

@dataclass(slots=True)
class ListType(TypeSpecifier):
    element_type: TypeSpecifier
