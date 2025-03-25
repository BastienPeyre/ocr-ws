# OCR-WS

API Django pour l'OCR de documents.

## Description

OCR-WS est un service web développé avec Django REST Framework qui expose une API POST pour traiter des documents et extraire leur contenu textuel via OCR. Le service agit comme un intermédiaire qui transmet les documents à une API OCR externe et normalise la réponse.

## Fonctionnalités

- Endpoint API pour l'upload de documents
- Validation des formats de fichiers
- Traitement OCR via une API externe
- Stockage des résultats en base de données
- Interface d'administration pour consulter les documents et les résultats
- API RESTful conforme aux standards
- Conteneurisation avec Docker

## Installation

### Environnement local

```bash
# Cloner le dépôt
git clone https://github.com/BastienPeyre/ocr-ws.git
cd ocr-ws

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement et ajuster les variables
cp .env.example .env

# Créer les migrations et appliquer
python manage.py makemigrations
python manage.py migrate

# Lancer le serveur de développement
python manage.py runserver
```

### Avec Docker

```bash
# Cloner le dépôt
git clone https://github.com/BastienPeyre/ocr-ws.git
cd ocr-ws

# Copier le fichier d'environnement et ajuster les variables
cp .env.example .env

# Lancer avec Docker Compose
docker-compose up -d
```

## Utilisation de l'API

### Endpoint pour l'OCR

```
POST /api/ocr/
```

#### Paramètres de la requête

- `document` : Le fichier à analyser (PDF, PNG, JPEG, etc.)

#### Exemple de requête avec cURL

```bash
curl -X POST -F "document=@chemin/vers/le/document.pdf" http://localhost:8000/api/ocr/
```

#### Exemple de réponse

```json
{
  "status": "success",
  "data": {
    "text": "Contenu extrait du document",
    "confidence": 0.95
  }
}
```

## Configuration

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
# Configuration Django
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration API OCR
OCR_API_URL=https://example.com/api/ocr
OCR_API_KEY=your_api_key_here
```

## Tests

Pour exécuter les tests unitaires :

```bash
python manage.py test
```

## Déploiement

Le projet inclut un Dockerfile et un fichier docker-compose.yml pour faciliter le déploiement en production.

## Licence

Ce projet est sous licence MIT.
