import unicodedata
from automata.fa.dfa import DFA
from typing import Generator
from lib.lexer.token import Token, TokenType
from lib.lexer.tables import KEYWORDS_TABLE, OPERATORS_TABLE, PUNCTUATION_TABLE
from lib.lexer.nfa_to_dfa import dfa
from lib.utils.error_handler import LexerError

class Lexer:
    def __init__(self, code: str):
        self.normalized = unicodedata.normalize('NFKC', code)
        self.code = ''.join(c if ord(c) < 128 else ' ' for c in self.normalized)
        self.dfa: DFA = dfa
        self.i = 0
        self.n = len(code)
        self.line = 1
        self.column = 1

    def get_next_token(self) -> Token:
        if self.i >= self.n:
            return Token(TokenType.EOF, '', self.line, self.column)

        state = self.dfa.initial_state
        last_final_state = None
        last_final_index = self.i
        j = self.i

        while j < self.n:
            char = self.code[j]

            if char not in self.dfa.input_symbols:
                break

            if char in self.dfa.transitions.get(state, {}):
                state = self.dfa.transitions[state][char]
            else:
                break

            if state in self.dfa.final_states:
                last_final_state = state
                last_final_index = j + 1

            j += 1

        if last_final_state is None:
            raise LexerError("Invalid token", self.line, self.column, self.code[self.i])

        token_text = self.code[self.i:last_final_index]
        token_type = self.classify_token(token_text)

        token = Token(token_type, token_text, self.line, self.column)

        for c in token_text:
            if c == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

        self.i = last_final_index
        return token

    def classify_token(self, token_text: str) -> TokenType:
        # --- Whitespace ---
        if token_text.strip() == '':
            return TokenType.WHITESPACE

        # --- Comments ---
        if token_text.startswith("//"):
            return TokenType.COMMENT

        # --- Keywords ---
        if token_text in KEYWORDS_TABLE:
            return KEYWORDS_TABLE[token_text]

        # --- Operators ---
        if token_text in OPERATORS_TABLE:
            return OPERATORS_TABLE[token_text]

        # --- Punctuation ---
        if token_text in PUNCTUATION_TABLE:
            return PUNCTUATION_TABLE[token_text]

        # --- Strings ---
        if token_text.startswith('"') and token_text.endswith('"'):
            return TokenType.STRING

        # --- Numbers ---
        if token_text.replace('.', '', 1).isdigit():
            return TokenType.FLOAT if '.' in token_text else TokenType.INTEGER

        # --- Identifiers ---
        return TokenType.IDENTIFIER

    def tokenize(self) -> Generator[Token, None, None]:
        while True:
            token = self.get_next_token()

            # Skip whitespaces and comments
            if token.type not in {TokenType.WHITESPACE, TokenType.COMMENT}:
                yield token

            if token.type == TokenType.EOF:
                break
