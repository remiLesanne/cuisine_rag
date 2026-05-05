import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from dataclasses import dataclass, field 
from qdrant_client.models import VectorParams, Distance
import pickle


@dataclass
class Document:
    content: str
    meta: dict = field(default_factory=dict)


load_dotenv()  # Charger les variables d'environnement depuis le fichier .env
#debug
print("QDRANT_PORT lu depuis .env :", os.getenv("QDRANT_PORT"))

#pour .pkl
BASE_DIR = os.path.dirname(__file__)
DOCS_PATH = os.path.join(BASE_DIR, "documents.pkl")
VECTORS_PATH = os.path.join(BASE_DIR, "vectors.pkl")
#pour Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

#debug
print("QDRANT_PORT =", os.getenv("QDRANT_PORT"))
print("QDRANT_HOST =", os.getenv("QDRANT_HOST"))
print("COLLECTION_NAME =", os.getenv("QDRANT_COLLECTION"))
print("EMBEDDING_MODEL =", os.getenv("EMBEDDING_MODEL"))

# Connexion à Qdrant local depuis le .env
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

client.recreate_collection( #attention bientot obsolète la méthode
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
print("Collection 'recettes' créée ✅")

with open(DOCS_PATH, "rb") as f:
    docs = pickle.load(f)

with open(VECTORS_PATH, "rb") as f:
    vectors = pickle.load(f)

print(docs[0].meta)  # doit afficher {"title": "Spaghetti bolognaise"} par ex.

points = [
    {
        "id": i,
        "vector": v,
        "payload": {
            "title": doc.meta["title"],
            "content": doc.content
        }
    }
    for i, (v, doc) in enumerate(zip(vectors, docs))
]


client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

