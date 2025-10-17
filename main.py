import sys
import argparse
import pyfiglet
from pprint import pprint
from typing import Generator
from lib.utils.args_validators import clash_file
from lib.lexer.token import Token
from lib.lexer.lexer import Lexer

def main() -> None:
    if len(sys.argv) == 1:
        print(pyfiglet.figlet_format("Clash", font="slant"))

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        'filename',
        type=clash_file,
        help="input file with .clash extension"
    )
    args_parser.add_argument(
        '-l', '--lexer',
        action='store_true',
        help="run only the lexer and print the tokens to the console"
    )

    args = args_parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as f:
        code = f.read()
    
    lexer: Lexer = Lexer(code)
    tokens: Generator[Token, None, None] = lexer.tokenize()

    for token in tokens:
        if args.lexer: pprint(token)

if __name__ == "__main__":
    main()
