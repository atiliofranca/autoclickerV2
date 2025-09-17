#!/bin/bash

echo "========================================"
echo "   Automação v2.0 - Setup Automático"
echo "========================================"
echo

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não está instalado"
    echo "Por favor, instale o Python 3.7+ usando seu gerenciador de pacotes"
    echo "Exemplo: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "✓ Python encontrado"
echo

# Verifica se já existe um ambiente virtual
if [ -d "venv" ]; then
    echo "Ambiente virtual já existe. Ativando..."
    source venv/bin/activate
else
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao criar ambiente virtual"
        exit 1
    fi
    
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
fi

echo "✓ Ambiente virtual ativado"
echo

# Atualiza pip
echo "Atualizando pip..."
python -m pip install --upgrade pip

# Instala dependências
echo "Instalando dependências..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependências"
    exit 1
fi

echo "✓ Dependências instaladas com sucesso"
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

echo
echo "========================================"
echo "Ambiente virtual configurado com sucesso!"
echo "Para próximas execuções, use: ./run_linux.sh"
echo "========================================"
echo
echo "Pressione Enter para manter o ambiente virtual ativo..."
read

# Mantém o ambiente virtual ativo
echo "Ambiente virtual ativo! Digite 'python menu_principal.py' para executar novamente."
exec bash
