"""
Script de peuplement de la base de données
Lit metadata.csv et insère tous les produits dans la table products
"""
import os
import sys
import csv
import json
import time
from pathlib import Path
from tqdm import tqdm

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / '.env')

from models.database import DatabaseConnection
from config import Config

# Configuration
DATASET_DIR = Path(__file__).parent.parent / 'dataset'
METADATA_FILE = DATASET_DIR / 'metadata.csv'
IMAGES_DIR = DATASET_DIR / 'images'


def validate_product_data(row):
    """
    Valide les données d'un produit
    
    Args:
        row: Dictionnaire avec les données du produit
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['name', 'category', 'price', 'image_path', 'image_hash']
    
    # Vérifier les champs requis
    for field in required_fields:
        if not row.get(field):
            return False, f"Champ requis manquant: {field}"
    
    # Vérifier le prix (doit être un nombre)
    try:
        price = float(row['price'])
        if price < 0:
            return False, f"Prix invalide: {price} (doit être >= 0)"
    except (ValueError, TypeError):
        return False, f"Prix invalide: {row['price']} (doit être un nombre)"
    
    # Vérifier le hash (doit être une chaîne de 32 caractères hexadécimaux)
    image_hash = row['image_hash'].strip()
    if len(image_hash) != 32:
        return False, f"Hash invalide: {image_hash} (doit faire 32 caractères)"
    
    # Vérifier que l'image existe
    image_path = row['image_path'].strip()
    full_image_path = IMAGES_DIR / image_path
    if not full_image_path.exists():
        return False, f"Image introuvable: {full_image_path}"
    
    return True, None


def check_product_exists(db, image_hash):
    """
    Vérifie si un produit avec ce hash existe déjà
    
    Args:
        db: Connexion à la base de données
        image_hash: Hash MD5 de l'image
    
    Returns:
        bool: True si le produit existe déjà
    """
    query = "SELECT id FROM products WHERE image_hash = %s"
    result = db.execute_query(query, (image_hash,))
    return len(result) > 0 if result else False


def insert_product(db, row):
    """
    Insère un produit dans la base de données
    
    Args:
        db: Connexion à la base de données
        row: Dictionnaire avec les données du produit
    
    Returns:
        tuple: (success, product_id, error_message)
    """
    try:
        cursor = db.conn.cursor()
        
        # Préparer les valeurs
        name = row['name'].strip()
        category = row['category'].strip()
        price = float(row['price'])
        description = row.get('description', '').strip() or None
        brand = row.get('brand', '').strip() or None
        color = row.get('color', '').strip() or None
        image_path = row['image_path'].strip()
        image_hash = row['image_hash'].strip()
        
        # Vérifier si le produit existe déjà (par hash)
        if check_product_exists(db, image_hash):
            cursor.close()
            return False, None, f"Produit déjà existant (hash: {image_hash})"
        
        # Insérer le produit
        query = """
            INSERT INTO products (name, category, price, description, brand, color, image_path, image_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(query, (name, category, price, description, brand, color, image_path, image_hash))
        product_id = cursor.fetchone()[0]
        
        db.conn.commit()
        cursor.close()
        
        return True, product_id, None
        
    except Exception as e:
        db.conn.rollback()
        return False, None, str(e)


def load_metadata():
    """
    Charge le fichier metadata.csv
    
    Returns:
        list: Liste de dictionnaires avec les données des produits
    """
    if not METADATA_FILE.exists():
        print(f"[!] Fichier metadata.csv introuvable: {METADATA_FILE}")
        return None
    
    products = []
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    
    return products


def populate_database(force=False, skip_duplicates=True):
    """
    Peuple la base de données avec les produits du metadata.csv
    
    Args:
        force: Si True, supprime tous les produits existants avant insertion
        skip_duplicates: Si True, ignore les produits déjà existants
    """
    print("=" * 60)
    print("PEUPLEMENT DE LA BASE DE DONNEES")
    print("=" * 60)
    print()
    
    # Connexion à la base de données
    db = DatabaseConnection()
    try:
        db.connect()
        print("[+] Connexion à la base de données établie")
        print()
    except Exception as e:
        print(f"[!] Erreur de connexion à la base de données: {e}")
        return
    
    # Vérifier que les tables existent
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 0:
            if force:
                print(f"[*] Suppression de {existing_count} produit(s) existant(s)...")
                cursor = db.conn.cursor()
                cursor.execute("DELETE FROM products")
                db.conn.commit()
                cursor.close()
                print("[+] Produits existants supprimés")
            else:
                print(f"[!] {existing_count} produit(s) déjà présent(s) dans la base")
                print("[!] Utilisez --force pour les supprimer avant insertion")
                print()
    except Exception as e:
        print(f"[!] Erreur lors de la vérification des tables: {e}")
        print("[!] Assurez-vous d'avoir exécuté scripts/init_database.py")
        db.disconnect()
        return
    
    # Charger metadata.csv
    print("[*] Chargement de metadata.csv...")
    products = load_metadata()
    
    if not products:
        print("[!] Aucun produit trouvé dans metadata.csv")
        db.disconnect()
        return
    
    print(f"[+] {len(products)} produit(s) trouvé(s) dans metadata.csv")
    print()
    
    # Statistiques
    stats = {
        'total': len(products),
        'valid': 0,
        'inserted': 0,
        'skipped': 0,
        'errors': 0,
        'errors_list': [],
        'start_time': time.time()
    }
    
    # Traiter chaque produit
    print("[*] Insertion des produits en cours...")
    print()
    
    for row in tqdm(products, desc="Insertion"):
        # Valider les données
        is_valid, error_msg = validate_product_data(row)
        
        if not is_valid:
            stats['errors'] += 1
            stats['errors_list'].append({
                'row': row.get('id', 'Unknown'),
                'name': row.get('name', 'Unknown'),
                'error': error_msg
            })
            continue
        
        stats['valid'] += 1
        
        # Insérer le produit
        success, product_id, error_msg = insert_product(db, row)
        
        if success:
            stats['inserted'] += 1
        else:
            if 'déjà existant' in error_msg and skip_duplicates:
                stats['skipped'] += 1
            else:
                stats['errors'] += 1
                stats['errors_list'].append({
                    'row': row.get('id', 'Unknown'),
                    'name': row.get('name', 'Unknown'),
                    'error': error_msg
                })
    
    # Calculer le temps total
    total_time = time.time() - stats['start_time']
    
    # Afficher le rapport
    print()
    print("=" * 60)
    print("RAPPORT D'INSERTION")
    print("=" * 60)
    print()
    print(f"Total de produits dans CSV: {stats['total']}")
    print(f"Produits valides: {stats['valid']}")
    print(f"Produits insérés: {stats['inserted']}")
    print(f"Produits ignorés (doublons): {stats['skipped']}")
    print(f"Erreurs: {stats['errors']}")
    print(f"Temps total: {total_time:.2f} secondes")
    print()
    
    if stats['errors'] > 0:
        print(f"[!] {stats['errors']} erreur(s) détectée(s):")
        for error in stats['errors_list'][:10]:  # Afficher max 10 erreurs
            print(f"   - Produit {error['row']} ({error.get('name', 'Unknown')}): {error['error']}")
        if len(stats['errors_list']) > 10:
            print(f"   ... et {len(stats['errors_list']) - 10} autres erreurs")
        print()
    
    # Vérifier le nombre final de produits en base
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        final_count = cursor.fetchone()[0]
        cursor.close()
        print(f"[+] Nombre total de produits en base: {final_count}")
        print()
    except Exception as e:
        print(f"[!] Erreur lors de la vérification: {e}")
    
    # Sauvegarder le rapport
    report_path = DATASET_DIR / 'population_report.json'
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total': stats['total'],
        'valid': stats['valid'],
        'inserted': stats['inserted'],
        'skipped': stats['skipped'],
        'errors': stats['errors'],
        'total_time_seconds': total_time,
        'errors_list': stats['errors_list']
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Rapport sauvegardé: {report_path}")
    print()
    
    if stats['inserted'] == stats['valid']:
        print("[+] Peuplement terminé avec succès !")
    else:
        print(f"[!] Peuplement terminé avec {stats['errors']} erreur(s)")
    
    db.disconnect()


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Peuple la base de données avec les produits du metadata.csv')
    parser.add_argument('--force', action='store_true',
                        help='Supprimer tous les produits existants avant insertion')
    parser.add_argument('--no-skip-duplicates', action='store_true',
                        help='Ne pas ignorer les doublons (afficher une erreur)')
    args = parser.parse_args()
    
    try:
        populate_database(
            force=args.force,
            skip_duplicates=not args.no_skip_duplicates
        )
    except KeyboardInterrupt:
        print("\n[!] Interruption par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Erreur lors du peuplement: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

