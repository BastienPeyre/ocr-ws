import requests
import time
import os
import logging
from django.conf import settings
from .models import Document, OCRResult

logger = logging.getLogger(__name__)


class OCRService:
    """Service pour interagir avec l'API externe d'OCR"""
    
    @staticmethod
    def process_document(document):
        """
        Traite un document via l'API OCR externe
        
        Args:
            document (Document): L'instance du modèle Document à traiter
            
        Returns:
            dict: Résultat de l'OCR avec les clés 'text' et 'confidence'
        """
        try:
            start_time = time.time()
            
            # URL et clé API depuis les paramètres
            api_url = settings.OCR_API_URL
            api_key = settings.OCR_API_KEY
            
            # Prépare les headers pour l'authentification
            headers = {
                'Authorization': f'Bearer {api_key}'
            }
            
            # Ouvre le fichier
            with open(document.file.path, 'rb') as f:
                # Prépare les données
                files = {'file': (os.path.basename(document.file.name), f)}
                
                # Appel à l'API externe
                logger.info(f"Envoi du document {document.id} à l'API OCR")
                response = requests.post(api_url, headers=headers, files=files)
                
                # Vérifie la réponse
                response.raise_for_status()
                
                # Parse la réponse
                result = response.json()
                
            # Calcule le temps de traitement
            processing_time = time.time() - start_time
            
            # Crée ou met à jour le résultat OCR
            ocr_result, created = OCRResult.objects.update_or_create(
                document=document,
                defaults={
                    'text': result.get('text', ''),
                    'confidence': result.get('confidence', 0),
                    'processing_time': processing_time
                }
            )
            
            # Marque le document comme traité
            document.processed = True
            document.save()
            
            return {
                'text': ocr_result.text,
                'confidence': ocr_result.confidence
            }
            
        except requests.RequestException as e:
            logger.error(f"Erreur lors de l'appel à l'API OCR: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors du traitement OCR: {str(e)}")
            raise
