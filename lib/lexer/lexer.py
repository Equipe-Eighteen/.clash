from lib.lexer.token import *
from lib.lexer.tables.keywords_table import KEYWORDS_TABLE
from lib.lexer.tables.operators_table import OPERATORS_TABLE
from lib.utils.error_handler import LexerError

class Lexer:
    def __init__(self, text: str) -> None:
        self._text: str = text
        self._pos: int = 0
        self._line: int = 1
        self._column: int = 1

    # Tools
    def peek(self, offset: int = 1) -> str:
        peek_pos: int = self._pos + offset
        return self._text[peek_pos] if peek_pos < len(self._text) else "\0"
    
    def current(self) -> str:
        return self.peek(0)

    def advance(self) -> None:
        if self.current() == "\n":
            self._line += 1
            self._column = 0
        else:
            self._column += 1
        self._pos += 1

    def skip_whitespace(self) -> None:
        while self.current().isspace():
            self.advance()

    def skip_comments(self) -> None:
        while True:
            if self.current() == "/" and self.peek() == "/":
                self.advance()
                self.advance()
                while self.current() not in ("\n", "\0"):
                    self.advance()
            elif self.current() == "/" and self.peek() == "*":
                self.advance()
                self.advance()
                while not (self.current() == "*" and self.peek() == "/"):
                    if self.current() == "\0":
                        raise LexerError("Unterminated multi-line comment", self._line, self._column, "")
                    self.advance()
                self.advance()
                self.advance()
            else:
                break

    # AFD's
    def afd_number(self) -> Token:
        result: str = ""
        is_float: bool = False

        while self.current().isdigit():
            result += self.current()
            self.advance()

        if self.current() == ".":
            if self.peek().isdigit():
                is_float = True
                result += "."
                self.advance()
                while self.current().isdigit():
                    result += self.current()
                    self.advance()
            else:
                raise LexerError("Malformed float", self._line, self._column, self.current())

        token_type: TokenType = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, result, self._line, self._column)

    def afd_string(self) -> Token:
        quote: str = self.current()
        self.advance()
        result: str = ""

        while self.current() != quote:
            if self.current() == "\0":
                raise LexerError("Unterminated string", self._line, self._column, "")

            if self.current() == "\\":
                self.advance()
                if self.current() == "n":
                    result += "\n"
                elif self.current() == "t":
                    result += "\t"
                else:
                    result += self.current()
            else:
                result += self.current()
            self.advance()

        self.advance()
        return Token(TokenType.STRING, result, self._line, self._column)

    def afd_identifier(self) -> Token:
        result: str = ""

        if not (self.current().isalpha() or self.current() == "_"):
            raise LexerError("Invalid identifier", self._line, self._column, self.current())

        while self.current().isalnum() or self.current() == "_":
            result += self.current()
            self.advance()

        token_type: TokenType = TokenType.IDENTIFIER
        if result in KEYWORDS_TABLE:
            token_type = KEYWORDS_TABLE[result]

        return Token(token_type, result, self._line, self._column)

    def afd_operator(self) -> Token:
        current: str = self.current()
        next_char: str = self.peek()

        two_char: str = current + next_char
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
        tokens: list[Token] = []
        while self.current() != "\0":
            while True:
                initial_pos: int = self._pos
                self.skip_whitespace()
                self.skip_comments()
                if self._pos == initial_pos:
                    break

            if self.current() == "\0":
                break
            elif self.current().isdigit():
                tokens.append(self.afd_number())
            elif self.current() == '"':
                tokens.append(self.afd_string())
            elif self.current().isalpha() or self.current() == "_":
                tokens.append(self.afd_identifier())
            else:
                tokens.append(self.afd_operator())

        tokens.append(Token(TokenType.EOF, "", self._line, self._column))
        return tokens
