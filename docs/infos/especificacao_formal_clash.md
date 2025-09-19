# Especificação Formal da Linguagem Clash

## 1. Introdução

Esta seção apresenta a especificação formal da linguagem de programação Clash, detalhando seus componentes léxicos, sintáticos e semânticos. O objetivo é fornecer uma descrição precisa e não ambígua da linguagem, utilizando notação matemática baseada em conjuntos para as definições formais. Esta versão incorpora a definição de `structs` e `métodos` vinculados a `structs`, expandindo as capacidades de modelagem de dados da linguagem.

## 2. Alfabeto (Σ)

O alfabeto (Σ) da linguagem Clash é o conjunto finito de todos os símbolos básicos que podem ser utilizados para construir programas válidos. Ele é definido como a união dos seguintes subconjuntos:

*   **Letras Latinas (L):** `L = { 'a', ..., 'z', 'A', ..., 'Z' }`
*   **Algarismos (D):** `D = { '0', ..., '9' }`
*   **Símbolo de Sublinhado (U):** `U = { '_' }`
*   **Operadores e Pontuação (P):** `P = { '+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '[', ']', '{', '}', '(', ')', ';', ',', '.', '"' }`
*   **Espaços em Branco (W):** `W = { ' ', '\t', '\n', '\r' }` (espaço, tabulação, quebra de linha, retorno de carro)

Formalmente, o alfabeto Σ é dado por:

`Σ = L ∪ D ∪ U ∪ P ∪ W`

## 3. Tokens

Tokens são as menores unidades significativas da linguagem. A análise léxica transforma uma sequência de caracteres do alfabeto em uma sequência de tokens.

### 3.1 Identificadores (ID)

Identificadores são nomes dados a variáveis, funções, tipos, etc. Em Clash, um identificador deve começar com uma letra ou um sublinhado, seguido por zero ou mais letras, algarismos ou sublinhados. Identificadores são case-sensitive.

Formalmente, o conjunto de identificadores (ID) é definido por:

`ID = { s ∈ Σ* | s = l c* ∧ l ∈ (L ∪ U) ∧ c ∈ (L ∪ D ∪ U) }`

Onde `s` é uma string de caracteres, `l` é o primeiro caractere (letra ou sublinhado) e `c*` representa zero ou mais caracteres subsequentes (letras, algarismos ou sublinhados).

Exemplos: `idade`, `nome`, `_temp1`, `minhaVariavel`, `totalVendas`

### 3.2 Literais Numéricos

#### 3.2.1 Inteiros (INT)

Literais inteiros são sequências de algarismos que representam números inteiros. Não podem ter zeros à esquerda, exceto o próprio zero.

Formalmente, o conjunto de inteiros (INT) é definido por:

`INT = { s ∈ D* | s = '0' ∨ (s = d d'* ∧ d ∈ D \ { '0' } ∧ d' ∈ D) }`

Exemplos: `0`, `25`, `1024`, `98765`

#### 3.2.2 Decimais (FLOAT)

Literais decimais representam números de ponto flutuante e contêm um ponto decimal.

Formalmente, o conjunto de decimais (FLOAT) é definido por:

`FLOAT = { s ∈ Σ* | s = d+ '.' d+ ∧ d ∈ D }`

Exemplos: `1.75`, `3.0`, `0.5`, `123.456`

#### 3.2.3 Notação Científica (SCI)

Literais em notação científica representam números de ponto flutuante com um expoente.

Formalmente, o conjunto de notações científicas (SCI) é definido por:

`SCI = { s ∈ Σ* | s = (i | f) ('e' | 'E') ('+' | '-')? d+ ∧ i ∈ INT ∧ f ∈ FLOAT ∧ d ∈ D }`

Exemplos: `3.14e10`, `2E-3`, `1.0e+5`, `6.022E23`

### 3.3 Literais String (STRING)

Literais string são sequências de caracteres delimitadas por aspas duplas. Podem conter qualquer caractere do alfabeto, exceto aspas duplas não escapadas e quebras de linha não escapadas.

Formalmente, o conjunto de strings (STRING) é definido por:

`STRING = { s ∈ Σ* | s = '"' c* '"' ∧ c ∈ (Σ \ { '"', '\n', '\r' }) }`

Exemplos: `"Lucas"`, `"Maior de idade"`, `"Olá Mundo!"`

#### 3.3.1 Concatenação de Strings

A concatenação de strings é uma operação binária que une duas strings. Em Clash, é representada pelo operador `+` quando ambos os operandos são do tipo `string`.

Formalmente, a operação de concatenação é uma função `C: STRING × STRING → STRING` definida como:

`C(s1, s2) = s1s2` (onde `s1s2` denota a concatenação das sequências de caracteres `s1` e `s2`)

#### 3.3.2 Interpolação de Strings

A interpolação de strings permite a inclusão de expressões dentro de literais string, delimitadas por `${ }`. A expressão é avaliada e seu resultado é convertido para string e inserido no local.

Formalmente, uma string interpolada pode ser vista como uma sequência de segmentos de string e expressões:

`STRING_INTERP = { s ∈ Σ* | s = (c* ('${' EXP '}')?)* c* ∧ c ∈ (Σ \ { '"', '\n', '\r' }) }`

Onde `EXP` representa uma expressão válida na linguagem.

Exemplos: `"Olá, ${nome}!"`, `"Meu nome é ${nome} e tenho ${idade} anos."`

### 3.4 Literais Booleanos (BOOL)

Literais booleanos representam os valores verdade `true` e `false`.

Formalmente, o conjunto de booleanos (BOOL) é definido por:

`BOOL = { "true", "false" }`

### 3.5 Palavras-chave (KEYWORD)

Palavras-chave são identificadores reservados que possuem um significado predefinido na linguagem e não podem ser utilizados como identificadores definidos pelo usuário.

Formalmente, o conjunto de palavras-chave (KEYWORD) é:

`KEYWORD = { "int", "float", "bool", "string", "struct", "if", "else", "else if", "for", "while", "foreach", "in", "break", "continue", "print", "true", "false", "void" }`

### 3.6 Operadores (OP)

Operadores são símbolos que representam operações a serem realizadas sobre um ou mais operandos.

Formalmente, o conjunto de operadores (OP) é a união dos seguintes subconjuntos:

*   **Aritméticos (OP_ARITH):** `OP_ARITH = { '+', '-', '*', '/', '%' }`
*   **Relacionais (OP_REL):** `OP_REL = { '==', '!=', '>', '>=', '<', '<=' }`
*   **Lógicos (OP_LOGIC):** `OP_LOGIC = { '&&', '||', '!' }`
*   **Atribuição (OP_ASSIGN):** `OP_ASSIGN = { '=' }`
*   **Acesso a Membro (OP_MEMBER):** `OP_MEMBER = { '.' }`

`OP = OP_ARITH ∪ OP_REL ∪ OP_LOGIC ∪ OP_ASSIGN ∪ OP_MEMBER`

### 3.7 Comentários (COMMENT)

Comentários são sequências de caracteres ignoradas pelo compilador, utilizadas para documentação do código. Clash suporta comentários de linha única e de bloco.

*   **Comentário de Linha Única (SINGLE_LINE_COMMENT):** Começa com `//` e vai até o final da linha.
    `SINGLE_LINE_COMMENT = { s ∈ Σ* | s = '//' c* '\n' ∧ c ∈ Σ }`

*   **Comentário de Bloco (BLOCK_COMMENT):** Começa com `/*` e termina com `*/`. Não podem ser aninhados.
    `BLOCK_COMMENT = { s ∈ Σ* | s = '/*' c* '*/' ∧ c ∈ (Σ \ { '*' '/' })* }`

## 4. Tipos de Dados

Clash é uma linguagem tipada, com tipos primitivos e tipos definidos pelo usuário.

### 4.1 Tipos Primitivos (TP)

`TP = { "int", "float", "bool", "string", "void" }`

### 4.2 Tipos Estruturados (Structs)

Structs permitem agrupar dados de diferentes tipos sob um único nome, criando tipos de dados compostos. Uma `struct` é uma coleção de campos, onde cada campo tem um nome (identificador) e um tipo.

Formalmente, uma `StructType` é um par `(S_name, Fields)`, onde:

*   `S_name` é o nome da struct, um `ID`.
*   `Fields` é um conjunto finito de pares `(Field_name, Field_type)`, onde `Field_name` é um `ID` e `Field_type` é um `Type` (primitivo ou outra struct).

`StructType = { (S_name, Fields) | S_name ∈ ID ∧ Fields ⊆ (ID × Type) }`

Onde `Type = TP ∪ { S_name | (S_name, _) ∈ StructType }` (recursivo).

Exemplo de declaração de struct:

```clash
struct Pessoa {
    string nome;
    int idade;
}
```

Representação formal para `Pessoa`:

`Pessoa = ("Pessoa", { ("nome", "string"), ("idade", "int") })`

### 4.3 Arrays (ARRAY_TYPE)

Arrays são coleções ordenadas de elementos do mesmo tipo.

Formalmente, um `ARRAY_TYPE` é um par `(Element_Type, Dimension)`, onde `Element_Type` é qualquer `Type` e `Dimension` é um inteiro não negativo (opcionalmente, pode ser indefinido para arrays dinâmicos).

`ARRAY_TYPE = { (T, D) | T ∈ Type ∧ D ∈ (INT ∪ {undefined}) }`

Exemplo: `int[] numeros`, `string[] nomes`

## 5. Declarações

### 5.1 Declaração de Variáveis

Uma declaração de variável associa um identificador a um tipo e, opcionalmente, a um valor inicial.

Formalmente, uma `VarDecl` é uma tupla `(Var_name, Var_type, Initial_Value?)`, onde:

*   `Var_name` é o nome da variável, um `ID`.
*   `Var_type` é o tipo da variável, um `Type`.
*   `Initial_Value` é uma `Expression` opcional cujo tipo deve ser compatível com `Var_type`.

`VarDecl = { (V_name, V_type, Init_Val) | V_name ∈ ID ∧ V_type ∈ Type ∧ Init_Val ∈ (Expression ∪ {null}) }`

Exemplo: `int idade = 25;`

### 5.2 Declaração de Métodos (Funções Vinculadas a Structs)

Métodos são funções associadas a um tipo `struct`. Eles operam sobre instâncias dessa `struct` e podem acessar e modificar seus campos. O primeiro parâmetro de um método é implicitamente a instância da struct (`receiver`).

Formalmente, um `MethodDecl` é uma tupla `(Receiver_Type, Method_name, Parameters, Return_Type, Body)`, onde:

*   `Receiver_Type` é o tipo da struct à qual o método está vinculado, um `StructType`.
*   `Method_name` é o nome do método, um `ID`.
*   `Parameters` é uma lista ordenada de pares `(Param_name, Param_type)`, onde `Param_name` é um `ID` e `Param_type` é um `Type`.
*   `Return_Type` é o tipo de retorno do método, um `Type` (incluindo `void`).
*   `Body` é uma sequência de `Statement`s que compõem o corpo do método.

`MethodDecl = { (R_type, M_name, Params, Ret_type, Body) | R_type ∈ StructType ∧ M_name ∈ ID ∧ Params ⊆ (ID × Type)* ∧ Ret_type ∈ Type ∧ Body ∈ Statement* }`

Exemplo de declaração de método:

```clash
void (p Pessoa) saudacao() {
    print(p.nome, " tem ", p.idade, " anos");
}
```

Representação formal para `saudacao`:

`saudacao = (Pessoa, "saudacao", [], "void", bodySaudacao)`

Onde `bodySaudacao` é a representação formal do corpo do método `print(p.nome, " tem ", p.idade, " anos");`.

Exemplo de método que altera o estado da struct:

```clash
void (p Pessoa) aniversario() {
    p.idade++;
}
```

Representação formal para `aniversario`:

`aniversario = (Pessoa, "aniversario", [], "void", bodyAniversario)`

Onde `bodyAniversario` é a representação formal do corpo do método `p.idade++;`.

## 6. Expressões

Expressões são combinações de literais, identificadores, operadores e chamadas de métodos que produzem um valor.

### 6.1 Acesso a Membro de Struct

O acesso a um campo de uma struct é realizado usando o operador `.`.

Formalmente, uma `MemberAccess` é uma tupla `(Instance, Field_name)`, onde:

*   `Instance` é uma `Expression` cujo tipo é uma `StructType`.
*   `Field_name` é o nome do campo, um `ID`, que deve pertencer ao conjunto de `Fields` da `StructType` de `Instance`.

`MemberAccess = { (Inst, F_name) | Inst ∈ Expression ∧ Type(Inst) ∈ StructType ∧ F_name ∈ Fields(Type(Inst)) }`

Exemplo: `pessoa.nome`, `p.idade`

### 6.2 Chamada de Método

A chamada de um método em uma instância de struct é realizada usando a sintaxe `instance.MethodName(arguments)`.

Formalmente, uma `MethodCall` é uma tupla `(Instance, Method_name, Arguments)`, onde:

*   `Instance` é uma `Expression` cujo tipo é uma `StructType`.
*   `Method_name` é o nome do método, um `ID`, que deve ser um método definido para a `StructType` de `Instance`.
*   `Arguments` é uma lista ordenada de `Expression`s, cujos tipos devem ser compatíveis com os `Parameters` do `MethodDecl` correspondente.

`MethodCall = { (Inst, M_name, Args) | Inst ∈ Expression ∧ Type(Inst) ∈ StructType ∧ (Type(Inst), M_name, Params, _, _) ∈ MethodDecl ∧ CompatibleTypes(Args, Params) }`

Exemplo: `pessoa.saudacao()`, `pessoa.aniversario()`

## 7. Semântica Operacional (Exemplo Simplificado)

Para ilustrar a semântica, consideremos um fragmento de programa e como seu estado é alterado.

**Estado (State):** Um mapeamento de identificadores para seus valores e tipos.

`State = ID → (Value × Type)`

**Valores de Struct (StructValue):** Uma instância de struct é um mapeamento de nomes de campos para seus valores.

`StructValue = Field_name → Value`

### Exemplo de Execução:

Considere o seguinte fragmento de código:

```clash
struct Pessoa {
    string nome;
    int idade;
}

Pessoa pessoa = { nome: "Ana", idade: 25 };

pessoa.saudacao();

pessoa.aniversario();
pessoa.saudacao();
```

1.  **Declaração da Struct `Pessoa`:**
    A definição da `struct Pessoa` é adicionada ao ambiente de tipos.

2.  **`Pessoa pessoa = { nome: "Ana", idade: 25 };`**
    *   Uma nova instância de `Pessoa` é criada. `v_pessoa = { "nome": "Ana", "idade": 25 }`.
    *   O estado é atualizado: `State = { "pessoa": (v_pessoa, Pessoa) }`.

3.  **`pessoa.saudacao();`**
    *   O método `Saudacao` da instância `pessoa` é invocado.
    *   Dentro de `Saudacao`, `p` refere-se a `v_pessoa`.
    *   `p.nome` avalia para `"Ana"`.
    *   `p.idade` avalia para `25`.
    *   A função `print` é chamada com os argumentos `"Ana"`, `" tem "`, `25`, `" anos"`.
    *   Saída: `Ana tem 25 anos`

4.  **`pessoa.aniversario();`**
    *   O método `Aniversario` da instância `pessoa` é invocado.
    *   Dentro de `Aniversario`, `p` refere-se a `v_pessoa`.
    *   `p.idade++` é avaliado:
        *   `p.idade` (25) é incrementado para 26.
        *   `v_pessoa` é atualizado para `{ "nome": "Ana", "idade": 26 }`.
    *   O estado é atualizado: `State = { "pessoa": (v_pessoa, Pessoa) }`.

5.  **`pessoa.saudacao();`**
    *   O método `Saudacao` da instância `pessoa` é invocado novamente.
    *   Dentro de `Saudacao`, `p` refere-se a `v_pessoa` (agora com idade 26).
    *   `p.nome` avalia para `"Ana"`.
    *   `p.idade` avalia para `26`.
    *   A função `print` é chamada com os argumentos `"Ana"`, `" tem "`, `26`, `" anos"`.
    *   Saída: `Ana tem 26 anos`

## 8. Considerações Finais

Esta especificação formal serve como base para a implementação e verificação da linguagem Clash. A utilização de notação de conjuntos visa garantir a precisão e a clareza das definições, minimizando ambiguidades. Futuras expansões da linguagem deverão seguir este rigor formal para manter a consistência e a robustez do design.



### 3.1.1 Convenções de Nomenclatura

A linguagem Clash adota convenções de nomenclatura específicas para melhorar a legibilidade e consistência do código:

*   **camelCase:** Utilizado para a maioria dos identificadores, incluindo nomes de variáveis, parâmetros, campos de structs e nomes de métodos. O primeiro caractere é minúsculo, e as primeiras letras de palavras subsequentes são maiúsculas (ex: `minhaVariavel`, `calcularTotal`, `nomeCompleto`).

*   **PascalCase:** Exclusivamente utilizado para nomes de `structs`. O primeiro caractere de cada palavra é maiúsculo (ex: `Pessoa`, `Produto`, `DadosDoCliente`).

Formalmente, para um identificador `id ∈ ID`:

*   `isCamelCase(id)` se `id` começa com uma letra minúscula e segue o padrão `[a-z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*`.
*   `isPascalCase(id)` se `id` começa com uma letra maiúscula e segue o padrão `[A-Z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*`.

As regras de validação de `ID` (Seção 3.1) permanecem as mesmas, e estas convenções são diretrizes de estilo que devem ser seguidas pelos programadores.
