"""
Search Engine qui charge les features depuis un fichier .npy
Au lieu de la base de données, utilise des fichiers .npy pour plus de simplicité
"""
import numpy as np
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class SearchEngineNPY:
    """
    Moteur de recherche par similarité d'images
    Charge les features depuis des fichiers .npy au lieu de la base de données
    """
    
    def __init__(self):
        self.feature_database = None
        self.product_ids = None
        self._index_built = False
    
    def load_features_from_npy(self, features_path=None, product_ids_path=None, products_json_path=None):
        """
        Charge les features depuis des fichiers .npy
        
        Args:
            features_path: Chemin vers product_features_resnet50.npy
            product_ids_path: Chemin vers product_ids.npy (ou product_labels.npy)
            products_json_path: Chemin vers products.json (pour mapper les indices aux vrais IDs)
        
        Returns:
            bool: True si le chargement a réussi
        """
        try:
            # Chemins par défaut
            base_path = Path(__file__).parent.parent.parent / 'data'
            
            if features_path is None:
                features_path = base_path / 'product_features_resnet50.npy'
            else:
                features_path = Path(features_path)
            
            if product_ids_path is None:
                product_ids_path = base_path / 'product_ids.npy'
            else:
                product_ids_path = Path(product_ids_path)
            
            if products_json_path is None:
                products_json_path = base_path / 'products.json'
            else:
                products_json_path = Path(products_json_path)
            
            if not features_path.exists():
                logger.error(f"Fichier features non trouvé: {features_path}")
                return False
            
            if not product_ids_path.exists():
                logger.error(f"Fichier product_ids non trouvé: {product_ids_path}")
                return False
            
            # Charger les features
            self.feature_database = np.load(features_path)
            
            # Charger les product_ids
            # Si products.json existe, utiliser les vrais IDs depuis products.json (champ db_id)
            # Sinon, utiliser les indices depuis product_ids.npy
            if products_json_path.exists():
                import json
                with open(products_json_path, 'r', encoding='utf-8') as f:
                    products_info = json.load(f)
                
                # Extraire les vrais IDs de la base de données (champ db_id)
                # Si db_id n'existe pas, chercher dans la base de données par nom
                real_product_ids = []
                for i, product_info in enumerate(products_info):
                    if 'db_id' in product_info:
                        # Utiliser le vrai ID de la base de données
                        real_product_ids.append(product_info['db_id'])
                    else:
                        # Fallback: chercher dans la base de données
                        from models.database import get_db
                        db = get_db()
                        query = "SELECT id FROM products WHERE name = %s ORDER BY id LIMIT 1"
                        result = db.execute_query(query, (product_info['name'],))
                        if result:
                            real_product_ids.append(result[0]['id'])
                        else:
                            # Dernier fallback: utiliser l'index
                            real_product_ids.append(i)
                
                self.product_ids = np.array(real_product_ids)
                logger.info(f"Product IDs mappés depuis products.json: {len(real_product_ids)} produits")
            else:
                # Pas de products.json, utiliser les indices directement
                self.product_ids = np.load(product_ids_path)
            
            self._index_built = True
            
            logger.info(f"Features chargées depuis {features_path}")
            logger.info(f"Shape des features: {self.feature_database.shape}")
            logger.info(f"Nombre de produits: {len(self.product_ids)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des features: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def is_index_ready(self) -> bool:
        """Vérifie si l'index est prêt"""
        return self._index_built and self.feature_database is not None
    
    def search_similar(self, query_features: np.ndarray, top_k: int = 10, 
                      min_similarity: float = 0.0,
                      method: str = 'cosine') -> List[Dict]:
        """
        Trouve les produits similaires en utilisant cosine similarity
        
        Args:
            query_features: Vecteur de features de l'image query (shape: (1, 2048) ou (2048,))
            top_k: Nombre de résultats à retourner
            min_similarity: Score de similarité minimum (0.0 à 1.0)
            method: Méthode de comparaison ('cosine' uniquement pour l'instant)
        
        Returns:
            Liste de dictionnaires avec 'product_id' et 'similarity_score'
        """
        if not self.is_index_ready():
            logger.warning("Index non construit, impossible de rechercher")
            return []
        
        if method != 'cosine':
            raise ValueError(f"Méthode invalide: {method}. Utilisez 'cosine'")
        
        try:
            # S'assurer que query_features est de la bonne forme
            if len(query_features.shape) == 1:
                query_features = query_features.reshape(1, -1)
            elif len(query_features.shape) == 2 and query_features.shape[0] != 1:
                raise ValueError(f"Shape invalide pour query_features: {query_features.shape}")
            
            query_vector = query_features[0]  # Shape: (2048,)
            
            # Calculer la similarité cosinus
            # IMPORTANT: cosine_similarity de sklearn normalise AUTOMATIQUEMENT les vecteurs
            # Donc les features n'ont pas besoin d'être normalisées L2 avant
            # Cela fonctionne même si query_features et feature_database ne sont pas normalisés
            similarities = cosine_similarity(query_features, self.feature_database)[0]
            
            # Trier par similarité décroissante (plus élevé = plus similaire)
            top_indices = np.argsort(similarities)[::-1]
            
            # Filtrer par min_similarity et prendre top_k
            results = []
            for idx in top_indices:
                score = float(similarities[idx])
                if score >= min_similarity and len(results) < top_k:
                    results.append({
                        'product_id': int(self.product_ids[idx]),
                        'similarity_score': score
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
            return []

