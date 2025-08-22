# Diário de Desenvolvimento

**Grupo:** Clash Royale

**Integrantes:** Eduardo Akira, Davi Reina, Gabriel Santos, João Pedro Fusco

## Semana 1

### Informações Básicas

**Data:** 15/08/2025

**Membros presentes:** Eduardo Akira, Davi Reina, Gabriel Santos, João Pedro Fusco

**Tema da semana:** Fundamentos e Planejamento Inicial

### Atividades Realizadas

**Descrição das atividades:**

*   Realizamos a reunião inicial para a formação oficial da equipe e alinhamento de expectativas.
*   Conduzimos uma sessão de brainstorming para definir a visão, os objetivos e o público-alvo da nossa linguagem de programação, batizada de "Clash".
*   Elaboramos a primeira versão do documento "Proposta Inicial da Linguagem", consolidando as ideias discutidas.
*   Criamos um cronograma preliminar para o projeto, dividindo-o em etapas semanais até a entrega final.
*   Definimos os papéis e as responsabilidades iniciais de cada membro da equipe para garantir uma colaboração organizada.
*   Iniciamos este Diário de Desenvolvimento para registrar nosso progresso.

**Artefatos produzidos:**

*   Proposta Inicial da Linguagem
*   Cronograma e Definição de Papéis
*   Diário de Desenvolvimento

**Distribuição de tarefas:**

*   Davi Reina: Liderou a discussão sobre a visão da linguagem e iniciou a redação da Proposta Inicial.
*   Gabriel Santos: Estruturou o cronograma preliminar do projeto e mapeou as principais entregas.
*   Eduardo Akira: Coordenou a definição de papéis e responsabilidades e ajudou na revisão da proposta.
*   João Pedro Fusco: Configurou o repositório do projeto e ficou responsável por documentar as decisões no Diário de Desenvolvimento.

### Dificuldades e Soluções

**Desafios encontrados:**

*   **Desafio 1:** Chegar a um consenso sobre o escopo inicial da linguagem. A tentação de adicionar muitas funcionalidades avançadas desde o início foi grande.
*   **Desafio 2:** Estimar o tempo necessário para cada etapa do desenvolvimento do compilador de forma realista.

**Soluções adotadas:**

*   **Para desafio 1:** Decidimos focar em um MVP (Minimum Viable Product), definindo um conjunto mínimo de funcionalidades (variáveis, tipos básicos, operadores, if/else, for/while) para a primeira versão funcional. Funcionalidades mais complexas como orientação a objetos ou concorrência foram movidas para um escopo futuro.
*   **Para desafio 2:** Pesquisamos cronogramas de projetos similares e adicionamos uma margem de segurança em nossas estimativas. O cronograma será revisado semanalmente para refletir o progresso real.

**Conhecimentos adquiridos:**

*   Planejamento de alto nível de projetos de software.
*   Técnicas de brainstorming e definição de escopo (MVP).
*   Importância da documentação inicial para alinhar a equipe.

### Reflexão sobre Aplicação dos Conceitos

**Conceitos teóricos aplicados:**

*   **Engenharia de Requisitos:** A criação da "Proposta Inicial da Linguagem" é um exercício prático da fase de levantamento e elicitação de requisitos, definindo o "o quê" e o "porquê" do projeto.
*   **Gerenciamento de Projetos:** A elaboração do cronograma e a divisão de papéis são aplicações diretas de conceitos de planejamento e organização de equipes, fundamentais para o sucesso do projeto.

**Insights obtidos:**

*   Um planejamento inicial bem-feito, mesmo que preliminar, é crucial para dar direção e evitar retrabalho.
*   A clareza na comunicação e a definição de responsabilidades desde o início evitam conflitos e aumentam a produtividade.

### Próximos Passos

**Planejamento para próxima aula:**

*   Apresentar a Proposta Inicial para feedback.
*   Começar a estudar e definir a gramática formal da linguagem (em BNF ou EBNF).

**Tarefas pendentes:**

*   Revisar e finalizar a Proposta Inicial com base em feedbacks
*   Pesquisar ferramentas para análise léxica e sintática (Lex/Yacc, ANTLR, etc.)

**Objetivos para próxima semana:**

*   Ter a primeira versão da especificação léxica da linguagem (tokens, palavras-chave, operadores).
*   Esboçar a gramática para as estruturas de controle básicas (if, for, while).

## Semana 2

### Informações Básicas

**Data:** 22/08/2025

**Membros presentes:** Eduardo Akira, Davi Reina, Gabriel Santos, João Pedro Fusco

**Tema da semana:** Definição de Sintaxe e Decisões sobre Elementos da Linguagem

### Atividades Realizadas

**Descrição das atividades:**

*   Realizamos uma reunião para revisar as decisões da semana anterior e consolidar as escolhas de sintaxe.
*   Definimos o comportamento dos identificadores, strings, comentários, e outros elementos fundamentais da linguagem "Clash".
*   Começamos a trabalhar na especificação léxica da linguagem, com ênfase na identificação de tokens e palavras-chave.
*   Realizamos uma análise das ferramentas disponíveis para análise léxica e sintática (Lex/Yacc, ANTLR), decidindo que vamos explorar ANTLR como nossa ferramenta principal.
*   Esboçamos as primeiras estruturas de controle da linguagem (if, for, while), visando garantir uma implementação simples e eficiente.

**Artefatos produzidos:**

*   Especificação Léxica Inicial (Tokens, palavras-chave)
*   Análise das ferramentas (Lex/Yacc, ANTLR)
*   Esboço das estruturas de controle (if, for, while)

**Distribuição de tarefas:**

*   Davi Reina: Liderou a definição da sintaxe e dos identificadores da linguagem, além de ajudar na análise das ferramentas de parser.
*   Gabriel Santos: Continuou com a elaboração da especificação léxica e pesquisou ferramentas de análise sintática.
*   Eduardo Akira: Colaborou nas definições de sintaxe e na pesquisa de implementações para estruturas de controle.
*   João Pedro Fusco: Atualizou o repositório com as novas decisões e documentou as escolhas feitas durante a semana.

### Dificuldades e Soluções

**Desafios encontrados:**

*   **Desafio 1:** Tomar decisões sobre os detalhes da sintaxe, especialmente sobre as convenções de comentários, espaços em branco e regras para identificadores.
*   **Desafio 2:** Escolher a ferramenta certa para análise léxica e sintática, considerando tanto a flexibilidade quanto a curva de aprendizado.

**Soluções adotadas:**

*   **Para desafio 1:** Discutimos e decidimos adotar convenções que seguem a prática comum de linguagens populares (C, Java, Python), equilibrando simplicidade e flexibilidade. Cada decisão foi justificada com base na necessidade de clareza e manutenção da consistência.
*   **Para desafio 2:** Optamos por ANTLR, que oferece maior flexibilidade na criação de gramáticas e integra bem com outras ferramentas e linguagens, como Java, o que facilita nossa implementação.

**Conhecimentos adquiridos:**

*   Como definir uma sintaxe clara e consistente para uma linguagem de programação.
*   A importância de escolher ferramentas adequadas para análise léxica e sintática.
*   Estratégias para equilibrar as convenções da linguagem com a simplicidade de implementação.

### Reflexão sobre Aplicação dos Conceitos

**Conceitos teóricos aplicados:**

*   **Teoria de Linguagens Formais e Autômatos:** As decisões sobre a sintaxe e análise léxica são baseadas em conceitos de autômatos finitos e gramáticas formais, fundamentais para o desenvolvimento de compiladores.
*   **Ferramentas para Análise Sintática:** A escolha de ANTLR como ferramenta principal para o parsing é um exemplo de aplicação prática das técnicas de análise de sintaxe em compiladores.

**Insights obtidos:**

*   A sintaxe de uma linguagem deve ser simples e intuitiva, sem perder a expressividade necessária.
*   A escolha da ferramenta para parsing pode impactar diretamente a produtividade e a flexibilidade no desenvolvimento do compilador.

### Próximos Passos

**Planejamento para próxima aula:**

*   Revisar a especificação léxica e garantir que os tokens estejam bem definidos.
*   Iniciar a construção da gramática para estruturas de controle (if, for, while) e outras construções simples.
*   Preparar um protótipo inicial do analisador léxico com ANTLR.

**Tarefas pendentes:**

*   Finalizar as definições de tokens e palavras-chave.
*   Começar a trabalhar na implementação do analisador léxico (lexer) utilizando ANTLR.
*   Explorar mais profundamente a gramática da linguagem e como implementá-la de forma eficiente.

**Objetivos para próxima semana:**

*   Ter uma versão funcional do analisador léxico.
*   Concluir a definição das estruturas de controle da linguagem.

*   Começar a testar o analisador léxico com exemplos simples de código.

