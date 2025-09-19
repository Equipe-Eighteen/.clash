from lib.lexer.token import TokenType

KEYWORDS_TABLE = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elif": TokenType.ELIF,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "struct": TokenType.STRUCT,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "foreach": TokenType.FOREACH,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "in": TokenType.IN,
    "void": TokenType.VOID,
    "int": TokenType.INT_TYPE,
    "float": TokenType.FLOAT_TYPE,
    "string": TokenType.STRING_TYPE,
    "bool": TokenType.BOOL_TYPE
}
