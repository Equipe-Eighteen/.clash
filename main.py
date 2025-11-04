import sys
import argparse
import pyfiglet
from pprint import pprint
from lib.utils.args_validators import clash_file
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.semantic.semantic_analyzer import SemanticAnalyzer
from lib.codegen.codegen import CodeGenerator
from lib.utils.error_handler import LexerError, ParserError, CodegenError

def main() -> None:
    if len(sys.argv) == 1:
        print(pyfiglet.figlet_format("Clash", font="slant"))

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        '-v', '--version',
        action='version',
        version='Clash 1.0.0',
        help="show program's version number and exit"
    )
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
    
     # Lexer
    try:
        lexer: Lexer = Lexer(code)
        tokens = list(lexer.tokenize())
    except LexerError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if args.lexer:
        pprint(tokens)
        return

    # Parser
    try:
        parser: Parser = Parser(tokens)
        ast = parser.parse()
    except ParserError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if args.parser:
        pprint(ast)
        return
    
    # Semantic
    semantic_analyzer = SemanticAnalyzer()
    semantic_errors = semantic_analyzer.analyze(ast)

    if semantic_errors:
        for err in semantic_errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    if args.semantic and not semantic_errors:
        print("No semantic errors found.")
        return

    # Codegen/Run
    gen = CodeGenerator()
    if args.codegen:
        try:
            src = gen.generate(ast, args.run)
        except CodegenError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        pprint(src)
        return

    if args.run or not any((args.lexer, args.parser, args.semantic, args.codegen, args.run)):
        try:
            gen.run(ast)
        except CodegenError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        return

if __name__ == "__main__":
    main()
