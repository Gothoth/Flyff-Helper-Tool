import tkinter as tk
from tkinter import messagebox, font
import win32api
import win32gui
import win32con
import json
import os

# Costanti dei tasti
KEYBD_CONSTS = {'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74,
                'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78}

# Variabili globali
handlers = []
primary_client_id = None
secondary_client_id = None

# Configurazione mappatura dei tasti
key_mapping = {key: key for key in KEYBD_CONSTS}

# File JSON per salvare e caricare la mappatura
KEY_MAPPING_FILE = "keymapping.json"

# Funzione per caricare la mappatura dei tasti dal file JSON
def load_key_mapping():
    global key_mapping
    if os.path.exists(KEY_MAPPING_FILE):
        try:
            with open(KEY_MAPPING_FILE, "r") as f:
                key_mapping = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading key mapping: {e}")

# Funzione per salvare la mappatura dei tasti nel file JSON
def save_key_mapping():
    try:
        with open(KEY_MAPPING_FILE, "w") as f:
            json.dump(key_mapping, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving key mapping: {e}")

# Funzione per trovare i client aperti
def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        win_name = win32gui.GetWindowText(hwnd)
        if "Insanity MMORPG (" in win_name:
            handlers.append([hwnd, win_name])

# Attacca il client
def attach_client():
    global handlers
    handlers = []
    win32gui.EnumWindows(enumHandler, None)
    client_listbox.delete(0, tk.END)
    
    if handlers:
        for i, handler in enumerate(handlers):
            client_listbox.insert(tk.END, f'{i + 1}. {handler[1]}')
    else:
        messagebox.showinfo("Info", "No clients found.")

# Seleziona il client secondario e primario
def select_client():
    global primary_client_id, secondary_client_id
    selected_index = client_listbox.curselection()
    
    if selected_index:
        secondary_client_id = handlers[selected_index[0]][0]
        secondary_client_name = handlers[selected_index[0]][1]

        if len(handlers) > 1:
            primary_index = 0 if selected_index[0] == 1 else 1
            primary_client_id = handlers[primary_index][0]
            primary_client_name = handlers[primary_index][1]
        else:
            primary_client_id = None
            primary_client_name = "None"

        update_client_labels(primary_client_name, secondary_client_name)
        messagebox.showinfo("Info", f"Secondary Client selected: {secondary_client_name}")
    else:
        messagebox.showinfo("Info", "Please select a client first.")

# Aggiorna le etichette dei client selezionati
def update_client_labels(primary_name, secondary_name):
    primary_client_label.config(text=f"Primary Client:\n{primary_name}")
    secondary_client_label.config(text=f"Secondary Client:\n{secondary_name}")

# Invia un tasto al client selezionato
def send_key(client_id, key):
    if client_id:
        win32gui.SendMessage(client_id, win32con.WM_KEYDOWN, KEYBD_CONSTS[key], 0)
        win32gui.SendMessage(client_id, win32con.WM_KEYUP, KEYBD_CONSTS[key], 0)
    else:
        messagebox.showinfo("Info", "No client selected.")

# Controlla i tasti premuti e li invia al client secondario
def check_keys():
    for key in KEYBD_CONSTS:
        if win32api.GetAsyncKeyState(KEYBD_CONSTS[key]):
            if secondary_client_id:
                send_key(secondary_client_id, key_mapping[key])
    root.after(100, check_keys)


root = tk.Tk()
root.title("Insanity MMORPG Tool")
root.geometry("480x400")  
root.configure(bg="#2E3440")
root.attributes("-topmost", True)


title_font = font.Font(family="Helvetica", size=12, weight="bold")
label_font = font.Font(family="Helvetica", size=10)
button_font = font.Font(family="Helvetica", size=9)


main_frame = tk.Frame(root, bg="#2E3440")
main_frame.pack(pady=10)


main_label = tk.Label(main_frame, text="Client Selection", font=title_font, fg="#ECEFF4", bg="#2E3440")
main_label.pack()


attach_button = tk.Button(main_frame, text="Attach Client", command=attach_client, font=button_font, bg="#4C566A", fg="#ECEFF4")
attach_button.pack(pady=5)


client_listbox = tk.Listbox(main_frame, width=50, height=4, bg="#3B4252", fg="#ECEFF4", font=label_font)
client_listbox.pack(pady=5)


select_button = tk.Button(main_frame, text="Select Client", command=select_client, font=button_font, bg="#4C566A", fg="#ECEFF4")
select_button.pack(pady=5)

# **Frame per mostrare i client selezionati**
client_frame = tk.Frame(root, bg="#2E3440")
client_frame.pack(pady=5)

# Etichette per i client selezionati
primary_client_label = tk.Label(client_frame, text="Primary Client:\nNone", font=label_font, fg="#88C0D0", bg="#2E3440")
primary_client_label.grid(row=0, column=0, padx=10)

secondary_client_label = tk.Label(client_frame, text="Secondary Client:\nNone", font=label_font, fg="#88C0D0", bg="#2E3440")
secondary_client_label.grid(row=0, column=1, padx=10)

# **Frame per la mappatura dei tasti**
key_mapping_frame = tk.Frame(root, bg="#2E3440")
key_mapping_frame.pack(pady=5)

# Titolo della sezione Key Mapping
key_mapping_label = tk.Label(key_mapping_frame, text="Key Mapping Configuration", font=title_font, fg="#ECEFF4", bg="#2E3440")
key_mapping_label.pack(pady=5)

# Mappatura dei tasti in orizzontale (3 tasti per riga) - solo F1, F2, F3
keys = ['F1', 'F2', 'F3']  # Limitato a F1, F2, F3
for i in range(0, len(keys), 3):
    row_frame = tk.Frame(key_mapping_frame, bg="#2E3440")
    row_frame.pack()

    for j in range(3):
        idx = i + j
        if idx < len(keys):
            key_label = tk.Label(row_frame, text=f"{keys[idx]} →", fg="#ECEFF4", bg="#2E3440", font=("Helvetica", 9))
            key_label.grid(row=0, column=j * 2, padx=5)

            mapped_key_var = tk.StringVar(value=key_mapping[keys[idx]])
            dropdown = tk.OptionMenu(row_frame, mapped_key_var, *KEYBD_CONSTS.keys(),
                                     command=lambda selected, orig=keys[idx]: key_mapping.update({orig: selected}))
            dropdown.config(bg="#4C566A", fg="#ECEFF4", font=("Helvetica", 9))
            dropdown.grid(row=1, column=j * 2, padx=5)


root.after(100, check_keys)


load_key_mapping()


root.mainloop()

save_key_mapping()

