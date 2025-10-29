# cuisine_rag
construction d'un rag pour aider dans la préparation culinaire

## How to use

1. Start the Qdrant database with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Clean the data:
   ```bash
   python clean.py
   ```

3. Ingest the data into Qdrant:
   ```bash
   python ingest_qdrant.py
   ```

4. Search the data:
   ```bash
   python search_qdrant.py
   ```

## Explication des fichiers Python

*   **`clean.py`**: Ce script lit les recettes à partir du fichier `data/recettes.json`, les formate en objets `Document` et génère des embeddings (vecteurs numériques) pour chaque recette à l'aide d'un modèle de transformeur de phrases. Les documents et les vecteurs sont ensuite sauvegardés dans des fichiers `documents.pkl` et `vectors.pkl`.

*   **`ingest_qdrant.py`**: Ce script se connecte à la base de données Qdrant, recrée une collection nommée "recettes", puis charge les documents et les vecteurs depuis les fichiers pickle. Enfin, il insère ces données dans la collection Qdrant pour permettre la recherche sémantique.

*   **`search_qdrant.py`**: Ce script se connecte à Qdrant et utilise le même modèle de langage pour transformer des requêtes de recherche (en langage naturel) en vecteurs. Il effectue ensuite une recherche de similarité dans la collection "recettes" pour trouver les recettes les plus pertinentes par rapport à la requête et affiche les meilleurs résultats.
