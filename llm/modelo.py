from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from huggingface_hub import login
from dotenv import load_dotenv
import os

def cargar_modelo():
    """
    Carga un modelo de lenguaje preentrenado desde Hugging Face y configura un generador de texto.
    Esta función realiza las siguientes tareas:
    1. Carga las variables de entorno desde un archivo .env.
    2. Obtiene el token de autenticación de Hugging Face desde las variables de entorno.
    3. Inicia sesión en Hugging Face utilizando el token proporcionado.
    4. Carga el tokenizador y el modelo preentrenado especificado.
    5. Configura un pipeline de generación de texto con parámetros predefinidos.
    Returns:
        tuple: Una tupla que contiene el modelo y el tokenizador cargados.
    """
    modelo = "meta-llama/Llama-3.2-3B-Instruct"

    load_dotenv()

    token_huggingface = os.getenv('TOKEN_HUGGINGFACE')
    login(token_huggingface)

    tokenizer = AutoTokenizer.from_pretrained(modelo, token=token_huggingface)    
    model = AutoModelForCausalLM.from_pretrained(
        modelo,
        torch_dtype=torch.float16,
        device_map="auto",
        token=token_huggingface,
    )

    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=100,
        temperature=0.2
    )
    return model, tokenizer

