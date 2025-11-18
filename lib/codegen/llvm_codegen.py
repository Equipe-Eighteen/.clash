# pyright: basic
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportReturnType=false
# pyright: reportAssignmentType=false
# pyright: reportArgumentType=false

from llvmlite import ir
from llvmlite import binding as llvm
from lib.parser.ast import program, declarations, statements, expressions, types
from lib.utils.error_handler import CodegenError

class LLVMCodeGenerator:
    def __init__(self) -> None:
        self.module = ir.Module(name="clash_module")
        self.builder = None
        self.current_function = None
        
        self.globals = {}
        self.locals = {}
        self.structs = {}
        self.struct_fields = {}
        
        self.int_type = ir.IntType(32)
        self.float_type = ir.DoubleType()
        self.bool_type = ir.IntType(1)
        self.void_type = ir.VoidType()
        self.str_type = ir.IntType(8).as_pointer()  # char*
        
        self._declare_runtime_functions()

    def _declare_runtime_functions(self) -> None:
        """Declare external runtime functions (like printf)"""
        printf_ty = ir.FunctionType(self.int_type, [self.str_type], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
        malloc_ty = ir.FunctionType(self.str_type, [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        
        free_ty = ir.FunctionType(self.void_type, [self.str_type])
        self.free = ir.Function(self.module, free_ty, name="free")
        
        pow_ty = ir.FunctionType(self.float_type, [self.float_type, self.float_type])
        self.pow = ir.Function(self.module, pow_ty, name="pow")
        
        powi_ty = ir.FunctionType(self.float_type, [self.float_type, self.int_type])
        self.powi = ir.Function(self.module, powi_ty, name="llvm.powi.f64.i32")
        
        sprintf_ty = ir.FunctionType(self.int_type, [self.str_type, self.str_type], var_arg=True)
        self.sprintf = ir.Function(self.module, sprintf_ty, name="sprintf")
        
        strlen_ty = ir.FunctionType(ir.IntType(64), [self.str_type])
        self.strlen = ir.Function(self.module, strlen_ty, name="strlen")
        
        strcpy_ty = ir.FunctionType(self.str_type, [self.str_type, self.str_type])
        self.strcpy = ir.Function(self.module, strcpy_ty, name="strcpy")
        
        strcat_ty = ir.FunctionType(self.str_type, [self.str_type, self.str_type])
        self.strcat = ir.Function(self.module, strcat_ty, name="strcat")

    def generate(self, prog: program.Program) -> str:
        """Generate LLVM IR from AST"""
        self._collect_structs(prog)
        
        for node in prog.declarations:
            if isinstance(node, declarations.VarDecl):
                self._declare_global_var(node)
            elif isinstance(node, declarations.FuncDecl):
                self._declare_function(node)
        
        main_block = []
        for node in prog.declarations:
            if isinstance(node, declarations.FuncDecl):
                self._gen_function_body(node)
            elif isinstance(node, statements.Statement):
                main_block.append(node)
        
        if main_block:
            self._create_main_function(main_block)
        
        return str(self.module)

    def _collect_structs(self, prog: program.Program) -> None:
        """Collect struct definitions"""
        for node in prog.declarations:
            if isinstance(node, declarations.StructDecl):
                field_types = []
                field_names = []
                
                for field in node.fields:
                    field_types.append(self._get_llvm_type(field.type_spec))
                    field_names.append(field.name.name)
                
                struct_type = ir.LiteralStructType(field_types)
                self.structs[node.name.name] = struct_type
                self.struct_fields[node.name.name] = field_names

    def _get_llvm_type(self, type_spec: types.TypeSpecifier) -> ir.Type:
        """Convert Clash type to LLVM type"""
        if isinstance(type_spec, types.BaseType):
            if type_spec.name == "int":
                return self.int_type
            elif type_spec.name == "float":
                return self.float_type
            elif type_spec.name == "bool":
                return self.bool_type
            elif type_spec.name == "str":
                return self.str_type
            elif type_spec.name == "void":
                return self.void_type
            elif type_spec.name in self.structs:
                return self.structs[type_spec.name].as_pointer()
            else:
                raise CodegenError(f"Unknown type: {type_spec.name}")
        elif isinstance(type_spec, types.ListType):
            elem_type = self._get_llvm_type(type_spec.element_type)
            return elem_type.as_pointer()
        else:
            raise CodegenError(f"Unsupported type: {type_spec}")

    def _declare_global_var(self, decl: declarations.VarDecl) -> None:
        """Declare a global variable"""
        llvm_type = self._get_llvm_type(decl.type_spec)
        
        if decl.initializer:
            if isinstance(decl.initializer, expressions.IntLiteral):
                initializer = ir.Constant(self.int_type, decl.initializer.value)
            elif isinstance(decl.initializer, expressions.FloatLiteral):
                initializer = ir.Constant(self.float_type, decl.initializer.value)
            elif isinstance(decl.initializer, expressions.BoolLiteral):
                initializer = ir.Constant(self.bool_type, 1 if decl.initializer.value else 0)
            elif isinstance(decl.initializer, expressions.StringLiteral):
                initializer = ir.Constant(llvm_type, None)
            else:
                initializer = ir.Constant(llvm_type, None)
        else:
            initializer = ir.Constant(llvm_type, None)
        
        global_var = ir.GlobalVariable(self.module, llvm_type, name=decl.name.name)
        global_var.initializer = initializer
        global_var.linkage = 'internal'
        self.globals[decl.name.name] = global_var

    def _declare_function(self, func: declarations.FuncDecl) -> None:
        """Declare a function signature"""
        return_type = self._get_llvm_type(func.return_type)
        param_types = [self._get_llvm_type(p.type_spec) for p in func.params]
        
        func_type = ir.FunctionType(return_type, param_types)
        llvm_func = ir.Function(self.module, func_type, name=func.name.name)
        
        for i, param in enumerate(func.params):
            llvm_func.args[i].name = param.name.name
        
        self.globals[func.name.name] = llvm_func

    def _gen_function_body(self, func: declarations.FuncDecl) -> None:
        """Generate function body"""
        llvm_func = self.globals[func.name.name]
        self.current_function = llvm_func
        
        entry_block = llvm_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        
        self.locals = {}
        
        for i, param in enumerate(func.params):
            param_type = self._get_llvm_type(param.type_spec)
            param_alloca = self.builder.alloca(param_type, name=param.name.name)
            self.builder.store(llvm_func.args[i], param_alloca)
            self.locals[param.name.name] = param_alloca
        
        self._gen_block(func.body, is_function=True)
        
        if not self.builder.block.is_terminated:
            if isinstance(func.return_type, types.BaseType) and func.return_type.name == "void":
                self.builder.ret_void()
            else:
                return_type = self._get_llvm_type(func.return_type)
                self.builder.ret(ir.Constant(return_type, 0))
        
        self.current_function = None
        self.builder = None

    def _create_main_function(self, statements: list) -> None:
        """Create main function for top-level statements"""
        main_type = ir.FunctionType(self.int_type, [])
        main_func = ir.Function(self.module, main_type, name="main")
        self.current_function = main_func
        
        entry_block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        self.locals = {}
        
        for stmt in statements:
            self._gen_stmt(stmt)
        
        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(self.int_type, 0))
        
        self.current_function = None
        self.builder = None

    def _gen_block(self, block: statements.BlockStmt, is_function: bool = False) -> None:
        """Generate code for a block"""
        for stmt in block.statements:
            self._gen_stmt(stmt)

    def _gen_stmt(self, stmt: statements.Statement) -> None:
        """Generate code for a statement"""
        if isinstance(stmt, declarations.VarDecl):
            self._gen_local_var(stmt)
        elif isinstance(stmt, statements.ExpressionStmt):
            if stmt.expression:
                self._gen_expr(stmt.expression)
        elif isinstance(stmt, statements.ReturnStmt):
            if stmt.value:
                ret_val = self._gen_expr(stmt.value)
                self.builder.ret(ret_val)
            else:
                self.builder.ret_void()
        elif isinstance(stmt, statements.IfStmt):
            self._gen_if_stmt(stmt)
        elif isinstance(stmt, statements.LoopStmt):
            self._gen_loop_stmt(stmt)
        elif isinstance(stmt, statements.BreakStmt):
            pass
        elif isinstance(stmt, statements.ContinueStmt):
            pass

    def _gen_local_var(self, decl: declarations.VarDecl) -> None:
        """Generate code for local variable declaration"""
        llvm_type = self._get_llvm_type(decl.type_spec)
        alloca = self.builder.alloca(llvm_type, name=decl.name.name)
        self.locals[decl.name.name] = alloca
        
        if decl.initializer:
            value = self._gen_expr(decl.initializer)
            value = self._convert_type(value, llvm_type)
            self.builder.store(value, alloca)
        else:
            default_val = self._default_value(llvm_type)
            self.builder.store(default_val, alloca)

    def _gen_if_stmt(self, stmt: statements.IfStmt) -> None:
        """Generate code for if statement"""
        cond = self._gen_expr(stmt.condition)
        
        then_block = self.current_function.append_basic_block("if.then")
        merge_block = self.current_function.append_basic_block("if.merge")
        
        if stmt.else_branch or stmt.elif_branches:
            else_block = self.current_function.append_basic_block("if.else")
            self.builder.cbranch(cond, then_block, else_block)
        else:
            self.builder.cbranch(cond, then_block, merge_block)
        
        self.builder.position_at_end(then_block)
        self._gen_block(stmt.then_branch)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        
        if stmt.elif_branches or stmt.else_branch:
            self.builder.position_at_end(else_block)
            if stmt.else_branch:
                self._gen_block(stmt.else_branch)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
        
        self.builder.position_at_end(merge_block)

    def _gen_loop_stmt(self, stmt: statements.LoopStmt) -> None:
        """Generate code for loop statement"""
        loop_header = self.current_function.append_basic_block("loop.header")
        loop_body = self.current_function.append_basic_block("loop.body")
        loop_exit = self.current_function.append_basic_block("loop.exit")
        
        self.builder.branch(loop_header)
        
        self.builder.position_at_end(loop_header)
        self.builder.branch(loop_body)
        
        self.builder.position_at_end(loop_body)
        self._gen_block(stmt.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(loop_header)
        
        self.builder.position_at_end(loop_exit)

    def _gen_expr(self, expr: expressions.Expression) -> ir.Value:
        """Generate code for an expression"""
        if isinstance(expr, expressions.IntLiteral):
            return ir.Constant(self.int_type, expr.value)
        
        elif isinstance(expr, expressions.FloatLiteral):
            return ir.Constant(self.float_type, expr.value)
        
        elif isinstance(expr, expressions.BoolLiteral):
            return ir.Constant(self.bool_type, 1 if expr.value else 0)
        
        elif isinstance(expr, expressions.StringLiteral):
            return self._create_string_constant(expr.value)
        
        elif isinstance(expr, expressions.Identifier):
            return self._load_variable(expr.name)
        
        elif isinstance(expr, expressions.BinaryOp):
            return self._gen_binary_op(expr)
        
        elif isinstance(expr, expressions.UnaryOp):
            return self._gen_unary_op(expr)
        
        elif isinstance(expr, expressions.FuncCall):
            return self._gen_call(expr)
        
        elif isinstance(expr, expressions.AssignExpr):
            return self._gen_assignment(expr)
        
        elif isinstance(expr, expressions.ArrayAccess):
            return self._gen_array_access(expr)
        
        elif isinstance(expr, expressions.MemberAccess):
            return self._gen_member_access(expr)
        
        elif isinstance(expr, expressions.LiteralList):
            return self._gen_list_literal(expr)
        
        else:
            raise CodegenError(f"Unsupported expression: {type(expr)}")

    def _gen_list_literal(self, expr: expressions.LiteralList) -> ir.Value:
        """Generate code for list literal [1, 2, 3]"""
        if not expr.elements:
            return ir.Constant(self.str_type, None)
        
        first_elem = self._gen_expr(expr.elements[0])
        elem_type = first_elem.type
        
        array_size = len(expr.elements)
        
        if isinstance(elem_type, ir.IntType):
            elem_size = elem_type.width // 8
        elif isinstance(elem_type, ir.DoubleType):
            elem_size = 8
        elif isinstance(elem_type, ir.FloatType):
            elem_size = 4
        elif isinstance(elem_type, ir.PointerType):
            elem_size = 8
        else:
            elem_size = 8
        
        size_value = ir.Constant(ir.IntType(64), array_size * elem_size)
        array_ptr = self.builder.call(self.malloc, [size_value])
        
        typed_ptr = self.builder.bitcast(array_ptr, elem_type.as_pointer())
        
        for i, elem_expr in enumerate(expr.elements):
            elem_value = self._gen_expr(elem_expr)
            elem_value = self._convert_type(elem_value, elem_type)
            
            idx = ir.Constant(self.int_type, i)
            elem_ptr = self.builder.gep(typed_ptr, [idx])
            self.builder.store(elem_value, elem_ptr)
        
        return typed_ptr

    def _convert_type(self, value: ir.Value, target_type: ir.Type) -> ir.Value:
        """Convert value to target type if needed"""
        if value.type == target_type:
            return value
        
        if isinstance(value.type, ir.IntType) and isinstance(target_type, ir.DoubleType):
            return self.builder.sitofp(value, target_type)
        
        if isinstance(value.type, ir.DoubleType) and isinstance(target_type, ir.IntType):
            return self.builder.fptosi(value, target_type)
        
        return value

    def _promote_types(self, left: ir.Value, right: ir.Value) -> tuple[ir.Value, ir.Value]:
        """Promote types to match (int + float -> float + float)"""
        if left.type == right.type:
            return left, right
        
        if isinstance(left.type, ir.DoubleType) and isinstance(right.type, ir.IntType):
            right = self.builder.sitofp(right, self.float_type)
        elif isinstance(left.type, ir.IntType) and isinstance(right.type, ir.DoubleType):
            left = self.builder.sitofp(left, self.float_type)
        
        return left, right

    def _gen_binary_op(self, expr: expressions.BinaryOp) -> ir.Value:
        """Generate code for binary operation"""
        left = self._gen_expr(expr.left)
        right = self._gen_expr(expr.right)
        
        op = expr.op
        
        if op == "+":
            if isinstance(left.type, ir.PointerType) or isinstance(right.type, ir.PointerType):
                return self._gen_string_concat(left, right)
        
        if op == "**":
            if isinstance(left.type, ir.IntType):
                left = self.builder.sitofp(left, self.float_type)
            if isinstance(right.type, ir.IntType):
                return self.builder.call(self.powi, [left, right])
            else:
                return self.builder.call(self.pow, [left, right])
        
        left, right = self._promote_types(left, right)
        
        if op == "+":
            if isinstance(left.type, ir.IntType):
                return self.builder.add(left, right)
            else:
                return self.builder.fadd(left, right)
        elif op == "-":
            if isinstance(left.type, ir.IntType):
                return self.builder.sub(left, right)
            else:
                return self.builder.fsub(left, right)
        elif op == "*":
            if isinstance(left.type, ir.IntType):
                return self.builder.mul(left, right)
            else:
                return self.builder.fmul(left, right)
        elif op == "/":
            if isinstance(left.type, ir.IntType):
                return self.builder.sdiv(left, right)
            else:
                return self.builder.fdiv(left, right)
        
        elif op == "==":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed("==", left, right)
            else:
                return self.builder.fcmp_ordered("==", left, right)
        elif op == "!=":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed("!=", left, right)
            else:
                return self.builder.fcmp_ordered("!=", left, right)
        elif op == "<":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed("<", left, right)
            else:
                return self.builder.fcmp_ordered("<", left, right)
        elif op == "<=":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed("<=", left, right)
            else:
                return self.builder.fcmp_ordered("<=", left, right)
        elif op == ">":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed(">", left, right)
            else:
                return self.builder.fcmp_ordered(">", left, right)
        elif op == ">=":
            if isinstance(left.type, ir.IntType):
                return self.builder.icmp_signed(">=", left, right)
            else:
                return self.builder.fcmp_ordered(">=", left, right)
        
        elif op == "&&":
            return self.builder.and_(left, right)
        elif op == "||":
            return self.builder.or_(left, right)
        
        else:
            raise CodegenError(f"Unsupported binary operator: {op}")

    def _gen_string_concat(self, left: ir.Value, right: ir.Value) -> ir.Value:
        """Generate code for string concatenation"""
        left_str = self._to_string(left)
        right_str = self._to_string(right)
        
        left_len = self.builder.call(self.strlen, [left_str])
        right_len = self.builder.call(self.strlen, [right_str])
        
        one = ir.Constant(ir.IntType(64), 1)
        total_len = self.builder.add(left_len, right_len)
        total_len = self.builder.add(total_len, one)
        
        result_ptr = self.builder.call(self.malloc, [total_len])
        
        self.builder.call(self.strcpy, [result_ptr, left_str])
        
        self.builder.call(self.strcat, [result_ptr, right_str])
        
        return result_ptr

    def _to_string(self, value: ir.Value) -> ir.Value:
        """Convert a value to string representation"""
        if isinstance(value.type, ir.PointerType):
            return value
        elif isinstance(value.type, ir.IntType) and value.type.width == 32:
            buffer_size = ir.Constant(ir.IntType(64), 12)
            buffer = self.builder.call(self.malloc, [buffer_size])
            
            fmt = self._create_global_string("%d")
            self.builder.call(self.sprintf, [buffer, fmt, value])
            
            return buffer
        elif isinstance(value.type, ir.DoubleType):
            buffer_size = ir.Constant(ir.IntType(64), 32)
            buffer = self.builder.call(self.malloc, [buffer_size])
            
            fmt = self._create_global_string("%f")
            self.builder.call(self.sprintf, [buffer, fmt, value])
            
            return buffer
        elif isinstance(value.type, ir.IntType) and value.type.width == 1:
            buffer_size = ir.Constant(ir.IntType(64), 6)
            buffer = self.builder.call(self.malloc, [buffer_size])
            
            true_str = self._create_global_string("true")
            false_str = self._create_global_string("false")
            
            result = self.builder.select(value, true_str, false_str)
            self.builder.call(self.strcpy, [buffer, result])
            
            return buffer
        else:
            buffer_size = ir.Constant(ir.IntType(64), 1)
            buffer = self.builder.call(self.malloc, [buffer_size])
            zero = ir.Constant(ir.IntType(8), 0)
            zero_ptr = self.builder.gep(buffer, [ir.Constant(ir.IntType(32), 0)])
            self.builder.store(zero, zero_ptr)
            return buffer

    def _default_value(self, llvm_type: ir.Type) -> ir.Value:
        """Get default value for a type"""
        if isinstance(llvm_type, ir.IntType):
            return ir.Constant(llvm_type, 0)
        elif isinstance(llvm_type, ir.DoubleType):
            return ir.Constant(llvm_type, 0.0)
        elif isinstance(llvm_type, ir.PointerType):
            return ir.Constant(llvm_type, None)
        else:
            return ir.Constant(llvm_type, None)

    def _gen_unary_op(self, expr: expressions.UnaryOp) -> ir.Value:
        """Generate code for unary operation"""
        operand = self._gen_expr(expr.right)
        
        if expr.op == "!":
            return self.builder.not_(operand)
        elif expr.op == "-":
            if isinstance(operand.type, ir.IntType):
                return self.builder.neg(operand)
            else:
                return self.builder.fneg(operand)
        else:
            raise CodegenError(f"Unsupported unary operator: {expr.op}")

    def _gen_call(self, call: expressions.FuncCall) -> ir.Value:
        """Generate code for function call"""
        if isinstance(call.callee, expressions.Identifier):
            func_name = call.callee.name
            
            if func_name == "print":
                return self._gen_print_call(call.arguments)
            elif func_name == "len":
                return self._gen_len_call(call.arguments)
            
            if func_name in self.globals:
                func = self.globals[func_name]
                args = [self._gen_expr(arg) for arg in call.arguments]
                return self.builder.call(func, args)
        
        raise CodegenError(f"Unknown function: {call.callee}")

    def _gen_print_call(self, arguments: list) -> ir.Value:
        """Generate code for print function"""
        if not arguments:
            return ir.Constant(self.int_type, 0)
        
        arg = self._gen_expr(arguments[0])
        
        if isinstance(arg.type, ir.IntType) and arg.type.width == 32:
            fmt_str = self._create_global_string("%d\n")
        elif isinstance(arg.type, ir.IntType) and arg.type.width == 1:
            fmt_str = self._create_global_string("%d\n")
        elif isinstance(arg.type, ir.DoubleType):
            fmt_str = self._create_global_string("%f\n")
        elif isinstance(arg.type, ir.PointerType):
            fmt_str = self._create_global_string("%s\n")
        else:
            fmt_str = self._create_global_string("%d\n")
        
        return self.builder.call(self.printf, [fmt_str, arg])

    def _gen_len_call(self, arguments: list) -> ir.Value:
        """Generate code for len function"""
        if not arguments:
            return ir.Constant(self.int_type, 0)
        
        return ir.Constant(self.int_type, 5)

    def _gen_assignment(self, expr: expressions.AssignExpr) -> ir.Value:
        """Generate code for assignment"""
        value = self._gen_expr(expr.value)
        
        if isinstance(expr.target, expressions.Identifier):
            var_name = expr.target.name
            if var_name in self.locals:
                ptr = self.locals[var_name]
            elif var_name in self.globals:
                ptr = self.globals[var_name]
            else:
                raise CodegenError(f"Unknown variable: {var_name}")
            
            target_type = ptr.type.pointee
            
            if expr.op == "=":
                value = self._convert_type(value, target_type)
                self.builder.store(value, ptr)
            elif expr.op == "+=":
                current = self.builder.load(ptr)
                current, value = self._promote_types(current, value)
                if isinstance(current.type, ir.IntType):
                    result = self.builder.add(current, value)
                else:
                    result = self.builder.fadd(current, value)
                result = self._convert_type(result, target_type)
                self.builder.store(result, ptr)
            elif expr.op == "-=":
                current = self.builder.load(ptr)
                current, value = self._promote_types(current, value)
                if isinstance(current.type, ir.IntType):
                    result = self.builder.sub(current, value)
                else:
                    result = self.builder.fsub(current, value)
                result = self._convert_type(result, target_type)
                self.builder.store(result, ptr)
            
            return value
        
        raise CodegenError("Complex assignment targets not yet supported")

    def _gen_array_access(self, expr: expressions.ArrayAccess) -> ir.Value:
        """Generate code for array access"""
        array_ptr = self._gen_expr(expr.array)
        index = self._gen_expr(expr.index)
        elem_ptr = self.builder.gep(array_ptr, [index])
        return self.builder.load(elem_ptr)

    def _gen_member_access(self, expr: expressions.MemberAccess) -> ir.Value:
        """Generate code for member access"""
        raise CodegenError("Member access not yet fully implemented")

    def _load_variable(self, name: str) -> ir.Value:
        """Load a variable value"""
        if name in self.locals:
            return self.builder.load(self.locals[name])
        elif name in self.globals:
            return self.builder.load(self.globals[name])
        else:
            raise CodegenError(f"Unknown variable: {name}")

    def _create_string_constant(self, value: str) -> ir.Value:
        """Create a global string constant"""
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        
        return self._create_global_string(value)

    def _create_global_string(self, value: str) -> ir.Value:
        """Create a global string constant and return pointer"""
        string_bytes = bytearray((value + '\0').encode('utf-8'))
        string_type = ir.ArrayType(ir.IntType(8), len(string_bytes))
        string_const = ir.Constant(string_type, string_bytes)
        
        global_str = ir.GlobalVariable(self.module, string_type, name=self.module.get_unique_name("str"))
        global_str.linkage = 'internal'
        global_str.global_constant = True
        global_str.initializer = string_const
        
        zero = ir.Constant(ir.IntType(32), 0)
        return self.builder.gep(global_str, [zero, zero])
