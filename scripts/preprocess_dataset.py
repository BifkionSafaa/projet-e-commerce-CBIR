#!/usr/bin/env python3
"""
Script de prétraitement batch pour le dataset d'images
Traite toutes les images d'un dossier et génère un rapport
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse

# Ajouter le dossier backend au path pour importer les modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image

from services.preprocessing import (
    validate_image_format,
    is_image_valid,
    load_and_preprocess_image,
    ALLOWED_FORMATS
)


def setup_logging(log_file):
    """Configure le logging pour les erreurs"""
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def find_images(directory):
    """Trouve toutes les images dans un répertoire et ses sous-répertoires"""
    images = set()  # Utiliser un set pour éviter les doublons
    directory = Path(directory)
    
    # Chercher seulement les extensions en minuscules (Windows est insensible à la casse)
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        found = list(directory.rglob(f"*{ext}"))
        images.update(found)
        # Chercher aussi en majuscules pour être sûr
        found_upper = list(directory.rglob(f"*{ext.upper()}"))
        images.update(found_upper)
    
    return sorted(list(images))


def get_image_stats(image_path):
    """Récupère les statistiques d'une image"""
    try:
        img = cv2.imread(str(image_path))
        if img is not None:
            h, w = img.shape[:2]
            return {
                'width': w,
                'height': h,
                'channels': img.shape[2] if len(img.shape) > 2 else 1,
                'size_bytes': os.path.getsize(image_path)
            }
    except Exception:
        pass
    return None


def preprocess_dataset(
    input_dir,
    output_dir,
    target_size=(224, 224),
    apply_equalization=False,
    apply_augmentation=False
):
    """
    Prétraite toutes les images d'un dataset
    
    Args:
        input_dir: Dossier contenant les images brutes
        output_dir: Dossier où sauvegarder les images préprocessées
        target_size: Taille cible (height, width)
        apply_equalization: Appliquer histogram equalization
        apply_augmentation: Appliquer augmentation de données
    
    Returns:
        dict: Statistiques du prétraitement
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Créer le dossier de sortie
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Configuration du logging
    log_file = output_dir / "preprocessing_errors.log"
    logger = setup_logging(log_file)
    
    # Trouver toutes les images
    print(f"[*] Recherche d'images dans {input_dir}...")
    image_paths = find_images(input_dir)
    
    if not image_paths:
        print(f"[!] Aucune image trouvee dans {input_dir}")
        return None
    
    print(f"[+] {len(image_paths)} images trouvees\n")
    
    # Statistiques
    stats = {
        'total_images': len(image_paths),
        'processed': 0,
        'errors': 0,
        'skipped': 0,
        'formats': defaultdict(int),
        'sizes': [],
        'errors_list': [],
        'start_time': datetime.now().isoformat(),
        'end_time': None,
        'duration_seconds': None
    }
    
    # Traiter chaque image
    print(f"[*] Pretraitement en cours...\n")
    
    for image_path in tqdm(image_paths, desc="Prétraitement", unit="image"):
        try:
            # 1. Valider le format
            if not validate_image_format(str(image_path)):
                stats['skipped'] += 1
                logger.warning(f"Format non supporté : {image_path}")
                continue
            
            # 2. Vérifier l'intégrité
            if not is_image_valid(str(image_path)):
                stats['errors'] += 1
                stats['errors_list'].append({
                    'file': str(image_path),
                    'error': 'Image corrompue ou invalide'
                })
                logger.error(f"Image corrompue : {image_path}")
                continue
            
            # 3. Récupérer les statistiques
            img_stats = get_image_stats(image_path)
            if img_stats:
                stats['sizes'].append(img_stats)
                ext = image_path.suffix.lower()
                stats['formats'][ext] += 1
            
            # 4. Prétraiter l'image
            processed = load_and_preprocess_image(
                str(image_path),
                target_size=target_size,
                apply_equalization=apply_equalization,
                apply_augmentation=apply_augmentation
            )
            
            if processed is None:
                stats['errors'] += 1
                stats['errors_list'].append({
                    'file': str(image_path),
                    'error': 'Échec du prétraitement'
                })
                logger.error(f"Échec du prétraitement : {image_path}")
                continue
            
            # 5. Sauvegarder l'image préprocessée
            # Conserver la structure de dossiers relative
            relative_path = image_path.relative_to(input_dir)
            output_path = output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convertir de (1, 224, 224, 3) float32 [0-1] à (224, 224, 3) uint8 [0-255]
            img_to_save = processed[0]  # Retirer dimension batch
            img_to_save = (img_to_save * 255).astype(np.uint8)
            img_to_save = cv2.cvtColor(img_to_save, cv2.COLOR_RGB2BGR)  # RGB -> BGR pour cv2.imwrite
            
            # Sauvegarder
            cv2.imwrite(str(output_path), img_to_save)
            
            stats['processed'] += 1
            
        except Exception as e:
            stats['errors'] += 1
            stats['errors_list'].append({
                'file': str(image_path),
                'error': str(e)
            })
            logger.error(f"Erreur avec {image_path}: {e}")
    
    # Finaliser les statistiques
    stats['end_time'] = datetime.now().isoformat()
    start = datetime.fromisoformat(stats['start_time'])
    end = datetime.fromisoformat(stats['end_time'])
    stats['duration_seconds'] = (end - start).total_seconds()
    
    # Calculer la taille moyenne
    if stats['sizes']:
        avg_width = sum(s['width'] for s in stats['sizes']) / len(stats['sizes'])
        avg_height = sum(s['height'] for s in stats['sizes']) / len(stats['sizes'])
        stats['average_size'] = {
            'width': int(avg_width),
            'height': int(avg_height)
        }
    else:
        stats['average_size'] = None
    
    # Convertir defaultdict en dict pour JSON
    stats['formats'] = dict(stats['formats'])
    
    return stats


def print_report(stats):
    """Affiche un rapport des statistiques"""
    if not stats:
        return
    
    print("\n" + "="*60)
    print("=" * 50)
    print("RAPPORT DE PRETRAITEMENT")
    print("=" * 50)
    print("="*60)
    
    print(f"\n[*] Statistiques generales :")
    print(f"   Total d'images : {stats['total_images']}")
    print(f"   [+] Traitees : {stats['processed']}")
    print(f"   [!] Erreurs : {stats['errors']}")
    print(f"   [-] Ignorees : {stats['skipped']}")
    
    if stats['duration_seconds']:
        duration = stats['duration_seconds']
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"\n[*] Duree : {minutes}m {seconds}s")
        if stats['processed'] > 0:
            avg_time = duration / stats['processed'] * 1000  # en ms
            print(f"   Temps moyen par image : {avg_time:.2f} ms")
    
    if stats['average_size']:
        print(f"\n[*] Taille moyenne (originale) :")
        print(f"   {stats['average_size']['width']}x{stats['average_size']['height']} pixels")
    
    if stats['formats']:
        print(f"\n[*] Formats detectes :")
        for fmt, count in sorted(stats['formats'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {fmt}: {count} images")
    
    if stats['errors_list']:
        print(f"\n⚠️  Erreurs ({len(stats['errors_list'])}):")
        for error in stats['errors_list'][:10]:  # Afficher les 10 premières
            print(f"   - {Path(error['file']).name}: {error['error']}")
        if len(stats['errors_list']) > 10:
            print(f"   ... et {len(stats['errors_list']) - 10} autres (voir le log)")
    
    print("\n" + "="*60)


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Prétraite un dataset d'images en batch"
    )
    parser.add_argument(
        '--input',
        type=str,
        default='dataset/images',
        help='Dossier contenant les images brutes (défaut: dataset/images)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dataset/processed',
        help='Dossier de sortie pour les images préprocessées (défaut: dataset/processed)'
    )
    parser.add_argument(
        '--size',
        type=int,
        nargs=2,
        default=[224, 224],
        metavar=('HEIGHT', 'WIDTH'),
        help='Taille cible des images (défaut: 224 224)'
    )
    parser.add_argument(
        '--equalization',
        action='store_true',
        help='Appliquer histogram equalization'
    )
    parser.add_argument(
        '--augmentation',
        action='store_true',
        help='Appliquer augmentation de données'
    )
    
    args = parser.parse_args()
    
    # Vérifier que le dossier d'entrée existe
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"[!] Erreur : Le dossier {input_dir} n'existe pas")
        print(f"[*] Creez le dossier et ajoutez-y vos images")
        return 1
    
    # Prétraiter le dataset
    stats = preprocess_dataset(
        input_dir=input_dir,
        output_dir=args.output,
        target_size=tuple(args.size),
        apply_equalization=args.equalization,
        apply_augmentation=args.augmentation
    )
    
    if stats is None:
        return 1
    
    # Afficher le rapport
    print_report(stats)
    
    # Sauvegarder le rapport JSON
    output_dir = Path(args.output)
    report_file = output_dir / "preprocessing_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n[*] Rapport sauvegarde : {report_file}")
    print(f"[*] Log des erreurs : {output_dir / 'preprocessing_errors.log'}")
    
    # Code de retour
    if stats['errors'] > 0:
        print(f"\n⚠️  {stats['errors']} erreurs détectées. Vérifiez le log pour plus de détails.")
        return 1
    
    print(f"\n[+] Pretraitement termine avec succes !")
    return 0


if __name__ == "__main__":
    sys.exit(main())


