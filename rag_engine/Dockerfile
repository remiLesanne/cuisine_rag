# === Dockerfile pour le moteur RAG ===

# 1️⃣ Image de base
FROM python:3.11-slim

# 2️⃣ Définir le répertoire de travail
WORKDIR /app

# 3️⃣ Copier les dépendances
COPY requirements.txt .

# 4️⃣ Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

