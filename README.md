# 🎮 Automação v2.0

Sistema de automação simplificado com interface gráfica para scripts de automação de jogos.

## 📋 Funcionalidades

- **🥚 Rachar Ovos**: Automação completa para quebrar ovos com:
  - Configuração simples de ponto de clique
  - Execução de 100 ciclos com movimentos aleatórios
  - Sistema inteligente de pausa/retomar com retomada exata
  - Contadores em tempo real (execução e tempo restante)
  - Janela de controle flutuante centralizada
  - Detecção automática de monitor principal
- **🎣 Pesca Automática**: Sistema completo de pesca com:
  - Detecção de imagem e reações automáticas
  - Sistema de carinho automático (a cada 100 segundos)
  - Sistema de ataques de Pokémon com persistência
  - Gerenciamento completo de Pokémon (cadastrar, editar, excluir, selecionar)
  - Janela de controle flutuante
- **🖥️ Interface Inteligente**: Centralização automática em qualquer configuração de monitor
- **⚙️ Configuração Simples**: Setup manual fácil para Windows e Linux
- **💾 Persistência de Dados**: Pokémon cadastrados são salvos automaticamente

## 🚀 Como Usar

### Instalação e Configuração

#### Windows
1. **Instale Python 3.7+** de [python.org](https://python.org)
2. **Abra o Prompt de Comando** como administrador
3. **Navegue até a pasta do projeto**:
   ```cmd
   cd C:\caminho\para\autoclickerV2
   ```
4. **Crie o ambiente virtual**:
   ```cmd
   python -m venv venv
   ```
5. **Ative o ambiente virtual**:
   ```cmd
   venv\Scripts\activate
   ```
6. **Instale as dependências**:
   ```cmd
   pip install -r requirements.txt
   ```
7. **Execute o script**:
   ```cmd
   python rachar_egg.py
   ```

#### Linux (Ubuntu/Debian)
1. **Instale Python 3 e dependências**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-tk python3-dev
   ```
2. **Navegue até a pasta do projeto**:
   ```bash
   cd /caminho/para/autoclickerV2
   ```
3. **Crie o ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```
4. **Ative o ambiente virtual**:
   ```bash
   source venv/bin/activate
   ```
5. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Execute o script**:
   ```bash
   python3 rachar_egg.py
   ```

### Execuções Subsequentes

#### Windows
```cmd
cd C:\caminho\para\autoclickerV2
venv\Scripts\activate
python rachar_egg.py
```

#### Linux
```bash
cd /caminho/para/autoclickerV2
source venv/bin/activate
python3 rachar_egg.py
```

## 📦 Dependências

- **pyautogui**: Automação de mouse e teclado
- **Pillow**: Processamento de imagens
- **tkinter**: Interface gráfica (incluído com Python)

## 🎯 Como Funciona

### Rachar Ovos - Funcionalidades Principais

#### 🎮 **Interface Simplificada**
- **Sem Menu Centralizado**: Executa diretamente o script de rachar ovos
- **Configuração Única**: Apenas uma janela de configuração de ponto de clique
- **Janela de Controle Flutuante**: Sempre visível durante a execução

#### ⚙️ **Sistema de Controle Inteligente**
- **Botão Único**: Alterna entre "Iniciar", "Pausar" e "Retomar"
- **Estados do Botão**:
  - **▶️ Iniciar** (verde): Inicia a automação do zero
  - **⏸️ Pausar** (laranja): Pausa durante contagem de segundos (desabilitado durante movimento)
  - **▶️ Retomar** (verde): Retoma exatamente do ponto onde foi pausado

#### 📊 **Contadores em Tempo Real**
- **Contador de Execução**: Mostra "Execução: X/100" em tempo real
- **Contador de Tempo**: Mostra "Tempo restante: Xs" durante a contagem
- **Status Inteligente**: 
  - Durante execução: mostra progresso atual
  - Durante pausa: mostra execução e tempo exatos onde parou
  - Antes de iniciar: mostra "0/100" e "---"

#### 🖥️ **Centralização Automática**
- **Detecção Inteligente**: Detecta automaticamente o monitor principal
- **Pop-ups**: Centralizados no monitor principal
- **Janela Suspensa**: Posicionada no quadrante inferior esquerdo do monitor principal
- **Compatibilidade Universal**: Funciona em qualquer configuração de monitor

#### 🔄 **Sistema de Pausa/Retomar Avançado**
- **Pausa Precisa**: Pausa exatamente no segundo atual da contagem
- **Retomada Exata**: Continua exatamente de onde parou
- **Estado Persistente**: Mantém informações de execução e tempo durante pausa
- **Múltiplas Pausas**: Permite pausar e retomar quantas vezes necessário

### Pesca Automática
- **Configuração Completa**:
  - Tecla de atalho de pesca (F1-F12)
  - Região de busca da exclamação
  - Ponto de clique para lançar a isca
  - Sistema de carinho opcional (a cada 100 segundos)
- **Sistema de Pokémon**:
  - Cadastro de até 4 ataques por Pokémon (F1-F12)
  - Cooldown personalizado para cada Pokémon
  - Persistência automática dos dados
  - Gerenciamento completo (editar, excluir, selecionar)
- **Automação Inteligente**:
  - Detecção de imagem da exclamação
  - Reações automáticas com movimentos aleatórios
  - Reinício automático após timeout
  - Execução de ataques de Pokémon no cooldown
- **Janela de Controle Flutuante**:
  - Status da automação em tempo real
  - Contador de carinho
  - Contador de ataques de Pokémon
  - Botões para iniciar e parar

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

### Erro "ModuleNotFoundError"
Se você receber erros de módulos não encontrados:
1. Certifique-se de que o ambiente virtual está ativado
2. Execute: `pip install -r requirements.txt`
3. Se ainda houver problemas, use: `pip install --upgrade pip`

### Segmentation Fault (Linux)
Se você encontrar erros de segmentation fault:
1. Certifique-se de que todas as dependências estão instaladas
2. Use Python 3.x em vez de Python 2.x
3. Execute: `python3 rachar_egg.py` em vez de `python rachar_egg.py`

### Problemas de Centralização
- O sistema detecta automaticamente o monitor principal
- Funciona em configurações de monitor único ou múltiplos
- Se houver problemas, verifique se o cursor está no monitor desejado

## 📁 Estrutura do Projeto

```
autoclickerV2/
├── rachar_egg.py          # Script principal de rachar ovos
├── pesca.py               # Script de pesca automática
├── menu_principal.py      # Menu principal (opcional)
├── requirements.txt        # Dependências do projeto
├── pokemon_data.json      # Dados dos Pokémon (gerado automaticamente)
├── exclamacao-pesca-sem-fundo.png  # Imagem para detecção
└── README.md              # Este arquivo
```

## 🎮 Uso do Script Rachar Ovos

### Passo a Passo Completo

1. **Execute o script**:
   - Windows: `python rachar_egg.py`
   - Linux: `python3 rachar_egg.py`

2. **Configure o ponto de clique**:
   - Clique em "OK" na janela "Configurar Clique"
   - Posicione o mouse no local desejado
   - Aguarde 5 segundos para captura automática
   - Confirme as coordenadas na janela "Ponto Salvo"

3. **Use a janela de controle**:
   - **Iniciar**: Clique em "▶️ Iniciar" para começar
   - **Pausar**: Durante contagem de segundos, clique em "⏸️ Pausar"
   - **Retomar**: Clique em "▶️ Retomar" para continuar exatamente de onde parou
   - **Acompanhar**: Veja execução atual e tempo restante em tempo real

4. **Funcionamento**:
   - Executa 100 ciclos de automação
   - Cada ciclo: clique + movimentos aleatórios + espera (183-203s)
   - Botão fica desabilitado durante movimentos do personagem
   - Pode pausar/retomar quantas vezes necessário

### Pesca Automática
1. Execute o menu principal: `python menu_principal.py`
2. Clique em "🎣 Pesca Automática"
3. Configure a tecla de atalho (F1-F12)
4. Configure o ponto de carinho (opcional)
5. Configure a região de detecção da exclamação
6. Configure o ponto de clique de pesca
7. Use os controles para iniciar/parar a pesca

## 📝 Notas Importantes

- **Segurança**: Os scripts são seguros e não modificam arquivos do sistema
- **Performance**: Para melhor performance, feche outros programas desnecessários
- **Compatibilidade**: Testado em Windows 10/11 e Ubuntu 20.04+
- **Portabilidade**: Funciona em qualquer configuração de monitor automaticamente

## 🤝 Suporte

Para problemas ou sugestões, verifique:
1. Se todas as dependências estão instaladas
2. Se o Python está na versão correta (3.7+)
3. Se as permissões de automação estão habilitadas
4. Se a resolução da tela é compatível
5. Se o ambiente virtual está ativado

---

**Desenvolvido para automação de jogos com interface amigável e configuração simplificada.**
