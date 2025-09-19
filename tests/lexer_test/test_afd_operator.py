import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType

@pytest.mark.parametrize("text, expected_type", [
    ("+", TokenType.PLUS),
    ("-", TokenType.MINUS),
    ("*", TokenType.MULTIPLY),
    ("/", TokenType.DIVIDE),
    ("**", TokenType.POWER),
    ("==", TokenType.EQUAL_EQUAL),
    ("=", TokenType.EQUALS),
    ("!=", TokenType.NOT_EQUAL),
    ("<=", TokenType.LESS_OR_EQUAL),
    ("<", TokenType.LESS),
    (">=", TokenType.GREATER_OR_EQUAL),
    (">", TokenType.GREATER),
    ("&&", TokenType.AND),
    ("||", TokenType.OR),
    (";", TokenType.SEMICOLON),
    ("(", TokenType.LPAREN),
    (")", TokenType.RPAREN),
    ("{", TokenType.LBRACE),
    ("}", TokenType.RBRACE),
    ("[", TokenType.LBRACKET),
    ("]", TokenType.RBRACKET),
    (",", TokenType.COMMA),
    (".", TokenType.DOT),
])
def test_afd_operator(text, expected_type):
    lexer = Lexer(text)
    token = lexer.afd_operator()
    assert token.type == expected_type
    assert token.value == text
