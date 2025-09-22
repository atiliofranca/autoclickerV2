import pyautogui
import time
import random
import tkinter as tk
import threading
import json
import os
from tkinter import simpledialog, messagebox
from screeninfo import get_monitors

# Variáveis globais para controle da aplicação
fishing_is_active = False
last_direction = None
last_action_time = 0
last_pet_time = 0
last_attack_time = 0

# Variáveis para configurações
pokemon_attacks = {}
pet_coordinates = None
pet_is_active = False
fishing_key = None
search_region = None
mouse_x = None
mouse_y = None

# Arquivo para persistência dos dados
POKEMON_DATA_FILE = "pokemon_data.json"

# Variáveis para controle de threads
after_id_fishing = None
after_id_pet = None
after_id_attack = None

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

def create_centered_parent_window():
    """Cria uma janela invisível para usar como pai dos pop-ups."""
    root = tk.Tk()
    root.title("")
    root.geometry("1x1")
    root.attributes('-alpha', 0)
    center_on_primary(root, 1, 1)
    root.update()
    return root

def load_pokemon_data():
    """Carrega os dados dos Pokémon salvos do arquivo JSON."""
    global pokemon_attacks
    try:
        if os.path.exists(POKEMON_DATA_FILE):
            with open(POKEMON_DATA_FILE, 'r', encoding='utf-8') as f:
                pokemon_attacks = json.load(f)
            print(f"Dados de {len(pokemon_attacks)} Pokémon carregados.")
        else:
            pokemon_attacks = {}
            print("Nenhum Pokémon salvo encontrado.")
    except Exception as e:
        print(f"Erro ao carregar dados dos Pokémon: {e}")
        pokemon_attacks = {}

def save_pokemon_data():
    """Salva os dados dos Pokémon no arquivo JSON."""
    try:
        with open(POKEMON_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(pokemon_attacks, f, ensure_ascii=False, indent=2)
        print("Dados dos Pokémon salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar dados dos Pokémon: {e}")

def edit_pokemon(pokemon_name, parent):
    """Edita um Pokémon existente."""
    global pokemon_attacks
    
    if pokemon_name not in pokemon_attacks:
        messagebox.showerror("Erro", "Pokémon não encontrado!", parent=parent)
        return
    
    current_data = pokemon_attacks[pokemon_name]
    
    # Mostra dados atuais
    current_attacks = ', '.join(current_data['attacks'])
    messagebox.showinfo("Dados Atuais", 
        f"Pokémon: {pokemon_name}\nAtaques: {current_attacks}\nCooldown: {current_data['cooldown']}s", 
        parent=parent)
    
    # Pergunta o que editar
    edit_choice = messagebox.askyesnocancel("Editar Pokémon", 
        "Escolha o que editar:\n\nSim = Editar ataques\nNão = Editar cooldown\nCancelar = Renomear Pokémon", 
        parent=parent)
    
    if edit_choice is None:  # Renomear
        new_name = simpledialog.askstring("Renomear Pokémon", f"Novo nome para {pokemon_name}:", parent=parent)
        if new_name and new_name != pokemon_name:
            pokemon_attacks[new_name] = pokemon_attacks.pop(pokemon_name)
            save_pokemon_data()
            messagebox.showinfo("Sucesso", f"Pokémon renomeado para {new_name}!", parent=parent)
    elif edit_choice:  # Editar ataques
        attacks = []
        for i in range(1, 5):
            if i == 1:
                key = simpledialog.askstring(f"Ataque {i}", f"Digite a tecla do ataque {i} (F1-F12):", parent=parent)
            else:
                key = simpledialog.askstring(f"Ataque {i} (Opcional)", f"Digite a tecla do ataque {i} (F1-F12) ou deixe vazio:", parent=parent)
            
            if key and key.upper() in [f'F{j}' for j in range(1, 13)]:
                attacks.append(key.upper())
            elif i == 1:
                messagebox.showerror("Erro", "Pelo menos um ataque é obrigatório!", parent=parent)
                return
            else:
                break
        
        if attacks:
            pokemon_attacks[pokemon_name]['attacks'] = attacks
            save_pokemon_data()
            messagebox.showinfo("Sucesso", "Ataques atualizados!", parent=parent)
    else:  # Editar cooldown
        new_cooldown = simpledialog.askinteger("Editar Cooldown", 
            f"Novo cooldown em segundos (atual: {current_data['cooldown']}s):", 
            parent=parent, minvalue=1, maxvalue=3600)
        if new_cooldown:
            pokemon_attacks[pokemon_name]['cooldown'] = new_cooldown
            save_pokemon_data()
            messagebox.showinfo("Sucesso", f"Cooldown atualizado para {new_cooldown}s!", parent=parent)

# --- Fase 1: Configuração Inicial ---

def configure_pokemon_attacks(parent):
    """Configura os ataques de Pokémon seguindo o XML."""
    global pokemon_attacks
    
    if not messagebox.askyesno("Configuração de Pokémon", "Deseja configurar ataques de Pokémon?", parent=parent):
        return True
    
    # Menu de opções
    while True:
        if pokemon_attacks:
            choice = messagebox.askyesnocancel("Menu Pokémon", 
                "Escolha uma opção:\n\nSim = Gerenciar Pokémon existente\nNão = Cadastrar novo Pokémon\nCancelar = Pular configuração", 
                parent=parent)
        else:
            choice = messagebox.askyesnocancel("Menu Pokémon", 
                "Escolha uma opção:\n\nSim = Cadastrar novo Pokémon\nNão = Pular configuração\nCancelar = Pular configuração", 
                parent=parent)
        
        if choice is None:  # Cancelar
            return True
        elif choice:  # Gerenciar existente ou cadastrar novo
            if pokemon_attacks:  # Se há Pokémon cadastrados, mostra menu de gerenciamento
                manage_choice = messagebox.askyesnocancel("Gerenciar Pokémon", 
                    "Escolha uma ação:\n\nSim = Escolher Pokémon\nNão = Editar Pokémon\nCancelar = Excluir Pokémon", 
                    parent=parent)
                
                if manage_choice is None:  # Excluir
                    pokemon_names = list(pokemon_attacks.keys())
                    pokemon_name = simpledialog.askstring("Excluir Pokémon", 
                        f"Digite o nome do Pokémon para excluir:\n{', '.join(pokemon_names)}", parent=parent)
                    
                    if pokemon_name and pokemon_name in pokemon_attacks:
                        del pokemon_attacks[pokemon_name]
                        save_pokemon_data()
                        messagebox.showinfo("Sucesso", f"Pokémon {pokemon_name} excluído!", parent=parent)
                        continue
                elif manage_choice:  # Escolher
                    pokemon_names = list(pokemon_attacks.keys())
                    pokemon_name = simpledialog.askstring("Escolher Pokémon", 
                        f"Digite o nome do Pokémon:\n{', '.join(pokemon_names)}", parent=parent)
                    
                    if pokemon_name and pokemon_name in pokemon_attacks:
                        pokemon_attacks = {pokemon_name: pokemon_attacks[pokemon_name]}
                        messagebox.showinfo("Sucesso", f"Pokémon {pokemon_name} selecionado!", parent=parent)
                        return True
                else:  # Editar
                    pokemon_names = list(pokemon_attacks.keys())
                    pokemon_name = simpledialog.askstring("Editar Pokémon", 
                        f"Digite o nome do Pokémon para editar:\n{', '.join(pokemon_names)}", parent=parent)
                    
                    if pokemon_name and pokemon_name in pokemon_attacks:
                        edit_pokemon(pokemon_name, parent)
                        continue
            else:  # Cadastrar novo
                pass  # Continua para o código de cadastro
        else:  # Pular configuração
            return True
        
        # Se chegou aqui e não há Pokémon cadastrados, cadastra um novo
        if not pokemon_attacks:
            pokemon_name = simpledialog.askstring("Nome do Pokémon", "Digite o nome do Pokémon:", parent=parent)
            if not pokemon_name:
                continue
                
            # Coleta as teclas de atalho
            attacks = []
            for i in range(1, 5):
                if i == 1:
                    key = simpledialog.askstring(f"Ataque {i}", f"Digite a tecla do ataque {i} (F1-F12):", parent=parent)
                else:
                    key = simpledialog.askstring(f"Ataque {i} (Opcional)", f"Digite a tecla do ataque {i} (F1-F12) ou deixe vazio:", parent=parent)
                
                if key and key.upper() in [f'F{j}' for j in range(1, 13)]:
                    attacks.append(key.upper())
                elif i == 1:
                    messagebox.showerror("Erro", "Pelo menos um ataque é obrigatório!", parent=parent)
                    break
                else:
                    break
            
            if attacks:
                cooldown = simpledialog.askinteger("Cooldown", "Digite o cooldown em segundos:", parent=parent, minvalue=1, maxvalue=3600)
                if cooldown:
                    pokemon_attacks[pokemon_name] = {
                        'attacks': attacks,
                        'cooldown': cooldown
                    }
                    save_pokemon_data()  # Salva os dados após cadastrar
                    messagebox.showinfo("Sucesso", f"Pokémon {pokemon_name} cadastrado e salvo!", parent=parent)
                    return True

def configure_pet_coordinates(parent):
    """Configura as coordenadas do carinho seguindo o XML."""
    global pet_coordinates, pet_is_active
    
    if messagebox.askyesno("Configurar Carinho", "Deseja ativar a funcionalidade de carinho?", parent=parent):
        pet_is_active = True
        messagebox.showinfo("Captura de Ponto", "Posicione o mouse no ponto de clique de carinho.\nCapturando em 5 segundos...", parent=parent)
        print("Capturando ponto de carinho em 5 segundos...")
        time.sleep(5)
            
        pet_coordinates = pyautogui.position()
        print(f"Ponto de carinho salvo: ({pet_coordinates.x}, {pet_coordinates.y})")
        return True
    else:
        pet_is_active = False
        return True

def configure_fishing_key(parent):
    """Configura a tecla de pesca seguindo o XML."""
    global fishing_key
    
    keys = [f'F{i}' for i in range(1, 13)]
    user_key = simpledialog.askstring("Tecla de Pesca", "Escolha a tecla de pesca (F1 a F12):", parent=parent)
    
    if user_key and user_key.upper() in keys:
        fishing_key = user_key.lower()
        print(f"Tecla de pesca salva: {user_key.upper()}")
        return True
    else:
        messagebox.showerror("Erro", "Tecla inválida!", parent=parent)
        return False

def configure_exclamation_region(parent):
    """Configura a região de busca da exclamação seguindo o XML."""
    global search_region
    
    messagebox.showinfo("Configurar Região", "Posicione o mouse no centro da exclamação para definir a área de busca.", parent=parent)
    messagebox.showinfo("Captura de Região", "Capturando em 5 segundos...", parent=parent)
    print("Capturando ponto central da região em 5 segundos...")
    time.sleep(5)
        
    center_x, center_y = pyautogui.position()
    width = 100
    height = 60
        
    left = center_x - width // 2
    top = center_y - height // 2
    search_region = (left, top, width, height)
    
    print(f"Região de busca salva: {search_region}")
    return True

def configure_fishing_click(parent):
    """Configura o ponto de clique de pesca seguindo o XML."""
    global mouse_x, mouse_y
    
    messagebox.showinfo("Configurar Clique", "Posicione o mouse no ponto de clique para lançar a isca.", parent=parent)
    messagebox.showinfo("Captura de Ponto", "Capturando em 5 segundos...", parent=parent)
    print("Capturando ponto de clique em 5 segundos...")
    time.sleep(5)
        
    mouse_x, mouse_y = pyautogui.position()
    print(f"Ponto de clique salvo: ({mouse_x}, {mouse_y})")
    return True

# --- Fase 2 e 3: Execução e Funcionalidades Adicionais ---

def start_fishing_action():
    """Prepara o personagem e inicia a pesca."""
    global last_direction, last_action_time
    
    print("Iniciando a pesca...")
    pyautogui.hotkey('ctrl', 'down')
    time.sleep(3)
    last_direction = 'down'
    last_action_time = time.time()

    pyautogui.click(mouse_x, mouse_y)
    time.sleep(1)
    pyautogui.press(fishing_key)
    time.sleep(1) 
    pyautogui.click(mouse_x, mouse_y)
    print(f"'{fishing_key.upper()}' apertado e clique realizado em ({mouse_x}, {mouse_y}).")

def monitor_screen_and_react(root, target_image_path, direction_label):
    """Monitora a tela e reage se a pesca estiver ativa."""
    global fishing_is_active, last_direction, last_action_time, after_id_fishing

    if not fishing_is_active:
        return

    if last_direction:
        direction_label.config(text=f"Direção: {last_direction.capitalize()}")
    
    # Verifica se passou tempo suficiente desde a última ação (1.9 segundos)
    if time.time() - last_action_time < 1.9:
        # Ainda está no período de delay, agenda próxima verificação
        after_id_fishing = root.after(100, lambda: monitor_screen_and_react(root, target_image_path, direction_label))
        return
    
    try:
        exclamation_location = pyautogui.locateOnScreen(
            target_image_path,
            region=search_region
        )
    except pyautogui.ImageNotFoundException:
        exclamation_location = None
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
        
        # Atualiza o tempo da última ação para evitar múltiplas execuções
        last_action_time = time.time()
    else:
        print("Imagem não encontrada. Aguardando...")
        if time.time() - last_action_time > 8:
            print("Timeout de 8 segundos alcançado. Reiniciando a pesca...")
            start_fishing_action()

    after_id_fishing = root.after(100, lambda: monitor_screen_and_react(root, target_image_path, direction_label))

def pet_action_loop(root):
    """Loop de carinho seguindo o XML."""
    global pet_is_active, last_pet_time, after_id_pet

    if pet_is_active and pet_coordinates and (time.time() - last_pet_time) > 100:
        print("Tempo de carinho alcançado. Dando carinho no Pokémon...")
        pyautogui.click(pet_coordinates.x, pet_coordinates.y)
        last_pet_time = time.time()
    
    after_id_pet = root.after(1000, lambda: pet_action_loop(root))

def pokemon_attack_loop(root):
    """Loop de ataques de Pokémon seguindo o XML."""
    global pokemon_attacks, last_attack_time, after_id_attack

    if pokemon_attacks and (time.time() - last_attack_time) > min(attack['cooldown'] for attack in pokemon_attacks.values()):
        for pokemon_name, pokemon_data in pokemon_attacks.items():
            for attack_key in pokemon_data['attacks']:
                pyautogui.press(attack_key)
                time.sleep(0.5)
        last_attack_time = time.time()
        print("Ataques de Pokémon executados!")
    
    after_id_attack = root.after(1000, lambda: pokemon_attack_loop(root))

def update_counters(root, pet_label, attack_label):
    """Atualiza os contadores da GUI seguindo o XML."""
    global pet_is_active, pokemon_attacks, last_pet_time, last_attack_time, fishing_is_active
    
    # Só atualiza se a automação estiver ativa
    if fishing_is_active:
        # Atualiza contador de carinho
        if pet_is_active and pet_coordinates and last_pet_time > 0:
            pet_remaining = max(0, 100 - (time.time() - last_pet_time))
            pet_label.config(text=f"Carinho em: {int(pet_remaining)}s")
        else:
            pet_label.config(text="Carinho: Desativado")
        
        # Atualiza contador de ataques
        if pokemon_attacks and last_attack_time > 0:
            min_cooldown = min(attack['cooldown'] for attack in pokemon_attacks.values())
            attack_remaining = max(0, min_cooldown - (time.time() - last_attack_time))
            attack_label.config(text=f"Ataque em: {int(attack_remaining)}s")
        else:
            attack_label.config(text="Ataque: Desativado")
    
    # SEMPRE agenda próxima atualização, independente do estado
    # Isso garante que o contador continue funcionando mesmo durante timeouts
    root.after(1000, lambda: update_counters(root, pet_label, attack_label))

# --- Fase 4: Controle de Estado ---

def create_control_window():
    """Cria e exibe a janela de controle seguindo o padrão do rachar_egg.py."""
    global fishing_is_active, last_pet_time, last_attack_time, after_id_fishing, after_id_pet, after_id_attack
    
    root = tk.Tk()
    root.title("Controle de Pesca Automática")
    
    # Posiciona a janela no centro do quadrante inferior esquerdo
    screen_width, screen_height = get_primary_monitor_dimensions()[:2]
    window_width = 300
    window_height = 250
    
    # Calcula o centro do quadrante inferior esquerdo
    quadrant_center_x = screen_width // 4
    quadrant_center_y = screen_height * 3 // 4
    x = quadrant_center_x - (window_width // 2)
    y = quadrant_center_y - (window_height // 2)
    
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    root.attributes('-topmost', True)
    root.resizable(False, False)

    # Frame principal
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack()

    # Título
    title_label = tk.Label(main_frame, text="🎣 Pesca Automática", font=("Arial", 12, "bold"))
    title_label.pack(pady=(0, 10))

    # Frame de informações
    info_frame = tk.Frame(main_frame)
    info_frame.pack(pady=5)

    status_label = tk.Label(info_frame, text="Status: Aguardando", font=("Arial", 10))
    status_label.pack()

    direction_label = tk.Label(info_frame, text="Direção: ---", font=("Arial", 10))
    direction_label.pack()

    pet_label = tk.Label(info_frame, text="Carinho: Desativado", font=("Arial", 10))
    pet_label.pack()

    attack_label = tk.Label(info_frame, text="Ataque: Desativado", font=("Arial", 10))
    attack_label.pack()

    # Frame de botões
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    start_button = tk.Button(
        buttons_frame, 
        text="▶️ Começar", 
        bg="#27ae60", 
        fg="white",
        command=lambda: start_fishing(),
        width=10
    )
    start_button.pack(side=tk.LEFT, padx=5)
    
    stop_button = tk.Button(
        buttons_frame, 
        text="⏹️ Parar", 
        bg="#e74c3c", 
        fg="white",
        command=lambda: stop_fishing(root),
        width=10,
        state="disabled"
    )
    stop_button.pack(side=tk.LEFT, padx=5)

    def start_fishing():
        """Inicia a automação de pesca."""
        global fishing_is_active, last_pet_time, last_attack_time
        fishing_is_active = True
        last_pet_time = time.time()
        last_attack_time = time.time()
        
        status_label.config(text="Status: Executando")
        start_button.config(state="disabled")
        stop_button.config(state="normal")
        
        # Inicia as threads
        start_fishing_action()
        monitor_screen_and_react(root, 'exclamacao-pesca-sem-fundo.png', direction_label)
        pet_action_loop(root)
        pokemon_attack_loop(root)
        update_counters(root, pet_label, attack_label)

    def stop_fishing(root):
        """Para a automação de pesca."""
        global fishing_is_active, after_id_fishing, after_id_pet, after_id_attack, last_pet_time, last_attack_time
        fishing_is_active = False
        
        # Cancela todos os timers
        if after_id_fishing:
            root.after_cancel(after_id_fishing)
            after_id_fishing = None
        if after_id_pet:
            root.after_cancel(after_id_pet)
            after_id_pet = None
        if after_id_attack:
            root.after_cancel(after_id_attack)
            after_id_attack = None
        
        # Zera os contadores
        last_pet_time = 0
        last_attack_time = 0
        
        # Atualiza a interface
        status_label.config(text="Status: Parado")
        direction_label.config(text="Direção: ---")
        pet_label.config(text="Carinho: Desativado")
        attack_label.config(text="Ataque: Desativado")
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        
        print("Automação interrompida pelo usuário.")
    
    root.mainloop()

def main():
    """Função principal que executa todas as fases do XML."""
    # Carrega os dados dos Pokémon salvos
    load_pokemon_data()

    parent_root = create_centered_parent_window()

    try:
        # Fase 1: Configuração Inicial
        if not configure_pokemon_attacks(parent_root):
            return
        if not configure_pet_coordinates(parent_root):
            return
        if not configure_fishing_key(parent_root):
            return
        if not configure_exclamation_region(parent_root):
            return
        if not configure_fishing_click(parent_root):
            return
        
        parent_root.destroy()
        print("Configurações salvas. A janela de controle está pronta.")
        
        # Fase 2: Execução
        create_control_window()
        
    except Exception as e:
        print(f"Erro na execução: {e}")
        parent_root.destroy()
    
if __name__ == "__main__":
    main()