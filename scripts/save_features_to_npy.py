"""
Sauvegarde les features dans un fichier .npy
Au lieu de la base de données, on utilise un fichier .npy pour plus de simplicité
"""
import sys
from pathlib import Path
import numpy as np
import json

backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / '.env')

from models.database import get_db

def save_features_to_npy():
    """Sauvegarde les features depuis la base de données vers un fichier .npy"""
    print("=" * 80)
    print("SAUVEGARDE DES FEATURES DANS UN FICHIER .NPY")
    print("=" * 80)
    print()
    
    db = get_db()
    
    # Charger les features depuis la base de données
    query = """
        SELECT pf.product_id, pf.feature_vector, p.name, p.category
        FROM product_features pf
        JOIN products p ON pf.product_id = p.id
        ORDER BY pf.product_id
    """
    
    results = db.execute_query(query, ())
    
    if not results or len(results) == 0:
        print("[ERREUR] Aucune feature trouvee dans la base de donnees")
        print("   Executez d'abord: python scripts/extract_features_from_processed.py --confirm")
        return False
    
    print(f"[OK] {len(results)} features trouvees dans la base de donnees")
    print()
    
    # Extraire les features et product_ids
    features_list = []
    product_ids = []
    products_info = []
    
    for row in results:
        product_id = row['product_id']
        feature_json = row['feature_vector']
        name = row['name']
        category = row['category']
        
        try:
            feature_vector = json.loads(feature_json)
            features_list.append(feature_vector)
            product_ids.append(product_id)
            products_info.append({
                'id': product_id,
                'name': name,
                'category': category
            })
        except json.JSONDecodeError as e:
            print(f"  [ERREUR] Erreur de parsing pour produit {product_id}: {e}")
            continue
    
    if len(features_list) == 0:
        print("[ERREUR] Aucune feature valide")
        return False
    
    # Convertir en numpy array
    features = np.array(features_list, dtype=np.float32)
    product_ids_array = np.array(product_ids, dtype=np.int32)
    
    print(f"[OK] Features converties: shape={features.shape}")
    print(f"     Dimension: {features.shape[1]} (ResNet50 = 2048)")
    print()
    
    # Créer le dossier data s'il n'existe pas
    data_dir = Path(backend_path.parent) / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Sauvegarder les features
    features_path = data_dir / 'product_features_resnet50.npy'
    np.save(features_path, features)
    print(f"[OK] Features sauvegardees: {features_path}")
    
    # Sauvegarder les product_ids
    product_ids_path = data_dir / 'product_ids.npy'
    np.save(product_ids_path, product_ids_array)
    print(f"[OK] Product IDs sauvegardes: {product_ids_path}")
    
    # Sauvegarder les infos des produits (products.json)
    import json as json_lib
    products_json_path = data_dir / 'products.json'
    with open(products_json_path, 'w', encoding='utf-8') as f:
        json_lib.dump(products_info, f, indent=2, ensure_ascii=False)
    print(f"[OK] Infos produits sauvegardees: {products_json_path}")
    
    print()
    print("=" * 80)
    print("RESUME")
    print("=" * 80)
    print(f"Total features: {len(features)}")
    print(f"Dimension: {features.shape[1]}")
    print(f"Fichiers crees:")
    print(f"  - {features_path}")
    print(f"  - {product_ids_path}")
    print(f"  - {products_json_path}")
    print()
    print("[IMPORTANT] Ces fichiers .npy sont utilises au lieu de la base de donnees")
    print("   Le search_engine charge depuis ces fichiers")
    
    return True

if __name__ == "__main__":
    try:
        save_features_to_npy()
    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()

