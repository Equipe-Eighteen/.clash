from dataclasses import dataclass, field
from lib.parser.ast.base import Node

@dataclass(slots=True)
class Program(Node):
    declarations: list[Node] = field(default_factory=list[Node])
