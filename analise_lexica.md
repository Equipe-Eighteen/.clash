### Entrega da Semana: Análise Léxica da Linguagem Clash

---

### 1. Especificação Completa Usando Expressões Regulares

A seguir, são apresentadas as expressões regulares para cada um dos tokens da linguagem Clash, com base em sua especificação formal e gramática.

| Tipo de Token | Expressão Regular (Regex) | Descrição |
| :--- | :--- | :--- |
| **PALAVRAS-CHAVE** | | |
| `INT_KEYWORD` | `\bint\b` | Palavra-chave para o tipo inteiro. |
| `FLOAT_KEYWORD`| `\bfloat\b` | Palavra-chave para o tipo ponto flutuante. |
| `BOOL_KEYWORD` | `\bbool\b` | Palavra-chave para o tipo booleano. |
| `STRING_KEYWORD`| `\bstring\b` | Palavra-chave para o tipo string. |
| `STRUCT_KEYWORD`| `\bstruct\b` | Palavra-chave para declaração de estruturas. |
| `IF_KEYWORD` | `\bif\b` | Palavra-chave para declaração condicional. |
| `ELSE_KEYWORD` | `\belse\b` | Palavra-chave para alternativa condicional. |
| `FOR_KEYWORD` | `\bfor\b` | Palavra-chave para laços de repetição. |
| `WHILE_KEYWORD` | `\bwhile\b` | Palavra-chave para laços de repetição. |
| `FOREACH_KEYWORD`| `\bforeach\b`| Palavra-chave para iteração em coleções. |
| `IN_KEYWORD` | `\bin\b` | Usada em laços `foreach`. |
| `BREAK_KEYWORD` | `\bbreak\b` | Palavra-chave para interromper laços. |
| `CONTINUE_KEYWORD`| `\bcontinue\b`| Palavra-chave para pular uma iteração. |
| `PRINT_KEYWORD` | `\bprint\b` | Palavra-chave para a função de impressão. |
| `TRUE_KEYWORD` | `\btrue\b` | Literal booleano verdadeiro. |
| `FALSE_KEYWORD` | `\bfalse\b` | Literal booleano falso. |
| `VOID_KEYWORD` | `\bvoid\b` | Palavra-chave para tipo de retorno vazio. |
| **IDENTIFICADORES**| | |
| `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nomes de variáveis, funções, structs, etc. |
| **LITERAIS** | | |
| `INT_LIT` | `0\|[1-9][0-9]*` | Números inteiros. |
| `FLOAT_LIT` | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` | Números de ponto flutuante, incluindo notação científica opcional. |
| `STRING_LIT` | `\"([^\"\\]\|\\.)*\"` | Sequência de caracteres entre aspas duplas. |
| **OPERADORES** | | |
| `OP_SOMA` | `\+` | Adição. |
| `OP_SUB` | `-` | Subtração. |
| `OP_MULT` | `\*` | Multiplicação. |
| `OP_DIV` | `/` | Divisão. |
| `OP_MOD` | `%` | Módulo. |
| `OP_IGUAL` | `==` | Igualdade. |
| `OP_DIF` | `!=` | Diferença. |
| `OP_MAIOR` | `>` | Maior que. |
| `OP_MAIOR_IGUAL`| `>=` | Maior ou igual a. |
| `OP_MENOR` | `<` | Menor que. |
| `OP_MENOR_IGUAL`| `<=` | Menor ou igual a. |
| `OP_E` | `&&` | E lógico. |
| `OP_OU` | `\|\|` | Ou lógico. |
| `OP_NAO` | `!` | Negação lógica. |
| `OP_ATRIB` | `=` | Atribuição. |
| `OP_ACESS` | `\.` | Acesso a membro de struct. |
| **PONTUAÇÃO** | | |
| `PONTO_VIRGULA` | `;` | Final de declaração. |
| `VIRGULA` | `,` | Separador de argumentos/parâmetros. |
| `ABRE_PARENTESES`| `\(` | Abertura de parênteses. |
| `FECHA_PARENTESES`| `\)` | Fechamento de parênteses. |
| `ABRE_CHAVES` | `\{` | Abertura de bloco de código. |
| `FECHA_CHAVES` | `\}` | Fechamento de bloco de código. |
| `ABRE_COLCHETES`| `\[` | Abertura de colchetes (arrays). |
| `FECHA_COLCHETES`| `\]` | Fechamento de colchetes (arrays). |
| **COMENTÁRIOS** | | |
| `COMENT_LINHA` | `\/\/.*` | Comentário de uma única linha. |
| `COMENT_BLOCO` | `\/\*([^*]|\*+[^/])*\*\/` | Comentário de múltiplas linhas. |
| **ESPAÇOS EM BRANCO**| | |
| `ESPACO` | `[ \t\r\n]+` | Espaços, tabulações e quebras de linha a serem ignorados. |

---

### 2. Análise de Ambiguidades e Regras de Resolução

A especificação léxica pode apresentar ambiguidades, que devem ser resolvidas com regras claras.

* **Palavras-chave vs. Identificadores**: Uma sequência como "if" corresponde tanto à expressão regular de uma palavra-chave (`\bif\b`) quanto à de um identificador (`[a-zA-Z_][a-zA-Z0-9_]*`).
    * **Regra de Resolução**: A regra da "correspondência mais longa" (maximal munch) é aplicada. Caso o comprimento seja o mesmo, as palavras-chave têm prioridade sobre os identificadores. O analisador léxico primeiro verifica se o lexema corresponde a uma palavra-chave. Se não, ele é classificado como um identificador.

* **Operadores Compostos**: Os operadores `<`, `<=`, `>` e `>=` podem gerar ambiguidades. Por exemplo, em `<=`, o analisador poderia reconhecer o token `<` e depois um token `=` separado.
    * **Regra de Resolução**: Novamente, a regra da "correspondência mais longa" é utilizada. O analisador léxico tentará corresponder a maior sequência de caracteres possível. Assim, `<=`, `>=`, `==` e `!=` serão sempre reconhecidos como um único token.

* **Literais Numéricos**: A expressão para `FLOAT_LIT` (`[0-9]+\.[0-9]+...`) pode ser ambígua com o operador de acesso a membro (`.`).
    * **Regra de Resolução**: O contexto sintático geralmente resolve essa ambiguidade. No entanto, em nível léxico, a presença de dígitos antes e depois do ponto caracteriza um `FLOAT_LIT`. A análise da sequência de caracteres determinará a natureza do token.

---

### 3. Estratégia para Tratamento de Erros Léxicos

O analisador léxico deve ser robusto e capaz de lidar com caracteres ou sequências inesperadas.

* **Caracteres Inválidos**: Quando um caractere que não pertence ao alfabeto da linguagem é encontrado (por exemplo, `@`, `#`, `$` fora de uma string ou comentário), um erro léxico é gerado.

* **Modo Pânico (Panic Mode)**: Esta é uma estratégia de recuperação de erro simples e eficaz. Ao encontrar um erro, o analisador léxico pode descartar caracteres até encontrar um delimitador bem definido, como um ponto e vírgula, uma chave de fechamento (`}`) ou uma quebra de linha. Isso permite que a análise continue, possibilitando a detecção de múltiplos erros em uma única compilação.

* **Relatórios de Erro Detalhados**: As mensagens de erro devem ser informativas, indicando a localização precisa do erro (número da linha e da coluna) e uma descrição do problema.

---

### 4. Primeiros Esboços de Mensagens de Erro para Usuários

A seguir, alguns exemplos de mensagens de erro que podem ser geradas pelo analisador léxico da Clash:

* **Caractere Inválido**:
    * `Erro Léxico (Linha 5, Coluna 10): O caractere '@' não é válido nesta linguagem.`
    * `Erro Léxico (Linha 12, Coluna 3): Símbolo inesperado '#'.`

* **String Malformada**:
    * `Erro Léxico (Linha 8, Coluna 25): A string iniciada não foi finalizada. Faltando '"'.`

* **Número Malformado**:
    * `Erro Léxico (Linha 20, Coluna 15): Número de ponto flutuante malformado: '3.14.15'.`

* **Comentário de Bloco Não Finalizado**:

    * `Erro Léxico (Fim do arquivo): O comentário de bloco iniciado na linha 30 não foi finalizado com '*/'.`
