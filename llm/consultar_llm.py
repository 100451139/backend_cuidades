import torch

def consultar_llm(model, tokenizer, prompt_base, mensaje, tokens = 20):
    print(" Consultando LLM...")
    prompt = prompt_base.format(mensaje=mensaje)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Tokeniza el prompt y lo convierte en tensores
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Genera una respuesta utilizando el modelo
    outputs = model.generate(
        **inputs,
        max_new_tokens=tokens, 
        pad_token_id=tokenizer.eos_token_id,  
        do_sample=False  
    )

    # Extrae los tokens generados, omitiendo los tokens del prompt
    num_tokens_prompt = inputs['input_ids'].shape[1]
    output_tokens = outputs[0][num_tokens_prompt:]

    respuesta = tokenizer.decode(output_tokens, skip_special_tokens=True).strip()

    return respuesta
