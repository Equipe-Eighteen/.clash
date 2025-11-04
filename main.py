import sys
import argparse
import pyfiglet
from pprint import pprint
from lib.utils.args_validators import clash_file
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser

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
    args_parser.add_argument(
        '-p', '--parser',
        action='store_true',
        help="run only the parser and print the AST to the console"
    )

    args = args_parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as f:
        code = f.read()
    
    lexer: Lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    if args.lexer:
        pprint(tokens)
        return

    parser: Parser = Parser(tokens)
    ast = parser.parse()

    if args.parser:
        pprint(ast)
        return

if __name__ == "__main__":
    main()
