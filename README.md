# Clash Compiler

Este é o repositório oficial do compilador para a linguagem de programação "Clash". O `README` a seguir contém todas as instruções necessárias para configurar o ambiente de desenvolvimento, rodar os testes e executar o compilador.

## 📋 Índice

- [🚀 Começando](#-começando)
  - [Pré-requisitos](#pré-requisitos)
  - [⚙️ Configuração do Ambiente](#️-configuração-do-ambiente)
    - [Opção 1: Usando `pip` e `venv` (Padrão)](#opção-1-usando-pip-e-venv-padrão)
    - [Opção 2: Usando `uv` (Alternativa Rápida)](#opção-2-usando-uv-alternativa-rápida)
- [✅ Testes](#-testes)
- [▶️ Executando o Compilador](#️-executando-o-compilador)

## 🚀 Começando

Siga os passos abaixo para preparar seu ambiente de desenvolvimento e começar a usar o compilador.

### Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- `pip` e `venv` (geralmente inclusos na instalação do Python).
- Opcional: [uv](https://github.com/astral-sh/uv), um gerenciador de pacotes e ambientes virtuais extremamente rápido.

### ⚙️ Configuração do Ambiente

Para garantir um ambiente de desenvolvimento limpo e isolado, recomendamos o uso de ambientes virtuais. Abaixo estão duas maneiras de configurar o projeto:

---

#### Opção 1: Usando `pip` e `venv` (Padrão)

Esta é a abordagem tradicional e recomendada se você não tiver `uv` instalado.

1.  **Crie um ambiente virtual:**
    O ambiente virtual isola as dependências, evitando conflitos com outros projetos.
    ```sh
    python -m venv .venv
    ```

2.  **Ative o ambiente virtual:**
    - No **Windows**:
      ```sh
      .\.venv\Scripts\activate
      ```
    - No **macOS/Linux**:
      ```sh
      source .venv/bin/activate
      ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.
    ```sh
    pip install -r requirements.txt
    ```

---

#### Opção 2: Usando `uv` (Alternativa Rápida)

Se você busca mais velocidade na criação do ambiente e instalação de pacotes, `uv` é uma excelente escolha que esse projeto suporta.

1.  **Instale os pacotes com `uv`:**
    `uv` cria o ambiente virtual de forma automática muito mais rápida que o `venv` padrão.
    ```sh
    uv sync
    ```
  
2.  **Execute comandos no ambiente virtual:**
    Após a sincronização, você tem duas opções para rodar os comandos:

    - **Opção A: Ativar o shell (tradicional)**
      Você pode ativar o ambiente para a sessão atual do seu terminal.
      - No **Windows**:
        ```sh
        .\.venv\Scripts\activate
        ```
      - No **macOS/Linux**:
        ```sh
        source .venv/bin/activate
        ```

    - **Opção B: Usar `uv run` (recomendado)**
      Para evitar a ativação manual, você pode executar qualquer comando diretamente com `uv run`.
      ```sh
      uv run ...
      ```

---

## ✅ Testes

Para verificar a integridade do compilador e garantir que todas as funcionalidades operam como esperado, execute a suíte de testes automatizados com `pytest`. O comando abaixo irá rodar todos os testes na pasta `tests/` com detalhes (`-v`).

```sh
pytest ./tests/
```

## ▶️ Executando o Compilador

Para compilar um arquivo-fonte da linguagem Clash (com a extensão `.clash`), utilize o script `main.py` seguido do caminho para o arquivo.

```sh
python main.py "caminho/para/seu/arquivo.clash"
```

**Exemplo:**

```sh
python main.py examples/codigo.clash
```

## 📦 Build (Binário)

Gere um executável standalone com PyInstaller. Este projeto usa `pyfiglet`, então inclua os arquivos de fontes:

```sh
pyinstaller --onefile --add-data="/dir/to/repo/clash/.venv/lib/python3.12/site-packages/pyfiglet/fonts:pyfiglet/fonts" main.py
```

Observações:
- O caminho de `pyfiglet/fonts` pode variar conforme seu Python/venv. Ajuste se necessário.
- O executável será criado em `dist/main` (ou renomeie com `--name clash`).

Exemplo com nome do binário:
```sh
pyinstaller --onefile --name clash --add-data="/dir/to/repo/clash/.venv/lib/python3.12/site-packages/pyfiglet/fonts:pyfiglet/fonts" main.py
```

Após o build:
```sh
./dist/clash examples/codigo.clash
```

## 🛠 Instalação no Linux (via curl)

Instale o Clash em uma máquina Linux usando um script `install.sh` hospedado no GitHub:

```sh
curl -fsSL https://raw.githubusercontent.com/Equipe-Eighteen/.clash/refs/heads/main/install.sh | bash
```
