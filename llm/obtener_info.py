import uuid
from .consultar_llm import consultar_llm
import ast
from .prompts import GENERAR_TITULO_PROMPT, CLASIFICAR_MENSAJE_PROMPT, HORARIO_PROMPT, FECHA_PROMPT, EXTRAER_DESCRIPCION_PROMPT, EXTRAER_LOCALIZACION_PROMPT

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
    json_data = {
        "id": str(uuid.uuid4()),
        "titulo": titulo,
        "clasificacion": clasificacion,
        "horario": horario,
        "fecha": fecha,
        "descripcion": descripcion,
        "tipo": tipo,
        "localizacion": localizacion
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
    raw = consultar_llm(model, tokenizer, HORARIO_PROMPT, mensaje, tokens=5)
    return raw.split("\n")[0].strip()

def obtener_fecha(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, FECHA_PROMPT, mensaje, tokens=10)

def extraer_descripcion(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, EXTRAER_DESCRIPCION_PROMPT, mensaje, tokens=50)

def obtener_localizacion(mensaje, model, tokenizer):
    return consultar_llm(model, tokenizer, EXTRAER_LOCALIZACION_PROMPT, mensaje, tokens=10)