import pytest
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.semantic.semantic_analyzer import SemanticAnalyzer


def analyze(src: str):
    tokens = list(Lexer(src).tokenize())
    ast = Parser(tokens).parse()
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(ast)

def has_err(errors: list[str], snippet: str) -> bool:
    return any(snippet in e for e in errors)


def test_no_errors_simple_program():
    src = """
    var x: int = 1;
    var y: float = x;
    func main(): void {
        print(x);
        print(y);
    }
    """
    errors = analyze(src)
    assert errors == []


def test_redeclaration_top_level_symbols():
    src = """
    var x: int;
    var x: int;
    func f(): void {}
    func f(): void {}
    struct S { a: int, a: int };
    """
    errors = analyze(src)
    assert has_err(errors, "Redeclaration of symbol 'x'.")
    assert has_err(errors, "Redeclaration of symbol 'f'.")
    assert has_err(errors, "Duplicate field 'a' in struct 'S'.")


def test_undeclared_identifier_usage():
    errors = analyze("print(y);")
    assert has_err(errors, "Undeclared identifier 'y'.")


def test_type_mismatch_in_var_init_and_assignment():
    src = """
    var a: int = 3.5;
    var b: float = 1;
    var c: str = "ok";
    a = "nope";
    """
    errors = analyze(src)
    assert has_err(errors, "Type mismatch in variable initialization of 'a' (expected int, got float).")
    assert not has_err(errors, "Type mismatch in variable initialization of 'b'")
    assert has_err(errors, "Type mismatch in assignment (expected int, got str).")


def test_list_literal_checks():
    src = """
    var xs: list[int] = [1, 2, 3];
    var ys: list[int] = [1, 2.0];
    var zs: list[float] = [1, 2.5];
    """
    errors = analyze(src)
    assert not has_err(errors, "xs")
    assert has_err(errors, "Incompatible list element type (expected int, got float).")
    assert not has_err(errors, "zs")


def test_struct_literal_assignment_checks():
    src = """
    struct Point { x: int, y: int };
    var ok: Point = { x: 1, y: 2 };
    var miss: Point = { x: 1 };
    var wrong: Point = { x: "a", y: 2 };
    """
    errors = analyze(src)
    assert has_err(errors, "Missing field 'y' for struct 'Point'.")
    assert has_err(errors, "Incompatible type for field 'x' in struct 'Point' (expected int, got str).")


def test_member_access_rules():
    src = """
    struct P { x: int };
    var p: P = { x: 1 };
    var xs: list[int] = [1, 2];
    var a: int = xs.length;
    var b: int = p.x;
    var c: int = xs.foo;
    var d: int = p.z;
    var e: int = 10.length;
    """
    errors = analyze(src)
    assert not has_err(errors, "xs.length")
    assert not has_err(errors, "p.x")
    assert has_err(errors, "List type has no member 'foo'.")
    assert has_err(errors, "Struct 'P' has no field 'z'.")
    assert has_err(errors, "Member access on non-struct type.")


def test_if_condition_must_be_bool_and_elif_too():
    src = """
    if (1) { print(1); }
    elif ("x") { print(2); }
    else { print(3); }
    """
    errors = analyze(src)
    assert has_err(errors, "If condition must be 'bool'.")
    assert has_err(errors, "Elif condition must be 'bool'.")


def test_break_and_continue_outside_loop():
    src = """
    break;
    continue;
    """
    errors = analyze(src)
    assert has_err(errors, "Break used outside of loop.")
    assert has_err(errors, "Continue used outside of loop.")


def test_return_rules_and_mismatches():
    src = """
    return 1;
    func f(): int { return "a"; }
    func g(): int { return; }
    func h(): int { return { x: 1 }; }
    struct S { x: int };
    """
    errors = analyze(src)
    assert has_err(errors, "Return used outside of function.")
    assert has_err(errors, "Return type mismatch (expected int, got str).")
    assert has_err(errors, "Missing return value (expected int).")
    assert has_err(errors, "Could not infer return type.")


def test_builtins_print_and_len():
    src = """
    var s: str = "hi";
    var xs: list[int] = [1,2,3];
    print(s);
    print(xs);
    var n1: int = len(xs);
    var n2: int = len(s);
    var n3: int = len();    // wrong arity
    var n4: int = len(123); // wrong type
    """
    errors = analyze(src)
    assert has_err(errors, "'len' expects 1 argument, got 0.")
    assert has_err(errors, "Argument to 'len' must be a list or 'str'.")


def test_function_call_argument_checks():
    src = """
    func add(a: int, b: int): int { return a + b; }
    var x: int = add(1, 2);
    var y: int = add(1);             // arity
    var z: int = add(1, "s");        // type
    (add)("not a function");         // call target must be function (identifier is checked)
    """
    errors = analyze(src)
    assert has_err(errors, "Function 'add' expects 2 arguments, got 1.")
    assert has_err(errors, "Argument type mismatch for 'add' (expected int, got str).")


def test_array_access_rules():
    src = """
    var xs: list[int] = [1,2,3];
    var a: int = xs[0];
    var b: int = xs["i"];     // index must be int
    var c: int = 10[0];       // non-list subscript
    """
    errors = analyze(src)
    assert not has_err(errors, "xs[0]")
    assert has_err(errors, "Array index must be of type 'int'.")
    assert has_err(errors, "Subscript operator used on non-list type.")


def test_compound_assignment_type_check():
    src = """
    var x: int = 0;
    x += 1;
    x += 1.5;
    """
    errors = analyze(src)
    assert has_err(errors, "Incompatible types for '+=' (left int, right float).")


def test_binary_operation_type_checks_and_results():
    src = """
    var a: int = 1 + 2;
    var b: float = 1 + 2.5;
    var c: str = "a" + "b";
    var d: bool = 1 && 2;    // bad
    var e: bool = "a" == "b";
    var f: bool = 1 < "b";   // bad
    """
    errors = analyze(src)
    assert has_err(errors, "Incompatible types for '&&' (left int, right int).")
    assert has_err(errors, "Incompatible types for '<' (left int, right str).")


@pytest.mark.parametrize("src", [
    "var a: int = 1;",
    "var xs: list[int] = [1,2,3];",
    "struct S { x: int }; var s: S = { x: 1 };",
    "func add(a: int, b: int): int { return a + b; }",
    "struct P { x: int }; var p: P = { x: 1 }; var v: int = p.x;",
])
def test_semantic_success_parametrized(src: str):
    errors = analyze(src)
    assert errors == []

@pytest.mark.parametrize(("src", "snippet"), [
    ("print(y);", "Undeclared identifier 'y'."),
    ("break;", "Break used outside of loop."),
    ("continue;", "Continue used outside of loop."),
    ("if (1) { print(1); }", "If condition must be 'bool'."),
    ("return 1;", "Return used outside of function."),
    ("var xs: list[int] = [1]; var n: int = len();", "'len' expects 1 argument, got 0."),
    ("var xs: list[int] = [1]; var n: int = len(123);", "Argument to 'len' must be a list or 'str'."),
    ("var a: int = 3.5;", "Type mismatch in variable initialization"),
    ("var xs: list[int] = [1, 2.0];", "Incompatible list element type"),
])
def test_semantic_errors_parametrized(src: str, snippet: str):
    errors = analyze(src)
    assert has_err(errors, snippet)