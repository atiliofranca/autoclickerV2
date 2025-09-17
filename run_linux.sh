#!/bin/bash

echo "========================================"
echo "   Automação v2.0 - Execução Rápida"
echo "========================================"
echo

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "ERRO: Ambiente virtual não encontrado!"
    echo "Execute primeiro o start_linux.sh para configurar o ambiente."
    exit 1
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "✓ Ambiente virtual ativado"
echo

# Executa o menu principal
echo "Iniciando aplicação..."
echo
python menu_principal.py

# Verifica se houve erro
if [ $? -ne 0 ]; then
    echo
    echo "ERRO: Aplicação encerrada com erro"
    read -p "Pressione Enter para continuar..."
fi
