import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType, Token

@pytest.mark.parametrize("text, expected_type, expected_value", [
    ("123", TokenType.INTEGER, "123"),
    ("0", TokenType.INTEGER, "0"),
    ("12.34", TokenType.FLOAT, "12.34"),
    ("0.0", TokenType.FLOAT, "0.0"),
    ("123.0", TokenType.FLOAT, "123.0"),
])
def test_afd_number(text: str, expected_type: TokenType, expected_value: str) -> None:
    lexer: Lexer = Lexer(text)
    token: Token = lexer.afd_number()
    assert token.type == expected_type
    assert token.value == expected_value
