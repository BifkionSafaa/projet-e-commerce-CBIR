"""
Efface toutes les features de la base de données
Utile avant de réextraire avec un nouveau modèle/preprocessing
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / '.env')

from models.database import get_db

def clear_all_features():
    """Efface toutes les features de la base de données"""
    print("=" * 80)
    print("EFFACEMENT DE TOUTES LES FEATURES")
    print("=" * 80)
    print()
    
    db = get_db()
    
    # Compter les features existantes
    count_query = "SELECT COUNT(*) as count FROM product_features"
    result = db.execute_query(count_query, ())
    count = result[0]['count'] if result else 0
    
    print(f"[INFO] Nombre de features dans la base: {count}")
    print()
    
    if count == 0:
        print("[INFO] Aucune feature a effacer")
        return True
    
    # Effacer toutes les features
    try:
        cursor = db.conn.cursor()
        delete_query = "DELETE FROM product_features"
        cursor.execute(delete_query)
        db.conn.commit()
        cursor.close()
        
        print(f"[OK] {count} features effacees avec succes")
        print()
        print("[IMPORTANT] Prochaines etapes:")
        print("  1. Preprocesser et sauvegarder les images:")
        print("     python scripts/preprocess_and_save_all_images.py --confirm")
        print("  2. Extraire les nouvelles features:")
        print("     python scripts/extract_features_from_processed.py --confirm")
        
        return True
    
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'effacement: {e}")
        db.conn.rollback()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Efface toutes les features de la base de donnees')
    parser.add_argument('--confirm', action='store_true', help='Confirmer l effacement')
    
    args = parser.parse_args()
    
    if not args.confirm:
        print("[ATTENTION] Ce script va EFFACER TOUTES les features de la base de donnees!")
        print("  Cela est necessaire avant de reextraire avec ResNet50 + preprocessing simplifie")
        print()
        print("Pour executer, ajoutez --confirm")
        sys.exit(1)
    
    try:
        clear_all_features()
    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()

