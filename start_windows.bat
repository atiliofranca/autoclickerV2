@echo off
echo ========================================
echo    Automação v2.0 - Setup Automático
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não está instalado ou não está no PATH
    echo Por favor, instale o Python 3.7+ de https://python.org
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verifica se já existe um ambiente virtual
if exist "venv" (
    echo Ambiente virtual já existe. Ativando...
    call venv\Scripts\activate.bat
) else (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

echo ✓ Ambiente virtual ativado
echo.

REM Atualiza pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instala dependências
echo Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)

echo ✓ Dependências instaladas com sucesso
echo.

REM Executa o menu principal
echo Iniciando aplicação...
echo.
python menu_principal.py

REM Pausa para mostrar mensagens de erro se houver
if errorlevel 1 (
    echo.
    echo ERRO: Aplicação encerrada com erro
    pause
)

echo.
echo ========================================
echo Ambiente virtual configurado com sucesso!
echo Para próximas execuções, use: run_windows.bat
echo ========================================
echo.
echo Pressione qualquer tecla para manter o ambiente virtual ativo...
pause >nul

REM Mantém o ambiente virtual ativo
cmd /k "call venv\Scripts\activate.bat && echo Ambiente virtual ativo! Digite 'python menu_principal.py' para executar novamente."
