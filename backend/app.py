from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_compress import Compress
from dotenv import load_dotenv
from config import Config
from routes.products import products_bp
from routes.search import search_bp, load_search_index
from routes.upload import upload_bp
import os
import logging
import json
from datetime import datetime

# Charger les variables d'environnement depuis .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Configuration du logging structuré
class StructuredFormatter(logging.Formatter):
    """Formatter pour logs structurés en JSON"""
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Ajouter exception si présente
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Ajouter extra fields si présents
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data, ensure_ascii=False)

# Configurer le handler pour les logs structurés
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

# Compression gzip des réponses
Compress(app)

# Register blueprints
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

# Servir les images depuis dataset/images
@app.route('/dataset/images/<path:filename>')
def serve_dataset_image(filename):
    """Sert les images depuis dataset/images"""
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'images')
    return send_from_directory(dataset_path, filename)

# Servir les images depuis static/product_images (pour compatibilité)
@app.route('/static/product_images/<path:filename>')
def serve_static_image(filename):
    """Sert les images depuis static/product_images"""
    static_path = os.path.join(os.path.dirname(__file__), 'static', 'product_images')
    return send_from_directory(static_path, filename)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {'status': 'ok'}, 200

@app.route('/api/cache/stats', methods=['GET'])
def cache_stats():
    """Retourne les statistiques du cache"""
    from services.cache import get_cache
    cache = get_cache()
    return jsonify(cache.get_stats()), 200

@app.route('/api/cache/clear', methods=['POST'])
def cache_clear():
    """Vide le cache (admin seulement)"""
    from services.cache import get_cache
    cache = get_cache()
    cache.clear()
    logger.info("Cache cleared via API")
    return jsonify({'message': 'Cache cleared'}), 200

# Note: L'index sera chargé automatiquement lors de la première recherche
# ou peut être chargé manuellement en appelant load_search_index()

if __name__ == '__main__':
    # Charger l'index au démarrage
    logger.info("Démarrage du serveur Flask...")
    logger.info("Chargement de l'index de recherche...")
    load_search_index()
    logger.info("Serveur prêt sur http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
