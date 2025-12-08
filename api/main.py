import sys
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

# Add the project root to sys.path to import rag_engine
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from rag_engine import RagEngine

app = FastAPI(title="Cuisine RAG API")

# Initialize RAG Engine
try:
    rag_engine = RagEngine()
except Exception as e:
    print(f"Error initializing RagEngine: {e}")
    rag_engine = None

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class SearchRequest(BaseModel):
    query: str
    limit: int = 3

class SearchResult(BaseModel):
    score: float
    title: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(static_dir, "index.html"), "r") as f:
        return f.read()

@app.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    if not rag_engine:
        return []
    results = rag_engine.search(request.query, request.limit)
    return results

@app.get("/health")
async def health():
    return {"status": "ok", "rag_engine": "connected" if rag_engine else "disconnected"}
