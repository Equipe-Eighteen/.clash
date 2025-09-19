import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType

@pytest.mark.parametrize("code, expected_types", [
    ('print("Hello World");', [
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.STRING,
        TokenType.RPAREN,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]),
    ('string x = "hello";', [
        TokenType.STRING_TYPE,
        TokenType.IDENTIFIER,
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
def test_lexer_tokenize(code, expected_types):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    token_types = [t.type for t in tokens]
    assert token_types == expected_types
