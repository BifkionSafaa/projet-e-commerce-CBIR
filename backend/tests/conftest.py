"""
Fixtures partagées pour les tests
"""
import pytest
import os
import sys
import tempfile
import numpy as np
from pathlib import Path
from PIL import Image
import io

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Configuration pour les tests
os.environ.setdefault('FLASK_ENV', 'testing')


@pytest.fixture
def sample_image():
    """Crée une image de test RGB"""
    # Image RGB simple (100x50, fond blanc + rectangle rouge)
    rgb_image = np.ones((50, 100, 3), dtype=np.uint8) * 255
    rgb_image[10:40, 30:70] = [255, 0, 0]  # rectangle rouge
    return rgb_image


@pytest.fixture
def sample_image_file(sample_image):
    """Crée un fichier image temporaire"""
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    tmp.close()
    try:
        Image.fromarray(sample_image).save(tmp.name, format="JPEG")
        yield tmp.name
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)


@pytest.fixture
def sample_image_bytes(sample_image):
    """Retourne les bytes d'une image de test"""
    buf = io.BytesIO()
    Image.fromarray(sample_image).save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def sample_features():
    """Crée des features de test (2048 dimensions pour ResNet50)"""
    np.random.seed(42)
    return np.random.rand(5, 2048).astype(np.float32)


@pytest.fixture
def flask_app():
    """Crée une instance Flask pour les tests"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(flask_app):
    """Crée un client de test Flask"""
    return flask_app.test_client()


@pytest.fixture
def mock_db():
    """Mock de la base de données pour les tests"""
    # Cette fixture peut être étendue pour simuler une DB de test
    pass



