#!/bin/bash

# Este script executa a sequência de tarefas de autenticação e proxy.

echo "Iniciando a execução dos scripts Python..."

# Mudar para o diretório de trabalho correto
# O caminho completo é usado para garantir que o script funcione de qualquer lugar
cd /mnt/c/users/rf17/downloads/dl

echo "Diretório alterado para $(pwd)"

echo "Executando generate_auth_list.py..."
python3 generate_auth_list.py

echo "Executando generate_signature_urls.py..."
python3 generate_signature_urls.py

echo "Executando curl.py..."
python3 curl.py

echo "Executando fproxy.py..."
python3 fproxy.py
