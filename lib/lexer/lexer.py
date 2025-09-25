from lib.lexer.token import *
from lib.lexer.tables.keywords_table import KEYWORDS_TABLE
from lib.lexer.tables.operators_table import OPERATORS_TABLE
from lib.utils.error_handler import LexerError

class Lexer:
    def __init__(self, text: str):
        self._text = text
        self._pos = 0
        self._line = 0
        self._column = 0
        self._current_char = text[0] if text else "\0"

    # Tools
    def peek(self) -> str:
        peek_pos = self._pos + 1
        return self._text[peek_pos] if peek_pos < len(self._text) else "\0"

    def advance(self) -> None:
        if self._current_char == "\n":
            self._line += 1
            self._column = 0
        else:
            self._column += 1

        self._pos += 1
        self._current_char = self._text[self._pos] if self._pos < len(self._text) else "\0"

    def skip_whitespace(self) -> None:
        while self._current_char.isspace():
            self.advance()

    def skip_comments(self) -> None:
        while True:
            if self._current_char == "/" and self.peek() == "/":
                self.advance()
                self.advance()
                while self._current_char not in ("\n", "\0"):
                    self.advance()
            elif self._current_char == "/" and self.peek() == "*":
                self.advance()
                self.advance()
                while not (self._current_char == "*" and self.peek() == "/"):
                    if self._current_char == "\0":
                        return
                    self.advance()
                self.advance()
                self.advance()
            else:
                break

    # AFD's
    def afd_number(self) -> Token:
        result = ""
        is_float = False

        while self._current_char.isdigit():
            result += self._current_char
            self.advance()

        if self._current_char == ".":
            if self.peek().isdigit():
                is_float = True
                result += "."
                self.advance()
                while self._current_char.isdigit():
                    result += self._current_char
                    self.advance()
            else:
                raise LexerError("Malformed float", self._line, self._column, self._current_char)

        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, result, self._line, self._column)

    def afd_string(self) -> Token:
        quote = self._current_char
        self.advance()
        result = ""

        while self._current_char != quote:
            if self._current_char == "\0":
                raise LexerError("Unterminated string", self._line, self._column, "")

            if self._current_char == "\\":
                self.advance()
                if self._current_char == "n":
                    result += "\n"
                elif self._current_char == "t":
                    result += "\t"
                else:
                    result += self._current_char
            else:
                result += self._current_char
            self.advance()

        self.advance()
        return Token(TokenType.STRING, result, self._line, self._column)

    def afd_identifier(self) -> Token:
        result = ""

        if not (self._current_char.isalpha() or self._current_char == "_"):
            raise LexerError("Invalid identifier", self._line, self._column, self._current_char)

        while self._current_char.isalnum() or self._current_char == "_":
            result += self._current_char
            self.advance()

        if result in KEYWORDS_TABLE:
            token_type = KEYWORDS_TABLE[result]
        else:
            token_type = TokenType.IDENTIFIER

        return Token(token_type, result, self._line, self._column)

    def afd_operator(self) -> Token:
        current = self._current_char
        next_char = self.peek()

        two_char = current + next_char
        if two_char in OPERATORS_TABLE:
            self.advance()
            self.advance()
            return Token(OPERATORS_TABLE[two_char], two_char, self._line, self._column)

        if current in OPERATORS_TABLE:
            self.advance()
            return Token(OPERATORS_TABLE[current], current, self._line, self._column)

        raise LexerError("Invalid operator", self._line, self._column, current)

    # Tokens
    def tokenize(self) -> list[Token]:
        tokens = []
        while self._current_char != "\0":
            self.skip_whitespace()
            self.skip_comments()

            if self._current_char == "\0":
                break
            elif self._current_char.isdigit():
                tokens.append(self.afd_number())
            elif self._current_char == '"':
                tokens.append(self.afd_string())
            elif self._current_char.isalpha() or self._current_char == "_":
                tokens.append(self.afd_identifier())
            else:
                tokens.append(self.afd_operator())

        tokens.append(Token(TokenType.EOF, "", self._line, self._column))
        return tokens
