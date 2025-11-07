import pytest
from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.codegen.codegen import CodeGenerator
from lib.utils.error_handler import CodegenError


def compile_and_run(src: str) -> dict[str, object]:
    tokens = list(Lexer(src).tokenize())
    ast = Parser(tokens).parse()
    cg = CodeGenerator()
    return cg.run(ast)


def generate(src: str) -> str:
    tokens = list(Lexer(src).tokenize())
    ast = Parser(tokens).parse()
    cg = CodeGenerator()
    return cg.generate(ast)


def test_var_defaults_and_initializers():
    src = """
    struct S { a: int, b: str };
    var x: int;
    var y: float;
    var s: str;
    var b: bool;
    var xs: list[int];
    var p: S;
    var xs2: list[int] = [1, 2, 3];
    var p2: S = { a: 1, b: "ok" };
    """
    env = compile_and_run(src)
    assert env["x"] == 0
    assert env["y"] == 0.0
    assert env["s"] == ""
    assert env["b"] is False
    assert env["xs"] == []
    assert env["p"] == {"a": None, "b": None}
    assert env["xs2"] == [1, 2, 3]
    assert env["p2"] == {"a": 1, "b": "ok"}


def test_functions_and_calls_and_string_plus():
    src = """
    func add(a: int, b: int): int { return a + b; }
    var r: int = add(2, 3);
    var t: str = "a" + "b";
    """
    env = compile_and_run(src)
    assert "add" in env and callable(env["add"])
    assert env["r"] == 5
    assert env["t"] == "ab"
    assert env["add"](10, 32) == 42


def test_if_else_and_loop_break_continue():
    src = """
    func abs(x: int): int {
        if (x < 0) { return -x; }
        else { return x; }
    }
    func count(n: int): int {
        var i: int = 0;
        loop {
            if (i == n) { break; }
            i += 1;
        }
        return i;
    }
    """
    env = compile_and_run(src)
    assert callable(env["abs"])
    assert env["abs"](-5) == 5
    assert env["abs"](7) == 7
    assert callable(env["count"])
    assert env["count"](0) == 0
    assert env["count"](3) == 3


def test_member_index_and_length_and_assignments():
    src = """
    struct P { x: int, y: int };
    var p: P = { x: 1, y: 2 };
    var xs: list[int] = [9, 8, 7];
    var a: int = p.x;
    var b: int = xs[1];
    var n: int = xs.length;
    p.x = 5;
    xs[0] = 42;
    var a2: int = p.x;
    var b2: int = xs[0];
    """
    env = compile_and_run(src)
    assert env["a"] == 1
    assert env["b"] == 8
    assert env["n"] == 3
    assert env["a2"] == 5
    assert env["b2"] == 42


def test_generate_contains_runtime_helpers_and_defs():
    src = """
    func add(a: int, b: int): int { return a + b; }
    var x: int = 1 + 2;
    """
    py = generate(src)
    assert "def _op_add(a, b):" in py
    assert "def add(" in py
    assert "_op_add(1, 2)" in py or "_op_add(" in py


def test_assign_to_length_raises_codegen_error():
    src = """
    var xs: list[int] = [1,2,3];
    xs.length = 10;
    """
    tokens = list(Lexer(src).tokenize())
    ast = Parser(tokens).parse()
    cg = CodeGenerator()
    with pytest.raises(CodegenError):
        cg.generate(ast)