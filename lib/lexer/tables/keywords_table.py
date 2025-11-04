from lib.lexer.token import TokenType

KEYWORDS_TABLE: dict[str, TokenType] = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elif": TokenType.ELIF,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "struct": TokenType.STRUCT,
    "new": TokenType.NEW,
    "loop": TokenType.LOOP,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "in": TokenType.IN,
    "void": TokenType.VOID,
    "int": TokenType.INT_TYPE,
    "float": TokenType.FLOAT_TYPE,
    "str": TokenType.STRING_TYPE,
    "bool": TokenType.BOOL_TYPE,
    "list": TokenType.LIST_TYPE,
    "var": TokenType.VAR,
    "func": TokenType.FUNC,
}
