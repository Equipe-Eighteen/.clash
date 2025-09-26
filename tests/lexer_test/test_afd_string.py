import pytest
from lib.lexer.lexer import Lexer
from lib.lexer.token import TokenType, Token

@pytest.mark.parametrize("text, expected_value", [
    ('"hello"', "hello"),
    ('"line\\nnew"', "line\nnew"),
    ('"tab\\tchar"', "tab\tchar"),
])
def test_afd_string(text: str, expected_value: str) -> None:
    lexer: Lexer = Lexer(text)
    token: Token = lexer.afd_string()
    assert token.type == TokenType.STRING
    assert token.value == expected_value
