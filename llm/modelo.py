from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from huggingface_hub import login
from dotenv import load_dotenv
import os

def cargar_modelo():
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

