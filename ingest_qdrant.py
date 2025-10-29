from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import pickle

# Connexion à Qdrant local
client = QdrantClient(host="localhost", port=6333) #via docker 

client.recreate_collection( #attention bientot obsolète la méthode
    collection_name="recettes",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
print("Collection 'recettes' créée ✅")

with open("documents.pkl", "rb") as f:
    docs = pickle.load(f)

with open("vectors.pkl", "rb") as f:
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
    collection_name="recettes",
    points=points
)

