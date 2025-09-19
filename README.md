# Clash Compiler

Este é o `README` para o projeto do compilador da linguagem Clash. Abaixo estão as instruções essenciais para configurar o ambiente, rodar os testes e executar o compilador.

## 🚀 Começando

Siga os passos abaixo para preparar seu ambiente de desenvolvimento.

### Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- `pip` e `venv` (geralmente inclusos na instalação do Python)

### ⚙️ Configuração do Ambiente

1.  **Crie um ambiente virtual:**
    O ambiente virtual isola as dependências do projeto, evitando conflitos com outros projetos em sua máquina.

    ```sh
    python -m venv .venv
    ```

2.  **Ative o ambiente virtual:**
    - No Windows:
      ```sh
      .\.venv\Scripts\activate
      ```
    - No macOS/Linux:
      ```sh
      source .venv/bin/activate
      ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias para o projeto.

    ```sh
    pip install -r requirements.txt
    ```

## ✅ Testes

Para garantir que tudo está funcionando como esperado, execute a suíte de testes automatizados usando `pytest`. O comando abaixo irá rodar todos os testes na pasta `tests/` com detalhes (`-v`).

```sh
pytest ./tests/ -v
```

## ▶️ Executando o Compilador

Para compilar um arquivo-fonte da linguagem Clash (com a extensão `.clash`), utilize o script `main.py` seguido do caminho para o arquivo.

```sh
python main.py "caminho/para/seu/arquivo.clash"
```

**Exemplo:**

```sh
python main.py "examples/codigo.clash"
```
