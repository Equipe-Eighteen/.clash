from typing import Generator
import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType, Token

@pytest.mark.parametrize("code, expected_types", [
    ('print("Hello World");', [
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.STRING,
        TokenType.RPAREN,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('var x: str = "hello";', [
        TokenType.VAR,
        TokenType.IDENTIFIER,
        TokenType.COLON,
        TokenType.STRING_TYPE,
        TokenType.EQUALS,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('if (x == 10) return x;', [
        TokenType.IF,
        TokenType.LPAREN,
        TokenType.IDENTIFIER,
        TokenType.EQUAL_EQUAL,
        TokenType.INTEGER,
        TokenType.RPAREN,
        TokenType.RETURN,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ])
])
def test_lexer_tokenize(code: str, expected_types: list[TokenType]) -> None:
    lexer: Lexer = Lexer(code)
    tokens: Generator[Token, None, None] = lexer.tokenize()
    token_types = [t.type for t in tokens]
    assert token_types == expected_types
