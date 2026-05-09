FROM node:20-alpine

WORKDIR /app

# On copie les fichiers de dépendances en premier pour profiter du cache Docker
COPY package*.json ./

RUN npm install

# On copie le reste des fichiers du projet
COPY . .

# Next.js utilise le port 3000 par défaut
EXPOSE 3000

# Commande pour lancer le serveur de développement
CMD ["npm", "run", "dev"]
