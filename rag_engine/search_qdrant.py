import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class RagEngine:
    def __init__(self):
        load_dotenv()
        self.qdrant_host = os.getenv("QDRANT_HOST")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
        self.collection_name = os.getenv("QDRANT_COLLECTION")
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL")
        
        self.client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
        self.model = SentenceTransformer(self.embedding_model_name)

    def search(self, query: str, limit: int = 3):
        """
        Search for relevant recipes based on the query.
        """
        query_vector = self.model.encode(query).tolist()
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        results = []
        for r in search_result:
            results.append({
                "score": r.score,
                "title": r.payload.get("title"),
                "content": r.payload.get("content")
            })
        return results

if __name__ == "__main__":
    rag = RagEngine()
    queries = [
        "Je veux un plat avec des pommes de terre et de la crème",
        "Quelle recette contient du poulet et du curry ?",
        "Je cherche une recette avec des tomates et de la feta",
        "Je veux faire un dessert sucré avec des pommes"
    ]

    for q in queries:
        print("\n\n===> Question :", q)
        results = rag.search(q)
        for r in results:
            print(f" - {r['title']} (score={r['score']:.3f})")

