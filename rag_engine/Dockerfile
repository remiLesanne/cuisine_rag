# === Dockerfile pour le moteur RAG ===

# 1️⃣ Image de base
FROM python:3.11-slim

# 2️⃣ Définir le répertoire de travail
WORKDIR /app

# 3️⃣ Copier les dépendances
COPY requirements.txt .

# 4️⃣ Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copier le code du moteur
COPY . .

# 6️⃣ Définir la commande par défaut (optionnelle pour tests)
CMD ["python", "search_qdrant.py"]
