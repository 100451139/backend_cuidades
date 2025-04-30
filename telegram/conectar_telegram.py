from dotenv import load_dotenv
import asyncio
from telethon import TelegramClient, events
import os
import sqlite3
from threading import Thread
from llm.obtener_info import obtener_info
from functools import partial

with sqlite3.connect('ayto_session_thread.session') as conn:
    conn.execute('PRAGMA journal_mode=WAL;')

canal = 'canalaytodemo'

load_dotenv()

mensajes = []
mensajes_procesados = [
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "titulo": "Mercado de Antigüedades",
        "clasificacion": "Evento",
        "tipo": "Evento",
        "horario": "10:00 - 14:00",
        "fecha": ["2025-05-25", "2025-06-29"],
        "descripcion": "Un mercado para disfrutar de antigüedades y objetos únicos en la Plaza Mayor."
    },
    {
        "id": "987f6543-e21a-34c5-b678-123456789abc",
        "titulo": "Concierto de Verano",
        "clasificacion": "Anuncio",
        "tipo": "Anuncio",
        "horario": "19:00 - 22:00",
        "fecha": ["2025-07-15"],
        "descripcion": "Concierto al aire libre con artistas locales en el Parque Central."
    }
]

api_id = int(os.getenv('API_ID_TELEGRAM'))
api_hash = os.getenv('API_HASH_TELEGRAM')
bot_token = os.getenv('TOKEN_BOT')

client = TelegramClient('memory', api_id, api_hash)

global_model = None
global_tokenizer = None

@client.on(events.NewMessage(chats=canal))
async def manejar_mensaje(event, model, tokenizer):
    mensaje = event.message.message
    mensajes.append(mensaje)
    print(f"Mensaje recibido: {mensaje}")

    Thread(target=procesar_mensaje, args=(mensaje, model, tokenizer), daemon=True).start()

def procesar_mensaje(mensaje, model, tokenizer):
    global global_model, global_tokenizer
    info = obtener_info(mensaje, model, tokenizer)
    mensajes_procesados.append(info)
    print(f"Información procesada: {info}")

def obtener_info_anuncio():
    if mensajes_procesados:
        info = mensajes_procesados.pop(0)
        return info
    else:
        return None

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