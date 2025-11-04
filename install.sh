#!/bin/sh
set -e

APP_NAME="clash"
GITHUB_REPO="Equipe-Eighteen/.clash"
RELEASE_TAG="v1.0.0"

INSTALL_DIR="$HOME/.local/bin"
INSTALL_PATH="$INSTALL_DIR/$APP_NAME"
SHELL_PROFILE="$HOME/.bashrc"

ARCH=$(uname -m)
BIN_NAME=""

echo "Arquitetura detectada: $ARCH"

if [ "$ARCH" = "x86_64" ]; then
    BIN_NAME="clash" 
else
    echo "Erro: Este script suporta apenas Linux x86_64 (amd64)."
    echo "Arquitetura encontrada: $ARCH"
    exit 1
fi

TARGET_URL="https://github.com/$GITHUB_REPO/releases/download/$RELEASE_TAG/$BIN_NAME"

echo "Baixando $APP_NAME de $TARGET_URL..."

mkdir -p "$INSTALL_DIR"

curl -L -f "$TARGET_URL" -o "$INSTALL_PATH"

chmod +x "$INSTALL_PATH"

echo "$APP_NAME instalado com sucesso em $INSTALL_PATH"

if ! grep -q "export PATH=\"$INSTALL_DIR:\$PATH\"" "$SHELL_PROFILE" 2>/dev/null; then
    echo "Adicionando $INSTALL_DIR ao seu PATH em $SHELL_PROFILE..."

    {
        echo ""
        echo "# Adicionado pelo instalador do $APP_NAME"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\""
    } >> "$SHELL_PROFILE"

    echo ""
    echo "Instalação concluída!"
    echo "Por favor, reinicie seu terminal ou execute o seguinte comando:"
    echo "source $SHELL_PROFILE"
else
    echo "Instalação concluída! $APP_NAME está pronto para usar."
fi
