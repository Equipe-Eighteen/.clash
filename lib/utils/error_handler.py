from typing import Optional, Any

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int, char: str) -> None:
        super().__init__(f"Lexical error at line {line}, column {column}: {message} -> '{char}'")


class ParserError(Exception):
    def __init__(self, message: str, line: int = 1, column: int = 1, token: Optional[Any] = None) -> None:
        token_val = getattr(token, "value", None)
        token_repr = f" -> '{token_val}'" if token_val is not None else ""
        super().__init__(f"Parser error at line {line}, column {column}: {message}{token_repr}")


class SemanticError(Exception):
    def __init__(self, message: str, line: int = 1, column: int = 1, node: Optional[Any] = None) -> None:
        node_val = None
        if node is not None:
            for attr in ("name", "value", "identifier", "symbol"):
                node_val = getattr(node, attr, None)
                if node_val is not None:
                    break
        node_repr = f" -> '{node_val}'" if node_val is not None else ""
        super().__init__(f"Semantic error at line {line}, column {column}: {message}{node_repr}")


class CodegenError(Exception):
    def __init__(self, message: str, node: Optional[Any] = None) -> None:
        node_val = None
        if node is not None:
            for attr in ("name", "value"):
                node_val = getattr(node, attr, None)
                if node_val is not None:
                    break
        node_repr = f" -> '{node_val}'" if node_val is not None else ""
        super().__init__(f"Codegen error: {message}{node_repr}")
