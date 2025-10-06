# Diagrama AFD para Números (`afd_number`)

Este diagrama representa o Autômato Finito Determinístico (AFD) para reconhecer números inteiros e de ponto flutuante, conforme implementado no método `afd_number`.

-   **q0**: Estado inicial.
-   **q1**: Estado de aceitação para **números inteiros**. O autômato chega aqui após ler um ou mais dígitos.
-   **q2**: Estado de transição após encontrar um ponto decimal. Este estado não é de aceitação; ele exige que um dígito venha a seguir.
-   **q3**: Estado de aceitação para **números de ponto flutuante**. O autômato chega aqui após ler um ponto decimal e um ou mais dígitos.
-   **q_err**: Estado de erro, alcançado se um ponto decimal não for seguido por um dígito.

```mermaid
graph LR
    subgraph AFD para Números
        direction LR
        q0 -- "\\d" --> q1;
        q1 -- "\\d" --> q1;
        q1 -- ". (?=\\d)" --> q2;
        q1 -- ". (?!\\d)" --> q_err;
        q2 -- "\\d" --> q3;
        q3 -- "\\d" --> q3;
    end
    style q0 fill:#lightblue,stroke:#333,stroke-width:2px
    style q1 fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q2 fill:#lightblue,stroke:#333,stroke-width:2px
    style q3 fill:#9f9,stroke:#333,stroke-width:2px,color:#000
    style q_err fill:#f99,stroke:#333,stroke-width:2px,color:#000
```