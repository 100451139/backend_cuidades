import json
import os

FILE_PATH = './data/mensajes.json'

if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as f:
        json.dump([], f)

def guardar_mensaje(mensaje):
    try:
        with open(FILE_PATH, 'r') as f:
            mensajes = json.load(f)
        mensajes.append(mensaje)
        with open(FILE_PATH, 'w') as f:
            json.dump(mensajes, f, indent=2)
    except Exception as e:
        print(f"Error al guardar el mensaje: {e}")

def obtener_mensajes():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f: 
            return json.load(f)
    except Exception as e:
        print(f"Error al leer los mensajes: {e}")
        return []