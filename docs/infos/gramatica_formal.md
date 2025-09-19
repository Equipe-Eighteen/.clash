# Gramática Formal — Clash

> Este documento entrega a **primeira versão da gramática formal**, a **classificação na hierarquia de Chomsky**, **exemplos de derivações** e uma **análise de ambiguidades/estratégias**.

---

## 1) Definição da Gramática:  G = (V, T, P, S)

### 1.1 Símbolo Inicial

- **S = Program**

### 1.2 Conjunto de variáveis — **V**

```
V = {
  Program, DeclList, Decl, VarDecl, StructDecl, FieldDeclList, FieldDecl,
  MethodDecl, Receiver, ParamList, Param, OptParamList,
  FuncDecl, OptReturnType,
  Block, StmtList, Stmt,
  IfStmt, ElseChain, WhileStmt, ForStmt, ForeachStmt,
  AssignStmt, PrintStmt, ReturnStmt, BreakStmt, ContinueStmt,
  Expr, OrExpr, AndExpr, RelExpr, AddExpr, MulExpr, UnaryExpr, PostfixExpr, Primary,
  ArgList, OptArgList,
  MemberAccess, ObjectLiteral, FieldInitList, FieldInit,
  Type, BaseType, ArrayType, OptArrayBrackets
}
```

### 1.3 Conjunto de terminais — **T**

Palavras-chave: `int`, `float`, `bool`, `string`, `void`, `struct`, `if`, `else`, `for`, `while`, `foreach`, `in`, `break`, `continue`, `return`, `print`, `true`, `false`  
Operadores e pontuação: `+ - * / % == != > >= < <= && || ! = . , ; : ( ) { } [ ]`  
Identificadores e literais: `ID`, `INT_LIT`, `FLOAT_LIT`, `STRING_LIT`

---

## 2) Regras de Produção — **P** (EBNF limpa e fatorada por precedência)

### 2.1 Programa e Declarações

```
Program        → DeclList
DeclList       → Decl DeclList | ε
Decl           → VarDecl ";"
               | StructDecl
               | FuncDecl
               | MethodDecl
```

### 2.2 Tipos e Arrays

```
Type           → BaseType OptArrayBrackets
OptArrayBrackets → "[]" OptArrayBrackets | ε
BaseType       → "int" | "float" | "bool" | "string" | "void" | ID   // ID = nome de struct
```

### 2.3 Declaração de Variáveis, Funções e Métodos

```
VarDecl        → Type ID OptInit
OptInit        → "=" Expr | ε

// funções “livres” (sem palavra-chave extra), padrão estilo C
FuncDecl       → Type ID "(" OptParamList ")" Block

// métodos vinculados a struct (estilo com receptor, inspirado em Go)
MethodDecl     → Type Receiver ID "(" OptParamList ")" Block
Receiver       → "(" ID BaseType ")"  // ex.: (p Pessoa)

OptParamList   → ParamList | ε
ParamList      → Param ("," Param)*
Param          → Type ID
```

### 2.4 Structs e Literais de Objeto

```
StructDecl     → "struct" ID "{" FieldDeclList "}"
FieldDeclList  → FieldDecl FieldDeclList | ε
FieldDecl      → Type ID ";"

ObjectLiteral  → "{" FieldInitList "}"
FieldInitList  → FieldInit ("," FieldInit)* | ε
FieldInit      → ID ":" Expr
```

### 2.5 Blocos e Comandos

```
Block          → "{" StmtList "}"
StmtList       → Stmt StmtList | ε

Stmt           → VarDecl ";"
               | AssignStmt ";"
               | IfStmt
               | WhileStmt
               | ForStmt
               | ForeachStmt
               | PrintStmt ";"
               | ReturnStmt ";"
               | BreakStmt ";"
               | ContinueStmt ";"
               | Expr ";"              // chamada, ++/-- isolados, etc.

AssignStmt     → PostfixExpr "=" Expr

IfStmt         → "if" "(" Expr ")" Block ElseChain
ElseChain      → "else" "if" "(" Expr ")" Block ElseChain
               | "else" Block
               | ε

WhileStmt      → "while" "(" Expr ")" Block

ForStmt        → "for" "(" OptSimpleStmt ";" OptExpr ";" OptSimpleStmt ")" Block
OptSimpleStmt  → AssignStmt | VarDecl | Expr | ε
OptExpr        → Expr | ε

ForeachStmt    → "foreach" "(" Type ID "in" Expr ")" Block

PrintStmt      → "print" "(" OptArgList ")"
ReturnStmt     → "return" OptExpr
BreakStmt      → "break"
ContinueStmt   → "continue"
OptArgList     → ArgList | ε
ArgList        → Expr ("," Expr)*
```

### 2.6 Expressões (precedência e associatividade explícitas)

**Or (||), And (&&), Relacionais, Aditivas, Multiplicativas, Unárias e Pós-fixas.**

```
Expr           → OrExpr
OrExpr         → AndExpr ("||" AndExpr)*
AndExpr        → RelExpr ("&&" RelExpr)*
RelExpr        → AddExpr (("==" | "!=" | ">" | ">=" | "<" | "<=") AddExpr)*
AddExpr        → MulExpr (("+" | "-") MulExpr)*
MulExpr        → UnaryExpr (("*" | "/" | "%") UnaryExpr)*
UnaryExpr      → ("!" | "-" ) UnaryExpr
               | PostfixExpr

PostfixExpr    → Primary ( PostfixOp )*
PostfixOp      → "++" | "--"
               | "." ID
               | "(" OptArgList ")"   // chamada de função/método
               | "[" Expr "]"         // indexação (arrays)

Primary        → "(" Expr ")"
               | "true"
               | "false"
               | INT_LIT
               | FLOAT_LIT
               | STRING_LIT
               | ID
               | ID ObjectLiteral     // ex.: Pessoa { nome: "Ana", idade: 25 }
               | ID "(" OptArgList ")"// chamada direta de função livre
```

**Observações de associatividade**  
- `||`, `&&`, relacionais, `+/-`, `*/%` → **associativas à esquerda**.  
- Unárias `!` e `-` → **associativas à direita**.  
- Pós-fixos (`.`, `()`, `[]`, `++`, `--`) têm **maior precedência**.

---

## 3) Exemplos de Derivações (esquerda) para construtos-chave

### 3.1 Declaração de variável com inicialização

Objetivo: `int idade = 25;`

1. `Program ⇒ DeclList ⇒ Decl DeclList ⇒ VarDecl ";" DeclList`
2. `VarDecl ⇒ Type ID OptInit`
3. `Type ⇒ BaseType OptArrayBrackets ⇒ "int" ε`
4. `ID ⇒ idade`
5. `OptInit ⇒ "=" Expr`
6. `Expr ⇒ OrExpr ⇒ AndExpr ⇒ RelExpr ⇒ AddExpr ⇒ MulExpr ⇒ UnaryExpr ⇒ PostfixExpr ⇒ Primary ⇒ INT_LIT ⇒ 25`

**Resultado**: derivado `int idade = 25;`

---

### 3.2 Condicional com `else if` e `else`

Objetivo:
```clash
if (a + b * c > 0) { print(a); }
else if (cond) { print(b); }
else { print(c); }
```

Esboço da derivação (trechos principais):

1. `Stmt ⇒ IfStmt`
2. `IfStmt ⇒ "if" "(" Expr ")" Block ElseChain`
3. Em `Expr`: `a + b * c > 0` segue `RelExpr → AddExpr (">" AddExpr)` com `AddExpr → MulExpr ("+" MulExpr)` etc.
4. `Block ⇒ "{" StmtList "}"` com `StmtList ⇒ PrintStmt ";"` e `PrintStmt ⇒ "print" "(" ArgList ")"`.
5. `ElseChain ⇒ "else" "if" "(" Expr ")" Block ElseChain`
6. Segundo `ElseChain` termina em `"else" Block`.

---

### 3.3 Declaração de `struct` e uso de literal de objeto + chamada de método

Objetivo:
```clash
struct Pessoa { string nome; int idade; }

void (p Pessoa) saudacao() { print(p.nome, " tem ", p.idade, " anos"); }

Pessoa pessoa = { nome: "Ana", idade: 25 };
pessoa.saudacao();
```

Esboço da derivação (pontos centrais):

- `StructDecl ⇒ "struct" ID "{" FieldDeclList "}"` com `FieldDeclList` gerando `string nome; int idade;`  
- `MethodDecl ⇒ Type Receiver ID "(" OptParamList ")" Block` com `Type ⇒ "void"` e `Receiver ⇒ "(" ID BaseType ")"` = `(p Pessoa)`  
- `VarDecl ⇒ Type ID OptInit` com `Type ⇒ ID` (nome do tipo `Pessoa`) e `OptInit ⇒ "=" Expr` onde `Expr ⇒ Primary ⇒ ID ObjectLiteral`  
- `Expr ⇒ PostfixExpr "(" OptArgList ")"` para a chamada `pessoa.saudacao()`

---

## 4) Classificação na Hierarquia de Chomsky

**Classificação:** **Tipo 2 — Gramática Livre de Contexto (GLC)**

**Justificativa sintática (resumo):**
- Todas as produções têm **um único não-terminal à esquerda** (`A → α`), sem dependência de contexto.
- A linguagem apresenta **estruturas aninhadas** (blocos `{…}`, chamadas aninhadas, encadeamento de `else if`), não regular.
- Um **autômato de pilha** é suficiente para reconhecer a estrutura (balanceamento de `{}` e `()`), logo **GLC** é apropriada.

**O que *não* é checado sintaticamente (sensível a contexto):**
- “Variável **deve ser declarada antes** de usada”;  
- **Compatibilidade de tipos** em atribuições e argumentos;  
- **Métodos existentes** para uma `struct` específica.  
  
Esses pontos ficam para a **análise semântica** (tabela de símbolos, verificação de tipos), fora do escopo da GLC.

---

## 5) Ambiguidades Potenciais e Estratégias de Resolução

1. **Dangling else**  
   - **Regra**: em `IfStmt`, `ElseChain` pertence ao `if` **mais interno** ainda não casado.  
   - **Implementação**: a nossa fatoração de `IfStmt` + `ElseChain` já induz essa ligação, evitando conflito.

2. **Precedência e associatividade de operadores**  
   - **Estratégia**: gramática em **camadas** (`Or > And > Rel > Add > Mul > Unary > Postfix`) com repetições **à esquerda** nas camadas binárias, impondo associatividade e precedência canônicas.
   - **Efeito**: expressões como `a + b * c` são interpretadas como `a + (b * c)` sem ambiguidades.

3. **VarDecl vs. FuncDecl** (padrão estilo C)  
   - **Observação**: `Type ID "(" …` inicia **função**; `Type ID` seguido de `;` ou `=` inicia **variável**.  
   - **Estratégia**: usar *lookahead* no parser (LL(1) com _peeking_) ou um parser LR. A gramática permanece **livre de contexto**.

4. **Literal de objeto vs. bloco**  
   - **Risco**: `{ ... }` pode ser tanto `Block` quanto `ObjectLiteral`.  
   - **Resolução**: em `Primary`, o literal de objeto **sempre** vem após um **ID de tipo** (`ID ObjectLiteral`), o que o distingue estruturalmente de `Block`.

5. **Inclusão de `++/--`** (_assunção_)  
   - **Risco**: interações com `;` e `=` (ex.: `a = b++`).  
   - **Estratégia**: restringir `AssignStmt` à forma `PostfixExpr "=" Expr` e permitir `Expr ";"` puro quando o objetivo é apenas o efeito colateral (`p.idade++;`).  
   - **Alternativa**: se `++/--` não forem desejados, **remover** de `PostfixOp` e dos testes. A gramática continua coesa.

6. **“else if” como açúcar sintático**  
   - **Decisão**: modelamos `else if` como `else` seguido de um novo `if`, via `ElseChain`.  
   - **Benefício**: remoção de ambiguidade e implementação direta no parser.

---

## 6) Tabela de Precedência (resumo pragmático do §2.6)

| Grupo       | Operadores                         | Associatividade |
|-------------|------------------------------------|-----------------|
| Pós-fixos   | `.`, `()`, `[]`, `++`, `--`        | esquerda        |
| Unários     | `!`, `-`                           | direita         |
| Multiplic.  | `*`, `/`, `%`                      | esquerda        |
| Aditivos    | `+`, `-`                           | esquerda        |
| Relacionais | `==`, `!=`, `>`, `>=`, `<`, `<=`   | esquerda        |
| Lógicos     | `&&`                               | esquerda        |
| Lógicos     | `||`                               | esquerda        |

> **Parênteses** sempre forçam a ordem de avaliação desejada.

---

## 7) Exemplos de Programas Válidos (sanidade sintática)

```clash
// 7.1 variável + expressão
int x = 1 + 2 * 3;

// 7.2 if / else if / else
if (x > 3) { print("maior"); }
else if (x == 3) { print("igual"); }
else { print("menor"); }

// 7.3 struct + método + literal de objeto
struct Pessoa { string nome; int idade; }

void (p Pessoa) saudacao() {
  print(p.nome, " tem ", p.idade, " anos");
}

Pessoa pessoa = { nome: "Ana", idade: 25 };
pessoa.saudacao();
pessoa.idade++;
print(pessoa.idade);
```

---

## 8) Considerações sobre Expressividade × Simplicidade

- **Começar simples** (declarações, expressões, controles básicos) reduz a chance de ambiguidade e facilita o parser.
- **Adicionar recursos por camadas** (ex.: arrays, métodos com receptor, literais de objeto) mantém a gramática sob controle.
- **Separar sintaxe de semântica**: regras de escopo/tipos no analisador semântico, não na GLC.
- **Heurística prática**: qualquer novo construto deve entrar em **uma** das famílias existentes (declaração, comando, expressão) e **respeitar a hierarquia de precedência**.
