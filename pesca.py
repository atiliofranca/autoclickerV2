import pyautogui
import time
import random
import tkinter as tk
import threading
from tkinter import simpledialog, messagebox

# Variáveis globais para controlar a execução do script de pesca e a última direção
fishing_is_active = False
last_direction = None
after_id_fishing = None
after_id_pet = None
last_action_time = 0

# Variáveis globais para a nova funcionalidade de carinho
pet_is_active = False
pet_coordinates = None
last_pet_time = 0

# Variável para controlar o início do script
is_first_start = True

def get_screen_dimensions():
    """Retorna as dimensões do monitor principal."""
    return pyautogui.size()

def create_centered_parent_window():
    """
    Cria uma janela real, centraliza e a mantém invisível para usar como pai dos pop-ups.
    Isso força o SO a posicionar os pop-ups corretamente.
    """
    root = tk.Tk()
    root.title("")
    root.geometry("1x1")
    root.attributes('-alpha', 0)  # Torna a janela invisível
    
    screen_width, screen_height = get_screen_dimensions()
    x = (screen_width // 2)
    y = (screen_height // 2)
    root.geometry(f'+{x}+{y}')
    root.update()
    
    return root

# --- Funções de Configuração ---

def get_fishing_key(parent):
    """Pede ao usuário para escolher a tecla de atalho de pesca."""
    keys = [f'F{i}' for i in range(1, 13)]
    message = "Escolha a tecla de atalho para pesca (F1 a F12)."
    
    user_key = simpledialog.askstring("Tecla de Atalho", message, parent=parent)
    
    if user_key and user_key.upper() in keys:
        print(f"Tecla de atalho salva: {user_key.upper()}")
        return user_key.lower()
    else:
        messagebox.showerror("Erro", "Tecla de atalho inválida. Saindo do script.", parent=parent)
        return None

def get_pet_coordinates(parent):
    """Guia o usuário para definir as coordenadas do clique para dar carinho."""
    global pet_is_active, pet_coordinates
    
    if messagebox.askyesno("Funcionalidade Opcional", "Deseja ativar a funcionalidade de 'dar carinho ao Pokémon' a cada 100 segundos?", parent=parent):
        pet_is_active = True
        
        if messagebox.askokcancel("Configurar Carinho", "Clique em OK e, em seguida, posicione o mouse no local exato onde o clique de carinho deve ocorrer.", parent=parent):
            messagebox.showinfo("Captura de Ponto", "Capturando em 5 segundos...", parent=parent)
            print("Capturando ponto de carinho em 5 segundos...")
            time.sleep(5)
            
            pet_coordinates = pyautogui.position()
            print(f"Ponto de carinho salvo: ({pet_coordinates.x}, {pet_coordinates.y})")
            return pet_coordinates
    
    pet_is_active = False
    return None

def get_exclamation_region(parent):
    """Guia o usuário para definir o ponto central da região da exclamação."""
    if messagebox.askokcancel("Configurar Região", "Agora vamos configurar a área de busca da exclamação.\n\nColoque o mouse no CENTRO do ícone da exclamação e clique em OK para continuar.", parent=parent):
        messagebox.showinfo("Captura de Região", "Capturando em 5 segundos...", parent=parent)
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

def get_fishing_click_coordinates(parent):
    """Pede ao usuário para posicionar o mouse e captura as coordenadas de clique de pesca."""
    if messagebox.askokcancel("Configurar Clique", "Agora vamos configurar o ponto de clique de pesca.\n\nClique em OK para continuar.", parent=parent):
        messagebox.showinfo("Captura de Ponto", "Colocando o mouse no local de clique de pesca.\nCapturando em 5 segundos...", parent=parent)
        print("Capturando ponto de clique em 5 segundos...")
        time.sleep(5)
        
        mouse_x, mouse_y = pyautogui.position()
        print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
        return mouse_x, mouse_y
    
    return None, None

# --- Funções de Automação ---


    """Prepara o personagem e inicia a pesca."""
    global last_direction
    print("Iniciando a pesca...")
    
    pyautogui.hotkey('ctrl', 'down')
    time.sleep(3)
    last_direction = 'down'

    pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(1)
    pyautogui.press(fishing_key)
    time.sleep(1) 
    pyautogui.click(x=mouse_x, y=mouse_y)
    print(f"'{fishing_key.upper()}' apertado e clique realizado em ({mouse_x}, {mouse_y}).")

def update_pet_countdown(root, pet_label):
    """Atualiza o contador de segundos para o próximo carinho."""
    global pet_is_active, last_pet_time, after_id_pet

    if pet_is_active:
        seconds_left = max(0, 100 - (time.time() - last_pet_time))
        pet_label.config(text=f"Carinho em: {int(seconds_left)}s")
        after_id_pet = root.after(1000, lambda: update_pet_countdown(root, pet_label))
    else:
        pet_label.config(text="Carinho: Desativado")

def pet_action_loop(root):
    """Verifica e executa a ação de dar carinho."""
    global pet_is_active, last_pet_time, pet_coordinates

    if pet_is_active and (time.time() - last_pet_time) > 100:
        print("Tempo de carinho alcançado. Dando carinho no Pokémon...")
        pyautogui.click(x=pet_coordinates.x, y=pet_coordinates.y)
        last_pet_time = time.time()
    
    root.after(1000, lambda: pet_action_loop(root))

def monitor_screen_and_react(root, target_image_path, mouse_x, mouse_y, fishing_key, search_region, direction_label):
    """Monitora a tela e reage se a pesca estiver ativa."""
    global fishing_is_active, last_direction, after_id_fishing, last_action_time

    if not fishing_is_active:
        return

    if last_direction:
        direction_label.config(text=f"Direção: {last_direction.capitalize()}")
    
    try:
        exclamation_location = pyautogui.locateOnScreen(
            target_image_path,
            confidence=0.8,
            region=search_region
        )
    except Exception as e:
        print(f"Erro na detecção de imagem: {e}")
        exclamation_location = None

    if exclamation_location:
        print("Imagem da exclamação encontrada! Reagindo...")
        
        last_action_time = time.time()
        
        directions = ['up', 'down', 'left', 'right']
        if last_direction and last_direction in directions:
            directions.remove(last_direction)
        
        selected_direction = random.choice(directions)
        last_direction = selected_direction
        
        print(f"Pressionando Control + {selected_direction.capitalize()}...")
        pyautogui.hotkey('ctrl', selected_direction)
        
        time.sleep(1.9)
    else:
        print("Imagem não encontrada. Aguardando...")
        if time.time() - last_action_time > 8:
            print("Timeout de 8 segundos alcançado. Reiniciando a pesca...")
            
            start_fishing_action(fishing_key, mouse_x, mouse_y)
            last_action_time = time.time()

    after_id_fishing = root.after(100, lambda: monitor_screen_and_react(root, target_image_path, mouse_x, mouse_y, fishing_key, search_region, direction_label))

# --- Funções de Controle da Janela Principal ---

def start_script(root, fishing_key, mouse_x, mouse_y, search_region, image_file, start_button, stop_button, direction_label, pet_label):
    """Inicia o script de pesca e a janela de controle."""
    global fishing_is_active, last_direction, last_action_time, last_pet_time, is_first_start
    
    if fishing_is_active:
        stop_script(root, start_button, stop_button, direction_label, pet_label)
        
    fishing_is_active = True
    print("Script ativado.")
    
    start_button.config(relief="sunken")
    stop_button.config(relief="raised")
    
    last_action_time = time.time()
    last_direction = None
    
    if is_first_start:
        last_pet_time = time.time()
        root.after(0, lambda: pet_action_loop(root))
        root.after(0, lambda: update_pet_countdown(root, pet_label))
        is_first_start = False
    
    time.sleep(1)
    
    start_fishing_action(fishing_key, mouse_x, mouse_y)

    monitor_screen_and_react(root, image_file, mouse_x, mouse_y, fishing_key, search_region, direction_label)

def stop_script(root, start_button, stop_button, direction_label, pet_label):
    """Para o script de pesca."""
    global fishing_is_active, after_id_fishing
    if fishing_is_active:
        fishing_is_active = False
        print("Script desativado.")
        
        stop_button.config(relief="sunken")
        start_button.config(relief="raised")
        
        direction_label.config(text="Direção: ---")
        
        if after_id_fishing:
            root.after_cancel(after_id_fishing)
            after_id_fishing = None

def exit_script(root):
    """Fecha a janela e encerra a aplicação."""
    global fishing_is_active, after_id_fishing, after_id_pet
    fishing_is_active = False
    if after_id_fishing:
        root.after_cancel(after_id_fishing)
    if after_id_pet:
        root.after_cancel(after_id_pet)
    root.destroy()
    print("Aplicação encerrada.")

def start_fishing_action(fishing_key, mouse_x, mouse_y):
    """Prepara o personagem e inicia a pesca."""
    global last_direction
    
    directions = ['up', 'down', 'left', 'right']
    if last_direction and last_direction in directions:
        directions.remove(last_direction)
    
    direction = random.choice(directions)
    last_direction = direction
    
    pyautogui.press(direction)
    time.sleep(0.5)
    pyautogui.press(fishing_key)
    time.sleep(0.5)
    pyautogui.click(mouse_x, mouse_y)

def create_control_window(fishing_key, mouse_x, mouse_y, search_region, image_file):
    """Cria e exibe a janela de controle seguindo o padrão do rachar ovos."""
    root = tk.Tk()
    root.title("Menu Principal - Automação")
    root.resizable(False, False)
    
    # Define o tamanho da janela igual ao rachar ovos
    window_width = 400
    window_height = 300
    
    # Centraliza a janela no quadrante inferior esquerdo
    screen_width, screen_height = get_screen_dimensions()
    quadrant_center_x = screen_width // 4
    quadrant_center_y = screen_height * 3 // 4
    x = quadrant_center_x - (window_width // 2)
    y = quadrant_center_y - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Torna a janela flutuante
    root.attributes('-topmost', True)
    
    # Frame principal
    main_frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    title_label = tk.Label(
        main_frame, 
        text="🎣 Pesca Automática", 
        font=("Arial", 16, "bold"),
        fg="#2c3e50",
        bg="#ecf0f1"
    )
    title_label.pack(pady=(0, 20))
    
    # Status
    status_label = tk.Label(
        main_frame,
        text="Aguardando configuração...",
        font=("Arial", 12),
        fg="#7f8c8d",
        bg="#ecf0f1"
    )
    status_label.pack(pady=(0, 10))
    
    # Progresso
    progress_label = tk.Label(
        main_frame,
        text="Progresso: ---",
        font=("Arial", 10),
        fg="#34495e",
        bg="#ecf0f1"
    )
    progress_label.pack(pady=(0, 20))
    
    # Botões principais
    buttons_frame = tk.Frame(main_frame, bg="#ecf0f1")
    buttons_frame.pack(pady=20)
    
    # Botão Configurar/Parar
    btn_configurar_parar = tk.Button(
        buttons_frame,
        text="⚙️ Configurar",
        font=("Arial", 12, "bold"),
        bg="#3498db",
        fg="white",
        width=15,
        height=2,
        command=lambda: toggle_configurar_parar(),
        cursor="hand2"
    )
    btn_configurar_parar.pack(side=tk.LEFT, padx=10)
    
    # Botão Pausar/Play
    btn_pausar_play = tk.Button(
        buttons_frame,
        text="⏸️ Pausar",
        font=("Arial", 12, "bold"),
        bg="#f39c12",
        fg="white",
        width=15,
        height=2,
        command=lambda: toggle_pausar_play(),
        cursor="hand2",
        state="disabled"
    )
    btn_pausar_play.pack(side=tk.LEFT, padx=10)
    
    # Botão Retornar (abaixo dos outros botões)
    btn_retornar = tk.Button(
        main_frame,
        text="⬅️ Retornar",
        font=("Arial", 12, "bold"),
        bg="#9b59b6",
        fg="white",
        width=15,
        height=2,
        command=lambda: voltar_ao_menu(),
        cursor="hand2",
        state="disabled"
    )
    btn_retornar.pack(pady=(20, 0))
    
    # Variáveis de controle
    is_configured = False
    is_paused = False
    fishing_thread = None
    next_pet_time = 0
    
    def toggle_configurar_parar():
        nonlocal is_configured, is_paused
        if not is_configured:
            # Configurar
            is_configured = True
            btn_configurar_parar.config(
                text="⏹️ Parar",
                bg="#e74c3c"
            )
            btn_pausar_play.config(
                state="normal",
                text="▶️ Iniciar",
                bg="#27ae60"
            )
            status_label.config(text="Configurado! Clique em Iniciar para começar.")
            progress_label.config(text="Progresso: Aguardando início")
            btn_retornar.config(state="disabled", bg="#95a5a6")
        else:
            # Parar
            stop_fishing()
    
    def toggle_pausar_play():
        nonlocal is_paused
        current_text = btn_pausar_play.cget("text")
        
        if "Iniciar" in current_text:
            # Primeira vez - iniciar automação
            start_fishing()
            btn_pausar_play.config(
                text="⏸️ Pausar",
                bg="#f39c12"
            )
            is_paused = False
            btn_retornar.config(state="disabled", bg="#95a5a6")
        elif "Pausar" in current_text:
            # Pausar
            pause_fishing()
            btn_pausar_play.config(
                text="▶️ Play",
                bg="#27ae60"
            )
            is_paused = True
            btn_retornar.config(state="disabled", bg="#95a5a6")
        elif "Play" in current_text:
            # Retomar
            resume_fishing()
            btn_pausar_play.config(
                text="⏸️ Pausar",
                bg="#f39c12"
            )
            is_paused = False
            btn_retornar.config(state="disabled", bg="#95a5a6")
    
    def start_fishing():
        """Inicia a automação de pesca."""
        global fishing_is_active, last_action_time, next_pet_time
        fishing_is_active = True
        last_action_time = time.time()
        next_pet_time = time.time() + 30  # Próximo carinho em 30 segundos
        
        status_label.config(text="Executando automação...")
        
        # Executa em uma thread separada
        fishing_thread = threading.Thread(
            target=run_fishing_automation,
            args=(fishing_key, mouse_x, mouse_y, search_region, image_file)
        )
        fishing_thread.daemon = True
        fishing_thread.start()
    
    def pause_fishing():
        """Pausa a automação de pesca."""
        global fishing_is_active
        fishing_is_active = False
        status_label.config(text="Automação pausada pelo usuário.")
    
    def resume_fishing():
        """Retoma a automação de pesca."""
        global fishing_is_active, last_action_time
        fishing_is_active = True
        last_action_time = time.time()
        status_label.config(text="Executando automação...")
        
        # Reinicia a pesca
        start_fishing_action(fishing_key, mouse_x, mouse_y)
    
    def stop_fishing():
        """Para completamente a automação e reseta."""
        global fishing_is_active, is_configured, is_paused
        fishing_is_active = False
        is_configured = False
        is_paused = False
        
        # Reset dos botões
        btn_configurar_parar.config(
            text="⚙️ Configurar",
            bg="#3498db"
        )
        btn_pausar_play.config(
            text="⏸️ Pausar",
            bg="#f39c12",
            state="disabled"
        )
        
        # Reset dos labels
        status_label.config(text="Aguardando configuração...")
        progress_label.config(text="Progresso: ---")
        
        btn_retornar.config(state="normal", bg="#9b59b6")
    
    def voltar_ao_menu():
        """Volta ao menu principal."""
        root.destroy()
    
    def update_progress():
        """Atualiza o progresso com tempo para próximo carinho."""
        global next_pet_time
        if fishing_is_active and next_pet_time > 0:
            remaining_time = max(0, int(next_pet_time - time.time()))
            if remaining_time > 0:
                progress_label.config(text=f"Próximo carinho em: {remaining_time}s")
            else:
                progress_label.config(text="Carinho disponível!")
        elif fishing_is_active:
            progress_label.config(text="Executando pesca...")
        
        if fishing_is_active:
            root.after(1000, update_progress)
    
    def run_fishing_automation(fishing_key, mouse_x, mouse_y, search_region, image_file):
        """Executa a automação de pesca."""
        global fishing_is_active, next_pet_time
        
        # Inicia o monitoramento da tela
        monitor_screen_and_react(root, image_file, mouse_x, mouse_y, fishing_key, search_region, status_label)
        
        # Inicia a atualização do progresso
        update_progress()
        
        # Loop principal de carinho
        while fishing_is_active:
            current_time = time.time()
            if current_time >= next_pet_time:
                # Executa carinho
                if pet_coordinates:
                    pyautogui.click(pet_coordinates[0], pet_coordinates[1])
                    status_label.config(text="Executando carinho...")
                    time.sleep(1)
                
                # Define próximo carinho
                next_pet_time = current_time + 30
                status_label.config(text="Executando automação...")
            
            time.sleep(1)
    
    # Inicia o loop principal
    root.mainloop()

if __name__ == "__main__":
    image_file = 'exclamacao-pesca-sem-fundo.png'

    parent_root = create_centered_parent_window()

    fishing_key = get_fishing_key(parent_root)
    if not fishing_key:
        parent_root.destroy()
        exit()
        
    pet_coordinates = get_pet_coordinates(parent_root)

    search_region = get_exclamation_region(parent_root)
    if not search_region:
        parent_root.destroy()
        exit()
        
    mouse_x, mouse_y = get_fishing_click_coordinates(parent_root)
    if mouse_x is None:
        parent_root.destroy()
        exit()
    
    parent_root.destroy()
    print("Configurações salvas. A janela de controle está pronta.")
    create_control_window(fishing_key, mouse_x, mouse_y, search_region, image_file)