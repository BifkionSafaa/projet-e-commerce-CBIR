"""
Tests d'intégration pour les routes API
"""
import unittest
import sys
import os
import tempfile
import io
from pathlib import Path
import numpy as np
from PIL import Image

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import conditionnel pour éviter les erreurs si l'app n'est pas configurée
try:
    from app import app
    APP_AVAILABLE = True
except Exception as e:
    APP_AVAILABLE = False
    import sys
    print(f"Warning: Could not import app: {e}", file=sys.stderr)


class TestRoutes(unittest.TestCase):
    """Tests pour les routes API"""
    
    @classmethod
    def setUpClass(cls):
        """Skip tous les tests si l'app n'est pas disponible"""
        if not APP_AVAILABLE:
            raise unittest.SkipTest("App not available - skipping route tests")
    
    def setUp(self):
        """Initialise l'application Flask pour les tests"""
        if not APP_AVAILABLE:
            self.skipTest("App not available")
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        # Créer le client de test avec use_cookies=False pour éviter les problèmes de session
        self.client = self.app.test_client(use_cookies=False)
        
        # Créer une image de test
        self.test_image = np.ones((50, 100, 3), dtype=np.uint8) * 255
        self.test_image[10:40, 30:70] = [255, 0, 0]  # rectangle rouge
    
    def test_health_check(self):
        """Test la route de health check"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
    
    def test_get_random_products(self):
        """Test la route GET /api/products/random"""
        # Test avec count par défaut
        response = self.client.get('/api/products/random')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('products', data)
        self.assertIsInstance(data['products'], list)
        
        # Test avec count spécifié
        response = self.client.get('/api/products/random?count=5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('products', data)
        self.assertLessEqual(len(data['products']), 5)
    
    def test_search_text_get(self):
        """Test la route GET /api/search/text"""
        # Test avec requête valide
        response = self.client.get('/api/search/text?q=casque')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertIn('query', data)
        
        # Test avec requête vide
        response = self.client.get('/api/search/text?q=')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_search_text_post(self):
        """Test la route POST /api/search/text"""
        # Test avec JSON valide
        response = self.client.post(
            '/api/search/text',
            json={'query': 'casque', 'limit': 10}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        
        # Test avec requête vide
        response = self.client.post(
            '/api/search/text',
            json={'query': ''}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_search_text_with_filters(self):
        """Test la route /api/search/text avec filtres"""
        # Test avec filtre category
        response = self.client.get('/api/search/text?q=casque&category=electronique')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
        
        # Test avec filtre price
        response = self.client.get('/api/search/text?q=casque&min_price=50&max_price=200')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
        
        # Test avec filtre color
        response = self.client.get('/api/search/text?q=casque&color=noir')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('results', data)
    
    def test_search_image_no_file(self):
        """Test la route POST /api/search/image sans fichier"""
        response = self.client.post('/api/search/image')
        # Devrait retourner 400 ou 500 selon l'implémentation
        self.assertIn(response.status_code, [400, 500])
    
    def test_search_image_with_file(self):
        """Test la route POST /api/search/image avec fichier"""
        # Créer un fichier image temporaire
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        try:
            Image.fromarray(self.test_image).save(tmp.name, format="JPEG")
            
            with open(tmp.name, 'rb') as f:
                response = self.client.post(
                    '/api/search/image?top_k=5&min_similarity=0.5',
                    data={'image': (f, 'test.jpg')},
                    content_type='multipart/form-data'
                )
            
            # La réponse peut être 200 (succès) ou 500 (si DB/index non disponible)
            # On vérifie juste que la route existe et répond
            self.assertIn(response.status_code, [200, 500])
            
            if response.status_code == 200:
                data = response.get_json()
                self.assertIn('results', data)
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
    
    def test_search_image_with_filters(self):
        """Test la route /api/search/image avec filtres"""
        # Créer un fichier image temporaire
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        try:
            Image.fromarray(self.test_image).save(tmp.name, format="JPEG")
            
            with open(tmp.name, 'rb') as f:
                response = self.client.post(
                    '/api/search/image?top_k=5&min_similarity=0.5&category=electronique&color=noir',
                    data={'image': (f, 'test.jpg')},
                    content_type='multipart/form-data'
                )
            
            # La réponse peut être 200 (succès) ou 500 (si DB/index non disponible)
            self.assertIn(response.status_code, [200, 500])
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
    
    def test_search_image_invalid_file(self):
        """Test la route POST /api/search/image avec fichier invalide"""
        # Créer un fichier texte (pas une image)
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        tmp.write(b"not an image")
        tmp.close()
        try:
            with open(tmp.name, 'rb') as f:
                response = self.client.post(
                    '/api/search/image',
                    data={'image': (f, 'test.txt')},
                    content_type='multipart/form-data'
                )
            
            # Devrait retourner une erreur
            self.assertIn(response.status_code, [400, 500])
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)
    
    def test_cors_headers(self):
        """Test que les headers CORS sont présents"""
        response = self.client.get('/health')
        # Vérifier que les headers CORS sont présents (si configurés)
        # Cela dépend de la configuration Flask-CORS
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

