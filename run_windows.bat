@echo off
echo ========================================
echo    Automação v2.0 - Execução Rápida
echo ========================================
echo.

REM Verifica se o ambiente virtual existe
if not exist "venv" (
    echo ERRO: Ambiente virtual não encontrado!
    echo Execute primeiro o start_windows.bat para configurar o ambiente.
    pause
    exit /b 1
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✓ Ambiente virtual ativado
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
