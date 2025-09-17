import pyautogui
import time
import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from screeninfo import get_monitors

# Variáveis globais para a aplicação
app_window = None
hatching_is_active = False
current_execution = 0
total_executions = 100
remaining_time = 0
after_id_hatching = None
after_id_countdown = None

def get_primary_monitor_dimensions():
    """Retorna as dimensões e a posição do monitor principal usando screeninfo."""
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height, monitor.x, monitor.y
    monitor = get_monitors()[0]
    return monitor.width, monitor.height, monitor.x, monitor.y

def center_on_primary(window, width, height):
    """Centraliza uma janela no monitor principal."""
    mon_width, mon_height, mon_x, mon_y = get_primary_monitor_dimensions()
    x = mon_x + (mon_width // 2) - (width // 2)
    y = mon_y + (mon_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def start_capture_timer_with_popup():
    """Inicia o timer com um pop-up para capturar as coordenadas."""
    root = tk.Toplevel()
    root.withdraw()
    center_on_primary(root, 300, 150)
    
    if messagebox.askokcancel("Configurar Clique", "Clique em OK para começar a configurar o ponto de clique.", parent=root):
        messagebox.showinfo("Captura de Ponto", "Coloque o mouse no local de clique.\nCapturando em 5 segundos...", parent=root)
        
        print("Capturando ponto de clique em 5 segundos...")
        time.sleep(5)
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
        
        if messagebox.askokcancel("Ponto Salvo!", f"Ponto de clique salvo: ({mouse_x}, {mouse_y})\n\nClique em OK para iniciar a automação.", parent=root):
            root.destroy()
            return mouse_x, mouse_y
    
    root.destroy()
    return None, None

def direcoes_aleatorias(num_direcoes = random.randint(4, 10)):
    """Muda o personagem de direção de forma aleatória."""
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

def run_egg_hatching(click_x, click_y, control_window=None):
    """Executa o loop principal de rachar ovos."""
    global hatching_is_active, current_execution, remaining_time, after_id_hatching, after_id_countdown
    
    print("Iniciando a automação em 5 segundos...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Iniciando agora!")

    hatching_is_active = True
    
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
            remaining_time = numero_aleatorio - j
            print(f'faltam {remaining_time} segundos')
            time.sleep(1)

    if hatching_is_active:
        print("Todas as 100 repetições foram concluídas!")
        messagebox.showinfo("Fim da Automação", "As 100 repetições foram concluídas!")
    
    hatching_is_active = False
    if control_window:
        control_window.destroy()

def update_countdown(root, execution_label, time_label):
    """Atualiza o contador de execução e tempo restante."""
    global hatching_is_active, current_execution, remaining_time, after_id_countdown
    
    if hatching_is_active:
        execution_label.config(text=f"Execução: {current_execution}/{total_executions}")
        time_label.config(text=f"Tempo restante: {remaining_time}s")
        after_id_countdown = root.after(1000, lambda: update_countdown(root, execution_label, time_label))
    else:
        execution_label.config(text="Execução: Pausado")
        time_label.config(text="Tempo restante: ---")

def pause_hatching():
    """Pausa a automação de rachar ovos."""
    global hatching_is_active
    hatching_is_active = False
    print("Automação pausada pelo usuário.")

def resume_hatching():
    """Retoma a automação de rachar ovos."""
    global hatching_is_active
    hatching_is_active = True
    print("Automação retomada pelo usuário.")

def stop_hatching(root):
    """Para completamente a automação."""
    global hatching_is_active, after_id_hatching, after_id_countdown
    hatching_is_active = False
    if after_id_hatching:
        root.after_cancel(after_id_hatching)
    if after_id_countdown:
        root.after_cancel(after_id_countdown)
    root.destroy()
    print("Automação interrompida pelo usuário.")

def create_control_window(click_x, click_y):
    """Cria e exibe a janela de controle flutuante."""
    global hatching_is_active, after_id_hatching, after_id_countdown
    
    root = tk.Tk()
    root.title("Controle de Rachar Ovos")
    
    # Posiciona a janela no canto superior direito
    screen_width, screen_height = get_primary_monitor_dimensions()[:2]
    root.geometry(f'+{screen_width - 250}+10')
    
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

    # Frame de botões
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    pause_button = tk.Button(
        buttons_frame, 
        text="⏸️ Pausar", 
        bg="#f39c12", 
        fg="white",
        command=pause_hatching,
        width=8
    )
    pause_button.pack(side=tk.LEFT, padx=5)

    resume_button = tk.Button(
        buttons_frame, 
        text="▶️ Retomar", 
        bg="#27ae60", 
        fg="white",
        command=resume_hatching,
        width=8
    )
    resume_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(
        buttons_frame, 
        text="⏹️ Parar", 
        bg="#e74c3c", 
        fg="white",
        command=lambda: stop_hatching(root),
        width=8
    )
    stop_button.pack(side=tk.LEFT, padx=5)

    # Inicia a atualização dos contadores
    update_countdown(root, execution_label, time_label)
    
    # Inicia a automação em uma thread separada
    import threading
    thread = threading.Thread(target=run_egg_hatching, args=(click_x, click_y, root))
    thread.daemon = True
    thread.start()
    
    root.mainloop()

def create_hatching_menu():
    """Cria e exibe o menu de rachar ovos."""
    global app_window

    click_x, click_y = start_capture_timer_with_popup()

    if click_x is not None:
        create_control_window(click_x, click_y)
    else:
        print("Operação cancelada. Saindo do script.")

if __name__ == "__main__":
    create_hatching_menu()