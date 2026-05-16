import os
from dotenv import load_dotenv
import json 
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass, field 
import pickle
# Load environment variables from .env file
load_dotenv() 

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/recettes.json")
DOCS_PATH = os.path.join(os.path.dirname(__file__), "documents.pkl")
VECTORS_PATH = os.path.join(os.path.dirname(__file__), "vectors.pkl")
MODEL_NAME = os.getenv("EMBEDDING_MODEL")

@dataclass
class Document:
    content: str
    meta: dict = field(default_factory=dict)


with open(DATA_PATH, 'r',encoding="utf-8") as f:
    recettes = json.load(f)

docs = []
for r in recettes:
    
    ingredients_text = ", ".join(r['ingredients'])

    text = (
        f"Recette de : {r['title']}\n"
        f"Cette recette contient : {ingredients_text}\n"
        f"Preparation : {r['instructions']}"
    )
    doc = Document(
    content=text,
    meta={
        "title": r["title"],
        "ingredients": r["ingredients"],
        "instructions": r["instructions"]
    } 
    )
    docs.append(doc)

embedding_model = SentenceTransformer(MODEL_NAME)
vectors = [embedding_model.encode(doc.content).tolist() for doc in docs]

with open(DOCS_PATH, "wb") as f:
    pickle.dump(docs, f)
    
with open(VECTORS_PATH, "wb") as f:
    pickle.dump(vectors, f)