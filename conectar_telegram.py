from dotenv import load_dotenv
import asyncio
from telethon import TelegramClient, events
import os
import sqlite3
from threading import Thread
from llm.obtener_info import obtener_info
from functools import partial
from telegram.storage import guardar_mensaje

# Configuración de SQLite con modo WAL
with sqlite3.connect('ayto_session_thread.session') as conn:
    conn.execute('PRAGMA journal_mode=WAL;')

canal = 'canalaytodemo'

load_dotenv()

mensajes = []
mensajes_procesados = [
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "titulo": "La Noche de los Libros en Valdemorillo",
        "clasificacion": "Evento",
        "tipo": "Evento",
        "horario": "17:30 - 20:00",
        "fecha": ["2025-04-25"],
        "descripcion": "Valdemorillo celebra la vigésima edición de La Noche de los Libros con un pasacalles teatral 'Historias al oído' del grupo COVAL y el espectáculo de magia literaria 'La magia de la lectura' con Lorenz de Parla en la Biblioteca Municipal.",
        "localizacion": "Recorrido desde el Edificio Municipal María Giralt hasta la Plaza de la Constitución.",
        "tematica": "Cultura y ocio"
    },
    {
        "id": "987f6543-e21a-34c5-b678-123456789abc",
        "titulo": "Concierto de Verano",
        "clasificacion": "Evento",
        "tipo": "Evento",
        "horario": "19:00 - 22:00",
        "fecha": ["2025-07-15"],
        "descripcion": "Concierto al aire libre con artistas locales en el patio de La Casa de la Cultura.",
        "localizacion": "La Casa de la Cultura."
    },
    {
        "id": "987f6543-e21a-34c5-b678-123456789abd",
        "titulo": "La Casa de Cultura, Bien de interés Patrimonial",
        "clasificacion": "Anuncio",
        "tipo": "Anuncio",
        "horario": "Horario no especificado",
        "fecha": "Fecha no especificada",
        "descripcion": "El alcalde de Valdemorillo, Santiago Villena, junto con la concejal de Cultura y Turismo, Victoria Gil, han asistido al plenario de la declaración en Bien de Interés Patrimonial de la Casa de la Cultura."
    }

]

# Carga de credenciales desde .env
api_id = int(os.getenv('API_ID_TELEGRAM'))
api_hash = os.getenv('API_HASH_TELEGRAM')
bot_token = os.getenv('TOKEN_BOT')

client = TelegramClient('memory', api_id, api_hash)

global_model = None
global_tokenizer = None

# Maneja mensajes nuevos del canal
@client.on(events.NewMessage(chats=canal))
async def manejar_mensaje(event, model, tokenizer):
    mensaje = event.message.message
    mensajes.append(mensaje)
    print(f"Mensaje recibido: {mensaje}")

    # Procesa el mensaje en un hilo separado
    Thread(target=procesar_mensaje, args=(mensaje, model, tokenizer), daemon=True).start()

# Procesa el mensaje recibido
def procesar_mensaje(mensaje, model, tokenizer):
    global global_model, global_tokenizer
    info = obtener_info(mensaje, model, tokenizer)
    mensajes_procesados.append(info)
    guardar_mensaje(info) 
    print(f"Información procesada y guardada: {info}")

# Obtiene el siguiente anuncio procesado
def obtener_info_anuncio():
    if mensajes_procesados:
        info = mensajes_procesados.pop(0)
        return info
    else:
        return None

# Conecta el bot a Telegram
async def cargar_telegram(model, tokenizer):
    print("🔌 Conectando a Telegram como BOT...")
    try:      
        global global_model, global_tokenizer
        global_model = model
        global_tokenizer = tokenizer

        await client.start(bot_token=bot_token)
        print("✅ Conectado. Esperando mensajes...")
        client.add_event_handler(partial(manejar_mensaje, model=model, tokenizer=tokenizer), events.NewMessage(chats=canal))
        await client.run_until_disconnected()
    except sqlite3.OperationalError as e:
        pass