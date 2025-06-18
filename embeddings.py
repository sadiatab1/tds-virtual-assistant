# embedding.py

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Lazy-load model
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model

# Load embeddings from file only when needed
def load_embeddings(path="embeddings.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Generate embedding for user input
def embed_text(text):
    model = get_model()
    return model.encode([text])[0]

# Find the closest match
def get_top_match(query_embedding, data):
    similarities = [
        cosine_similarity([query_embedding], [d["embedding"]])[0][0] for d in data
    ]
    top_index = np.argmax(similarities)
    top_entry = data[top_index]
    return top_entry["text"], float(similarities[top_index]), top_entry.get("links", [])
