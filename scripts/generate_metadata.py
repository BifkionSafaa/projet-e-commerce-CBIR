"""
Script pour générer automatiquement metadata.csv à partir des images du dataset
"""
import os
import hashlib
import csv
from pathlib import Path
from datetime import datetime
import random

# Configuration des prix par catégorie (en euros)
PRICE_RANGES = {
    'mode/vetements': (29.99, 199.99),
    'mode/chaussures': (49.99, 299.99),
    'mode/sacs': (39.99, 399.99),
    'electronique': (19.99, 1999.99),
    'jouets': (9.99, 149.99),
    'beaute/cosmetiques': (4.99, 89.99),
}

# Marques par catégorie
BRANDS = {
    'mode/vetements': ['Zara', 'H&M', 'Nike', 'Adidas', 'Levi\'s', 'Uniqlo', None],
    'mode/chaussures': ['Nike', 'Adidas', 'Converse', 'Vans', 'Puma', None],
    'mode/sacs': ['Nike', 'Adidas', 'Zara', 'H&M', None],
    'electronique': ['Apple', 'Samsung', 'Sony', 'Canon', 'Nikon', 'Bose', None],
    'jouets': ['Lego', 'Hasbro', 'Mattel', 'Fisher-Price', None],
    'beaute/cosmetiques': ['L\'Oréal', 'Maybelline', 'Revlon', 'MAC', None],
}

# Couleurs communes
COLORS = ['noir', 'blanc', 'rouge', 'bleu', 'vert', 'jaune', 'rose', 'gris', 'beige', 'marron', 'multicolore', None]


def calculate_image_hash(image_path):
    """Calcule le hash MD5 d'une image"""
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
            hash_md5 = hashlib.md5(image_bytes).hexdigest()
        return hash_md5
    except Exception as e:
        print(f"[!] Erreur lors du calcul du hash pour {image_path}: {e}")
        return None


def extract_category_from_path(image_path, base_dir):
    """Extrait la catégorie depuis le chemin de l'image"""
    relative_path = Path(image_path).relative_to(base_dir)
    parts = relative_path.parts
    
    # Exclure le nom du fichier (dernière partie)
    if len(parts) > 1:
        # Ex: mode/vetements/jeans_01.jpg -> mode/vetements
        # Exclure la dernière partie (nom du fichier)
        category_parts = parts[:-1]
        category = '/'.join(category_parts)
    elif len(parts) == 1:
        # Si une seule partie, c'est le nom du fichier directement dans le dossier racine
        # Prendre le parent (qui est le dossier racine)
        category = str(relative_path.parent) if relative_path.parent != Path('.') else "autre"
    else:
        category = "autre"
    
    # Normaliser les séparateurs et gérer le cas où category est vide
    category = category.replace('\\', '/')
    if not category or category == '.':
        category = "autre"
    
    return category


def generate_product_name(image_path, category):
    """Génère un nom de produit réaliste basé sur le nom du fichier et la catégorie"""
    filename = Path(image_path).stem  # Nom sans extension
    
    # Extraire des mots-clés du nom de fichier
    keywords = filename.lower().replace('_', ' ').replace('-', ' ').split()
    
    # Mapper les catégories
    category_names = {
        'mode/vetements': {
            'jeans': 'Jeans',
            'pull': 'Pull',
            'robe': 'Robe',
            't-shirt': 'T-shirt',
            'chemise': 'Chemise',
            'pantalon': 'Pantalon',
            'veste': 'Veste',
        },
        'mode/chaussures': {
            'chaussure': 'Chaussures',
            'basket': 'Baskets',
            'sneaker': 'Sneakers',
        },
        'mode/sacs': {
            'sac': 'Sac',
            'backpack': 'Sac à dos',
        },
        'electronique': {
            'telephone': 'Téléphone',
            'phone': 'Téléphone',
            'camera': 'Appareil photo',
            'casque': 'Casque audio',
            'airpods': 'AirPods',
            'ecouteurs': 'Écouteurs',
            'montre': 'Montre',
            'pc': 'Ordinateur portable',
            'laptop': 'Ordinateur portable',
        },
        'jouets': {
            'poupee': 'Poupée',
            'robot': 'Robot',
            'voiture': 'Voiture de jouet',
            'peluche': 'Peluche',
            'construction': 'Jeu de construction',
        },
        'beaute/cosmetiques': {
            'rouge': 'Rouge à lèvres',
            'mascara': 'Mascara',
            'fond': 'Fond de teint',
        },
    }
    
    # Chercher un mot-clé correspondant
    product_type = None
    for keyword in keywords:
        if category in category_names:
            for key, value in category_names[category].items():
                if key in keyword:
                    product_type = value
                    break
        if product_type:
            break
    
    # Si aucun type trouvé, utiliser le premier mot-clé en capitalisant
    if not product_type:
        product_type = keywords[0].capitalize() if keywords else "Produit"
    
    # Ajouter un qualificatif
    qualifiers = ['Classique', 'Moderne', 'Élégant', 'Sport', 'Casual', 'Premium', 'Design']
    qualifier = random.choice(qualifiers)
    
    return f"{product_type} {qualifier}"


def generate_price(category):
    """Génère un prix réaliste selon la catégorie"""
    if category in PRICE_RANGES:
        min_price, max_price = PRICE_RANGES[category]
        # Générer un prix avec 2 décimales
        price = round(random.uniform(min_price, max_price), 2)
        # Arrondir à .99 ou .49
        price = round(price) - 0.01 if random.random() > 0.5 else round(price) - 0.51
        return max(min_price, price)
    else:
        # Prix par défaut
        return round(random.uniform(19.99, 199.99), 2)


def generate_description(name, category):
    """Génère une description réaliste"""
    descriptions_templates = {
        'mode/vetements': [
            f"{name} de qualité supérieure, confortable et stylé.",
            f"{name} parfait pour toutes les occasions, design moderne et élégant.",
            f"{name} fabriqué avec des matériaux de qualité, coupe impeccable.",
        ],
        'mode/chaussures': [
            f"{name} confortables et durables, idéales pour un usage quotidien.",
            f"{name} avec un design moderne et une semelle de qualité.",
            f"{name} parfaites pour le sport et le quotidien.",
        ],
        'mode/sacs': [
            f"{name} spacieux et pratique, design élégant et moderne.",
            f"{name} fabriqué avec des matériaux résistants, parfait pour tous les jours.",
            f"{name} avec plusieurs compartiments, idéal pour transporter vos affaires.",
        ],
        'electronique': [
            f"{name} avec des fonctionnalités avancées et une qualité exceptionnelle.",
            f"{name} haute performance, design moderne et ergonomique.",
            f"{name} avec les dernières technologies, garantie constructeur incluse.",
        ],
        'jouets': [
            f"{name} éducatif et amusant, parfait pour les enfants.",
            f"{name} de qualité, sûr et durable pour des heures de jeu.",
            f"{name} avec un design attractif, idéal pour développer la créativité.",
        ],
        'beaute/cosmetiques': [
            f"{name} de qualité professionnelle, résultat parfait garanti.",
            f"{name} avec des ingrédients naturels, adapté à tous les types de peau.",
            f"{name} longue tenue, fini impeccable et naturel.",
        ],
    }
    
    if category in descriptions_templates:
        return random.choice(descriptions_templates[category])
    else:
        return f"{name} de qualité, design moderne et fonctionnel."


def generate_brand(category):
    """Génère une marque (retourne None par défaut pour remplissage manuel)"""
    # Retourner None par défaut - à remplir manuellement si nécessaire
    return None


def generate_color():
    """Génère une couleur aléatoire"""
    return random.choice(COLORS)


def find_all_images(base_dir):
    """Trouve toutes les images dans le dataset"""
    images = []
    base_path = Path(base_dir)
    
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'}
    
    for ext in allowed_extensions:
        images.extend(base_path.rglob(f"*{ext}"))
    
    # Retirer les doublons (Windows est insensible à la casse)
    unique_images = list(set(images))
    return sorted(unique_images)


def generate_metadata(input_dir, output_file):
    """Génère le fichier metadata.csv"""
    print(f"[*] Recherche d'images dans {input_dir}...")
    images = find_all_images(input_dir)
    
    if not images:
        print(f"[!] Aucune image trouvee dans {input_dir}")
        return
    
    print(f"[+] {len(images)} images trouvees\n")
    print(f"[*] Generation du metadata.csv...\n")
    
    base_dir = Path(input_dir)
    metadata = []
    
    for idx, image_path in enumerate(images, start=1):
        try:
            # Calculer le hash MD5
            image_hash = calculate_image_hash(image_path)
            if not image_hash:
                print(f"[!] Impossible de calculer le hash pour {image_path}, ignore")
                continue
            
            # Extraire la catégorie
            category = extract_category_from_path(image_path, base_dir)
            
            # Générer les métadonnées
            name = generate_product_name(image_path, category)
            price = generate_price(category)
            description = generate_description(name, category)
            brand = generate_brand(category)
            color = generate_color()
            
            # Chemin relatif depuis dataset/images/
            relative_path = image_path.relative_to(base_dir)
            image_path_str = str(relative_path).replace('\\', '/')
            
            metadata.append({
                'id': idx,
                'name': name,
                'category': category,
                'price': price,
                'description': description,
                'brand': brand if brand else '',
                'color': color if color else '',
                'image_path': image_path_str,
                'image_hash': image_hash
            })
            
            if idx % 20 == 0:
                print(f"  Traite: {idx}/{len(images)} images...")
                
        except Exception as e:
            print(f"[!] Erreur avec {image_path}: {e}")
            continue
    
    # Écrire le CSV
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = ['id', 'name', 'category', 'price', 'description', 'brand', 'color', 'image_path', 'image_hash']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata)
    
    print(f"\n[+] Metadata genere avec succes !")
    print(f"    Fichier: {output_path}")
    print(f"    Total: {len(metadata)} produits")
    print(f"    Categories: {len(set(m['category'] for m in metadata))} categories")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Genere metadata.csv depuis les images du dataset')
    parser.add_argument('--input', type=str, default='dataset/images',
                       help='Dossier contenant les images (default: dataset/images)')
    parser.add_argument('--output', type=str, default='dataset/metadata.csv',
                       help='Fichier CSV de sortie (default: dataset/metadata.csv)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[!] Erreur : Le dossier {args.input} n'existe pas")
        return
    
    generate_metadata(args.input, args.output)


if __name__ == "__main__":
    main()

