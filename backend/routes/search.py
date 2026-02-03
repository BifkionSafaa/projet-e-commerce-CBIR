"""
Routes de recherche (texte et image) - VERSION CORRIGÉE
"""
from flask import Blueprint, jsonify, request
from services.feature_extractor_resnet50 import ResNet50FeatureExtractor
from services.search_engine_npy import SearchEngineNPY
from services.preprocessing_simple import preprocess_from_bytes_simple
from services.cache import get_cache
from models.database import get_db
import logging
import hashlib
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__)

# Initialiser les services
feature_extractor = ResNet50FeatureExtractor()
search_engine = SearchEngineNPY()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_search_index():
    """Charge l'index de recherche depuis les fichiers .npy"""
    if not search_engine.is_index_ready():
        logger.info("Chargement de l'index de recherche...")
        try:
            success = search_engine.load_features_from_npy()
            if success:
                logger.info("Index chargé avec succès")
                return True
            else:
                logger.error("Échec du chargement de l'index")
                return False
        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}")
            return False
    return True


@search_bp.route('/image', methods=['POST'])
def search_image():
    """
    Recherche par image (CBIR) - VERSION CORRIGÉE
    """
    try:
        # 1. Vérifier l'image
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid format. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # 2. Vérifier la taille
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE or file_size == 0:
            return jsonify({'error': 'Invalid file size'}), 400
        
        # 3. Lire les bytes
        file_bytes = file.read()
        image_hash = hashlib.md5(file_bytes).hexdigest()
        
        # 4. Récupérer les paramètres
        top_k = min(request.args.get('top_k', 10, type=int), 50)
        # Par défaut: min_similarity = 0.5 (50%) pour n'afficher que les résultats vraiment similaires
        min_similarity = request.args.get('min_similarity', 0.5, type=float)
        search_method = request.args.get('method', 'cosine', type=str)
        
        # Filtres avancés
        filter_category = request.args.get('category', None)
        filter_min_price = request.args.get('min_price', None, type=float)
        filter_max_price = request.args.get('max_price', None, type=float)
        filter_brand = request.args.get('brand', None)
        filter_color = request.args.get('color', None)
        
        # 5. Vérifier le cache
        cache = get_cache()
        cache_key_data = {
            'image_hash': image_hash,
            'top_k': top_k,
            'min_similarity': min_similarity,
            'method': search_method,
            'category': filter_category,
            'min_price': filter_min_price,
            'max_price': filter_max_price,
            'brand': filter_brand,
            'color': filter_color
        }
        cache_key = cache._generate_key('search_image', **cache_key_data)
        
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            logger.info(f"Cache hit pour image {image_hash[:8]}")
            return jsonify(cached_result), 200
        
        # 6. Préprocesser l'image
        try:
            preprocessed_image = preprocess_from_bytes_simple(file_bytes)
        except Exception as e:
            logger.error(f"Erreur preprocessing: {e}")
            return jsonify({'error': f'Preprocessing failed: {str(e)}'}), 400
        
        # 7. Vérifier que le modèle est chargé
        if not feature_extractor.is_model_loaded():
            return jsonify({'error': 'Model not available'}), 500
        
        # 8. Extraire les features (SANS normalisation)
        # cosine_similarity normalise automatiquement, donc pas besoin de normaliser avant
        try:
            query_features = feature_extractor.extract_features(
                preprocessed_image,
                normalize=False  # Pas de normalisation - cosine_similarity normalise automatiquement
            )
            logger.info(f"Features extraites : shape={query_features.shape}")
        except Exception as e:
            logger.error(f"Erreur extraction: {e}")
            return jsonify({'error': f'Feature extraction failed: {str(e)}'}), 500
        
        # 9. Charger l'index si nécessaire
        if not search_engine.is_index_ready():
            success = load_search_index()
            if not success:
                return jsonify({'error': 'Search index not available'}), 500
        
        # 10. Rechercher les produits similaires
        # Chercher beaucoup plus de résultats pour compenser le filtrage des screenshots
        # et s'assurer d'avoir assez de résultats après filtrage
        search_top_k = min(top_k * 5, 200)  # Chercher 5x plus (max 200)
        similar_products = search_engine.search_similar(
            query_features,
            top_k=search_top_k,
            min_similarity=min_similarity,
            method=search_method
        )
        
        logger.info(f"Recherche: {len(similar_products)} produits trouvés (cherché {search_top_k} avec min_similarity={min_similarity})")
        
        if len(similar_products) == 0:
            logger.warning("Aucun produit similaire trouvé par search_engine!")
            logger.warning(f"  top_k demandé: {top_k}, min_similarity: {min_similarity}")
            logger.warning("  Cela peut indiquer que min_similarity est trop élevé ou que les features ne sont pas compatibles")
        
        # 11. Récupérer les détails depuis la DB
        db = get_db()
        results = []
        skipped_count = 0
        
        # Déterminer la catégorie du top-1 résultat pour filtrer par catégorie
        top_category = None
        if len(similar_products) > 0:
            first_product_id = int(similar_products[0]['product_id'])
            first_query = "SELECT category FROM products WHERE id = %s"
            first_result = db.execute_query(first_query, (first_product_id,))
            if first_result and first_result[0]['category'] != 'test_screenshots':
                top_category = first_result[0]['category']
                logger.info(f"Catégorie du top-1 résultat: {top_category}")
        
        for item in similar_products:
            if len(results) >= top_k:
                break
            
            product_id = int(item['product_id'])
            similarity_score = float(item['similarity_score'])
            
            # Exclure automatiquement les screenshots de test
            # Si on a une catégorie du top-1, filtrer par cette catégorie pour avoir des résultats cohérents
            if top_category:
                query = """
                    SELECT id, name, category, price, description, brand, color, image_path 
                    FROM products 
                    WHERE id = %s AND category = %s AND category != 'test_screenshots'
                """
                query_params = [product_id, top_category]
            else:
                query = """
                    SELECT id, name, category, price, description, brand, color, image_path 
                    FROM products 
                    WHERE id = %s AND category != 'test_screenshots'
                """
                query_params = [product_id]
            
            # Ajouter les filtres SEULEMENT si demandés par l'utilisateur
            filter_conditions = []
            if filter_category:
                filter_conditions.append("category = %s")
                query_params.append(filter_category)
            if filter_min_price is not None:
                filter_conditions.append("price >= %s")
                query_params.append(filter_min_price)
            if filter_max_price is not None:
                filter_conditions.append("price <= %s")
                query_params.append(filter_max_price)
            if filter_brand:
                filter_conditions.append("LOWER(brand) = LOWER(%s)")
                query_params.append(filter_brand)
            if filter_color:
                filter_conditions.append("LOWER(color) = LOWER(%s)")
                query_params.append(filter_color)
            
            if filter_conditions:
                query += " AND " + " AND ".join(filter_conditions)
            
            product_data = db.execute_query(query, tuple(query_params))
            
            if product_data and len(product_data) > 0:
                product = product_data[0]
                results.append({
                    'id': product['id'],
                    'name': product['name'],
                    'category': product['category'],
                    'price': float(product['price']),
                    'description': product.get('description', ''),
                    'brand': product.get('brand'),
                    'color': product.get('color'),
                    'image_path': product['image_path'],
                    'similarity_score': similarity_score
                })
            else:
                skipped_count += 1
                logger.debug(f"Produit {product_id} non trouvé dans la DB ou exclu par filtres (similarité: {similarity_score:.4f})")
        
        if skipped_count > 0:
            logger.warning(f"{skipped_count} produits similaires ont été ignorés (non trouvés dans DB ou exclus par filtres)")
        
        # 12. Retourner les résultats
        result = {
            'results': results,
            'count': len(results),
            'query_info': {
                'filename': secure_filename(file.filename),
                'file_size': file_size,
                'top_k': top_k,
                'min_similarity': min_similarity,
                'method': search_method,
                'results_count': len(results)
            },
            'success': True
        }
        
        # Mettre en cache
        cache.set(cache_key, result, ttl=3600)
        
        logger.info(f"Recherche terminée: {len(results)} résultat(s) sur {len(similar_products)} produits similaires trouvés")
        
        if len(results) == 0 and len(similar_products) > 0:
            logger.warning(f"ATTENTION: {len(similar_products)} produits similaires trouvés mais 0 résultats retournés!")
            logger.warning("  Cela peut être dû à:")
            logger.warning("  - Les product_ids ne correspondent pas aux IDs dans la base de données")
            logger.warning("  - Tous les produits sont des screenshots (exclus)")
            logger.warning("  - Les filtres utilisateur sont trop stricts")
            logger.warning(f"  Premier product_id trouvé: {similar_products[0]['product_id'] if similar_products else 'N/A'}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Erreur recherche image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal error: {str(e)}', 'success': False}), 500


@search_bp.route('/text', methods=['GET'])
def search_text():
    """
    Recherche par texte dans les produits
    """
    try:
        # Récupérer les paramètres
        query = request.args.get('q', '').strip()
        limit = min(request.args.get('limit', 20, type=int), 100)
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        # Récupérer les filtres optionnels
        filter_category = request.args.get('category', None)
        filter_min_price = request.args.get('min_price', None, type=float)
        filter_max_price = request.args.get('max_price', None, type=float)
        filter_brand = request.args.get('brand', None)
        filter_color = request.args.get('color', None)
        
        # Construire la requête SQL
        db = get_db()
        
        # Recherche dans name, description, category, brand
        search_conditions = [
            "category != 'test_screenshots'",  # Exclure les screenshots
            "(LOWER(name) LIKE %s OR LOWER(description) LIKE %s OR LOWER(category) LIKE %s OR LOWER(brand) LIKE %s)"
        ]
        
        search_pattern = f"%{query.lower()}%"
        query_params = [search_pattern, search_pattern, search_pattern, search_pattern]
        
        # Ajouter les filtres
        if filter_category:
            search_conditions.append("category = %s")
            query_params.append(filter_category)
        if filter_min_price is not None:
            search_conditions.append("price >= %s")
            query_params.append(filter_min_price)
        if filter_max_price is not None:
            search_conditions.append("price <= %s")
            query_params.append(filter_max_price)
        if filter_brand:
            search_conditions.append("LOWER(brand) = LOWER(%s)")
            query_params.append(filter_brand)
        if filter_color:
            search_conditions.append("LOWER(color) = LOWER(%s)")
            query_params.append(filter_color)
        
        sql_query = f"""
            SELECT id, name, category, price, description, brand, color, image_path
            FROM products
            WHERE {' AND '.join(search_conditions)}
            ORDER BY 
                CASE 
                    WHEN LOWER(name) LIKE %s THEN 1
                    WHEN LOWER(category) LIKE %s THEN 2
                    WHEN LOWER(brand) LIKE %s THEN 3
                    ELSE 4
                END,
                name
            LIMIT %s
        """
        
        # Ajouter les paramètres pour le tri
        exact_pattern = f"{query.lower()}"
        query_params.extend([exact_pattern, exact_pattern, exact_pattern, limit])
        
        results_data = db.execute_query(sql_query, tuple(query_params))
        
        if not results_data:
            results_data = []
        
        # Formater les résultats
        results = []
        for row in results_data:
            results.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'price': float(row['price']),
                'description': row.get('description', ''),
                'brand': row.get('brand'),
                'color': row.get('color'),
                'image_path': row['image_path']
            })
        
        logger.info(f"Recherche texte '{query}': {len(results)} résultat(s)")
        
        return jsonify({
            'results': results,
            'count': len(results),
            'query': query,
            'success': True
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur recherche texte: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal error: {str(e)}', 'success': False}), 500


# Garder les autres routes (search_hybrid) inchangées