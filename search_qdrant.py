from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Connexion à Qdrant
client = QdrantClient(host="localhost", port=6333)
print(client.get_collections())
#print(client.get_collection("recettes"))
print(client.count("recettes"))

# Charger le même modèle que pour les embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Exemple de requête utilisateur
query = "Je veux faire un plat avec des pâtes et du fromage, que puis-je préparer ?"
print(query)

# Transformer la requête en vecteur
query_vector = model.encode(query)
# print(query_vector)
# print("Taille du vecteur :", len(query_vector))
# print("Première dimension :", query_vector[:5])

# # Recherche dans la collection Qdrant
# search_result = client.query_points(
#     collection_name="recettes",
#     query=query_vector.tolist(),
#     limit=3
# ).points


# # Afficher les résultats
# print("Résultats de la recherche :")
# for i, r in enumerate(search_result, start=1):
#     print(f"\n--- Résultat {i} ---")
#     print("Score:", r.score)
#     print("Titre:", r.payload.get("title"))
#     print("Contenu:", r.payload.get("content")[:200], "...")  # Affiche les 200 premiers caractères

queries = [
    "Je veux un plat avec des pommes de terre et de la crème",
    "Quelle recette contient du poulet et du curry ?",
    "Je cherche une recette avec des tomates et de la feta",
    "Je veux faire un dessert sucré avec des pommes"
]

for q in queries:
    print("\n\n===> Question :", q)
    qv = model.encode(q).tolist()
    res = client.query_points(collection_name="recettes", query_vector=qv, limit=3).points
    for r in res:
        print(f" - {r.payload['title']} (score={r.score:.3f})")

