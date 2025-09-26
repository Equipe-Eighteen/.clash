from enum import Enum

class TokenType(Enum):
    # Palavras-chave
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    TRUE = "TRUE"
    FALSE = "FALSE"
    STRUCT = "STRUCT"
    WHILE = "WHILE"
    FOR = "FOR"
    FOREACH = "FOREACH"
    RETURN = "RETURN"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    IN = "IN"
    VOID = "VOID"
    INT_TYPE = "INT_TYPE"
    FLOAT_TYPE = "FLOAT_TYPE"
    STRING_TYPE = "STRING_TYPE"
    BOOL_TYPE = "BOOL_TYPE"

    # Literais
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"

    # Operadores
    EQUALS = "="
    EQUAL_EQUAL = "=="
    NOT = "!"
    NOT_EQUAL = "!="
    LESS = "<"
    LESS_OR_EQUAL = "<="
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    AND = "&&"
    OR = "||"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POWER = "**"
    DIVIDE = "/"
    MODULE = "%"

    # Pontuação
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    DOT = "."

    # Outros
    EOF = "EOF"

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type: TokenType = type_
        self.value: str = value
        self.line: int = line
        self.column: int = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"