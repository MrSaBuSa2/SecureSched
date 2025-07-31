# backend/Dockerfile

FROM python:3.11-slim

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y gcc libpq-dev

# Créer un dossier d'app
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Lancer uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
