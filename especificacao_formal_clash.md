# Especificação Formal – Linguagem Clash

## 1. Alfabeto

O alfabeto básico $\Sigma$ da linguagem Clash é composto por:

- Letras latinas: `a–z`, `A–Z`
- Algarismos: `0–9`
- Símbolo de sublinhado: `_`
- Operadores e pontuação: `+ - * / % = < > ! & | [ ] { } ( ) ; , . "`
- Espaço em branco, tabulação `\t` e quebra de linha `\n`

Formalmente:

$\Sigma = {a..z, A..Z, 0..9, _, +, -, *, /, %, =, <, >, !, &, |, [, ], {, }, (, ), ;, ,, ., ", \text{espaço}, \text{\t}, \text{\n}}$




## 2. Tokens

### 2.1 Identificadores

- Devem começar com letra ou `_`.
- Podem conter letras, números e `_`.
- São case-sensitive.

Definição formal:

`ID = ( [a-zA-Z_] ) ( [a-zA-Z0-9_]^* )`

Exemplos: `idade`, `nome`, `_temp1`

### 2.2 Literais Numéricos

**Inteiros:**

`INT = (0 | [1-9][0-9]^* )`

Ex: `0`, `25`, `1024`

**Decimais:**

`FLOAT = [0-9]^+ "." [0-9]^+`

Ex: `1.75`, `3.0`

**Notação científica:**

`SCI = (INT | FLOAT) (e|E) (+|−)? [0-9]^+`

Ex: `3.14e10`, `2E-3`

### 2.3 Literais String

- Cadeias delimitadas por aspas `" "`.
- Podem conter letras, números, espaços e caracteres especiais (exceto quebra de linha sem escape).

Definição formal:

`STRING = " ( Σ \ { " } )^* "`

Ex: `"Lucas"`, `"Maior de idade"`

- Mais funcionalidades:
  - Concatenação: `STRING_CONCAT=STRING “+” STRING`
  - Interpolação (Strings podem conter expressões delimitadas por `${ }`.):
    `STRING_INTERP=”(Σ∖{“})∗(“$”EXP””)∗”`

Exemplos:

- `"Olá " + "Mundo"`
- `"Nome: ${nome}, Idade: ${idade}"`

### 2.4 Literais Booleanos

`BOOL = "true" | "false"`

### 2.5 Palavras-chave

Reservadas da linguagem (não podem ser usadas como identificadores):

`int`, `float`, `bool`, `string`, `struct`,
`if`, `else`, `else if`, `for`, `while`, `foreach`, `in`,
`break`, `continue`, `print`, `true`, `false`

### 2.6 Operadores

- Aritméticos: `+ - * / %`
- Relacionais: `== != > >= < <=`
- Lógicos: `&& || !`
- Atribuição: `=`
- Concatenação de strings: `+` (quando ambos operandos forem strings)

### 2.7 Comentários

- Linha única:
  `"//"(Σ^* )`
- Bloco:
  `"/*" (Σ^*) "*/"`

**Atualização em 2.6 Operadores**

Adicionar:

- Concatenação de strings: `+` (quando ambos operandos forem strings)




## 3. Regras Léxicas Gerais

- Espaços em branco e quebras de linha são ignorados, exceto dentro de strings.
- Identificadores são case-sensitive (`idade ≠ Idade`).
- Arrays usam `[]` e podem ser inicializados com `[ ]`.
- Strings aceitam caracteres especiais e devem ser delimitadas por `" "` (aspas duplas).
- Comentários não podem ser aninhados.




## 4. Considerações de Design

- Usabilidade: case-sensitive dá mais flexibilidade, mas exige atenção do programador.
- Ambiguidade evitada: identificadores não podem começar com número → garante distinção clara entre números e variáveis.
- Strings: escolha deliberada por aspas duplas apenas → clareza e simplicidade.
- Espaços: ignorados fora de strings → maior legibilidade sem afetar análise léxica.




## 5. Exemplos Concretos de Programas Válidos

Abaixo, alguns exemplos reais de programas válidos escritos na linguagem Clash:

### Declaração de variáveis e arrays

```clash
int idade = 25;
float altura = 1.75;
bool aprovado = true;
string nome = "Lucas";
int[] numeros = [1, 2, 3, 4, 5];
string[] nomes = ["Ana", "João", "Maria"];
```

### Concatenação e interpolação

```clash
string nome = "Lucas";
int idade = 25;
print("Olá, " + nome + "!");
print("Meu nome é ${nome} e tenho ${idade} anos.");
```

### Estrutura de repetição for

```clash
for (int i = 0; i < numeros.length; i++) {
  if (numeros[i] == 3) {
    continue;
  }
  if (numeros[i] == 5) {
    break;
  }
  print(numeros[i]);
}
```

### Estrutura condicional

```clash
if (idade >= 18 && aprovado) {
  print("Maior de idade e aprovado");
} else if (idade >= 18 && !aprovado) {
  print("Maior de idade mas não aprovado");
} else {
  print("Menor de idade");
}
```

### Structs e acesso a campos

```clash
struct Pessoa {
  string nome;
  int idade;
  float altura;
};
Pessoa p1;
p1.nome = "Lucas";
p1.idade = 25;
p1["altura"] = 1.75;
```


