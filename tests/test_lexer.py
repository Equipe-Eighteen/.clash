from typing import Generator
import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType, Token

@pytest.mark.parametrize("code, expected_types", [
    ('print("Hello World");', [
        TokenType.PRINT,
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
        TokenType.STR_TYPE,
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


@pytest.mark.parametrize("code, expected_types", [
    ('var greet:str="hi";return greet;', [
        TokenType.VAR,
        TokenType.IDENTIFIER,
        TokenType.COLON,
        TokenType.STR_TYPE,
        TokenType.EQUALS,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.RETURN,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('x==10;', [
        TokenType.IDENTIFIER,
        TokenType.EQUAL_EQUAL,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('x = 3.14;', [
        TokenType.IDENTIFIER,
        TokenType.EQUALS,
        TokenType.FLOAT,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('   // comment only', [
        TokenType.EOF,
    ]),
    ('x = 1; // cmt\ny = 2;', [
        TokenType.IDENTIFIER,
        TokenType.EQUALS,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.EQUALS,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('var s: str = "olá";', [
        TokenType.VAR,
        TokenType.IDENTIFIER,
        TokenType.COLON,
        TokenType.STR_TYPE,
        TokenType.EQUALS,
        TokenType.STRING,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
])
def test_lexer_tokenize_additional(code: str, expected_types: list[TokenType]) -> None:
    lexer: Lexer = Lexer(code)
    tokens: Generator[Token, None, None] = lexer.tokenize()
    token_types = [t.type for t in tokens]
    assert token_types == expected_types


def test_token_positions_line_and_column() -> None:
    code = 'var x: str = "a";\nreturn x;'
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    got = [(t.type, t.line, t.column) for t in tokens]
    expected = [
        (TokenType.VAR, 1, 1),
        (TokenType.IDENTIFIER, 1, 5),
        (TokenType.COLON, 1, 6),
        (TokenType.STR_TYPE, 1, 8),
        (TokenType.EQUALS, 1, 12),
        (TokenType.STRING, 1, 14),
        (TokenType.SEMICOLON, 1, 17),
        (TokenType.RETURN, 2, 1),
        (TokenType.IDENTIFIER, 2, 8),
        (TokenType.SEMICOLON, 2, 9),
        (TokenType.EOF, 2, 10),
    ]
    assert got == expected
