import uuid
from .consultar_llm import consultar_llm
from .prompts import GENERAR_TITULO_PROMPT, CLASIFICAR_MENSAJE_PROMPT, HORARIO_PROMPT, FECHA_PROMPT, EXTRAER_DESCRIPCION_PROMPT, EXTRAER_LOCALIZACION_PROMPT, EXTRAER_TEMATICA_PROMPT

def obtener_info(mensaje, model, tokenizer):
    titulo = generar_titulo(mensaje, model, tokenizer)
    print(f"📝 Título generado: {titulo}")

    tipo = clasificar_mensaje(mensaje, model, tokenizer)
    print(f"📝 Tipo de mensaje: {tipo}")
    
    horario = obtener_horario(mensaje, model, tokenizer)
    print(f"📝 Horario extraído: {horario}")
    
    fecha = obtener_fecha(mensaje, model, tokenizer)
    print(f"📝 Fechas extraídas: {fecha}")
    
    descripcion = extraer_descripcion(mensaje, model, tokenizer)
    print(f"📝 Descripción extraída: {descripcion}")
    
    localizacion = obtener_localizacion(mensaje, model, tokenizer)
    print(f"📝 Localización extraída: {localizacion}")
    
    tematica = obtener_tematica(mensaje, model, tokenizer)
    print(f"📝 Temática extraída: {tematica}")
    # Crear un diccionario con toda la información extraída
    json_data = {
        "id": str(uuid.uuid4()),  # Generar un ID único
        "titulo": titulo,
        "horario": horario,
        "fecha": fecha,
        "descripcion": descripcion,
        "tipo": tipo,
        "localizacion": localizacion,
        "tematica": tematica
    }
    print(f"📝 Información extraída: {json_data}")
    return json_data

def generar_titulo(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, GENERAR_TITULO_PROMPT, mensaje, tokens=30)

def clasificar_mensaje(mensaje, model, tokenizer):
    respuesta = consultar_llm(model, tokenizer, CLASIFICAR_MENSAJE_PROMPT, mensaje, tokens=1).strip()
    if respuesta not in ["Evento", "Anuncio"]:
        return "Evento"
    return respuesta

def obtener_horario(mensaje, model, tokenizer):
    raw = consultar_llm(model, tokenizer, HORARIO_PROMPT, mensaje, tokens=10)
    if "Horario no especificado" in raw or "No hay horario claro" in raw:
        return None
    return raw.split("\n")[0].strip()

def obtener_fecha(mensaje, model, tokenizer):
    if "Fechas no especificadas" in mensaje:
        return None
    return consultar_llm(model, tokenizer, FECHA_PROMPT, mensaje, tokens=27)

def extraer_descripcion(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, EXTRAER_DESCRIPCION_PROMPT, mensaje, tokens=70)

def obtener_localizacion(mensaje, model, tokenizer):
    if "Localización no especificada" in mensaje:
        return None
    return consultar_llm(model, tokenizer, EXTRAER_LOCALIZACION_PROMPT, mensaje, tokens=20)

def obtener_tematica(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, EXTRAER_TEMATICA_PROMPT, mensaje, tokens=5)