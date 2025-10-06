from lib.lexer.token import TokenType

OPERATORS_TABLE: dict[str, TokenType]= {
    "=": TokenType.EQUALS,
    "==": TokenType.EQUAL_EQUAL,
    "!": TokenType.NOT,
    "!=": TokenType.NOT_EQUAL,
    "<": TokenType.LESS,
    "<=": TokenType.LESS_OR_EQUAL,
    ">": TokenType.GREATER,
    ">=": TokenType.GREATER_OR_EQUAL,
    "&&": TokenType.AND,
    "||": TokenType.OR,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "**": TokenType.POWER,
    "/": TokenType.DIVIDE,
    "%": TokenType.MODULE,
}
