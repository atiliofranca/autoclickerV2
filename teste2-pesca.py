import pyautogui
import time
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Variáveis globais para controlar a execução do script de pesca e a última direção
fishing_is_active = False
last_direction = None
after_id_fishing = None
after_id_pet = None

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

def start_fishing_action(fishing_key, mouse_x, mouse_y):
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

def create_control_window(fishing_key, mouse_x, mouse_y, search_region, image_file):
    """Cria e exibe a janela de controle."""
    root = tk.Tk()
    root.title("Controle de Pesca")
    
    screen_width, screen_height = get_screen_dimensions()
    root.geometry(f'+10+{screen_height - 100}')
    
    root.attributes('-topmost', True)

    frame_info = tk.Frame(root, padx=10, pady=5)
    frame_info.pack(fill=tk.X)

    direction_label = tk.Label(frame_info, text="Direção: ---")
    direction_label.pack(side=tk.LEFT, padx=5)

    pet_label = tk.Label(frame_info, text="Carinho: ---")
    pet_label.pack(side=tk.RIGHT, padx=5)

    frame_buttons = tk.Frame(root, padx=10, pady=10)
    frame_buttons.pack()
    
    start_button = tk.Button(frame_buttons, text="Iniciar Pesca", relief="raised", command=lambda: start_script(root, fishing_key, mouse_x, mouse_y, search_region, image_file, start_button, stop_button, direction_label, pet_label))
    start_button.pack(side=tk.LEFT, padx=5)
    
    stop_button = tk.Button(frame_buttons, text="Parar Pesca", relief="raised", command=lambda: stop_script(root, start_button, stop_button, direction_label, pet_label))
    stop_button.pack(side=tk.RIGHT, padx=5)
    
    frame_exit = tk.Frame(root, pady=5)
    frame_exit.pack()
    
    exit_button = tk.Button(frame_exit, text="Sair", bg="red", fg="white", command=lambda: exit_script(root))
    exit_button.pack(side=tk.BOTTOM, pady=5)
    
    pet_action_loop(root)
    
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