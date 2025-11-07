from typing import List, Optional
from lib.lexer.token import Token, TokenType
from lib.parser.ast import program, declarations, statements, expressions, types
from lib.utils.error_handler import ParserError

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> program.Program:
        prog_node = program.Program()

        while not self.is_at_end():
            self.skip_trivia()
            if self.is_at_end():
                break
            prog_node.declarations.append(self.parse_toplevel())

        return prog_node
    
    def parse_toplevel(self):
        if self.check(TokenType.VAR) or self.check(TokenType.FUNC) or self.check(TokenType.STRUCT):
            return self.parse_declaration()
        return self.parse_statement()

    def parse_declaration(self) -> declarations.Declaration:
        if self.match(TokenType.VAR):
            return self.parse_var_declaration()
        if self.match(TokenType.FUNC):
            return self.parse_func_declaration()
        if self.match(TokenType.STRUCT):
            return self.parse_struct_declaration()

        raise ParserError(
            "Unexpected token. Expected 'var', 'func' or 'struct'.",
            line=self.peek().line,
            column=self.peek().column,
            token=self.peek()
        )

    # region --- Declarations ---

    def parse_var_declaration(self) -> declarations.VarDecl:
        name_token = self.consume(TokenType.IDENTIFIER, "Expected a name for the variable.")
        name_node = expressions.Identifier(name=name_token.value)

        self.consume(TokenType.COLON, "Expected ':' after the name of the variable.")

        type_spec = self.parse_type_specifier()
        
        initializer: Optional[expressions.Expression] = None
        if self.match(TokenType.EQUALS):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after the variable declaration.")

        return declarations.VarDecl(name=name_node, type_spec=type_spec, initializer=initializer)

    def parse_func_declaration(self) -> declarations.FuncDecl:
        name_tok = self.consume(TokenType.IDENTIFIER, "Expected a name for the function.")
        name_node = expressions.Identifier(name=name_tok.value)

        self.consume(TokenType.LPAREN, "Expected '(' after the name of the function.")

        params: List[declarations.ParamDecl] = []
        if not self.check(TokenType.RPAREN):
            params.append(self.parse_param_decl())
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RPAREN):
                    break
                params.append(self.parse_param_decl())

        self.consume(TokenType.RPAREN, "Expected ')' after the parameter list.")
        self.consume(TokenType.COLON, "Expected ':' after ')'.")
        return_type = self.parse_type_specifier()

        body = self.parse_block_stmt()

        return declarations.FuncDecl(name=name_node, return_type=return_type, body=body, params=params)

    def parse_param_decl(self) -> declarations.ParamDecl:
        name_tok = self.consume(TokenType.IDENTIFIER, "Expected the name of the parameter.")
        self.consume(TokenType.COLON, "Expected ':' after the name of the parameter.")
        type_spec = self.parse_type_specifier()
        return declarations.ParamDecl(name=expressions.Identifier(name_tok.value), type_spec=type_spec)

    def parse_struct_declaration(self) -> declarations.StructDecl:
        name_token = self.consume(TokenType.IDENTIFIER, "Expected a name for the struct.")
        name_node = expressions.Identifier(name=name_token.value)

        self.consume(TokenType.LBRACE, "Expected '{' after the name of the struct.")

        fields: List[declarations.FieldDecl] = []
        if not self.check(TokenType.RBRACE):
            fields.append(self.parse_field_decl())
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RBRACE):
                    break
                fields.append(self.parse_field_decl())

        self.consume(TokenType.RBRACE, "Expected '}' after the fields of the struct.")
        self.consume(TokenType.SEMICOLON, "Expected ';' after the struct declaration.")

        return declarations.StructDecl(name=name_node, fields=fields)

    def parse_field_decl(self) -> declarations.FieldDecl:
        name_token = self.consume(TokenType.IDENTIFIER, "Expected a name for the field of the struct.")
        name_node = expressions.Identifier(name=name_token.value)

        self.consume(TokenType.COLON, "Expected ':' after the name of the field.")

        type_spec = self.parse_type_specifier()
        
        return declarations.FieldDecl(name=name_node, type_spec=type_spec)
    
    # endregion

    # region --- Type Analyzer ---

    def parse_type_specifier(self) -> types.TypeSpecifier:
        if self.match(TokenType.LIST_TYPE):
            self.consume(TokenType.LBRACKET, "Expected '[' after 'list'.")
            element_type = self.parse_type_specifier()
            self.consume(TokenType.RBRACKET, "Expected ']' after the list type.")
            return types.ListType(element_type=element_type)

        if self.match(
            TokenType.VOID_TYPE,
            TokenType.INT_TYPE,
            TokenType.FLOAT_TYPE,
            TokenType.BOOL_TYPE,
            TokenType.STR_TYPE,
            TokenType.IDENTIFIER
        ):
            base_type_name = self.previous().value
            return types.BaseType(name=base_type_name)

        raise ParserError(
            "Expected a type specifier (int, str, list, etc).",
            line=self.peek().line,
            column=self.peek().column,
            token=self.peek()
        )

    # endregion

    # region --- Statements ---

    def parse_block_stmt(self) -> statements.BlockStmt:
        self.consume(TokenType.LBRACE, "Expected '{' to start the block.")
        stmts: List[statements.Statement] = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.skip_trivia()
            if self.check(TokenType.RBRACE) or self.is_at_end():
                break
            stmts.append(self.parse_statement())
        self.consume(TokenType.RBRACE, "Expected '}' at the end of the block.")
        return statements.BlockStmt(statements=stmts)

    def parse_statement(self) -> statements.Statement:
        if self.match(TokenType.VAR):
            return self.parse_var_declaration()

        if self.match(TokenType.IF):
            return self.parse_if_stmt()

        if self.match(TokenType.LOOP):
            body = self.parse_block_stmt()
            return statements.LoopStmt(body=body)

        if self.match(TokenType.RETURN):
            value = None
            if not self.check(TokenType.SEMICOLON):
                value = self.parse_expression()
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'return'.")
            return statements.ReturnStmt(value=value)

        if self.match(TokenType.BREAK):
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'break'.")
            return statements.BreakStmt()

        if self.match(TokenType.CONTINUE):
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'continue'.")
            return statements.ContinueStmt()

        if self.check(TokenType.LBRACE):
            return self.parse_block_stmt()

        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after the expression.")
        return statements.ExpressionStmt(expression=expr)

    def parse_if_stmt(self) -> statements.IfStmt:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'.")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after the condition of 'if'.")
        then_branch = self.parse_block_stmt()

        elif_branches: List[statements.ElifBranch] = []
        while self.match(TokenType.ELIF):
            self.consume(TokenType.LPAREN, "Expected '(' after 'elif'.")
            elif_cond = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after the condition of 'elif'.")
            elif_body = self.parse_block_stmt()
            elif_branches.append(statements.ElifBranch(condition=elif_cond, body=elif_body))

        else_branch: Optional[statements.BlockStmt] = None
        if self.match(TokenType.ELSE):
            else_branch = self.parse_block_stmt()

        return statements.IfStmt(
            condition=condition,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch
        )
    
    # endregion

    # region --- Expressions ---

    def parse_expression(self) -> expressions.Expression:
        return self.parse_assignment()

    def parse_assignment(self) -> expressions.Expression:
        left = self.parse_logical_or()
        if self.match(
            TokenType.EQUALS,
            TokenType.PLUS_EQUAL,
            TokenType.MINUS_EQUAL,
            TokenType.MULTIPLY_EQUAL,
            TokenType.DIVIDE_EQUAL,
            TokenType.MODULE_EQUAL
        ):
            op_lexeme = self.previous().value
            value = self.parse_assignment()
            return expressions.AssignExpr(target=left, op=op_lexeme, value=value)
        return left

    def parse_logical_or(self) -> expressions.Expression:
        expr_left = self.parse_logical_and()
        while self.match(TokenType.OR):
            op_lexeme = self.previous().value
            right = self.parse_logical_and()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_logical_and(self) -> expressions.Expression:
        expr_left = self.parse_equality()
        while self.match(TokenType.AND):
            op_lexeme = self.previous().value
            right = self.parse_equality()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_equality(self) -> expressions.Expression:
        expr_left = self.parse_relational()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            op_lexeme = self.previous().value
            right = self.parse_relational()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_relational(self) -> expressions.Expression:
        expr_left = self.parse_additive()
        while self.match(
            TokenType.LESS, TokenType.LESS_OR_EQUAL,
            TokenType.GREATER, TokenType.GREATER_OR_EQUAL
        ):
            op_lexeme = self.previous().value
            right = self.parse_additive()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_additive(self) -> expressions.Expression:
        expr_left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_lexeme = self.previous().value
            right = self.parse_multiplicative()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left
        
    def parse_multiplicative(self) -> expressions.Expression:
        expr_left = self.parse_unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULE):
            op_lexeme = self.previous().value
            right = self.parse_unary()
            expr_left = expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_unary(self) -> expressions.Expression:
        if self.match(TokenType.NOT, TokenType.MINUS):
            op_lexeme = self.previous().value
            right = self.parse_unary()
            return expressions.UnaryOp(op=op_lexeme, right=right)
        return self.parse_power()

    def parse_power(self) -> expressions.Expression:
        expr_left = self.parse_postfix()
        if self.match(TokenType.POWER):
            op_lexeme = self.previous().value
            right = self.parse_unary()
            return expressions.BinaryOp(left=expr_left, op=op_lexeme, right=right)
        return expr_left

    def parse_postfix(self) -> expressions.Expression:
        expr_node = self.parse_primary()
        while True:
            if self.match(TokenType.DOT):
                ident_tok = self.consume(TokenType.IDENTIFIER, "Expected an identifier after '.'.")
                expr_node = expressions.MemberAccess(obj=expr_node, member=expressions.Identifier(name=ident_tok.value))
            elif self.match(TokenType.LBRACKET):
                index_expr = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after the index expression.")
                expr_node = expressions.ArrayAccess(array=expr_node, index=index_expr)
            elif self.match(TokenType.LPAREN):
                args: List[expressions.Expression] = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        if self.check(TokenType.RPAREN):
                            break
                        args.append(self.parse_expression())
                self.consume(TokenType.RPAREN, "Expected ')' after the arguments.")
                expr_node = expressions.FuncCall(callee=expr_node, arguments=args)
            else:
                break
        return expr_node

    def parse_primary(self) -> expressions.Expression:
        if self.match(TokenType.INTEGER):
            return expressions.IntLiteral(value=int(self.previous().value))
        if self.match(TokenType.FLOAT):
            return expressions.FloatLiteral(value=float(self.previous().value))
        if self.match(TokenType.STRING):
            return expressions.StringLiteral(value=self.previous().value)
        if self.match(TokenType.TRUE):
            return expressions.BoolLiteral(value=True)
        if self.match(TokenType.FALSE):
            return expressions.BoolLiteral(value=False)

        if self.match(TokenType.PRINT):
            return expressions.Identifier(name="print")
        if self.match(TokenType.LEN):
            return expressions.Identifier(name="len")
        if self.match(TokenType.IDENTIFIER):
            return expressions.Identifier(name=self.previous().value)

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after the expression.")
            return expr

        if self.match(TokenType.LBRACKET):
            elements: List[expressions.Expression] = []
            if not self.check(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACKET):
                        break
                    elements.append(self.parse_expression())
            self.consume(TokenType.RBRACKET, "Expected ']' at the end of the list literal.")
            return expressions.LiteralList(elements=elements)

        if self.match(TokenType.NEW):
            self.consume(TokenType.LBRACE, "Expected '{' after 'new'.")
            fields_inits: List[expressions.FieldInit] = []
            if not self.check(TokenType.RBRACE):
                fields_inits.append(self.parse_field_init())
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACE):
                        break
                    fields_inits.append(self.parse_field_init())
            self.consume(TokenType.RBRACE, "Expected '}' at the end of the struct literal.")
            return expressions.StructLiteral(fields=fields_inits)

        if self.match(TokenType.LBRACE):
            fields_inits: List[expressions.FieldInit] = []
            if not self.check(TokenType.RBRACE):
                fields_inits.append(self.parse_field_init())
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACE):
                        break
                    fields_inits.append(self.parse_field_init())
            self.consume(TokenType.RBRACE, "Expected '}' at the end of the struct literal.")
            return expressions.StructLiteral(fields=fields_inits)

        raise ParserError(
            "Invalid primary expression.",
            line=self.peek().line,
            column=self.peek().column,
            token=self.peek()
        )

    def parse_field_init(self) -> expressions.FieldInit:
        name_tok = self.consume(TokenType.IDENTIFIER, "Expected a field name in the struct literal.")
        self.consume(TokenType.COLON, "Expected ':' after the field name in the struct literal.")
        value_expr = self.parse_expression()
        return expressions.FieldInit(name=expressions.Identifier(name_tok.value), value=value_expr)
    
    # endregion

    # region --- Helpers ---

    def consume(self, t_type: TokenType, message: str) -> Token:
        if self.check(t_type):
            return self.advance()
        raise ParserError(
            f"{message} (received {self.peek().type.name})",
            line=self.peek().line,
            column=self.peek().column,
            token=self.peek()
        )

    def match(self, *types: TokenType) -> bool:
        for t_type in types:
            if self.check(t_type):
                self.advance()
                return True
        return False

    def check(self, t_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == t_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        if self.current >= len(self.tokens):
            return True
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def skip_trivia(self) -> None:
        while not self.is_at_end() and self.peek().type in (TokenType.WHITESPACE, TokenType.COMMENT):
            self.advance()
