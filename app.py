from flask import Flask
from blueprints.config import config_bp
from blueprints.routes import main_bp
from telegram.conectar_telegram import cargar_telegram
from llm.modelo import cargar_modelo
import asyncio
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(config_bp)
app.register_blueprint(main_bp)

model_ready_event = threading.Event()
lock = threading.Lock() 

def cargar_modelo_con_evento():
    global model, tokenizer
    model, tokenizer = cargar_modelo()
    model_ready_event.set()  

def cargar_telegram_con_bloqueo():
    with lock:
        asyncio.run(cargar_telegram(model, tokenizer))

if __name__ == "__main__":
    threading.Thread(target=cargar_modelo_con_evento, daemon=True).start()
    model_ready_event.wait()
    
    model, tokenizer = cargar_modelo()
    print("📦 Model loaded:", type(model))
    print("🧪 Tokenizer loaded:", type(tokenizer))

    threading.Thread(target=cargar_telegram_con_bloqueo, daemon=True).start()
    app.run(debug=False)