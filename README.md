# Backend cuidades

Este proyecto es una interfaz para gestionar y visualizar anuncios y eventos procesados desde un backend. Utiliza React en el frontend y Flask en el backend.

## Características

- Visualización de anuncios y eventos.
- Actualización automática de datos desde el backend.
- Backend con Flask para procesar y servir datos.

## Requisitos previos

- Node.js (para el frontend)
- Python 3.8+ (para el backend)
- `pip` (gestor de paquetes de Python)

## Instalación
cd backend_cuidades
python -m venv venv

- En Windows
    .\venv\Scripts\Activate
- En macOS/Linux
    source venv/bin/activate

pip install -r requirements.txt
python app.py

## Creación del env
- Crear un archivo .env
- El contenido deberá ser algo así:

        API_HASH_TELEGRAM = 
        API_ID_TELEGRAM = 
        API_KEY = 
        TOKEN_BOT = 
        TOKEN_HUGGINGFACE = 

## Requisitos adicionales
- Claves del bot de telegram 
- Tener levantada la interfaz https://github.com/100451139/interfaz_cuidades.git
