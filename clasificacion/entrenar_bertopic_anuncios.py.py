import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from umap import UMAP
import hdbscan
from llama_cpp import Llama
import joblib

# 1. Cargar los anuncios
df = pd.read_excel("anuncios.xlsx")
documentos = df["anuncio"].dropna().tolist()

# 2. Generar embeddings
embedding_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
embeddings = embedding_model.encode(documentos, show_progress_bar=True)

# 3. Configurar UMAP y HDBSCAN
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42)
hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom')

# 4. Cargar Llama 3
llama = Llama(
    model_path="llama-3-3b-instruct.Q4_K_M.gguf",  # tu modelo local
    n_ctx=4096,
    n_threads=4,
    n_gpu_layers=20,
)

def representador_llm(topic_docs, topic_words, topic_id):
    prompt = f"""
Eres un asistente que analiza contenido municipal. Resume el siguiente grupo de documentos en una temática general como si fuera una etiqueta para una categoría.

Palabras clave: {', '.join(topic_words[:10])}

Documentos:
{'. '.join(topic_docs[:5])}

Devuelve solo una frase muy breve (2-4 palabras), sin explicaciones.
Etiqueta:
""".strip()
    output = llama(prompt, max_tokens=25)
    return output["choices"][0]["text"].strip()

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    calculate_probabilities=True,
    verbose=True,
    representation_model=representador_llm,
)

# 6. Entrenar el modelo
topics, probs = topic_model.fit_transform(documentos)

# 7. Guardar el modelo
topic_model.save("modelo_bertopic_anuncios")
joblib.dump(embedding_model, "embedding_model_anuncios.pkl")

# 8. Exportar resultados
df["topic"] = topics
df["nombre_tema"] = df["topic"].apply(lambda x: topic_model.get_topic_info().set_index("Topic").loc[x]["Name"] if x != -1 else "Sin asignar")
df.to_csv("anuncios_con_temas.csv", index=False)

print("✅ Modelo entrenado y etiquetas generadas.")
