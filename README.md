# 🎮 Automação v2.0

Sistema de automação integrado com interface gráfica centralizada para scripts de automação de jogos.

## 📋 Funcionalidades

- **🥚 Rachar Ovos**: Automação para quebrar ovos com movimentos aleatórios
- **🎣 Pesca Automática**: Sistema de pesca com detecção de imagem e reações automáticas
- **🖥️ Interface Unificada**: Menu principal centralizado com navegação intuitiva
- **⚙️ Configuração Automática**: Setup automático de ambiente virtual e dependências

## 🚀 Como Usar

### Primeira Execução (Setup Completo)

#### Windows
1. Execute o arquivo `start_windows.bat`
2. O script irá automaticamente:
   - Criar um ambiente virtual Python
   - Instalar todas as dependências necessárias
   - Iniciar o menu principal
   - **Manter o ambiente virtual ativo** após a execução

#### Linux/macOS
1. Torne o script executável: `chmod +x start_linux.sh`
2. Execute: `./start_linux.sh`
3. O script irá automaticamente:
   - Criar um ambiente virtual Python
   - Instalar todas as dependências necessárias
   - Iniciar o menu principal
   - **Manter o ambiente virtual ativo** após a execução

### Execuções Subsequentes (Rápida)

#### Windows
- Execute `run_windows.bat` para execução rápida (ambiente já configurado)

#### Linux/macOS
- Execute `./run_linux.sh` para execução rápida (ambiente já configurado)

### Execução Manual
Se preferir executar manualmente:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python menu_principal.py
```

## 📦 Dependências

- **pyautogui**: Automação de mouse e teclado
- **screeninfo**: Detecção de monitores e resolução
- **Pillow**: Processamento de imagens
- **tkinter**: Interface gráfica (incluído com Python)

## 🎯 Como Funciona

### Menu Principal
- Interface centralizada com opções para cada script
- Centralização automática da janela na tela
- Navegação intuitiva entre diferentes funcionalidades

### Rachar Ovos
- Configuração de ponto de clique através de popup
- Execução de 100 ciclos de automação
- Movimentos aleatórios do personagem
- Tempos de espera variáveis entre 183-203 segundos
- **Janela de controle flutuante** com:
  - Contador de execução em tempo real
  - Tempo restante para próxima execução
  - Botões para pausar, retomar e parar

### Pesca Automática
- Configuração de tecla de atalho (F1-F12)
- Detecção de imagem da exclamação
- Reações automáticas com movimentos aleatórios
- Sistema de carinho opcional para Pokémon durante a pesca

## ⚠️ Requisitos do Sistema

- **Python 3.7+**
- **Windows 10+** ou **Linux/macOS**
- **Resolução mínima**: 1024x768
- **Permissões**: Acesso para automação de mouse/teclado

## 🔧 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de Compilação do Pillow (Windows)
Se você encontrar erros de compilação com o Pillow, o arquivo `requirements.txt` já foi otimizado para usar versões compatíveis:
- Usa `Pillow>=9.0.0` em vez de versões específicas problemáticas
- Usa `>=` em vez de `==` para permitir versões mais recentes e estáveis

### Erro de Permissões (Linux)
```bash
sudo apt install python3-tk python3-dev
```

### Erro de Centralização
- Verifique se o `screeninfo` está instalado corretamente
- Em sistemas multi-monitor, certifique-se de que o monitor principal está configurado

### Erro "ModuleNotFoundError"
Se você receber erros de módulos não encontrados:
1. Certifique-se de que o ambiente virtual está ativado
2. Execute: `pip install -r requirements.txt`
3. Se ainda houver problemas, use: `pip install --upgrade pip`

### Erro de Política de Execução do PowerShell (Windows)
Se você receber o seguinte erro ao executar os scripts `.bat`:

```
& : O arquivo C:caminho\do\arquivo não pode ser carregado porque a execução de scripts foi desabilitada neste sistema. Para obter mais informações, 
consulte about_Execution_Policies em https://go.microsoft.com/fwlink/?LinkID=135170.
No linha:1 caractere:3
+ & C:caminho\do\arquivo
+   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
+ CategoryInfo          : ErrodeSegurança: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
```

**Solução:**
1. Abra o PowerShell **sem ser administrador**
2. Execute o comando:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Confirme com `Y` quando solicitado
4. Agora você pode executar os scripts `.bat` normalmente

**Nota:** Este comando permite a execução de scripts assinados remotamente apenas para o usuário atual, mantendo a segurança do sistema.

## 📁 Estrutura do Projeto

```
autoclicker-2.0/
├── menu_principal.py      # Menu principal integrado
├── rachar_egg.py          # Script de rachar ovos com controle flutuante
├── pesca.py               # Script de pesca com controle flutuante
├── requirements.txt        # Dependências do projeto
├── start_windows.bat      # Setup completo Windows (mantém venv ativo)
├── start_linux.sh         # Setup completo Linux (mantém venv ativo)
├── run_windows.bat        # Execução rápida Windows
├── run_linux.sh           # Execução rápida Linux
├── exclamacao-pesca-sem-fundo.png  # Imagem para detecção
└── README.md              # Este arquivo
```

## 🎮 Uso dos Scripts

### Rachar Ovos
1. Execute o menu principal
2. Clique em "🥚 Rachar Ovos"
3. Configure o ponto de clique quando solicitado
4. Use a janela de controle flutuante para:
   - Acompanhar o progresso em tempo real
   - Pausar/retomar a automação quando necessário (o sistema de pausa funciona apenas quando os segundos entre uma execução e outra estão sendo contados)
   - Parar completamente se necessário
5. Aguarde a conclusão das 100 execuções

### Pesca Automática
1. Execute o menu principal
2. Clique em "🎣 Pesca Automática"
3. Configure a tecla de atalho (F1-F12)
4. Configure o ponto de carinho (opcional)
5. Configure a região de detecção da exclamação
6. Configure o ponto de clique de pesca
7. Use os controles para iniciar/parar a pesca

## 📝 Notas Importantes

- **Backup**: Sempre faça backup de suas configurações importantes
- **Segurança**: Os scripts são seguros e não modificam arquivos do sistema
- **Performance**: Para melhor performance, feche outros programas desnecessários
- **Compatibilidade**: Testado em Windows 10/11 e Ubuntu 20.04+

## 🤝 Suporte

Para problemas ou sugestões, verifique:
1. Se todas as dependências estão instaladas
2. Se o Python está na versão correta (3.7+)
3. Se as permissões de automação estão habilitadas
4. Se a resolução da tela é compatível

---

**Desenvolvido para automação de jogos com interface amigável e configuração simplificada.**
