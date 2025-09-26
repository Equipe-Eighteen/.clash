class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int, char: str) -> None:
        super().__init__(f"Lexical error at line {line}, column {column}: {message} -> '{char}'")
