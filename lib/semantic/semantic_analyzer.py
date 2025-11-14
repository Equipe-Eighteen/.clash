from typing import Optional
from lib.parser.ast import program, declarations, statements, expressions, types
from lib.utils.error_handler import SemanticError
from lib.semantic.symbols_table import (
    SymbolTable,
    VariableSymbol,
    FunctionSymbol,
    StructSymbol,
)

class SemanticAnalyzer:
    def __init__(self, symbol_table: Optional[SymbolTable] = None) -> None:
        self.symbol_table: SymbolTable = symbol_table if symbol_table is not None else SymbolTable()
        self.errors: list[str] = []
        self._function_return_stack: list[types.TypeSpecifier] = []
        self._loop_depth: int = 0
        self._install_builtins()

    def analyze(self, prog: program.Program) -> list[str]:
        for node in prog.declarations:
            self._analyze_toplevel(node)
        return self.errors

    def _install_builtins(self) -> None:
        void_t = types.BaseType(name="void")
        int_t = types.BaseType(name="int")
        self.symbol_table.define(FunctionSymbol(name="print", params=[], return_type=void_t))
        self.symbol_table.define(FunctionSymbol(name="len", params=[], return_type=int_t))

    def _report(self, message: str, node: Optional[object] = None) -> None:
        line = getattr(node, "line", 1)
        column = getattr(node, "col", 1)
        self.errors.append(str(SemanticError(message, line=line, column=column, node=node)))

    def _analyze_toplevel(self, node: object) -> None:
        if isinstance(node, declarations.StructDecl):
            self._analyze_struct_decl(node)
        elif isinstance(node, declarations.FuncDecl):
            self._declare_func(node)
        elif isinstance(node, declarations.VarDecl):
            self._analyze_var_decl(node)
        elif isinstance(node, statements.Statement):
            self._analyze_statement(node)
        else:
            self._report("Unknown top-level node.", node=node)

    def _analyze_struct_decl(self, decl: declarations.StructDecl) -> None:
        struct_name = decl.name.name
        if self.symbol_table.lookup_in_current(struct_name) is not None:
            self._report(f"Redeclaration of symbol '{struct_name}'.", node=decl.name)
            return
        field_map: dict[str, types.TypeSpecifier] = {}
        for field in decl.fields:
            fname = field.name.name
            if fname in field_map:
                self._report(f"Duplicate field '{fname}' in struct '{struct_name}'.", node=field)
                continue
            field_map[fname] = field.type_spec
        self.symbol_table.define(StructSymbol(name=struct_name, fields=field_map))

    def _declare_func(self, func: declarations.FuncDecl) -> None:
        name = func.name.name
        if self.symbol_table.lookup_in_current(name) is not None:
            self._report(f"Redeclaration of symbol '{name}'.", node=func.name)
            return
        self.symbol_table.define(FunctionSymbol(name=name, params=func.params, return_type=func.return_type))
        self._analyze_function_body(func)

    def _analyze_function_body(self, func: declarations.FuncDecl) -> None:
        self.symbol_table.begin_scope()
        for p in func.params:
            pname = p.name.name
            if self.symbol_table.lookup_in_current(pname) is not None:
                self._report(f"Redeclaration of parameter '{pname}' in function '{func.name.name}'.", node=p.name)
                continue
            self.symbol_table.define(VariableSymbol(name=pname, type_spec=p.type_spec))
        self._function_return_stack.append(func.return_type)
        self._analyze_block(func.body)
        self._function_return_stack.pop()
        self.symbol_table.end_scope()

    def _analyze_var_decl(self, decl: declarations.VarDecl) -> None:
        name = decl.name.name
        if self.symbol_table.lookup_in_current(name) is not None:
            self._report(f"Redeclaration of symbol '{name}'.", node=decl.name)
        else:
            self.symbol_table.define(VariableSymbol(name=name, type_spec=decl.type_spec))
        if decl.initializer is not None:
            # Handle list literal with a known list target type
            if isinstance(decl.type_spec, types.ListType) and isinstance(decl.initializer, expressions.LiteralList):
                self._check_list_literal_assignment(decl.type_spec, decl.initializer)
                return
            init_t = self._type_of_expression(decl.initializer)
            if init_t is None:
                if isinstance(decl.initializer, expressions.StructLiteral):
                    self._check_struct_literal_assignment(decl.type_spec, decl.initializer)
                return
            if not self._is_assignable(decl.type_spec, init_t):
                self._report(
                    f"Type mismatch in variable initialization of '{name}' (expected {self._type_str(decl.type_spec)}, got {self._type_str(init_t)}).",
                    node=decl
                )

    def _analyze_block(self, block: statements.BlockStmt) -> None:
        self.symbol_table.begin_scope()
        for st in block.statements:
            self._analyze_statement(st)
        self.symbol_table.end_scope()

    def _analyze_statement(self, st: statements.Statement) -> None:
        if isinstance(st, declarations.VarDecl):
            self._analyze_var_decl(st)
        elif isinstance(st, statements.BlockStmt):
            self._analyze_block(st)
        elif isinstance(st, statements.ExpressionStmt):
            if st.expression is not None:
                self._type_of_expression(st.expression)
        elif isinstance(st, statements.ReturnStmt):
            self._check_return_stmt(st)
        elif isinstance(st, statements.BreakStmt):
            if self._loop_depth <= 0:
                self._report("Break used outside of loop.", node=st)
        elif isinstance(st, statements.ContinueStmt):
            if self._loop_depth <= 0:
                self._report("Continue used outside of loop.", node=st)
        elif isinstance(st, statements.LoopStmt):
            self._loop_depth += 1
            self._analyze_block(st.body)
            self._loop_depth -= 1
        elif isinstance(st, statements.IfStmt):
            self._analyze_if_stmt(st)
        else:
            self._report("Unknown statement.", node=st)

    def _analyze_if_stmt(self, node: statements.IfStmt) -> None:
        cond_t = self._type_of_expression(node.condition)
        if not self._is_bool(cond_t):
            self._report("If condition must be 'bool'.", node=node.condition)
        self._analyze_block(node.then_branch)
        for br in node.elif_branches:
            c = self._type_of_expression(br.condition)
            if not self._is_bool(c):
                self._report("Elif condition must be 'bool'.", node=br.condition)
            self._analyze_block(br.body)
        if node.else_branch is not None:
            self._analyze_block(node.else_branch)

    def _check_return_stmt(self, st: statements.ReturnStmt) -> None:
        if not self._function_return_stack:
            self._report("Return used outside of function.", node=st)
            return
        expected = self._function_return_stack[-1]
        if st.value is None:
            if not self._is_void(expected):
                self._report(f"Missing return value (expected {self._type_str(expected)}).", node=st)
            return
        got = self._type_of_expression(st.value)
        if got is None:
            self._report("Could not infer return type.", node=st.value or st)
            return
        if not self._is_assignable(expected, got):
            self._report(f"Return type mismatch (expected {self._type_str(expected)}, got {self._type_str(got)}).", node=st)

    def _type_of_expression(self, expr: expressions.Expression) -> Optional[types.TypeSpecifier]:
        if isinstance(expr, expressions.Identifier):
            sym = self.symbol_table.lookup(expr.name)
            if sym is None:
                self._report(f"Undeclared identifier '{expr.name}'.", node=expr)
                return None
            if isinstance(sym, VariableSymbol):
                return sym.type_spec
            if isinstance(sym, FunctionSymbol):
                return sym.return_type
            if isinstance(sym, StructSymbol):
                return types.BaseType(name=sym.name)
            return None

        if isinstance(expr, expressions.IntLiteral):
            return types.BaseType(name="int")
        if isinstance(expr, expressions.FloatLiteral):
            return types.BaseType(name="float")
        if isinstance(expr, expressions.StringLiteral):
            return types.BaseType(name="str")
        if isinstance(expr, expressions.BoolLiteral):
            return types.BaseType(name="bool")

        if isinstance(expr, expressions.LiteralList):
            if len(expr.elements) == 0:
                self._report("Cannot infer element type of empty list literal.", node=expr)
                return types.ListType(element_type=types.BaseType(name="void"))
            first_t = self._type_of_expression(expr.elements[0])
            if first_t is None:
                self._report("Cannot infer element type of list literal.", node=expr)
                return types.ListType(element_type=types.BaseType(name="void"))
            for el in expr.elements[1:]:
                et = self._type_of_expression(el)
                if et is None or not self._is_assignable(first_t, et):
                    self._report("List literal elements must have a compatible type.", node=el)
                    break
            return types.ListType(element_type=first_t)

        if isinstance(expr, expressions.StructLiteral):
            return None

        if isinstance(expr, expressions.AssignExpr):
            target_t = self._type_of_expression(expr.target) if hasattr(expr, "target") else None
            value_t = self._type_of_expression(expr.value) if hasattr(expr, "value") else None
            op = getattr(expr, "op", "=")
            if op == "=":
                if isinstance(target_t, types.ListType) and isinstance(expr.value, expressions.LiteralList):
                    self._check_list_literal_assignment(target_t, expr.value)
                    return target_t
                if isinstance(expr.value, expressions.StructLiteral) and target_t is not None:
                    self._check_struct_literal_assignment(target_t, expr.value)
                    return target_t
                if target_t is not None and value_t is not None and not self._is_assignable(target_t, value_t):
                    self._report(
                        f"Type mismatch in assignment (expected {self._type_str(target_t)}, got {self._type_str(value_t)}).",
                        node=expr
                    )
                return target_t
            if target_t is None or value_t is None:
                self._report("Could not infer types in compound assignment.", node=expr)
                return target_t
            bin_op = op[:-1]
            res_t = self._binary_result_type(bin_op, target_t, value_t)
            if res_t is None or not self._is_assignable(target_t, res_t):
                self._report(
                    f"Incompatible types for '{op}' (left {self._type_str(target_t)}, right {self._type_str(value_t)}).",
                    node=expr
                )
            return target_t

        if isinstance(expr, expressions.BinaryOp):
            left_t = self._type_of_expression(expr.left) if hasattr(expr, "left") else None
            right_t = self._type_of_expression(expr.right) if hasattr(expr, "right") else None
            op = getattr(expr, "op", "")
            if left_t is None or right_t is None:
                self._report("Could not infer operand type for binary operation.", node=expr)
                return None
            res_t = self._binary_result_type(op, left_t, right_t)
            if res_t is None:
                self._report(
                    f"Incompatible types for '{op}' (left {self._type_str(left_t)}, right {self._type_str(right_t)}).",
                    node=expr
                )
            return res_t

        if isinstance(expr, expressions.UnaryOp):
            op = getattr(expr, "op", "")
            right_t = self._type_of_expression(expr.right) if hasattr(expr, "right") else None
            if op == "!":
                if not self._is_bool(right_t):
                    self._report("Operator '!' expects operand of type 'bool'.", node=expr)
                return types.BaseType(name="bool")
            if op == "-":
                if not self._is_number(right_t):
                    self._report("Unary '-' expects numeric operand.", node=expr)
                    return None
                return right_t
            self._report("Unknown unary operator.", node=expr)
            return None

        if isinstance(expr, expressions.MemberAccess):
            obj_t = self._type_of_expression(expr.obj) if hasattr(expr, "obj") else None
            mem = getattr(getattr(expr, "member", None), "name", "")
            if isinstance(obj_t, types.ListType):
                if mem == "length":
                    return types.BaseType(name="int")
                self._report(f"List type has no member '{mem}'.", node=expr)
                return None
            if isinstance(obj_t, types.BaseType):
                sym = self.symbol_table.lookup(obj_t.name)
                if isinstance(sym, StructSymbol):
                    if mem in sym.fields:
                        return sym.fields[mem]
                    self._report(f"Struct '{obj_t.name}' has no field '{mem}'.", node=expr)
                    return None
            self._report("Member access on non-struct type.", node=expr)
            return None

        if isinstance(expr, expressions.ArrayAccess):
            arr_t = self._type_of_expression(expr.array) if hasattr(expr, "array") else None
            idx_t = self._type_of_expression(expr.index) if hasattr(expr, "index") else None
            if not self._is_number(idx_t) and not self._is_int(idx_t):
                self._report("Array index must be of type 'int'.", node=expr.index if hasattr(expr, "index") else expr)
            if isinstance(arr_t, types.ListType):
                return arr_t.element_type
            self._report("Subscript operator used on non-list type.", node=expr)
            return None

        if isinstance(expr, expressions.FuncCall):
            callee_t = self._type_of_expression(expr.callee) if hasattr(expr, "callee") else None
            args = list(getattr(expr, "arguments", []))
            if isinstance(expr.callee, expressions.Identifier) and expr.callee.name == "print":
                for a in args:
                    self._type_of_expression(a)
                return types.BaseType(name="void")
            if isinstance(expr.callee, expressions.Identifier) and expr.callee.name == "len":
                if len(args) != 1:
                    self._report(f"'len' expects 1 argument, got {len(args)}.", node=expr)
                    for a in args:
                        self._type_of_expression(a)
                    return types.BaseType(name="int")
                at = self._type_of_expression(args[0])
                if isinstance(at, types.ListType) or (isinstance(at, types.BaseType) and at.name == "str"):
                    return types.BaseType(name="int")
                self._report("Argument to 'len' must be a list or 'str'.", node=args[0] if args else expr)
                return types.BaseType(name="int")
            if isinstance(expr.callee, expressions.Identifier):
                sym = self.symbol_table.lookup(expr.callee.name)
                if isinstance(sym, FunctionSymbol):
                    if len(sym.params) != len(args):
                        self._report(f"Function '{sym.name}' expects {len(sym.params)} arguments, got {len(args)}.", node=expr)
                    for p, a in zip(sym.params, args):
                        # If argument is a list literal and parameter is list-typed, validate elements against parameter element type
                        if isinstance(a, expressions.LiteralList) and isinstance(p.type_spec, types.ListType):
                            self._check_list_literal_assignment(p.type_spec, a)
                            continue
                        # If argument is struct literal and parameter is a struct type, validate fields
                        if isinstance(a, expressions.StructLiteral) and isinstance(p.type_spec, types.BaseType):
                            self._check_struct_literal_assignment(p.type_spec, a)
                            continue
                        at = self._type_of_expression(a)
                        if at is None:
                            continue
                        if not self._is_assignable(p.type_spec, at):
                            self._report(f"Argument type mismatch for '{sym.name}' (expected {self._type_str(p.type_spec)}, got {self._type_str(at)}).", node=a)
                    return sym.return_type
                self._report("Call target is not a function.", node=expr.callee)
                return None
            return callee_t

        return None

    def _check_struct_literal_assignment(self, target_t: types.TypeSpecifier, lit: expressions.StructLiteral) -> None:
        if not isinstance(target_t, types.BaseType):
            self._report("Struct literal assigned to non-struct type.", node=lit)
            return
        sym = self.symbol_table.lookup(target_t.name)
        if not isinstance(sym, StructSymbol):
            self._report("Struct literal assigned to non-struct type.", node=lit)
            return
        provided: dict[str, expressions.Expression] = {}
        for field_init in getattr(lit, "fields", []):
            fname = field_init.name.name if isinstance(field_init.name, expressions.Identifier) else ""
            provided[fname] = field_init.value
        for fname, ftype in sym.fields.items():
            if fname not in provided:
                self._report(f"Missing field '{fname}' for struct '{sym.name}'.", node=lit)
                continue
            vt = self._type_of_expression(provided[fname])
            if vt is None or not self._is_assignable(ftype, vt):
                self._report(f"Incompatible type for field '{fname}' in struct '{sym.name}' (expected {self._type_str(ftype)}, got {self._type_str(vt)}).", node=provided[fname])

    def _check_list_literal_assignment(self, target_t: types.ListType, lit: expressions.LiteralList) -> None:
        elem_t = target_t.element_type
        for el in lit.elements:
            if isinstance(el, expressions.StructLiteral):
                if isinstance(elem_t, types.BaseType):
                    self._check_struct_literal_assignment(elem_t, el)
                else:
                    self._report("Struct literal assigned to non-struct element type in list.", node=el)
            else:
                at = self._type_of_expression(el)
                if at is None:
                    self._report("Could not infer element type in list literal.", node=el)
                    continue
                if not self._is_assignable(elem_t, at):
                    self._report(f"Incompatible list element type (expected {self._type_str(elem_t)}, got {self._type_str(at)}).", node=el)

    def _binary_result_type(
        self,
        op: str,
        left: types.TypeSpecifier,
        right: types.TypeSpecifier,
    ) -> Optional[types.TypeSpecifier]:
        if op in ("&&", "||"):
            if self._is_bool(left) and self._is_bool(right):
                return types.BaseType(name="bool")
            return None
        if op in ("==", "!=", "<", "<=", ">", ">="):
            if (self._is_number(left) and self._is_number(right)) or (self._is_str(left) and self._is_str(right)) or (self._is_bool(left) and self._is_bool(right)):
                return types.BaseType(name="bool")
            return None
        if op in ("+", "-", "*", "/", "%", "**"):
            if op == "+" and (self._is_str(left) or self._is_str(right)):
                return types.BaseType(name="str")
            if self._is_number(left) and self._is_number(right):
                if self._is_float(left) or self._is_float(right):
                    return types.BaseType(name="float")
                return types.BaseType(name="int")
            return None
        return None

    def _is_assignable(self, target: types.TypeSpecifier, value: types.TypeSpecifier) -> bool:
        if isinstance(target, types.BaseType) and isinstance(value, types.BaseType):
            if target.name == value.name:
                return True
            if target.name == "float" and value.name == "int":
                return True
            return False
        if isinstance(target, types.ListType) and isinstance(value, types.ListType):
            return self._is_assignable(target.element_type, value.element_type)
        return False

    def _type_str(self, t: Optional[types.TypeSpecifier]) -> str:
        if t is None:
            return "unknown"
        if isinstance(t, types.BaseType):
            return t.name
        if isinstance(t, types.ListType):
            return f"list[{self._type_str(t.element_type)}]"
        return "type"

    def _is_void(self, t: types.TypeSpecifier) -> bool:
        return isinstance(t, types.BaseType) and t.name == "void"

    def _is_bool(self, t: Optional[types.TypeSpecifier]) -> bool:
        return isinstance(t, types.BaseType) and t.name == "bool" if t is not None else False

    def _is_str(self, t: Optional[types.TypeSpecifier]) -> bool:
        return isinstance(t, types.BaseType) and t.name == "str" if t is not None else False

    def _is_int(self, t: Optional[types.TypeSpecifier]) -> bool:
        return isinstance(t, types.BaseType) and t.name == "int" if t is not None else False

    def _is_float(self, t: Optional[types.TypeSpecifier]) -> bool:
        return isinstance(t, types.BaseType) and t.name == "float" if t is not None else False

    def _is_number(self, t: Optional[types.TypeSpecifier]) -> bool:
        return self._is_int(t) or self._is_float(t)
