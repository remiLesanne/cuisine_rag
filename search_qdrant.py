from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Connexion à Qdrant
client = QdrantClient(host="localhost", port=6333)
print(client.get_collections())
print(client.get_collection("recettes"))
print(client.count("recettes"))

# Charger le même modèle que pour les embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Exemple de requête utilisateur
query = "Je veux faire un plat avec des pâtes et du fromage, que puis-je préparer ?"
print(query)

# Transformer la requête en vecteur
query_vector = model.encode(query).tolist()
print(query_vector)
print("Taille du vecteur :", len(query_vector))
print("Première dimension :", query_vector[:5])

# Recherche dans la collection Qdrant
search_result = client.search(
    collection_name="recettes",
    query_vector=query_vector,
    limit=3  # nombre de résultats à retourner
)

# Afficher les résultats
for i, r in enumerate(search_result, start=1):
    print(f"\n--- Résultat {i} ---")
    print("Score:", r.score)
    print("Titre:", r.payload.get("title"))
