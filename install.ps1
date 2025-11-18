$ErrorActionPreference = "Stop"

$APP_NAME = "clash"
$GITHUB_REPO = "Equipe-Eighteen/.clash"
$RELEASE_TAG = "win-1.0.0"

$INSTALL_DIR = "$env:LOCALAPPDATA\Programs\$APP_NAME"
$INSTALL_PATH = "$INSTALL_DIR\$APP_NAME.exe"

Write-Host "Downloading $APP_NAME..."

$BIN_NAME = "clash.exe"
$TARGET_URL = "https://github.com/$GITHUB_REPO/releases/download/$RELEASE_TAG/$BIN_NAME"

New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null

Invoke-WebRequest -Uri $TARGET_URL -OutFile $INSTALL_PATH

Write-Host "$APP_NAME successfully installed at $INSTALL_PATH"

$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$INSTALL_DIR*") {
    Write-Host "Adding $INSTALL_DIR to your PATH..."
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$UserPath;$INSTALL_DIR",
        "User"
    )
    Write-Host "Installation complete! Please restart your terminal."
} else {
    Write-Host "Installation complete! $APP_NAME is ready to use."
}
