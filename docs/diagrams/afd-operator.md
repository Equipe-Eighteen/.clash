# Diagrama AFD para Operadores (`afd_operator`)

Este diagrama representa a lógica para reconhecer operadores usando notação Regex e incluindo a transição de erro, conforme a função `afd_operator`.

-   **q0**: Estado inicial.
-   **Estados Intermediários Não-Finais (azul claro)**: `q_amp` e `q_pipe`, para `&` e `|`.
-   **Estados de Aceitação (verde)**: Todos os outros estados que representam operadores válidos.
-   **q_err (vermelho)**: Estado de erro, alcançado se um caractere não puder iniciar nenhum operador válido.

```mermaid
graph TD
    subgraph "AFD para Operadores e Pontuação"
        direction LR

        %% Estados (Sintaxe corrigida)
        q0["q0"]
        q_eq["="]
        q_not["!"]
        q_less["<"]
        q_greater["'>'"]
        q_mult["'*'"]
        q_amp["q_amp"]
        q_pipe["q_pipe"]

        q_eqeq["=="]
        q_noteq["!="]
        q_lesseq["<="]
        q_greatereq["'>='"]
        q_power["'**'"]
        q_and["&&"]
        q_or["||"]
        
        q_single_op["Op. Simples"]
        q_err["q_err"]

        %% Transições
        q0 -- "=" --> q_eq;
        q_eq -- "=" --> q_eqeq;

        q0 -- "!" --> q_not;
        q_not -- "=" --> q_noteq;

        q0 -- "<" --> q_less;
        q_less -- "=" --> q_lesseq;

        q0 -- "'>'" --> q_greater;
        q_greater -- "=" --> q_greatereq;
        
        q0 -- "'*'" --> q_mult;
        q_mult -- "'*'" --> q_power;

        q0 -- "&" --> q_amp;
        q_amp -- "&" --> q_and;
        q_amp -- "[^&]" --> q_err;

        q0 -- "|" --> q_pipe;
        q_pipe -- "|" --> q_or;
        q_pipe -- "[^|]" --> q_err;

        q0 -- "[+\-/%();,{}\[\]\.,]" --> q_single_op;
        q0 -- "Outro caractere inválido" --> q_err;
    end

    style q0 fill:#lightblue,stroke:#333,stroke-width:2px
    style q_amp fill:#lightblue,stroke:#333,stroke-width:2px
    style q_pipe fill:#lightblue,stroke:#333,stroke-width:2px

    style q_eq fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_not fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_less fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_greater fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_mult fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_single_op fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    
    style q_eqeq fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_noteq fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_lesseq fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_greatereq fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_power fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_and fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_or fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    
    style q_err fill:#f99,stroke:#333,stroke-width:2px,color:#000
```