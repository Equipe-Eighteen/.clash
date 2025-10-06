from automata.fa.dfa import DFA
from lib.lexer.token import Token, TokenType
from lib.lexer.tables import KEYWORDS_TABLE, OPERATORS_TABLE, PUNCTUATION_TABLE
from lib.lexer.nfa_to_dfa import dfa

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.dfa: DFA = dfa
        self.tokens: list[Token] = []
        self.i = 0
        self.n = len(code)
        self.line = 1
        self.column = 1

    def skip_whitespace_and_comments(self):
        while self.i < self.n:
            if self.code[self.i].isspace():
                if self.code[self.i] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.i += 1
            elif self.code[self.i:self.i+2] == "//":
                self.i += 2
                while self.i < self.n and self.code[self.i] != '\n':
                    self.i += 1
                if self.i < self.n and self.code[self.i] == '\n':
                    self.line += 1
                    self.column = 1
                    self.i += 1
            elif self.code[self.i:self.i+2] == "/*":
                self.i += 2
                while self.i < self.n-1 and self.code[self.i:self.i+2] != "*/":
                    if self.code[self.i] == '\n':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                    self.i += 1
                if self.i < self.n-1:
                    self.i += 2
            else:
                break

    def get_next_token(self) -> Token:
        self.skip_whitespace_and_comments()
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
            raise ValueError(
                f"Invalid Token at line {self.line} and column {self.column}: {self.code[self.i]}"
            )

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
        if token_text in KEYWORDS_TABLE:
            return KEYWORDS_TABLE[token_text]
        elif token_text in OPERATORS_TABLE:
            return OPERATORS_TABLE[token_text]
        elif token_text in PUNCTUATION_TABLE:
            return PUNCTUATION_TABLE[token_text]
        elif token_text.startswith('"'):
            return TokenType.STRING
        elif token_text.replace('.', '', 1).isdigit():
            return TokenType.FLOAT if '.' in token_text else TokenType.INTEGER
        else:
            return TokenType.IDENTIFIER

    def tokenize(self) -> list[Token]:
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return self.tokens
