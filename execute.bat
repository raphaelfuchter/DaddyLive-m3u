@echo off
TITLE Executando Scripts WSL

echo Iniciando o script no WSL (Ubuntu)...
echo.

REM O comando abaixo executa o script shell dentro do WSL
wsl -e bash /mnt/c/users/rf17/downloads/dl/proxy.sh

echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul