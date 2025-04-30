
def consultar_llm(model, tokenizer, prompt_base, mensaje, tokens = 20):
    print("⏳ Consultando LLM...")

    prompt = prompt_base.format(mensaje=mensaje)

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = inputs.to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=tokens,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=False
    )

    num_tokens_prompt = inputs['input_ids'].shape[1]

    output_tokens = outputs[0][num_tokens_prompt:]
    respuesta = tokenizer.decode(output_tokens, skip_special_tokens=True).strip()

    return respuesta
