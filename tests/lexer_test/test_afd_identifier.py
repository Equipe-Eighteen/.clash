import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType

@pytest.mark.parametrize("text, expected_type", [
    ("myVar", TokenType.IDENTIFIER),
    ("_private", TokenType.IDENTIFIER),
    ("print", TokenType.IDENTIFIER),
    ("if", TokenType.IF),
    ("while", TokenType.WHILE),
    ("int", TokenType.INT_TYPE),
])
def test_afd_identifier(text, expected_type):
    lexer = Lexer(text)
    token = lexer.afd_identifier()
    assert token.type == expected_type
    assert token.value == text
