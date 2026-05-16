from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import ollama

load_dotenv()

# — Config —
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION")
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", 6))  # ← 3 échanges max par défaut


# — Clients —
ollama_client = ollama.Client(OLLAMA_HOST)
qdrant_client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=int(os.getenv("QDRANT_PORT")))
embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# — Modèles Pydantic —

class Query(BaseModel):
    question: str

class Message(BaseModel):
    role: str
    content: str

class ChatQuery(BaseModel):
    question : str
    history: list[Message] = []


# — Fonction utilitaire partagée —
def vector_search(question: str) -> list:
    limit = int(os.getenv("DEFAULT_SEARCH_LIMIT", 6))
    enriched = f"Je cherche une recette qui utilise : {question}"
    vector = embedding_model.encode(enriched).tolist()
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=limit
    )
    return [
        {
            "title": r.payload["title"],
            "ingredients": r.payload["ingredients"],
            "instructions": r.payload["instructions"],
            "score": r.score
        }
        for r in results
    ]

def build_context(results: list) -> str:
    context = ""
    for r in results:
        context += (
            f"Recette : {r['title']}\n"
            f"Ingrédients : {', '.join(r['ingredients'])}\n"
            f"Instructions : {r['instructions']}\n\n"
        )
    return context

def build_prompt(question: str, context: str) -> str:
    return f"""Tu es un assistant culinaire expert en cuisine française.
L'utilisateur cherche : {question}

Voici les recettes pertinentes trouvées :
{context}
Réponds en :
1. Recommandant en priorité la recette qui correspond le mieux à TOUS les ingrédients demandés
2. Mentionnant les autres comme alternatives
3. Expliquant pourquoi chaque recette correspond ou pas
Basé UNIQUEMENT sur les recettes fournies, sans ajouter d'informations externes."""

# — Endpoints —
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    return {
        "status": "ok",
        "qdrant": str(qdrant_client.get_collections()),
        "embedding_model": os.getenv("EMBEDDING_MODEL"),
        "collection": COLLECTION_NAME
    }

@app.post("/search")
def search(query: Query):
    return vector_search(query.question)

@app.post("/ask")
def ask(query: Query):
    results = vector_search(query.question)
    context = build_context(results)
    prompt = build_prompt(query.question, context)

    def generate():
        for chunk in ollama_client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            stream=True,
        ):
            yield chunk.response

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

@app.post("/chat")
def chat(query: ChatQuery):
    # 1. Recherche vectorielle basée sur la question actuelle
    results = vector_search(query.question)
    context = build_context(results)

    # 2. Message système avec le contexte des recettes
    messages = [
        {
            "role": "system",
            "content": f"""Tu es un assistant culinaire expert en cuisine française.
            Réponds uniquement à partir des recettes fournies dans le contexte.
            Si la question ne concerne pas la cuisine ou les recettes, réponds poliment que tu ne peux aider que sur ce sujet.
            Contexte des recettes disponibles :
            {context}"""
        }
    ]

    # 3. Ajouter l'historique limité
    recent_history = query.history[-HISTORY_LIMIT:]
    for msg in recent_history:
        messages.append({"role": msg.role, "content": msg.content})

    # 4. Ajouter la question actuelle
    messages.append({"role": "user", "content": query.question})

    # 5. Stream la réponse
    def generate():
        for chunk in ollama_client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            stream=True,
        ):
            yield chunk.message.content

    return StreamingResponse(generate(), media_type="text/plain")