"""
Script de validation du dataset
Vérifie la cohérence entre metadata.csv et les images réelles
Détecte les doublons, vérifie les résolutions, génère un rapport
"""
import os
import sys
import csv
import hashlib
from pathlib import Path
from collections import defaultdict
from PIL import Image
import cv2

# Ajouter le dossier backend au path pour importer les modules
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from services.preprocessing import validate_image_format, is_image_valid

# Configuration
DATASET_DIR = Path(__file__).parent.parent / 'dataset'
IMAGES_DIR = DATASET_DIR / 'images'
PROCESSED_DIR = DATASET_DIR / 'processed'
METADATA_FILE = DATASET_DIR / 'metadata.csv'
MIN_RESOLUTION = (224, 224)  # Résolution minimale requise pour ResNet50
MIN_DIMENSION = 100  # Dimension minimale (largeur OU hauteur) pour éviter agrandissement excessif


def calculate_image_hash(image_path):
    """Calcule le hash MD5 d'une image"""
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
            hash_md5 = hashlib.md5(image_bytes).hexdigest()
        return hash_md5
    except Exception as e:
        return None


def get_image_resolution(image_path):
    """Récupère la résolution d'une image"""
    try:
        img = Image.open(image_path)
        return img.size  # (width, height)
    except Exception:
        return None


def load_metadata():
    """Charge le fichier metadata.csv"""
    metadata = {}
    if not METADATA_FILE.exists():
        print(f"[!] Fichier metadata.csv introuvable : {METADATA_FILE}")
        return metadata
    
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_path = row.get('image_path', '')
            metadata[image_path] = row
    
    return metadata


def find_all_images():
    """Trouve toutes les images dans dataset/images/"""
    images = []
    if not IMAGES_DIR.exists():
        print(f"[!] Dossier images introuvable : {IMAGES_DIR}")
        return images
    
    ALLOWED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG', '.WEBP'}
    
    for ext in ALLOWED_FORMATS:
        images.extend(IMAGES_DIR.rglob(f"*{ext.lower()}"))
        images.extend(IMAGES_DIR.rglob(f"*{ext.upper()}"))
    
    # Éliminer les doublons (Windows est case-insensitive)
    unique_images = list(set(images))
    return sorted(unique_images)


def find_processed_images():
    """Trouve toutes les images préprocessées dans dataset/processed/"""
    images = []
    if not PROCESSED_DIR.exists():
        return images
    
    ALLOWED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG', '.WEBP'}
    
    for ext in ALLOWED_FORMATS:
        images.extend(PROCESSED_DIR.rglob(f"*{ext.lower()}"))
        images.extend(PROCESSED_DIR.rglob(f"*{ext.upper()}"))
    
    unique_images = list(set(images))
    return sorted(unique_images)


def validate_dataset(check_processed=False):
    """Valide le dataset complet
    
    Args:
        check_processed: Si True, vérifie les images préprocessées au lieu des images brutes
    """
    print("=" * 60)
    print("VALIDATION DU DATASET")
    if check_processed:
        print("(Vérification des images préprocessées)")
    else:
        print("(Vérification des images brutes)")
    print("=" * 60)
    print()
    
    # 1. Charger metadata.csv
    print("[*] Chargement de metadata.csv...")
    metadata = load_metadata()
    print(f"[+] {len(metadata)} entrées trouvées dans metadata.csv")
    print()
    
    # 2. Trouver toutes les images
    if check_processed:
        print("[*] Recherche des images dans dataset/processed/...")
        all_images = find_processed_images()
        base_dir = PROCESSED_DIR
    else:
        print("[*] Recherche des images dans dataset/images/...")
        all_images = find_all_images()
        base_dir = IMAGES_DIR
    
    print(f"[+] {len(all_images)} images trouvées")
    print()
    
    # Statistiques
    stats = {
        'total_images': len(all_images),
        'total_metadata': len(metadata),
        'images_without_metadata': [],
        'metadata_without_images': [],
        'invalid_images': [],
        'images_too_small': [],
        'duplicates': defaultdict(list),
        'invalid_paths': [],
        'hash_mismatches': []
    }
    
    # 3. Vérifier chaque image
    print("[*] Validation des images...")
    image_hashes = {}
    
    for image_path in all_images:
        # Chemin relatif depuis dataset/images/ ou dataset/processed/
        try:
            relative_path = image_path.relative_to(base_dir)
            relative_path_str = str(relative_path).replace('\\', '/')
        except Exception:
            stats['invalid_paths'].append(str(image_path))
            continue
        
        # Vérifier si l'image est dans metadata.csv
        if relative_path_str not in metadata:
            stats['images_without_metadata'].append(relative_path_str)
        
        # Vérifier le format
        if not validate_image_format(str(image_path)):
            stats['invalid_images'].append(relative_path_str)
            continue
        
        # Vérifier l'intégrité
        if not is_image_valid(str(image_path)):
            stats['invalid_images'].append(relative_path_str)
            continue
        
        # Vérifier la résolution
        # Note: On n'affiche pas les images préprocessées à l'utilisateur, mais les images originales
        # Le prétraitement se fait uniquement pour extraire les features (ResNet50)
        # Donc on accepte toutes les images, mais on avertit si très petites (< 100x100)
        resolution = get_image_resolution(str(image_path))
        if resolution:
            width, height = resolution
            # Avertir seulement si l'image est vraiment très petite (risque de features de mauvaise qualité)
            if width < MIN_DIMENSION and height < MIN_DIMENSION:
                stats['images_too_small'].append({
                    'path': relative_path_str,
                    'resolution': f"{width}x{height}",
                    'warning': 'Image tres petite, les features extraites peuvent etre de moindre qualite'
                })
        else:
            stats['invalid_images'].append(relative_path_str)
            continue
        
        # Calculer le hash MD5
        image_hash = calculate_image_hash(str(image_path))
        if image_hash:
            # Vérifier les doublons
            if image_hash in image_hashes:
                stats['duplicates'][image_hash].append(relative_path_str)
                stats['duplicates'][image_hash].append(image_hashes[image_hash])
            else:
                image_hashes[image_hash] = relative_path_str
            
            # Vérifier la cohérence du hash avec metadata.csv
            # Note: Ne pas vérifier les hash pour les images préprocessées car elles ont été modifiées
            if not check_processed and relative_path_str in metadata:
                metadata_hash = metadata[relative_path_str].get('image_hash', '')
                if metadata_hash and metadata_hash != image_hash:
                    stats['hash_mismatches'].append({
                        'path': relative_path_str,
                        'metadata_hash': metadata_hash,
                        'actual_hash': image_hash
                    })
    
    # 4. Vérifier les entrées metadata sans images correspondantes
    print("[*] Vérification des entrées metadata...")
    for metadata_path in metadata.keys():
        if check_processed:
            full_path = PROCESSED_DIR / metadata_path
        else:
            full_path = IMAGES_DIR / metadata_path
        if not full_path.exists():
            stats['metadata_without_images'].append(metadata_path)
    
    # 5. Nettoyer les listes de doublons (enlever les doublons dans la liste)
    for hash_key in stats['duplicates']:
        stats['duplicates'][hash_key] = list(set(stats['duplicates'][hash_key]))
    
    # 6. Générer le rapport
    print()
    print("=" * 60)
    print("RAPPORT DE VALIDATION")
    print("=" * 60)
    print()
    
    print(f"[*] STATISTIQUES GENERALES")
    print(f"   Total d'images trouvées : {stats['total_images']}")
    print(f"   Total d'entrées metadata : {stats['total_metadata']}")
    print()
    
    # Images sans metadata
    if stats['images_without_metadata']:
        print(f"[!] IMAGES SANS METADATA ({len(stats['images_without_metadata'])}):")
        for path in stats['images_without_metadata'][:10]:  # Afficher max 10
            print(f"   - {path}")
        if len(stats['images_without_metadata']) > 10:
            print(f"   ... et {len(stats['images_without_metadata']) - 10} autres")
        print()
    else:
        print("[+] Toutes les images ont une entree dans metadata.csv")
        print()
    
    # Metadata sans images
    if stats['metadata_without_images']:
        print(f"[!] ENTREES METADATA SANS IMAGES ({len(stats['metadata_without_images'])}):")
        for path in stats['metadata_without_images'][:10]:
            print(f"   - {path}")
        if len(stats['metadata_without_images']) > 10:
            print(f"   ... et {len(stats['metadata_without_images']) - 10} autres")
        print()
    else:
        print("[+] Toutes les entrees metadata ont une image correspondante")
        print()
    
    # Images invalides
    if stats['invalid_images']:
        print(f"[X] IMAGES INVALIDES ({len(stats['invalid_images'])}):")
        for path in stats['invalid_images'][:10]:
            print(f"   - {path}")
        if len(stats['invalid_images']) > 10:
            print(f"   ... et {len(stats['invalid_images']) - 10} autres")
        print()
    else:
        print("[+] Toutes les images sont valides")
        print()
    
    # Images très petites (avertissement seulement, pas de rejet)
    if stats['images_too_small']:
        print(f"[!] AVERTISSEMENT: Images tres petites (< {MIN_DIMENSION}x{MIN_DIMENSION}) ({len(stats['images_too_small'])}):")
        print(f"   Ces images seront affichees telles quelles a l'utilisateur.")
        print(f"   Le pretraitement pourra les gerer, mais les features extraites peuvent etre de moindre qualite.")
        print()
        for item in stats['images_too_small'][:10]:
            print(f"   - {item['path']} : {item['resolution']}")
        if len(stats['images_too_small']) > 10:
            print(f"   ... et {len(stats['images_too_small']) - 10} autres")
        print()
    else:
        print(f"[+] Toutes les images ont une dimension >= {MIN_DIMENSION} pixels")
        print()
    
    # Doublons
    if stats['duplicates']:
        print(f"[!] IMAGES DOUBLONS ({len(stats['duplicates'])} groupes):")
        for hash_key, paths in list(stats['duplicates'].items())[:5]:
            print(f"   Hash {hash_key[:8]}... :")
            for path in set(paths):
                print(f"      - {path}")
        if len(stats['duplicates']) > 5:
            print(f"   ... et {len(stats['duplicates']) - 5} autres groupes de doublons")
        print()
    else:
        print("[+] Aucun doublon detecte")
        print()
    
    # Hash mismatch
    if stats['hash_mismatches']:
        print(f"[!] HASH INCOHERENTS ({len(stats['hash_mismatches'])}):")
        for item in stats['hash_mismatches'][:5]:
            print(f"   - {item['path']}")
            print(f"     Metadata hash: {item['metadata_hash']}")
            print(f"     Actual hash:   {item['actual_hash']}")
        if len(stats['hash_mismatches']) > 5:
            print(f"   ... et {len(stats['hash_mismatches']) - 5} autres")
        print()
    else:
        print("[+] Tous les hash MD5 sont coherents")
        print()
    
    # Chemins invalides
    if stats['invalid_paths']:
        print(f"[!] CHEMINS INVALIDES ({len(stats['invalid_paths'])}):")
        for path in stats['invalid_paths'][:5]:
            print(f"   - {path}")
        print()
    
    # Résumé final
    print("=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    total_issues = (
        len(stats['images_without_metadata']) +
        len(stats['metadata_without_images']) +
        len(stats['invalid_images']) +
        len(stats['images_too_small']) +
        len(stats['duplicates']) +
        len(stats['hash_mismatches'])
    )
    
    if total_issues == 0:
        print("[+] DATASET VALIDE : Aucun probleme detecte !")
        return True
    else:
        print(f"[!] {total_issues} probleme(s) detecte(s)")
        print()
        print("[*] RECOMMANDATIONS:")
        if stats['images_without_metadata']:
            print("   - Exécuter scripts/generate_metadata.py pour ajouter les images manquantes")
        if stats['metadata_without_images']:
            print("   - Supprimer ou corriger les entrées metadata sans images")
        if stats['invalid_images'] or stats['images_too_small']:
            print("   - Supprimer ou remplacer les images invalides/trop petites")
        if stats['duplicates']:
            print("   - Supprimer les images en double (garder une seule version)")
        if stats['hash_mismatches']:
            print("   - Régénérer metadata.csv pour corriger les hash")
        return False


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Valide le dataset')
    parser.add_argument('--processed', action='store_true',
                        help='Vérifier les images préprocessées au lieu des images brutes')
    args = parser.parse_args()
    
    try:
        is_valid = validate_dataset(check_processed=args.processed)
        sys.exit(0 if is_valid else 1)
    except KeyboardInterrupt:
        print("\n[!] Interruption par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Erreur lors de la validation : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

