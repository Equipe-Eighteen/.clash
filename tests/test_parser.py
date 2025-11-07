import pytest

from lib.lexer.lexer import Lexer
from lib.parser.parser import Parser
from lib.utils.error_handler import ParserError
from lib.parser.ast import program, declarations, statements, expressions, types


def parse_program(src: str) -> program.Program:
    toks = list(Lexer(src).tokenize())
    return Parser(toks).parse()


def test_var_decl_simple():
    prog = parse_program("var x: int;")
    assert len(prog.declarations) == 1
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    assert isinstance(decl.name, expressions.Identifier)
    assert decl.name.name == "x"
    assert isinstance(decl.type_spec, types.BaseType)
    assert decl.type_spec.name == "int"
    assert decl.initializer is None


def test_var_decl_with_initializer_float():
    prog = parse_program("var y: float = 3.5;")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    assert isinstance(decl.initializer, expressions.FloatLiteral)
    assert decl.initializer.value == 3.5


def test_list_type_and_list_literal():
    prog = parse_program("var xs: list[int] = [1, 2, 3];")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    assert isinstance(decl.type_spec, types.ListType)
    assert isinstance(decl.type_spec.element_type, types.BaseType)
    assert decl.type_spec.element_type.name == "int"
    assert isinstance(decl.initializer, expressions.LiteralList)
    assert [type(e) for e in decl.initializer.elements] == [expressions.IntLiteral] * 3
    assert [e.value for e in decl.initializer.elements if isinstance(e, expressions.IntLiteral)] == [1, 2, 3]


def test_struct_decl():
    prog = parse_program("struct Point { x: int, y: int };")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.StructDecl)
    assert decl.name.name == "Point"
    assert len(decl.fields) == 2
    assert decl.fields[0].name.name == "x"
    assert isinstance(decl.fields[0].type_spec, types.BaseType)
    assert decl.fields[0].type_spec.name == "int"
    assert decl.fields[1].name.name == "y"


def test_struct_literal_in_var():
    prog = parse_program("var p: Point = { x: 1, y: 2 };")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    assert isinstance(decl.initializer, expressions.StructLiteral)
    lit: expressions.StructLiteral = decl.initializer
    assert len(lit.fields) == 2
    assert lit.fields[0].name.name == "x"
    assert isinstance(lit.fields[0].value, expressions.IntLiteral)
    assert lit.fields[0].value.value == 1


def test_func_decl_no_params():
    prog = parse_program("func one(): int { return 1; }")
    f = prog.declarations[0]
    assert isinstance(f, declarations.FuncDecl)
    assert f.name.name == "one"
    assert isinstance(f.return_type, types.BaseType)
    assert f.return_type.name == "int"
    assert isinstance(f.body, statements.BlockStmt)
    assert len(f.body.statements) == 1
    ret = f.body.statements[0]
    assert isinstance(ret, statements.ReturnStmt)
    assert isinstance(ret.value, expressions.IntLiteral)
    assert ret.value.value == 1


def test_func_decl_with_params_and_binary_return():
    prog = parse_program("func add(a: int, b: int): int { return a + b; }")
    f = prog.declarations[0]
    assert isinstance(f, declarations.FuncDecl)
    assert len(f.params) == 2
    assert f.params[0].name.name == "a"
    assert isinstance(f.params[0].type_spec, types.BaseType)
    assert f.params[0].type_spec.name == "int"
    assert f.params[1].name.name == "b"
    assert isinstance(f.params[1].type_spec, types.BaseType)
    assert f.params[1].type_spec.name == "int"
    ret = f.body.statements[0]
    assert isinstance(ret, statements.ReturnStmt)
    assert isinstance(ret.value, expressions.BinaryOp)
    assert ret.value.op == "+"
    assert isinstance(ret.value.left, expressions.Identifier)
    assert isinstance(ret.value.right, expressions.Identifier)


def test_if_elif_else_statement():
    src = """
    if (x > 0) { return x; }
    elif (x == 0) { return 0; }
    else { return -x; }
    """
    prog = parse_program(src)
    node = prog.declarations[0]
    assert isinstance(node, statements.IfStmt)
    assert isinstance(node.condition, expressions.BinaryOp)
    assert node.condition.op == ">"
    assert isinstance(node.then_branch, statements.BlockStmt)
    assert len(node.elif_branches) == 1
    assert isinstance(node.else_branch, statements.BlockStmt)
    # check then return
    then_ret = node.then_branch.statements[0]
    assert isinstance(then_ret, statements.ReturnStmt)
    # check else return is unary -
    else_ret = node.else_branch.statements[0]
    assert isinstance(else_ret, statements.ReturnStmt)
    assert isinstance(else_ret.value, expressions.UnaryOp)
    assert else_ret.value.op == "-"


def test_loop_break_continue():
    src = "loop { if (x > 0) { break; } continue; }"
    prog = parse_program(src)
    loop_stmt = prog.declarations[0]
    assert isinstance(loop_stmt, statements.LoopStmt)
    body = loop_stmt.body
    assert isinstance(body, statements.BlockStmt)
    # body: IfStmt, ContinueStmt
    assert isinstance(body.statements[0], statements.IfStmt)
    assert isinstance(body.statements[1], statements.ContinueStmt)
    inner_if = body.statements[0]
    assert isinstance(inner_if.then_branch.statements[0], statements.BreakStmt)


def test_expression_precedence_and_power():
    prog = parse_program("var x: int = 1 + 2 * 3 ** 2;")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    expr = decl.initializer
    assert isinstance(expr, expressions.BinaryOp) and expr.op == "+"
    left = expr.left
    right = expr.right
    assert isinstance(left, expressions.IntLiteral) and left.value == 1
    assert isinstance(right, expressions.BinaryOp) and right.op == "*"
    r_left = right.left
    r_right = right.right
    assert isinstance(r_left, expressions.IntLiteral) and r_left.value == 2
    assert isinstance(r_right, expressions.BinaryOp) and r_right.op == "**"
    assert isinstance(r_right.left, expressions.IntLiteral) and r_right.left.value == 3
    assert isinstance(r_right.right, expressions.IntLiteral) and r_right.right.value == 2


def test_postfix_member_call_index_chain():
    prog = parse_program("x.foo(1, 2)[3]();")
    stmt = prog.declarations[0]
    assert isinstance(stmt, statements.ExpressionStmt)
    call2 = stmt.expression
    assert isinstance(call2, expressions.FuncCall)
    arr_access = call2.callee
    assert isinstance(arr_access, expressions.ArrayAccess)
    call1 = arr_access.array
    assert isinstance(call1, expressions.FuncCall)
    member = call1.callee
    assert isinstance(member, expressions.MemberAccess)
    assert isinstance(member.obj, expressions.Identifier) and member.obj.name == "x"
    assert isinstance(member.member, expressions.Identifier) and member.member.name == "foo"
    assert [type(a) for a in call1.arguments] == [expressions.IntLiteral, expressions.IntLiteral]
    assert isinstance(arr_access.index, expressions.IntLiteral) and arr_access.index.value == 3
    assert call2.arguments == []


def test_assignment_and_compound_assignment():
    prog = parse_program("x += 1; y = x;")
    stmt1, stmt2 = prog.declarations
    assert isinstance(stmt1, statements.ExpressionStmt)
    assert isinstance(stmt1.expression, expressions.AssignExpr)
    assert stmt1.expression.op == "+="
    assert isinstance(stmt2, statements.ExpressionStmt)
    assert isinstance(stmt2.expression, expressions.AssignExpr)
    assert stmt2.expression.op == "="


def test_parenthesized_expression():
    prog = parse_program("var a: int = (1 + 2) * 3;")
    decl = prog.declarations[0]
    assert isinstance(decl, declarations.VarDecl)
    expr = decl.initializer
    assert isinstance(expr, expressions.BinaryOp) and expr.op == "*"
    assert isinstance(expr.left, expressions.BinaryOp) and expr.left.op == "+"
    assert isinstance(expr.right, expressions.IntLiteral) and expr.right.value == 3


def test_parse_error_missing_semicolon_in_var_decl():
    with pytest.raises(ParserError):
        parse_program("var x: int")


def test_parse_error_if_missing_paren():
    with pytest.raises(ParserError):
        parse_program("if x) { return 1; }")


def test_parse_error_param_missing_colon():
    with pytest.raises(ParserError):
        parse_program("func f(a int): int { return 0; }")