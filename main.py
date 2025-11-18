import os
import sys
import argparse
import pyfiglet
import subprocess
import tempfile
from pprint import pprint
from lib.utils.args_validators import clash_file
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.semantic.semantic_analyzer import SemanticAnalyzer
from lib.codegen.codegen import CodeGenerator
from lib.codegen.llvm_codegen import LLVMCodeGenerator
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
    # args_parser.add_argument(
    #     '-c', '--compiler',
    #     action='store_true',
    #     help="generate the LLVM IR code and execute it"
    # )

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
    
    gen = CodeGenerator()
    try:
        gen.run(ast)
    except CodegenError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if False:  # args.compiler:
        llvm_gen = LLVMCodeGenerator()
        try:
            src = llvm_gen.generate(ast)
        except CodegenError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ll', delete=False) as ll_file:
            ll_file.write(src)
            ll_filename = ll_file.name
        
        exe_filename = None
        try:
            exe_filename = ll_filename.replace('.ll', '.exe')
            
            compile_result = subprocess.run(
                ['clang', ll_filename, '-o', exe_filename, '-lm'],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode != 0:
                print(f"Compilation error:\n{compile_result.stderr}", file=sys.stderr)
                sys.exit(1)
            
            exec_result = subprocess.run(
                [exe_filename],
                capture_output=True,
                text=True
            )
            
            print(exec_result.stdout, end='')
            if exec_result.stderr:
                print(exec_result.stderr, file=sys.stderr, end='')
            
            sys.exit(exec_result.returncode)
        finally:
            if os.path.exists(ll_filename):
                os.remove(ll_filename)
            if exe_filename is not None and os.path.exists(exe_filename):
                os.remove(exe_filename)

if __name__ == "__main__":
    main()
