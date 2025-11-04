# 💡 Definição Formal da Gramática (Clash)

G = (V, Σ, P, S)

onde:

* **V** (variáveis / não-terminais):
    `{Program, Statement, ExpressionStmt, BlockStmt, IfStmt, LoopStmt, ReturnStmt, BreakStmt, ContinueStmt, Declaration, VarDecl, ParamDecl, FuncDecl, StructDecl, Expression, AssignExpr, AssignOp, LogicalOrExpr, LogicalAndExpr, EqualityExpr, RelationalExpr, AdditiveExpr, MultiplicativeExpr, UnaryExpr, PostfixExpr, PrimaryExpr, TypeSpecifier, BaseType, ListType, ParamList, ArgList, Literal, LiteralList, StructLiteral, FieldList, FieldDecl, FieldInitList, FieldInit}`

* **Σ** (terminais):
    Palavras reservadas, símbolos, identificadores e literais vindos do analisador léxico.
    * **Palavras Reservadas:**
        `if`, `else`, `elif`, `true`, `false`, `struct`, `loop`, `return`, `break`, `continue`, `void`, `int`, `float`, `str`, `bool`, `var`, `func`, `list`, `new`
    * **Símbolos:**
        `;`, `(`, `)`, `{`, `}`, `[`, `]`, `,`, `.`, `=`, `+=`, `==`, `!`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `+`, `-`, `*`, `/`, `%`, `:`
    * **Tokens de Literais/Identificadores:**
        `Identifier`, `IntLiteral`, `FloatLiteral`, `StringLiteral`

* **S** (símbolo inicial):
    `Program`

* **P** (regras de produção):
    O conjunto de produções segue abaixo, no formato EBNF e BNF.

---

## 📘 Gramática Clash em EBNF (Extended Backus–Naur Form)

```ebnf
/* ============================================= */
/* 1. Nível Superior e Declarações               */
/* ============================================= */

Program       = { Declaration } .

Declaration   = VarDecl
              | FuncDecl
              | StructDecl .

StructDecl    = "struct" Identifier "{" [ FieldList ] "}" ";" .

FuncDecl      = "func" Identifier "(" [ ParamList ] ")" ":" TypeSpecifier BlockStmt .

VarDecl       = "var" Identifier ":" TypeSpecifier [ "=" Expression ] ";" .

FieldList     = FieldDecl { "," FieldDecl } [ "," ] . /* Permite vírgula no final */

FieldDecl     = Identifier ":" TypeSpecifier .


/* ============================================= */
/* 2. Componentes de Declaração                  */
/* ============================================= */

TypeSpecifier = BaseType | ListType .

BaseType      = "void" | "int" | "float" | "bool" | "str" | Identifier .

ListType      = "list" "[" TypeSpecifier "]" .

ParamDecl     = Identifier ":" TypeSpecifier .

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
              | VarDecl .  /* Permite VarDecl dentro de blocos */

BlockStmt     = "{" { Statement } "}" .

ExpressionStmt = [ Expression ] ";" .

IfStmt        = "if" "(" Expression ")" BlockStmt
                { "elif" "(" Expression ")" BlockStmt }
                [ "else" BlockStmt ] .

LoopStmt      = "loop" BlockStmt .

ReturnStmt    = "return" [ Expression ] ";" .

BreakStmt     = "break" ";" .

ContinueStmt  = "continue" ";" .


/* ============================================= */
/* 4. Expressões (Hierarquia de Precedência)     */
/* ============================================= */

Expression    = AssignExpr .

AssignExpr    = LogicalOrExpr [ AssignOp AssignExpr ] .

AssignOp      = "=" | "+=" .

LogicalOrExpr = LogicalAndExpr { "||" LogicalAndExpr } .

LogicalAndExpr = EqualityExpr { "&&" EqualityExpr } .

EqualityExpr  = RelationalExpr { ( "==" | "!=" ) RelationalExpr } .

RelationalExpr = AdditiveExpr { ( "<" | "<=" | ">" | ">=" ) AdditiveExpr } .

AdditiveExpr  = MultiplicativeExpr { ( "+" | "-" ) MultiplicativeExpr } .

MultiplicativeExpr = UnaryExpr { ( "*" | "/" | "%" ) UnaryExpr } .

UnaryExpr     = ( "!" | "-" ) UnaryExpr 
              | PostfixExpr .

PostfixExpr   = PrimaryExpr { "." Identifier | "[" Expression "]" | "(" [ ArgList ] ")" } .

PrimaryExpr   = Literal
              | Identifier
              | "(" Expression ")"
              | LiteralList
              | StructLiteral .


/* ============================================= */
/* 5. Átomos                                     */
/* ============================================= */

LiteralList   = "[" [ ArgList ] "]" .

StructLiteral = "new" "{" [ FieldInitList ] "}" .

FieldInitList = FieldInit { "," FieldInit } [ "," ] .

FieldInit     = Identifier ":" Expression .

Literal       = IntLiteral 
              | FloatLiteral 
              | StringLiteral
              | "true" 
              | "false" .
```

## 📘 Gramática Clash em BNF (Backus–Naur Form)

```bnf
/* ============================================= */
/* 1. Nível Superior e Declarações               */
/* ============================================= */

<Program>        ::= <DeclarationSeq>

<DeclarationSeq> ::= <Declaration> <DeclarationSeq>
                   | ε

<Declaration>    ::= <VarDecl>
                   | <FuncDecl>
                   | <StructDecl>

<StructDecl>     ::= "struct" Identifier "{" <FieldListOpt> "}" ";"

<FieldListOpt>   ::= <FieldList>
                   | ε

<FieldList>      ::= <FieldDecl> <FieldListTail> <CommaOpt>

<FieldListTail>  ::= "," <FieldDecl> <FieldListTail>
                   | ε

<FieldDecl>      ::= Identifier ":" <TypeSpecifier>

<FuncDecl>       ::= "func" Identifier "(" <ParamListOpt> ")" ":" <TypeSpecifier> <BlockStmt>

<VarDecl>        ::= "var" Identifier ":" <TypeSpecifier> <InitOpt> ";"

<InitOpt>        ::= "=" <Expression>
                   | ε

<CommaOpt>       ::= "," | ε

/* ============================================= */
/* 2. Componentes de Declaração                  */
/* ============================================= */

<TypeSpecifier>  ::= <BaseType>
                   | <ListType>

<BaseType>       ::= "void" | "int" | "float" | "bool" | "str" | Identifier

<ListType>       ::= "list" "[" <TypeSpecifier> "]"

<ParamDecl>      ::= Identifier ":" <TypeSpecifier>

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

<LoopStmt>       ::= "loop" <BlockStmt>

<ReturnStmt>     ::= "return" <ExpressionOpt> ";"

<BreakStmt>      ::= "break" ";"

<ContinueStmt>   ::= "continue" ";"

/* ============================================= */
/* 4. Expressões (Hierarquia de Precedência)     */
/* ============================================= */

<Expression>     ::= <AssignExpr>

<AssignExpr>     ::= <LogicalOrExpr> <AssignExprOpt>
<AssignExprOpt>  ::= <AssignOp> <AssignExpr>
                   | ε
<AssignOp>       ::= "=" | "+="

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

<MultiplicativeExpr> ::= <UnaryExpr> <MultiplicativeExprTail>
<MultiplicativeExprTail> ::= <MulOp> <UnaryExpr> <MultiplicativeExprTail>
                           | ε
<MulOp>          ::= "*" | "/" | "%"

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
                   | <StructLiteral>

/* ============================================= */
/* 5. Átomos                                     */
/* ============================================= */

<LiteralList>    ::= "[" <ArgListOpt> "]"

<StructLiteral>  ::= "new" "{" <FieldInitListOpt> "}"

<FieldInitListOpt> ::= <FieldInitList>
                     | ε

<FieldInitList>  ::= <FieldInit> <FieldInitListTail> <CommaOpt>

<FieldInitListTail> ::= "," <FieldInit> <FieldInitListTail>
                      | ε

<FieldInit>      ::= Identifier ":" <Expression>

<Literal>        ::= IntLiteral 
                   | FloatLiteral 
                   | StringLiteral 
                   | "true" 
                   | "false" .
```

---

## 2. Conjuntos FIRST (Gramática V2)

O conjunto FIRST de um não-terminal é o conjunto de terminais (tokens) que podem iniciar uma sentença derivada desse não-terminal.

| Não-Terminal | Conjunto FIRST |
| :--- | :--- |
| `<Program>` | `{ var, func, struct, ε }` |
| `<DeclarationSeq>` | `{ var, func, struct, ε }` |
| `<Declaration>` | `{ var, func, struct }` |
| `<VarDecl>` | `{ var }` |
| `<FuncDecl>` | `{ func }` |
| `<StructDecl>` | `{ struct }` |
| `<TypeSpecifier>` | `{ void, int, float, bool, str, Identifier, list }` |
| `<BaseType>` | `{ void, int, float, bool, str, Identifier }` |
| `<ListType>` | `{ list }` |
| `<Statement>` | `{ ;, {, if, loop, return, break, continue, var } ∪ FIRST(<Expression>)` |
| | `{ ;, {, if, loop, return, break, continue, var, !, -, IntLiteral, FloatLiteral, StringLiteral, true, false, Identifier, (, [, new }` |
| `<BlockStmt>` | `{ { }` |
| `<ExpressionStmt>` | `{ ; } ∪ FIRST(<Expression>)` |
| `<IfStmt>` | `{ if }` |
| `<LoopStmt>` | `{ loop }` |
| `<ReturnStmt>` | `{ return }` |
| `<Expression>` | `{ !, -, IntLiteral, FloatLiteral, StringLiteral, true, false, Identifier, (, [, new }` |
| `<AssignExpr>` | `{ !, -, IntLiteral, ..., new }` (O mesmo que `FIRST(<Expression>)`) |
| `<LogicalOrExpr>` | `{ !, -, IntLiteral, ..., new }` (O mesmo que `FIRST(<Expression>)`) |
| `<UnaryExpr>` | `{ !, - } ∪ FIRST(<PostfixExpr>)` |
| `<PostfixExpr>` | `{ IntLiteral, FloatLiteral, StringLiteral, true, false, Identifier, (, [, new }` |
| `<PrimaryExpr>` | `{ IntLiteral, FloatLiteral, StringLiteral, true, false, Identifier, (, [, new }` |
| `<Literal>` | `{ IntLiteral, FloatLiteral, StringLiteral, true, false }` |
| `<LiteralList>` | `{ [ }` |
| `<StructLiteral>` | `{ new }` |

---

## 3. Conjuntos FOLLOW (Gramática V2)

O conjunto FOLLOW de um não-terminal `A` é o conjunto de terminais que podem aparecer imediatamente após uma sentença derivada de `A`. `$` é o marcador de fim de arquivo.

| Não-Terminal | Conjunto FOLLOW |
| :--- | :--- |
| `<Program>` | `{ $ }` |
| `<DeclarationSeq>` | `{ $ }` |
| `<Declaration>` | `{ var, func, struct, $ }` |
| `<VarDecl>` | (Como `VarDecl` pode ser `Declaration` ou `Statement`, seu `FOLLOW` é a união de `FOLLOW(<Declaration>)` e `FOLLOW(<Statement>)`) |
| `<Statement>` | `{ } } ∪ FIRST(<Statement>)` |
| `<BlockStmt>` | (FOLLOW de `FuncDecl`, `IfStmt`, `ElifList`, `ElseOpt`, `LoopStmt`) <br> `{ var, func, struct, $, elif, else, } } ∪ FIRST(<Statement>)` |
| `<Expression>` | `{ ;, ), ], , }` (Usado em `Expr;`, `if(Expr)`, `func(Expr)`, `list[Expr]`, `init: Expr,`) |
| `<AssignExpr>` | `{ ;, ), ], , }` |
| `<AssignOp>` | `FIRST(<AssignExpr>)` = `{ !, -, IntLiteral, ..., new }` |
| `<LogicalOrExpr>` | `{ =, +=, ;, ), ], , }` |
| `<LogicalAndExpr>` | `{ \|\|, =, +=, ;, ), ], , }` |
| `<EqualityExpr>` | `{ &&, \|\|, =, +=, ;, ), ], , }` |
| `<TypeSpecifier>` | `{ Identifier, {, ;, =, ), ] }` (Usado em `ParamDecl`, `FuncDecl`, `VarDecl`, `FieldDecl`, `ListType`) |
| `<ParamListOpt>` | `{ ) }` |
| `<ArgListOpt>` | `{ ), ] }` |
| `<Literal>` | (FOLLOW de `PrimaryExpr`, que é muito grande) `{ ., [, ( } ∪ FOLLOW(<UnaryExpr>)` |
| `<StructLiteral>` | (O mesmo que `FOLLOW(<Literal>)`) |

---

## 4. Análise: A Gramática V2 é LL(1)?

> **Resposta: Sim, a gramática do CLash é LL(1).**

Uma gramática é LL(1) se, para qualquer não-terminal, um analisador preditivo puder escolher a produção correta olhando apenas para o próximo (1) token de entrada.

Isso exige que duas condições sejam verdadeiras:

**1. Condição FIRST/FIRST:**
Para qualquer não-terminal `A` com múltiplas produções `A -> α | β`, os conjuntos `FIRST(α)` e `FIRST(β)` devem ser disjuntos (`FIRST(α) ∩ FIRST(β) = ∅`).

**Justificativa:** Sua nova gramática V2 satisfaz esta condição. Os conflitos da V1 foram resolvidos:

* **Conflito 1 (Declaração):**
    * `Declaration -> VarDecl | FuncDecl | StructDecl`
    * `FIRST(VarDecl)` = `{ var }`
    * `FIRST(FuncDecl)` = `{ func }`
    * `FIRST(StructDecl)` = `{ struct }`
    * **Resultado:** `{ var }`, `{ func }` e `{ struct }` são disjuntos. **CONFLITO RESOLVIDO.**

* **Conflito 2 (Statement):**
    * `Statement -> VarDecl | ExpressionStmt | BlockStmt | IfStmt | ...`
    * `FIRST(VarDecl)` = `{ var }`
    * `FIRST(ExpressionStmt)` = `{ !, -, IntLiteral, ..., Identifier, ... ; }`
    * `FIRST(BlockStmt)` = `{ { }`
    * `FIRST(IfStmt)` = `{ if }`
    * **Resultado:** Todos os tokens de início (`var`, `!`, `-`, `Identifier`, `(`, `[`, `new`, `{`, `if`, `loop`, `return`, `break`, `continue`, `;`) são únicos para cada escolha de produção. **CONFLITO RESOLVIDO.**

* **Conflito 3 (Bloco vs. Literal de Struct):**
    * Na V2 (antes do `new`), `FIRST(BlockStmt)` e `FIRST(StructLiteral)` eram ambos `{ { }`.
    * Na V2 final:
    * `FIRST(BlockStmt)` = `{ { }`
    * `FIRST(StructLiteral)` = `{ new }`
    * **Resultado:** `{ { }` e `{ new }` são disjuntos. **CONFLITO RESOLVIDO.**

**2. Condição FIRST/FOLLOW:**
Se um não-terminal `A` tem uma produção que pode derivar a sentença vazia (ε), (ex: `A -> α | ε`), então `FIRST(α)` e `FOLLOW(A)` devem ser disjuntos (`FIRST(α) ∩ FOLLOW(A) = ∅`).

**Justificativa:** Esta condição também é satisfeita. O exemplo mais claro está nas regras de Expressão (que usam `...Opt` e `...Tail` na BNF):

* Considere `<AssignExprOpt> ::= <AssignOp> <AssignExpr> | ε`
* `FIRST(<AssignOp> ...)` = `FIRST(AssignOp)` = `{ =, += }`
* `FOLLOW(<AssignExprOpt>)` = `FOLLOW(<AssignExpr>)` = `FOLLOW(<Expression>)` = `{ ;, ), ], , }`
* **Resultado:** `{ =, += } ∩ { ;, ), ], , } = ∅`. (Não há conflito).

**Conclusão Final:**
As mudanças de sintaxe (introduzindo `var`, `func`, `loop` e `new`) eliminaram todas as ambiguidades que impediam a gramática de ser LL(1). A gramática V2 resultante é LL(1) e pode ser implementada diretamente por um analisador preditivo recursivo descendente (*recursive descent parser*).
