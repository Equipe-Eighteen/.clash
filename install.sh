#!/bin/sh
set -e

APP_NAME="clash"
GITHUB_REPO="Equipe-Eighteen/.clash"
RELEASE_TAG="linux-1.0.0"

INSTALL_DIR="$HOME/.local/bin"
INSTALL_PATH="$INSTALL_DIR/$APP_NAME"
SHELL_PROFILE="$HOME/.bashrc"

ARCH=$(uname -m)
BIN_NAME=""

echo "Detected architecture: $ARCH"

if [ "$ARCH" = "x86_64" ]; then
    BIN_NAME="clash" 
else
    echo "Error: This script only supports Linux x86_64 (amd64)."
    echo "Found architecture: $ARCH"
    exit 1
fi

TARGET_URL="https://github.com/$GITHUB_REPO/releases/download/$RELEASE_TAG/$BIN_NAME"

echo "Downloading $APP_NAME from $TARGET_URL..."

mkdir -p "$INSTALL_DIR"

curl -L -f "$TARGET_URL" -o "$INSTALL_PATH"

chmod +x "$INSTALL_PATH"

echo "$APP_NAME successfully installed at $INSTALL_PATH"

if ! grep -q "export PATH=\"$INSTALL_DIR:\$PATH\"" "$SHELL_PROFILE" 2>/dev/null; then
    echo "Adding $INSTALL_DIR to your PATH in $SHELL_PROFILE..."

    {
        echo ""
        echo "# Added by $APP_NAME installer"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\""
    } >> "$SHELL_PROFILE"

    echo ""
    echo "Installation complete!"
    echo "Please restart your terminal or run the following command:"
    echo "source $SHELL_PROFILE"
else
    echo "Installation complete! $APP_NAME is ready to use."
fi
