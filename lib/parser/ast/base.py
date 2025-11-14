from dataclasses import dataclass, field

@dataclass(slots=True)
class Node:
    line: int = field(default=0, kw_only=True)
    col: int = field(default=0, kw_only=True)
