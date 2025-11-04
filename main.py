import sys
import argparse
import pyfiglet
from pprint import pprint
from lib.utils.args_validators import clash_file
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.semantic.semantic_analyzer import SemanticAnalyzer
from lib.codegen.codegen import CodeGenerator

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
    args_parser.add_argument(
        '-s', '--semantic',
        action='store_true',
        help="run only the semantic analyzer and print any errors to the console"
    )
    args_parser.add_argument(
        '-c', '--codegen',
        action='store_true',
        help="generate the code from the AST and print it"
    )
    args_parser.add_argument(
        '-r', '--run',
        action='store_true',
        help="generate the code and execute it"
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
    
    semantic_analyzer = SemanticAnalyzer()
    semantic_errors = semantic_analyzer.analyze(ast)

    if semantic_errors:
        pprint(semantic_errors)
        return

    if args.semantic and not semantic_errors:
        print("No semantic errors found.")
        return

    gen = CodeGenerator()
    if args.codegen:
        src = gen.generate(ast, args.run)
        pprint(src)
        return

    if args.run or not any((args.lexer, args.parser, args.semantic, args.codegen, args.run)):
        gen.run(ast)
        return

if __name__ == "__main__":
    main()
