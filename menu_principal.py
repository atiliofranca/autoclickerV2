import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import sys
import os
import pyautogui
import time
import random
import threading
from screeninfo import get_monitors

class MenuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
        # Variáveis para controle dos scripts
        self.current_script = None
        self.script_window = None
        
        # Variáveis para rachar ovos
        self.hatching_is_active = False
        self.current_execution = 0
        self.total_executions = 100
        self.remaining_time = 0
        self.after_id_hatching = None
        self.after_id_countdown = None
        
        # Variáveis para pesca
        self.fishing_is_active = False
        self.last_direction = None
        self.after_id_fishing = None
        self.after_id_pet = None
        self.pet_is_active = False
        self.pet_coordinates = None
        self.last_pet_time = 0
        self.is_first_start = True
        
    def get_primary_monitor_dimensions(self):
        """Retorna as dimensões e a posição do monitor principal usando screeninfo."""
        try:
            for monitor in get_monitors():
                if monitor.is_primary:
                    return monitor.width, monitor.height, monitor.x, monitor.y
            monitor = get_monitors()[0]
            return monitor.width, monitor.height, monitor.x, monitor.y
        except Exception as e:
            print(f"Erro ao obter dimensões do monitor: {e}")
            # Fallback para dimensões padrão
            return 1920, 1080, 0, 0
    
    def center_window(self, width=None, height=None):
        """Centraliza a janela no monitor principal."""
        if width is None or height is None:
            # Se não especificados, usa o tamanho atual da janela
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Se a janela ainda não foi renderizada, usa tamanhos padrão
            if width <= 1 or height <= 1:
                width = 400
                height = 300
        
        mon_width, mon_height, mon_x, mon_y = self.get_primary_monitor_dimensions()
        x = mon_x + (mon_width // 2) - (width // 2)
        y = mon_y + (mon_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_window(self):
        """Configura a janela principal."""
        self.root.title("Menu Principal - Automação")
        self.root.resizable(False, False)
        
        # Centraliza a janela
        window_width = 400
        window_height = 300
        self.center_window(window_width, window_height)
        
        # Configura o ícone da janela (opcional)
        try:
            self.root.iconbitmap(default="")
        except:
            pass
    
    def create_widgets(self):
        """Cria os widgets da interface."""
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Menu Principal", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Escolha uma das opções de automação:",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para os botões
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(expand=True)
        
        # Botão para Rachar Ovos
        btn_rachar_ovos = tk.Button(
            buttons_frame,
            text="🥚 Rachar Ovos",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=2,
            command=self.abrir_rachar_ovos,
            cursor="hand2"
        )
        btn_rachar_ovos.pack(pady=10)
        
        # Botão para Pesca
        btn_pesca = tk.Button(
            buttons_frame,
            text="🎣 Pesca Automática",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=2,
            command=self.abrir_pesca,
            cursor="hand2"
        )
        btn_pesca.pack(pady=10)
        
        # Botão Sair
        btn_sair = tk.Button(
            buttons_frame,
            text="❌ Sair",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            width=15,
            height=1,
            relief="raised",
            bd=2,
            command=self.sair_aplicacao,
            cursor="hand2"
        )
        btn_sair.pack(pady=(20, 0))
        
        # Informações do projeto
        info_label = tk.Label(
            main_frame,
            text="Projeto de Automação v2.0",
            font=("Arial", 8),
            fg="#bdc3c7"
        )
        info_label.pack(side="bottom", pady=(10, 0))
    
    def abrir_rachar_ovos(self):
        """Abre o script de rachar ovos integrado."""
        if self.current_script:
            messagebox.showwarning("Aviso", "Já existe um script em execução. Pare o script atual antes de iniciar outro.")
            return
            
        self.current_script = "rachar_ovos"
        self.create_rachar_ovos_interface()
    
    def abrir_pesca(self):
        """Abre o script de pesca automática integrado."""
        if self.current_script:
            messagebox.showwarning("Aviso", "Já existe um script em execução. Pare o script atual antes de iniciar outro.")
            return
            
        self.current_script = "pesca"
        self.create_pesca_interface()
    
    def sair_aplicacao(self):
        """Fecha a aplicação."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do Menu Principal?"):
            self.root.destroy()
    
    # === FUNÇÕES INTEGRADAS PARA RACHAR OVOS ===
    
    def start_capture_timer_with_popup(self):
        """Inicia o timer com um pop-up para capturar as coordenadas."""
        popup = tk.Toplevel(self.root)
        popup.title("Configurar Clique")
        popup.resizable(False, False)
        
        # Centraliza o popup
        popup_width = 300
        popup_height = 150
        self.center_window_on_popup(popup, popup_width, popup_height)
        
        if messagebox.askokcancel("Configurar Clique", "Clique em OK para começar a configurar o ponto de clique.", parent=popup):
            messagebox.showinfo("Captura de Ponto", "Coloque o mouse no local de clique.\nCapturando em 5 segundos...", parent=popup)
            
            print("Capturando ponto de clique em 5 segundos...")
            time.sleep(5)
            
            mouse_x, mouse_y = pyautogui.position()
            print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
            
            if messagebox.askokcancel("Ponto Salvo!", f"Ponto de clique salvo: ({mouse_x}, {mouse_y})\n\nClique em OK para iniciar a automação.", parent=popup):
                popup.destroy()
                return mouse_x, mouse_y
        
        popup.destroy()
        return None, None
    
    def center_window_on_popup(self, popup, width, height):
        """Centraliza um popup no monitor principal."""
        mon_width, mon_height, mon_x, mon_y = self.get_primary_monitor_dimensions()
        x = mon_x + (mon_width // 2) - (width // 2)
        y = mon_y + (mon_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
    
    def direcoes_aleatorias(self, num_direcoes=None):
        """Muda o personagem de direção de forma aleatória."""
        if num_direcoes is None:
            num_direcoes = random.randint(4, 10)
            
        direcoes_disponiveis = ['up', 'down', 'left', 'right']
        direcoes_a_acionar = []
        print(f"Preparando para acionar {num_direcoes} direções aleatórias...")

        for _ in range(num_direcoes):
            direcao_escolhida = random.choice(direcoes_disponiveis)
            direcoes_a_acionar.append(direcao_escolhida)
        print(f"Direções escolhidas para acionar: {direcoes_a_acionar}")

        for i, direcao in enumerate(direcoes_a_acionar):
            pyautogui.press(direcao)
            tempo_aleatorio = random.uniform(0.3, 0.8)
            time.sleep(tempo_aleatorio)
    
    def run_egg_hatching_integrated(self, click_x, click_y):
        """Executa o loop principal de rachar ovos integrado."""
        # Define como ativo desde o início
        self.hatching_is_active = True
        
        self.status_label.config(text="Iniciando automação...")
        print("Iniciando a automação em 5 segundos...")
        
        for i in range(5, 0, -1):
            if not self.hatching_is_active:
                return
            self.status_label.config(text=f"Iniciando em {i} segundos...")
            print(f"{i}...")
            time.sleep(1)
        
        self.status_label.config(text="Executando automação...")
        print("Iniciando agora!")
        
        for i in range(100):
            if not self.hatching_is_active:
                break
                
            self.current_execution = i + 1
            self.progress_label.config(text=f"Execução: {i + 1}/100")
            print(f"Execução número: {i + 1}")
            pyautogui.click(x=click_x, y=click_y)
            time.sleep(1)
            self.direcoes_aleatorias()
            numero_aleatorio = random.randint(183, 203)
            print(f'O tempo de espera será de {numero_aleatorio} segundos')
            
            for j in range(numero_aleatorio):
                if not self.hatching_is_active:
                    break
                self.remaining_time = numero_aleatorio - j
                self.progress_label.config(text=f"Execução: {i + 1}/100 - Aguardando: {self.remaining_time}s")
                print(f'faltam {self.remaining_time} segundos')
                time.sleep(1)

        if self.hatching_is_active:
            print("Todas as 100 repetições foram concluídas!")
            self.status_label.config(text="Automação concluída!")
            self.progress_label.config(text="100/100 - Concluído!")
            messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
            # Reset automático após conclusão
            self.stop_hatching()
        
        self.hatching_is_active = False
    
    def create_rachar_ovos_interface(self):
        """Cria a interface para o script de rachar ovos."""
        # Limpa a janela principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configura a janela para ser flutuante
        self.root.attributes('-topmost', True)
        
        # Posiciona a janela no canto inferior esquerdo
        self.position_window_bottom_left()
        
        # Cria nova interface
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="🥚 Rachar Ovos", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Aguardando configuração...",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Progresso
        self.progress_label = tk.Label(
            main_frame,
            text="Progresso: ---",
            font=("Arial", 10),
            fg="#34495e"
        )
        self.progress_label.pack(pady=(0, 20))
        
        # Botões principais
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        # Botão Configurar/Parar
        self.btn_configurar_parar = tk.Button(
            buttons_frame,
            text="⚙️ Configurar",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            height=2,
            command=self.toggle_configurar_parar,
            cursor="hand2"
        )
        self.btn_configurar_parar.pack(side=tk.LEFT, padx=10)
        
        # Botão Pausar/Play
        self.btn_pausar_play = tk.Button(
            buttons_frame,
            text="⏸️ Pausar",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=15,
            height=2,
            command=self.toggle_pausar_play,
            cursor="hand2",
            state="disabled"
        )
        self.btn_pausar_play.pack(side=tk.LEFT, padx=10)
        
        # Botão Sair
        btn_sair = tk.Button(
            buttons_frame,
            text="🚪 Sair",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            height=2,
            command=self.voltar_ao_menu,
            cursor="hand2"
        )
        btn_sair.pack(side=tk.RIGHT, padx=10)
        
        # Botão Retornar (abaixo dos outros botões)
        self.btn_retornar = tk.Button(
            main_frame,
            text="🔙 Retornar",
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            width=20,
            height=2,
            command=self.retornar_ao_menu,
            cursor="hand2",
            state="disabled"  # Inicia desabilitado
        )
        self.btn_retornar.pack(pady=(20, 0))
        
        # Variáveis de controle
        self.is_configured = False
        self.is_paused = False
        self.click_coordinates = None
        self.hatching_thread = None
        
        # Variáveis de estado para retomada precisa
        self.paused_execution = 0
        self.paused_wait_time = 0
        self.paused_remaining_time = 0
        self.paused_total_wait = 0
        
        # Atualiza o estado inicial do botão Retornar
        self.update_retornar_button_state()
    
    def retornar_ao_menu(self):
        """Retorna ao menu principal centralizando a janela."""
        self.current_script = None
        self.hatching_is_active = False
        # Remove o atributo flutuante
        self.root.attributes('-topmost', False)
        # Limpa a janela e recria o menu
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        # Centraliza a janela novamente
        self.center_window()
    
    def position_window_bottom_left(self):
        """Posiciona a janela no centro do quadrante inferior esquerdo da tela principal."""
        # Obtém as dimensões do monitor principal
        mon_width, mon_height, mon_x, mon_y = self.get_primary_monitor_dimensions()
        
        # Obtém o tamanho atual da janela
        self.root.update_idletasks()  # Força a atualização do layout
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Se a janela ainda não foi renderizada, usa tamanhos padrão
        if window_width <= 1 or window_height <= 1:
            window_width = 400
            window_height = 300
        
        # Calcula o centro do quadrante inferior esquerdo
        # Quadrante inferior esquerdo: metade da largura, metade da altura (parte inferior)
        quadrant_center_x = mon_x + (mon_width // 4)  # Centro do quadrante esquerdo
        quadrant_center_y = mon_y + (mon_height * 3 // 4)  # Centro do quadrante inferior
        
        # Posiciona a janela centralizada no quadrante
        x = quadrant_center_x - (window_width // 2)
        y = quadrant_center_y - (window_height // 2)
        
        # Define a geometria da janela
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def update_retornar_button_state(self):
        """Atualiza o estado do botão Retornar baseado nas regras definidas."""
        # O botão só fica ativo se:
        # 1. Não estiver configurando um ponto de clique
        # 2. Não estiver rodando a automação
        # 3. Não estiver em pausa
        # 4. Não estiver reiniciando
        # Basicamente, só fica ativo quando o botão "Configurar" estiver disponível
        
        # Verifica se o botão "Configurar" está disponível (texto "⚙️ Configurar")
        configurar_text = self.btn_configurar_parar.cget("text")
        is_configurar_available = "Configurar" in configurar_text
        
        if is_configurar_available:
            self.btn_retornar.config(state="normal", bg="#9b59b6")
        else:
            self.btn_retornar.config(state="disabled", bg="#95a5a6")
    
    def toggle_configurar_parar(self):
        """Alterna entre configurar e parar."""
        if not self.is_configured:
            # Configurar
            click_x, click_y = self.start_capture_timer_with_popup()
            
            if click_x is not None:
                self.click_coordinates = (click_x, click_y)
                self.is_configured = True
                self.btn_configurar_parar.config(
                    text="⏹️ Parar",
                    bg="#e74c3c"
                )
                self.btn_pausar_play.config(
                    state="normal",
                    text="▶️ Iniciar",
                    bg="#27ae60"
                )
                self.status_label.config(text="Configurado! Clique em Iniciar para começar.")
                self.progress_label.config(text="Progresso: 0/100")
                # Atualiza o estado do botão Retornar
                self.update_retornar_button_state()
            else:
                self.status_label.config(text="Configuração cancelada.")
        else:
            # Parar
            self.stop_hatching()
    
    def toggle_pausar_play(self):
        """Alterna entre iniciar, pausar e play."""
        current_text = self.btn_pausar_play.cget("text")
        
        if "Iniciar" in current_text:
            # Primeira vez - iniciar automação
            self.start_rachar_ovos()
            self.btn_pausar_play.config(
                text="⏸️ Pausar",
                bg="#f39c12"
            )
            self.is_paused = False
            # Atualiza o estado do botão Retornar
            self.update_retornar_button_state()
        elif "Pausar" in current_text:
            # Pausar
            self.pause_hatching()
            self.btn_pausar_play.config(
                text="▶️ Play",
                bg="#27ae60"
            )
            self.is_paused = True
            # Atualiza o estado do botão Retornar
            self.update_retornar_button_state()
        elif "Play" in current_text:
            # Play - retomar
            self.resume_hatching()
            self.btn_pausar_play.config(
                text="⏸️ Pausar",
                bg="#f39c12"
            )
            self.is_paused = False
            # Atualiza o estado do botão Retornar
            self.update_retornar_button_state()
    
    def start_rachar_ovos(self):
        """Inicia o processo de rachar ovos."""
        if self.click_coordinates:
            click_x, click_y = self.click_coordinates
            # Executa em uma thread separada para não travar a interface
            self.hatching_thread = threading.Thread(
                target=self.run_egg_hatching_integrated, 
                args=(click_x, click_y)
            )
            self.hatching_thread.daemon = True
            self.hatching_thread.start()
        else:
            print("Erro: Coordenadas não encontradas!")
    
    def pause_hatching(self):
        """Pausa a automação de rachar ovos."""
        self.hatching_is_active = False
        # Salva o estado exato onde foi pausada
        self.paused_execution = self.current_execution
        self.paused_remaining_time = self.remaining_time
        print("Automação pausada pelo usuário.")
        print(f"Estado salvo: Execução {self.paused_execution}, Tempo restante: {self.paused_remaining_time}s")
    
    def resume_hatching(self):
        """Retoma a automação de rachar ovos."""
        self.hatching_is_active = True
        print("Automação retomada pelo usuário.")
        
        # Retoma a execução do ponto exato onde foi pausada
        if self.paused_execution > 0:
            self.continue_hatching_from_exact_pause()
    
    def continue_hatching_from_exact_pause(self):
        """Continua a automação exatamente do ponto onde foi pausada."""
        if not self.click_coordinates:
            return
            
        click_x, click_y = self.click_coordinates
        
        # Executa em uma thread separada para não travar a interface
        self.hatching_thread = threading.Thread(
            target=self.run_hatching_from_exact_state, 
            args=(click_x, click_y, self.paused_execution, self.paused_remaining_time)
        )
        self.hatching_thread.daemon = True
        self.hatching_thread.start()
    
    def run_hatching_from_exact_state(self, click_x, click_y, paused_execution, paused_remaining_time):
        """Executa a automação exatamente do estado onde foi pausada."""
        self.status_label.config(text="Retomando automação...")
        print(f"Retomando exatamente da execução {paused_execution} com {paused_remaining_time}s restantes")
        
        # Se foi pausada durante o tempo de espera, continua o tempo de espera
        if paused_remaining_time > 0:
            self.current_execution = paused_execution
            self.progress_label.config(text=f"Execução: {paused_execution}/100 - Aguardando: {paused_remaining_time}s")
            print(f"Continuando tempo de espera: {paused_remaining_time}s restantes")
            
            # Continua o tempo de espera restante
            for j in range(paused_remaining_time):
                if not self.hatching_is_active:
                    break
                self.remaining_time = paused_remaining_time - j
                self.progress_label.config(text=f"Execução: {paused_execution}/100 - Aguardando: {self.remaining_time}s")
                print(f'faltam {self.remaining_time} segundos')
                time.sleep(1)
        
        # Continua com as próximas execuções
        for i in range(paused_execution, 100):
            if not self.hatching_is_active:
                break
                
            self.current_execution = i + 1
            self.progress_label.config(text=f"Execução: {i + 1}/100")
            print(f"Execução número: {i + 1}")
            pyautogui.click(x=click_x, y=click_y)
            time.sleep(1)
            self.direcoes_aleatorias()
            numero_aleatorio = random.randint(183, 203)
            print(f'O tempo de espera será de {numero_aleatorio} segundos')
            
            for j in range(numero_aleatorio):
                if not self.hatching_is_active:
                    break
                self.remaining_time = numero_aleatorio - j
                self.progress_label.config(text=f"Execução: {i + 1}/100 - Aguardando: {self.remaining_time}s")
                print(f'faltam {self.remaining_time} segundos')
                time.sleep(1)

        if self.hatching_is_active:
            print("Todas as 100 repetições foram concluídas!")
            self.status_label.config(text="Automação concluída!")
            self.progress_label.config(text="100/100 - Concluído!")
            messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
            # Reset automático após conclusão
            self.stop_hatching()
        
        self.hatching_is_active = False
    
    def continue_hatching_from_pause(self):
        """Continua a automação do ponto onde foi pausada."""
        if not self.click_coordinates:
            return
            
        click_x, click_y = self.click_coordinates
        
        # Executa em uma thread separada para não travar a interface
        self.hatching_thread = threading.Thread(
            target=self.run_hatching_from_execution, 
            args=(click_x, click_y, self.current_execution)
        )
        self.hatching_thread.daemon = True
        self.hatching_thread.start()
    
    def run_hatching_from_execution(self, click_x, click_y, start_execution):
        """Executa a automação a partir de uma execução específica."""
        self.status_label.config(text="Retomando automação...")
        print(f"Retomando a partir da execução {start_execution}")
        
        for i in range(start_execution, 100):
            if not self.hatching_is_active:
                break
                
            self.current_execution = i + 1
            self.progress_label.config(text=f"Execução: {i + 1}/100")
            print(f"Execução número: {i + 1}")
            pyautogui.click(x=click_x, y=click_y)
            time.sleep(1)
            self.direcoes_aleatorias()
            numero_aleatorio = random.randint(183, 203)
            print(f'O tempo de espera será de {numero_aleatorio} segundos')
            
            for j in range(numero_aleatorio):
                if not self.hatching_is_active:
                    break
                self.remaining_time = numero_aleatorio - j
                self.progress_label.config(text=f"Execução: {i + 1}/100 - Aguardando: {self.remaining_time}s")
                print(f'faltam {self.remaining_time} segundos')
                time.sleep(1)

        if self.hatching_is_active:
            print("Todas as 100 repetições foram concluídas!")
            self.status_label.config(text="Automação concluída!")
            self.progress_label.config(text="100/100 - Concluído!")
            messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
            # Reset automático após conclusão
            self.stop_hatching()
        
        self.hatching_is_active = False
    
    def stop_hatching(self):
        """Para completamente a automação e reseta."""
        self.hatching_is_active = False
        self.is_configured = False
        self.is_paused = False
        self.current_execution = 0
        self.remaining_time = 0
        
        # Reset das variáveis de estado para retomada precisa
        self.paused_execution = 0
        self.paused_wait_time = 0
        self.paused_remaining_time = 0
        self.paused_total_wait = 0
        
        # Reset dos botões
        self.btn_configurar_parar.config(
            text="⚙️ Configurar",
            bg="#3498db"
        )
        self.btn_pausar_play.config(
            text="⏸️ Pausar",
            bg="#f39c12",
            state="disabled"
        )
        
        # Reset dos labels
        self.status_label.config(text="Aguardando configuração...")
        self.progress_label.config(text="Progresso: ---")
        
        # Atualiza o estado do botão Retornar
        self.update_retornar_button_state()
        
        print("Automação interrompida e resetada pelo usuário.")
    
    def voltar_ao_menu(self):
        """Volta ao menu principal."""
        self.current_script = None
        self.hatching_is_active = False
        # Remove o atributo flutuante
        self.root.attributes('-topmost', False)
        # Limpa a janela e recria o menu
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        # Centraliza a janela novamente
        self.center_window()
    
    # === FUNÇÕES INTEGRADAS PARA PESCA ===
    
    def get_screen_dimensions(self):
        """Retorna as dimensões do monitor principal."""
        return pyautogui.size()
    
    def get_fishing_key(self):
        """Pede ao usuário para escolher a tecla de atalho de pesca."""
        keys = [f'F{i}' for i in range(1, 13)]
        message = "Escolha a tecla de atalho para pesca (F1 a F12)."
        
        user_key = simpledialog.askstring("Tecla de Atalho", message, parent=self.root)
        
        if user_key and user_key.upper() in keys:
            print(f"Tecla de atalho salva: {user_key.upper()}")
            return user_key.lower()
        else:
            messagebox.showerror("Erro", "Tecla de atalho inválida. Saindo do script.", parent=self.root)
            return None
    
    def get_pet_coordinates(self):
        """Guia o usuário para definir as coordenadas do clique para dar carinho."""
        if messagebox.askyesno("Funcionalidade Opcional", "Deseja ativar a funcionalidade de 'dar carinho ao Pokémon' a cada 100 segundos?", parent=self.root):
            self.pet_is_active = True
            
            if messagebox.askokcancel("Configurar Carinho", "Clique em OK e, em seguida, posicione o mouse no local exato onde o clique de carinho deve ocorrer.", parent=self.root):
                messagebox.showinfo("Captura de Ponto", "Capturando em 5 segundos...", parent=self.root)
                print("Capturando ponto de carinho em 5 segundos...")
                time.sleep(5)
                
                self.pet_coordinates = pyautogui.position()
                print(f"Ponto de carinho salvo: ({self.pet_coordinates.x}, {self.pet_coordinates.y})")
                return self.pet_coordinates
        
        self.pet_is_active = False
        return None
    
    def get_exclamation_region(self):
        """Guia o usuário para definir o ponto central da região da exclamação."""
        if messagebox.askokcancel("Configurar Região", "Agora vamos configurar a área de busca da exclamação.\n\nColoque o mouse no CENTRO do ícone da exclamação e clique em OK para continuar.", parent=self.root):
            messagebox.showinfo("Captura de Região", "Capturando em 5 segundos...", parent=self.root)
            print("Capturando ponto central da região em 5 segundos...")
            time.sleep(5)
            
            center_x, center_y = pyautogui.position()
            width = 100
            height = 60
            
            left = center_x - width // 2
            top = center_y - height // 2
            region = (left, top, width, height)
            
            print(f"Região de busca salva: {region}")
            return region
        
        return None
    
    def get_fishing_click_coordinates(self):
        """Pede ao usuário para posicionar o mouse e captura as coordenadas de clique de pesca."""
        if messagebox.askokcancel("Configurar Clique", "Agora vamos configurar o ponto de clique de pesca.\n\nClique em OK para continuar.", parent=self.root):
            messagebox.showinfo("Captura de Ponto", "Colocando o mouse no local de clique de pesca.\nCapturando em 5 segundos...", parent=self.root)
            print("Capturando ponto de clique em 5 segundos...")
            time.sleep(5)
            
            mouse_x, mouse_y = pyautogui.position()
            print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
            return mouse_x, mouse_y
        
        return None, None
    
    def start_fishing_action(self, fishing_key, mouse_x, mouse_y):
        """Prepara o personagem e inicia a pesca."""
        print("Iniciando a pesca...")
        
        pyautogui.hotkey('ctrl', 'down')
        time.sleep(3)
        self.last_direction = 'down'

        pyautogui.click(x=mouse_x, y=mouse_y)
        time.sleep(1)
        pyautogui.press(fishing_key)
        time.sleep(1) 
        pyautogui.click(x=mouse_x, y=mouse_y)
        print(f"'{fishing_key.upper()}' apertado e clique realizado em ({mouse_x}, {mouse_y}).")
    
    def create_pesca_interface(self):
        """Cria a interface para o script de pesca."""
        # Limpa a janela principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cria nova interface
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="🎣 Pesca Automática", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Status
        status_label = tk.Label(
            main_frame,
            text="Aguardando configuração...",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        status_label.pack(pady=(0, 10))
        
        # Informações
        info_label = tk.Label(
            main_frame,
            text="Configure as opções abaixo para iniciar a pesca automática",
            font=("Arial", 10),
            fg="#34495e"
        )
        info_label.pack(pady=(0, 20))
        
        # Botões
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        btn_configurar = tk.Button(
            buttons_frame,
            text="⚙️ Configurar Pesca",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.start_pesca_config(status_label),
            cursor="hand2"
        )
        btn_configurar.pack(side=tk.LEFT, padx=10)
        
        btn_voltar = tk.Button(
            buttons_frame,
            text="🔙 Voltar ao Menu",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            width=15,
            height=2,
            command=self.voltar_ao_menu,
            cursor="hand2"
        )
        btn_voltar.pack(side=tk.RIGHT, padx=10)
    
    def start_pesca_config(self, status_label):
        """Inicia a configuração da pesca."""
        status_label.config(text="Configurando pesca...")
        
        # Configurações
        fishing_key = self.get_fishing_key()
        if not fishing_key:
            status_label.config(text="Configuração cancelada.")
            return
            
        pet_coordinates = self.get_pet_coordinates()
        
        search_region = self.get_exclamation_region()
        if not search_region:
            status_label.config(text="Configuração cancelada.")
            return
            
        mouse_x, mouse_y = self.get_fishing_click_coordinates()
        if mouse_x is None:
            status_label.config(text="Configuração cancelada.")
            return
        
        status_label.config(text="Pesca configurada! Use os controles para iniciar.")
        messagebox.showinfo("Configuração Concluída", "Pesca automática configurada com sucesso!")
    
    def run(self):
        """Inicia o loop principal da aplicação."""
        self.root.mainloop()

def main():
    """Função principal."""
    try:
        app = MenuPrincipal()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar a aplicação:\n{str(e)}")

if __name__ == "__main__":
    main()
