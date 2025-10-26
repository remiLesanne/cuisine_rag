import json 
from haystack.schema import Document
from sentence_transformers import SentenceTransformer
import pickle


with open('data/recettes.json', 'r',encoding="utf-8") as f:
    recettes = json.load(f)

docs = []
for r in recettes:
    text = (
        f"Recette: {r['title']}\n"
        f"Ingrédients: {r['ingredients']}\n"
        f"Instructions: {r['instructions']}"
    )
    doc = Document(
    content=text,
    meta={"title": r["title"]} 
    )
    docs.append(doc)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = [embedding_model.encode(doc.content).tolist() for doc in docs]

with open("documents.pkl", "wb") as f:
    pickle.dump(docs, f)
    
with open("vectors.pkl", "wb") as f:
    pickle.dump(vectors, f)