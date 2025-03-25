from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import tempfile
from .models import Document, OCRResult


class OCRApiTests(TestCase):
    """Tests pour l'API OCR"""
    
    def setUp(self):
        """Configuration des tests"""
        self.client = APIClient()
        self.url = reverse('ocr_api')
        
        # Création d'un fichier test
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.temp_file.write(b'dummy content')
        self.temp_file.close()
    
    def tearDown(self):
        """Nettoyage après les tests"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('ocr_api.services.OCRService.process_document')
    def test_ocr_api_success(self, mock_process):
        """Test d'un appel API réussi"""
        # Configuration du mock
        mock_process.return_value = {
            'text': 'Exemple de texte reconnu',
            'confidence': 0.95
        }
        
        # Préparation du fichier
        with open(self.temp_file.name, 'rb') as file:
            image = SimpleUploadedFile(
                name='test.png',
                content=file.read(),
                content_type='image/png'
            )
        
        # Appel à l'API
        response = self.client.post(self.url, {'document': image}, format='multipart')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['text'], 'Exemple de texte reconnu')
        self.assertEqual(response.data['data']['confidence'], 0.95)
        
        # Vérification que le modèle a été créé
        self.assertEqual(Document.objects.count(), 1)
        
        # Vérification que le document a été marqué comme traité
        document = Document.objects.first()
        self.assertTrue(document.processed)
        
        # Vérification que le mock a été appelé
        mock_process.assert_called_once()
    
    def test_ocr_api_invalid_file(self):
        """Test avec un fichier invalide"""
        # Fichier avec une extension non supportée
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'dummy content',
            content_type='text/plain'
        )
        
        # Appel à l'API
        response = self.client.post(self.url, {'document': invalid_file}, format='multipart')
        
        # Vérifications
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('document', response.data['error'])
        
        # Vérification qu'aucun modèle n'a été créé
        self.assertEqual(Document.objects.count(), 0)
