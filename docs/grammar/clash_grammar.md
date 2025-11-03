# 💡 Definição Formal da Gramática (Clash)

G = (V, Σ, P, S)

onde:

* **V** (variáveis / não-terminais):
    `{Program, Statement, ExpressionStmt, BlockStmt, IfStmt, LoopStmt, ReturnStmt, BreakStmt, ContinueStmt, Declaration, VarDecl, ParamDecl, FuncDecl, MethodDecl, StructDecl, Expression, AssignExpr, LogicalOrExpr, LogicalAndExpr, EqualityExpr, RelationalExpr, AdditiveExpr, MultiplicativeExpr, PowerExpr, UnaryExpr, PostfixExpr, PrimaryExpr, TypeSpecifier, BaseType, Declarator, InitDeclarator, ParamList, ArgList, Literal, LiteralList}`

* **Σ** (terminais):
    Palavras reservadas, símbolos, identificadores e literais vindos do analisador léxico.
    * **Palavras Reservadas:**
        `if`, `else`, `elif`, `true`, `false`, `struct`, `while`, `return`, `break`, `continue`, `void`, `int`, `float`, `string`, `bool`
    * **Símbolos:**
        `;`, `(`, `)`, `{`, `}`, `[`, `]`, `,`, `.`, `=`, `==`, `!`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `+`, `-`, `*`, `**`, `/`, `%`
    * **Tokens de Literais/Identificadores:**
        `Identifier`, `IntLiteral`, `FloatLiteral`, `StringLiteral`

* **S** (símbolo inicial):
    `Program`

* **P** (regras de produção):
    O conjunto de produções segue abaixo, no formato EBNF.

---

## 📘 Gramática Clash em EBNF (Extended Backus–Naur Form)

```ebnf
/* ============================================= */
/* 1. Nível Superior e Declarações               */
/* ============================================= */

Program       = { Declaration } .

Declaration   = VarDecl
              | FuncDecl
              | MethodDecl
              | StructDecl .

StructDecl    = "struct" Identifier [ "{" { VarDecl } "}" ] ";" .

MethodDecl    = TypeSpecifier "(" ParamDecl ")" Declarator "(" [ ParamList ] ")" BlockStmt .

FuncDecl      = TypeSpecifier Declarator "(" [ ParamList ] ")" BlockStmt .

VarDecl       = TypeSpecifier InitDeclarator ({ "," InitDeclarator } | ";") .

/* ============================================= */
/* 2. Componentes de Declaração                  */
/* ============================================= */

TypeSpecifier = BaseType { "[" "]" } .

BaseType      = "void" | "int" | "float" | "string" | "bool" | Identifier .

Declarator    = Identifier .

InitDeclarator = Identifier [ "=" Expression ] .

ParamDecl     = TypeSpecifier Declarator .

ParamList     = ParamDecl { "," ParamDecl } .

ArgList       = Expression { "," Expression } .

/* ============================================= */
/* 3. Statements                                 */
/* ============================================= */

Statement     = ExpressionStmt
              | BlockStmt
              | IfStmt
              | LoopStmt
              | ReturnStmt
              | BreakStmt
              | ContinueStmt
              | VarDecl .  /* Permite declarações dentro de blocos */

BlockStmt     = "{" { Statement } "}" .

ExpressionStmt = [ Expression ] ";" .

IfStmt        = "if" "(" Expression ")" BlockStmt
                { "elif" "(" Expression ")" BlockStmt }
                [ "else" BlockStmt ] .

LoopStmt      = "while" "(" Expression ")" BlockStmt .

ReturnStmt    = "return" [ Expression ] ";" .

BreakStmt     = "break" ";" .

ContinueStmt  = "continue" ";" .

/* ============================================= */
/* 4. Expressões (Hierarquia de Precedência)     */
/* ============================================= */

Expression    = AssignExpr .

AssignExpr    = LogicalOrExpr [ "=" AssignExpr ] . /* Atribuição é R-Associativa */

LogicalOrExpr = LogicalAndExpr { "||" LogicalAndExpr } .

LogicalAndExpr = EqualityExpr { "&&" EqualityExpr } .

EqualityExpr  = RelationalExpr { ( "==" | "!=" ) RelationalExpr } .

RelationalExpr = AdditiveExpr { ( "<" | "<=" | ">" | ">=" ) AdditiveExpr } .

AdditiveExpr  = MultiplicativeExpr { ( "+" | "-" ) MultiplicativeExpr } .

MultiplicativeExpr = PowerExpr { ( "*" | "/" | "%" ) PowerExpr } .

PowerExpr     = UnaryExpr [ "**" PowerExpr ] . /* Potência é R-Associativa */

UnaryExpr     = ( "!" | "-" ) UnaryExpr 
              | PostfixExpr .

PostfixExpr   = PrimaryExpr { "." Identifier | "[" Expression "]" | "(" [ ArgList ] ")" } .

PrimaryExpr   = Literal
              | Identifier
              | "(" Expression ")"
              | LiteralList .

/* ============================================= */
/* 5. Átomos                                     */
/* ============================================= */

LiteralList   = "[" [ ArgList ] "]" .

Literal       = IntLiteral 
              | FloatLiteral 
              | StringLiteral 
              | "true" 
              | "false" .
```

## 📘 Gramática em BNF (Backus–Naur Form)

```bnf
/* ============================================= */
/* 1. Nível Superior e Declarações               */
/* ============================================= */

<Program>        ::= <DeclarationSeq>

<DeclarationSeq> ::= <Declaration> <DeclarationSeq>
                   | ε

<Declaration>    ::= <VarDecl>
                   | <FuncDecl>
                   | <MethodDecl>
                   | <StructDecl>

<StructDecl>     ::= "struct" Identifier <StructBodyOpt> ";"

<StructBodyOpt>  ::= "{" <VarDeclSeq> "}"
                   | ε

<VarDeclSeq>     ::= <VarDecl> <VarDeclSeq>
                   | ε

<MethodDecl>     ::= <TypeSpecifier> "(" <ParamDecl> ")" <Declarator> "(" <ParamListOpt> ")" <BlockStmt>

<FuncDecl>       ::= <TypeSpecifier> <Declarator> "(" <ParamListOpt> ")" <BlockStmt>

<VarDecl>        ::= <TypeSpecifier> <InitDeclarator> <InitDeclaratorTail> ";"

<InitDeclaratorTail> ::= "," <InitDeclarator> <InitDeclaratorTail>
                       | ε

/* ============================================= */
/* 2. Componentes de Declaração                  */
/* ============================================= */

<TypeSpecifier>  ::= <BaseType> <ArraySpecTail>

<ArraySpecTail>  ::= "[" "]" <ArraySpecTail>
                   | ε

<BaseType>       ::= "void" | "int" | "float" | "string" | "bool" | Identifier

<Declarator>     ::= Identifier

<InitDeclarator> ::= Identifier <InitOpt>

<InitOpt>        ::= "=" <Expression>
                   | ε

<ParamDecl>      ::= <TypeSpecifier> <Declarator>

<ParamListOpt>   ::= <ParamList>
                   | ε
                   
<ParamList>      ::= <ParamDecl> <ParamListTail>

<ParamListTail>  ::= "," <ParamDecl> <ParamListTail>
                   | ε

<ArgListOpt>     ::= <ArgList>
                   | ε

<ArgList>        ::= <Expression> <ArgListTail>

<ArgListTail>    ::= "," <Expression> <ArgListTail>
                   | ε

/* ============================================= */
/* 3. Statements                                 */
/* ============================================= */

<Statement>      ::= <ExpressionStmt>
                   | <BlockStmt>
                   | <IfStmt>
                   | <LoopStmt>
                   | <ReturnStmt>
                   | <BreakStmt>
                   | <ContinueStmt>
                   | <VarDecl>

<BlockStmt>      ::= "{" <StatementSeq> "}"

<StatementSeq>   ::= <Statement> <StatementSeq>
                   | ε

<ExpressionStmt> ::= <ExpressionOpt> ";"

<ExpressionOpt>  ::= <Expression>
                   | ε

<IfStmt>         ::= "if" "(" <Expression> ")" <BlockStmt> <ElifList> <ElseOpt>

<ElifList>       ::= "elif" "(" <Expression> ")" <BlockStmt> <ElifList>
                   | ε

<ElseOpt>        ::= "else" <BlockStmt>
                   | ε

<LoopStmt>       ::= "while" "(" <Expression> ")" <BlockStmt>

<ReturnStmt>     ::= "return" <ExpressionOpt> ";"

<BreakStmt>      ::= "break" ";"

<ContinueStmt>   ::= "continue" ";"

/* ============================================= */
/* 4. Expressões (Hierarquia de Precedência)     */
/* ============================================= */

<Expression>     ::= <AssignExpr>

<AssignExpr>     ::= <LogicalOrExpr> <AssignExprOpt>
<AssignExprOpt>  ::= "=" <AssignExpr>
                   | ε

<LogicalOrExpr>  ::= <LogicalAndExpr> <LogicalOrExprTail>
<LogicalOrExprTail> ::= "||" <LogicalAndExpr> <LogicalOrExprTail>
                      | ε

<LogicalAndExpr> ::= <EqualityExpr> <LogicalAndExprTail>
<LogicalAndExprTail> ::= "&&" <EqualityExpr> <LogicalAndExprTail>
                       | ε

<EqualityExpr>   ::= <RelationalExpr> <EqualityExprTail>
<EqualityExprTail> ::= <EqOp> <RelationalExpr> <EqualityExprTail>
                     | ε
<EqOp>           ::= "==" | "!="

<RelationalExpr> ::= <AdditiveExpr> <RelationalExprTail>
<RelationalExprTail> ::= <RelOp> <AdditiveExpr> <RelationalExprTail>
                       | ε
<RelOp>          ::= "<" | "<=" | ">" | ">="

<AdditiveExpr>   ::= <MultiplicativeExpr> <AdditiveExprTail>
<AdditiveExprTail> ::= <AddOp> <MultiplicativeExpr> <AdditiveExprTail>
                     | ε
<AddOp>          ::= "+" | "-"

<MultiplicativeExpr> ::= <PowerExpr> <MultiplicativeExprTail>
<MultiplicativeExprTail> ::= <MulOp> <PowerExpr> <MultiplicativeExprTail>
                           | ε
<MulOp>          ::= "*" | "/" | "%"

<PowerExpr>      ::= <UnaryExpr> <PowerExprOpt>
<PowerExprOpt>   ::= "**" <PowerPowerExpr>
                   | ε

<UnaryExpr>      ::= <UnaryOp> <UnaryExpr>
                   | <PostfixExpr>
<UnaryOp>        ::= "!" | "-"

<PostfixExpr>    ::= <PrimaryExpr> <PostfixExprTail>
<PostfixExprTail> ::= <PostfixOp> <PostfixExprTail>
                    | ε
<PostfixOp>      ::= "." Identifier
                   | "[" <Expression> "]"
                   | "(" <ArgListOpt> ")"

<PrimaryExpr>    ::= <Literal>
                   | Identifier
                   | "(" <Expression> ")"
                   | <LiteralList>

/* ============================================= */
/* 5. Átomos                                     */
/* ============================================= */

<LiteralList>    ::= "[" <ArgListOpt> "]"

<Literal>        ::= IntLiteral 
                   | FloatLiteral 
                   | StringLiteral 
                   | "true" 
                   | "false" .
```
