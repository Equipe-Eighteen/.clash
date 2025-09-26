import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType, Token

@pytest.mark.parametrize("text, expected_type", [
    ("myVar", TokenType.IDENTIFIER),
    ("_private", TokenType.IDENTIFIER),
    ("print", TokenType.IDENTIFIER),
    ("if", TokenType.IF),
    ("while", TokenType.WHILE),
    ("int", TokenType.INT_TYPE),
])
def test_afd_identifier(text: str, expected_type: TokenType) -> None:
    lexer: Lexer = Lexer(text)
    token: Token = lexer.afd_identifier()
    assert token.type == expected_type
    assert token.value == text
