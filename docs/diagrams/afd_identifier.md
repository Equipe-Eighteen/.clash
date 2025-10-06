# Diagrama AFD para Identificadores (`afd_identifier`)

Este diagrama representa o AFD para reconhecer identificadores e palavras-chave, conforme implementado em `afd_identifier`. Um identificador deve começar com uma letra ou underscore, seguido por qualquer número de letras, dígitos ou underscores.

-   **q0**: Estado inicial.
-   **q1**: Estado de aceitação. É alcançado após ler um caractere inicial válido (letra ou `_`) e permanece neste estado enquanto lê caracteres válidos para um identificador. A verificação se o identificador é uma palavra-chave ocorre após a aceitação da sequência.

```mermaid
graph LR
    subgraph AFD para Identificadores
        direction LR
        q0 -- "[a-zA-Z_]" --> q1;
        q1 -- "\\w" --> q1;
        q0 -- "[^a-zA-Z_]" --> q_err;
    end
    style q0 fill:#lightblue,stroke:#333,stroke-width:2px
    style q1 fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_err fill:#f99,stroke:#333,stroke-width:2px,color:#000
```