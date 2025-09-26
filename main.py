import argparse
from pprint import pprint
from lib.utils.args_validators import clash_file
from lib.lexer.token import Token
from lib.lexer.lexer import Lexer

def main() -> None:
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        'filename',
        type=clash_file,
        help="Input file with .clash extension"
    )
    args_parser.add_argument(
        '-l', '--lexer',
        action='store_true',
        help="Run only the lexer and print the tokens to the console"
    )

    args = args_parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as f:
        code = f.read()
    
    lexer: Lexer = Lexer(code)
    tokens: list[Token] = lexer.tokenize()

    if args.lexer:
        pprint(tokens)
        return

if __name__ == "__main__":
    main()
