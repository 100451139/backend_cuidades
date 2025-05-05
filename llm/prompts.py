GENERAR_TITULO_PROMPT = """
Actúa como un generador de títulos. Dado el siguiente mensaje, devuelve únicamente un título breve, claro y directo, sin explicaciones ni frases adicionales.

Mensaje: {mensaje}

Título:
"""

CLASIFICAR_MENSAJE_PROMPT = """
Clasifica el siguiente mensaje en una de dos categorías:

- "Evento" si contiene fecha, hora o lugar para una actividad específica a la que puedan asistir los ciudadanos. El mensaje debe ser en futuro o hablar de una fecha posterior, si no no es un evento.
- "Anuncio" si solo comunica información general y no es un evento. Si el mensaje está escrito en pasado clasificalo como "Anuncio".

Devuelve **solo** la palabra "Evento" o "Anuncio", **sin repetir ni añadir texto adicional**.

Mensaje:
{mensaje}

Respuesta:
"""

HORARIO_PROMPT = """Extrae el horario del evento del siguiente mensaje.

Si hay un horario (como "de 10 a 14h", "17:30", "9:00 a 13:00"), devuélvelo tal cual.

Si **no hay ningún horario claro**, devuelve exactamente: **"Horario no especificado"**

Mensaje:
{mensaje}

Horario:
"""

FECHA_PROMPT = """Extrae las fechas del siguiente mensaje. Usa formato dd/mm/yyyy.

Si hay un rango, usa el formato dd/mm/yyyy-dd/mm/yyyy.

Devuelve unícamente las fechas del mensaje.

Si no hay ninguna fecha clara, devuelve exactamente: **"Fechas no especificadas"**

Mensaje:
{mensaje}

Fechas:
"""

EXTRAER_DESCRIPCION_PROMPT = """Extrae una descripción breve y clara del siguiente mensaje.

La descripción debe explicar de qué trata el evento o anuncio, quién lo organiza, o qué tipo de actividad se menciona.

⚠️ No incluyas en la descripción fechas ni horarios. Esa información ya se procesa por separado.

Devuelve solo una frase o pequeño párrafo con la información esencial del contenido, sin mencionar días ni horas.

Mensaje:
{mensaje}

Descripción:
"""

EXTRAER_LOCALIZACION_PROMPT = """Extrae la localización principal del siguiente mensaje.

La localización puede ser una plaza, calle, centro cultural, edificio o cualquier otro lugar físico donde se realiza el evento.

Si se mencionan varios lugares, devuelve el más relevante o donde se desarrolla la actividad principal.

Si no se menciona ningún lugar o el lugar no queda claro, devuelve exactamente: "Localización no especificada".

Mensaje:
{mensaje}

Localización:
"""

EXTRAER_TEMATICA_PROMPT = """Analiza el siguiente mensaje y selecciona la temática más adecuada entre las siguientes opciones:

- Cultura y ocio
- Infraestructura y obras públicas
- Servicios y administración local
- Politica
- Deporte 
- Salud
- Educación

Mensaje:
{mensaje}

Devuelve únicamente una de las opciones anteriores, sin añadir explicación ni repetir el mensaje.

Temática:
"""