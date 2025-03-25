from rest_framework import serializers
from .models import Document, OCRResult


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Document"""
    class Meta:
        model = Document
        fields = ['id', 'file', 'upload_date', 'processed']
        read_only_fields = ['id', 'upload_date', 'processed']


class OCRResultSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle OCRResult"""
    class Meta:
        model = OCRResult
        fields = ['id', 'document', 'text', 'confidence', 'processing_time', 'date_processed']
        read_only_fields = ['id', 'date_processed']


class OCRRequestSerializer(serializers.Serializer):
    """Serializer pour la requête d'OCR"""
    document = serializers.FileField()
    
    def validate_document(self, value):
        """Valide que le document est d'un format accepté"""
        # Liste des extensions acceptées
        valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp']
        
        # Récupère l'extension du fichier
        ext = value.name.split('.')[-1].lower()
        
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Format de fichier non supporté. Formats acceptés : {', '.join(valid_extensions)}"
            )
        
        # Vérifie la taille du fichier (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Le document ne doit pas dépasser 10 Mo.")
            
        return value


class OCRResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse d'OCR"""
    status = serializers.CharField()
    data = serializers.JSONField(required=False)
    error = serializers.CharField(required=False)
