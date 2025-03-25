from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .serializers import OCRRequestSerializer, OCRResponseSerializer
from .models import Document
from .services import OCRService

logger = logging.getLogger(__name__)


class OCRAPIView(APIView):
    """
    Vue pour l'endpoint de traitement OCR
    """
    
    def post(self, request, format=None):
        """
        Traite une requête POST pour l'OCR d'un document
        
        Args:
            request: Requête HTTP
            format: Format de la requête
            
        Returns:
            Response: Réponse HTTP avec le résultat du traitement OCR
        """
        # Valide la requête
        serializer = OCRRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Requête OCR invalide: {serializer.errors}")
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Récupère le fichier
            file_obj = serializer.validated_data['document']
            
            # Enregistre le document
            document = Document.objects.create(file=file_obj)
            logger.info(f"Document enregistré avec l'ID {document.id}")
            
            # Traite le document via le service OCR
            ocr_result = OCRService.process_document(document)
            
            # Prépare la réponse
            response_data = {
                'status': 'success',
                'data': ocr_result
            }
            
            # Sérialise la réponse
            response_serializer = OCRResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                logger.error(f"Erreur de sérialisation de la réponse: {response_serializer.errors}")
                return Response({
                    'status': 'error',
                    'error': 'Erreur interne lors de la sérialisation de la réponse'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.exception("Erreur lors du traitement OCR")
            return Response({
                'status': 'error',
                'error': f"Erreur lors du traitement OCR: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
