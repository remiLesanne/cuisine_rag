from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI()

client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=int(os.getenv("QDRANT_PORT")))
model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION")

class Query(BaseModel):
    question: str
    limit: int = 3

@app.post("/search")
def search(query: Query):
    vector = model.encode(query.question).tolist()
    results = client.search(          # ← remplace client.search
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=query.limit
    )
    return [
        {"title": r.payload["title"], "content": r.payload["content"], "score": r.score}
        for r in results
    ]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {
        "status": "ok",
        "qdrant": str(client.get_collections()),
        "embedding_model": os.getenv("EMBEDDING_MODEL"),
        "collection": COLLECTION_NAME
    }
