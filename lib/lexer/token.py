from enum import Enum, auto

class TokenType(Enum):
    # KEYWORDS
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    TRUE = auto()
    FALSE = auto()
    STRUCT = auto()
    WHILE = auto()
    FOR = auto()
    FOREACH = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    IN = auto()
    VOID = auto()
    INT_TYPE = auto()
    FLOAT_TYPE = auto()
    STRING_TYPE = auto()
    BOOL_TYPE = auto()

    # LITERALS
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # OPERATORS
    EQUALS = auto()
    EQUAL_EQUAL = auto()
    NOT = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_OR_EQUAL = auto()
    GREATER = auto()
    GREATER_OR_EQUAL = auto()
    AND = auto()
    OR = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    POWER = auto()
    DIVIDE = auto()
    MODULE = auto()

    # PUNCTUATION
    COLON = auto()
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()

    # OTHERS
    COMMENT = auto()
    WHITESPACE = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int) -> None:
        self.type: TokenType = type_
        self.value: str = value
        self.line: int = line
        self.column: int = column

    def __repr__(self) -> str:
        return f"Token(type={self.type}, token='{self.value}', line={self.line}, col={self.column})"