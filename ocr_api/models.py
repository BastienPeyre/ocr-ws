from django.db import models
import uuid
import os


def document_path(instance, filename):
    """Génère un chemin unique pour le stockage des documents"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('documents', filename)


class Document(models.Model):
    """Modèle pour stocker les documents envoyés pour OCR"""
    file = models.FileField(upload_to=document_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Document {self.id} ({self.upload_date.strftime('%Y-%m-%d %H:%M')})"


class OCRResult(models.Model):
    """Modèle pour stocker les résultats d'OCR"""
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='ocr_result')
    text = models.TextField(blank=True)
    confidence = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(help_text="Temps de traitement en secondes", null=True, blank=True)
    date_processed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"OCR Result for Document {self.document.id}"
