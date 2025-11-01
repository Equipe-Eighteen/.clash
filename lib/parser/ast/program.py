from dataclasses import dataclass, field
from lib.parser.ast.base import Node
from lib.parser.ast.declarations import Declaration

@dataclass(slots=True)
class Program(Node):
    declarations: list[Declaration] = field(default_factory=list[Declaration])
