#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- INICIANDO CONSTRUÇÃO E INSTALAÇÃO (RENDER BUILD) ---"

# Atualizar pip e instalar dependências do requirements.txt
echo "Instalando pacotes python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "--- PROCESSO DE BUILD CONCLUÍDO COM SUCESSO ---"
