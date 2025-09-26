import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox
import threading
import os

# Variáveis globais para a aplicação
hatching_is_active = False
current_execution = 0
total_executions = 100
remaining_time = 0
is_moving_character = False
is_paused = False
paused_execution = 0
paused_remaining_time = 0

def get_primary_monitor_info():
    """Detecta informações do monitor principal de forma universal."""
    try:
        # Obtém o tamanho total da tela
        screen_width, screen_height = pyautogui.size()
        
        # Para sistemas com múltiplos monitores, tenta detectar o principal
        if screen_width > 2000:  # Provavelmente múltiplos monitores
            # Estratégia: assume que o monitor principal é onde o cursor está
            # ou usa a metade direita (comum em setups profissionais)
            try:
                # Obtém posição atual do cursor
                cursor_x, cursor_y = pyautogui.position()
                
                # Se o cursor está na metade direita, assume que é o monitor principal
                if cursor_x > screen_width // 2:
                    primary_width = screen_width // 2
                    primary_height = screen_height
                    primary_x = screen_width // 2
                    primary_y = 0
                else:
                    # Se está na metade esquerda, assume que é o monitor principal
                    primary_width = screen_width // 2
                    primary_height = screen_height
                    primary_x = 0
                    primary_y = 0
            except:
                # Fallback: assume metade direita como principal
                primary_width = screen_width // 2
                primary_height = screen_height
                primary_x = screen_width // 2
                primary_y = 0
        else:
            # Monitor único
            primary_width = screen_width
            primary_height = screen_height
            primary_x = 0
            primary_y = 0
            
        return primary_width, primary_height, primary_x, primary_y
    except Exception as e:
        # Fallback para resolução padrão
        return 1920, 1080, 0, 0

def center_window_on_primary(window, width, height):
    """Centraliza uma janela no monitor principal."""
    primary_width, primary_height, primary_x, primary_y = get_primary_monitor_info()
    
    # Calcula posição central
    x = primary_x + (primary_width // 2) - (width // 2)
    y = primary_y + (primary_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def position_window_bottom_left(window, width, height):
    """Posiciona uma janela no centro do quadrante inferior esquerdo do monitor principal."""
    primary_width, primary_height, primary_x, primary_y = get_primary_monitor_info()
    
    # Calcula o centro do quadrante inferior esquerdo
    quadrant_center_x = primary_x + (primary_width // 4)  # Centro do quadrante esquerdo
    quadrant_center_y = primary_y + (primary_height * 3 // 4)  # Centro do quadrante inferior
    
    # Posiciona a janela centralizada no quadrante
    x = quadrant_center_x - (width // 2)
    y = quadrant_center_y - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def start_capture_timer_with_popup():
    """Inicia o timer com um pop-up para capturar as coordenadas."""
    root = tk.Tk()
    root.withdraw()
    
    # Centraliza a janela no monitor principal
    center_window_on_primary(root, 300, 150)
    
    if messagebox.askokcancel("Configurar Clique", "Clique em OK para começar a configurar o ponto de clique.", parent=root):
        messagebox.showinfo("Captura de Ponto", "Coloque o mouse no local de clique.\nCapturando em 5 segundos...", parent=root)
        
        print("Capturando ponto de clique em 5 segundos...")
        time.sleep(5)
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
        
        if messagebox.askokcancel("Ponto Salvo!", f"Ponto de clique salvo: ({mouse_x}, {mouse_y})\n\nClique em OK para continuar.", parent=root):
            root.destroy()
            return mouse_x, mouse_y
    
    root.destroy()
    return None, None

def direcoes_aleatorias(num_direcoes = random.randint(4, 10)):
    """Muda o personagem de direção de forma aleatória."""
    global is_moving_character
    
    is_moving_character = True
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
    
    is_moving_character = False

def run_egg_hatching(click_x, click_y):
    """Executa o loop principal de rachar ovos."""
    global hatching_is_active, current_execution, remaining_time, is_paused, paused_execution, paused_remaining_time
    
    print("Iniciando a automação em 3 segundos...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Iniciando agora!")

    hatching_is_active = True
    is_paused = False
    current_execution = 0
    remaining_time = 0
    
    for i in range(100):
        if not hatching_is_active:
            break
            
        current_execution = i + 1
        print(f"Execução número: {i + 1}")
        pyautogui.click(x=click_x, y=click_y)
        time.sleep(1)
        direcoes_aleatorias()
        numero_aleatorio = random.randint(183, 203)
        print(f'O tempo de espera será de {numero_aleatorio} segundos')
        
        for j in range(numero_aleatorio):
            if not hatching_is_active:
                break
            
            # Verifica se foi pausado durante a contagem
            if is_paused:
                paused_execution = current_execution
                paused_remaining_time = numero_aleatorio - j
                print(f"Pausado na execução {paused_execution} com {paused_remaining_time}s restantes")
                return  # Sai da função para manter o estado
            
            remaining_time = numero_aleatorio - j
            print(f'faltam {remaining_time} segundos')
            time.sleep(1)

    if hatching_is_active:
        print("Todas as 100 repetições foram concluídas!")
        messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
    
    hatching_is_active = False
    is_paused = False

def run_egg_hatching_from_pause(click_x, click_y):
    """Retoma a automação exatamente do ponto onde foi pausado."""
    global hatching_is_active, current_execution, remaining_time, is_paused, paused_execution, paused_remaining_time
    
    print(f"Retomando da execução {paused_execution} com {paused_remaining_time}s restantes")
    
    hatching_is_active = True
    is_paused = False
    current_execution = paused_execution
    
    # Continua o tempo de espera restante
    for j in range(paused_remaining_time):
        if not hatching_is_active:
            break
        
        if is_paused:
            paused_remaining_time = paused_remaining_time - j
            print(f"Pausado novamente na execução {paused_execution} com {paused_remaining_time}s restantes")
            return
        
        remaining_time = paused_remaining_time - j
        print(f'faltam {remaining_time} segundos')
        time.sleep(1)
    
    # Continua com as próximas execuções
    for i in range(paused_execution, 100):
        if not hatching_is_active:
            break
            
        current_execution = i + 1
        print(f"Execução número: {i + 1}")
        pyautogui.click(x=click_x, y=click_y)
        time.sleep(1)
        direcoes_aleatorias()
        numero_aleatorio = random.randint(183, 203)
        print(f'O tempo de espera será de {numero_aleatorio} segundos')
        
        for j in range(numero_aleatorio):
            if not hatching_is_active:
                break
            
            if is_paused:
                paused_execution = current_execution
                paused_remaining_time = numero_aleatorio - j
                print(f"Pausado na execução {paused_execution} com {paused_remaining_time}s restantes")
                return
            
            remaining_time = numero_aleatorio - j
            print(f'faltam {remaining_time} segundos')
            time.sleep(1)

    if hatching_is_active:
        print("Todas as 100 repetições foram concluídas!")
        messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
    
    hatching_is_active = False
    is_paused = False

def update_countdown(root, execution_label, time_label, control_button):
    """Atualiza o contador de execução e tempo restante."""
    global hatching_is_active, current_execution, remaining_time, is_moving_character, is_paused, paused_execution, paused_remaining_time
    
    try:
        if hatching_is_active and not is_paused:
            execution_label.config(text=f"Execução: {current_execution}/{total_executions}")
            time_label.config(text=f"Tempo restante: {remaining_time}s")
            
            # Atualiza estado do botão baseado no movimento do personagem
            if is_moving_character:
                control_button.config(state="disabled")
            else:
                control_button.config(state="normal")
        elif is_paused:
            # Quando pausado, mostra o estado exato
            execution_label.config(text=f"Execução: {paused_execution}/{total_executions} (Pausado)")
            time_label.config(text=f"Tempo restante: {paused_remaining_time}s")
            control_button.config(state="normal")
        else:
            # Quando não está ativo, mostra status inicial
            execution_label.config(text="Execução: 0/100")
            time_label.config(text="Tempo restante: ---")
            control_button.config(state="normal")
        
        # Sempre agenda a próxima atualização
        root.after(1000, lambda: update_countdown(root, execution_label, time_label, control_button))
    except tk.TclError:
        # Janela foi fechada, para a atualização
        pass

def toggle_hatching(click_x, click_y, control_button, execution_label, time_label):
    """Alterna entre iniciar, pausar e retomar a automação."""
    global hatching_is_active, is_paused
    
    current_text = control_button.cget("text")
    
    if "Iniciar" in current_text:
        # Primeira vez - iniciar automação
        control_button.config(text="⏸️ Pausar", bg="#f39c12")
        hatching_is_active = True
        is_paused = False
        
        # Inicia a automação em uma thread separada
        thread = threading.Thread(target=run_egg_hatching, args=(click_x, click_y))
        thread.daemon = True
        thread.start()
        
    elif "Pausar" in current_text:
        # Pausar automação
        is_paused = True
        control_button.config(text="▶️ Retomar", bg="#27ae60")
        print("Automação pausada pelo usuário.")
        
    elif "Retomar" in current_text:
        # Retomar automação
        control_button.config(text="⏸️ Pausar", bg="#f39c12")
        hatching_is_active = True
        is_paused = False
        
        # Retoma a automação em uma thread separada
        thread = threading.Thread(target=run_egg_hatching_from_pause, args=(click_x, click_y))
        thread.daemon = True
        thread.start()

def create_control_window(click_x, click_y):
    """Cria e exibe a janela de controle flutuante."""
    root = tk.Tk()
    root.title("Controle de Rachar Ovos")
    
    # Posiciona a janela no centro do quadrante inferior esquerdo do monitor principal
    position_window_bottom_left(root, 250, 200)
    root.attributes('-topmost', True)
    root.resizable(False, False)

    # Frame principal
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack()

    # Título
    title_label = tk.Label(main_frame, text="🥚 Rachar Ovos", font=("Arial", 12, "bold"))
    title_label.pack(pady=(0, 10))

    # Frame de informações
    info_frame = tk.Frame(main_frame)
    info_frame.pack(pady=5)

    execution_label = tk.Label(info_frame, text="Execução: 0/100", font=("Arial", 10))
    execution_label.pack()

    time_label = tk.Label(info_frame, text="Tempo restante: ---", font=("Arial", 10))
    time_label.pack()

    # Botão único de controle
    control_button = tk.Button(
        main_frame, 
        text="▶️ Iniciar", 
        bg="#27ae60", 
        fg="white",
        command=lambda: toggle_hatching(click_x, click_y, control_button, execution_label, time_label),
        width=15,
        height=2,
        font=("Arial", 10, "bold")
    )
    control_button.pack(pady=20)

    # Inicia a atualização dos contadores
    update_countdown(root, execution_label, time_label, control_button)
    
    root.mainloop()

def create_hatching_menu():
    """Cria e exibe o menu de rachar ovos."""
    click_x, click_y = start_capture_timer_with_popup()

    if click_x is not None:
        create_control_window(click_x, click_y)
    else:
        print("Operação cancelada. Saindo do script.")

if __name__ == "__main__":
    create_hatching_menu()
