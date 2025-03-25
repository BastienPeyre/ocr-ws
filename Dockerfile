# Image Python de base
FROM python:3.10-slim

# Définition du répertoire de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Installation des dépendances système pour python-magic
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Création des répertoires media et static
RUN mkdir -p /app/media /app/staticfiles

# Exposition du port
EXPOSE 8000

# Commande pour les migrations et le démarrage du serveur
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn ocr_ws.wsgi:application --bind 0.0.0.0:8000
