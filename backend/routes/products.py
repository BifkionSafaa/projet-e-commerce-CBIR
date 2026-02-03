"""
Routes pour les produits
"""
from flask import Blueprint, jsonify, request
from models.database import get_db
import logging

logger = logging.getLogger(__name__)

products_bp = Blueprint('products', __name__)


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Retourne la liste des catégories avec une image par catégorie (pour bandeau catégories).
    """
    try:
        db = get_db()
        if not db:
            logger.error("Database connection failed")
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500

        query = """
            SELECT DISTINCT ON (category) category, image_path
            FROM products
            WHERE category IS NOT NULL AND category != 'test_screenshots' AND category != ''
            ORDER BY category, id
        """
        rows = db.execute_query(query, ())

        if not rows:
            return jsonify({'categories': [], 'count': 0}), 200

        categories = [{'category': r['category'], 'image_path': r['image_path']} for r in rows]
        return jsonify({'categories': categories, 'count': len(categories)}), 200

    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des catégories'}), 500


@products_bp.route('/random', methods=['GET'])
def get_random_products():
    """
    Récupère des produits aléatoires depuis la base de données
    
    Query params:
        - count (int, default=8): Nombre de produits à retourner
    
    Returns:
        JSON avec liste de produits
    """
    try:
        # 1. Récupérer le paramètre count
        count = request.args.get('count', 8, type=int)
        
        # Limiter à 50 produits maximum pour éviter la surcharge
        if count > 50:
            count = 50
        if count < 1:
            count = 1
        
        # 2. Récupérer les produits aléatoires depuis la base de données
        db = get_db()
        
        if not db:
            logger.error("Database connection failed")
            return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
        
        query = """
            SELECT 
                id, 
                name, 
                category, 
                price, 
                description, 
                brand, 
                color, 
                image_path
            FROM products
            WHERE category != 'test_screenshots'
            ORDER BY RANDOM()
            LIMIT %s
        """
        
        products = db.execute_query(query, (count,))
        
        # Debug: logger les résultats
        logger.info(f"Products query returned: {products}")
        logger.info(f"Products type: {type(products)}, length: {len(products) if products else 0}")
        
        # Vérifier si products est None (erreur) ou une liste vide
        if products is None:
            logger.error("Query execution returned None - possible database error")
            return jsonify({'error': 'Erreur lors de la requête à la base de données'}), 500
        
        if len(products) == 0:
            logger.warning("No products found in database")
            return jsonify({'products': [], 'message': 'Aucun produit trouvé'}), 200
        
        # 3. Convertir les produits en format JSON (déjà des dict grâce à RealDictCursor)
        # Convertir Decimal en float pour JSON
        products_list = []
        for product in products:
            product_dict = dict(product)
            if product_dict.get('price') is not None:
                product_dict['price'] = float(product_dict['price'])
            products_list.append(product_dict)
        
        return jsonify({'products': products_list, 'count': len(products_list)}), 200
        
    except Exception as e:
        logger.error(f"Error fetching random products: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des produits'}), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Récupère un produit spécifique par son ID
    
    Args:
        product_id: ID du produit
    
    Returns:
        JSON avec les détails du produit
    """
    try:
        db = get_db()
        query = """
            SELECT 
                id, 
                name, 
                category, 
                price, 
                description, 
                brand, 
                color, 
                image_path,
                created_at,
                updated_at
            FROM products
            WHERE id = %s
        """
        
        result = db.execute_query(query, (product_id,))
        
        if not result or len(result) == 0:
            return jsonify({'error': 'Produit non trouvé'}), 404
        
        product = dict(result[0])
        if product.get('price') is not None:
            product['price'] = float(product['price'])
        
        return jsonify(product), 200
        
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        return jsonify({'error': 'Erreur lors de la récupération du produit'}), 500
