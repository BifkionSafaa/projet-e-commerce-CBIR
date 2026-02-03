# Scripts du projet

## `extract_features.py`

Script principal pour extraire les features des images avec ResNet50.

### Utilisation

```bash
# Extraire les features depuis data/product_images/
python scripts/extract_features.py
```

Le script :
- Charge les images depuis `data/product_images/`
- Utilise ResNet50 avec preprocessing simplifié
- Sauvegarde les features dans `data/product_features_resnet50.npy`

---

## `preprocess_dataset.py`

Script de prétraitement batch pour traiter toutes les images d'un dataset.

### Utilisation

```bash
# Utilisation basique (avec valeurs par défaut)
python scripts/preprocess_dataset.py

# Spécifier les dossiers d'entrée et de sortie
python scripts/preprocess_dataset.py --input dataset/images --output dataset/processed

# Avec histogram equalization
python scripts/preprocess_dataset.py --equalization

# Avec augmentation de données
python scripts/preprocess_dataset.py --augmentation

# Taille personnalisée
python scripts/preprocess_dataset.py --size 256 256
```

### Options

- `--input` : Dossier contenant les images brutes (défaut: `dataset/images`)
- `--output` : Dossier de sortie pour les images préprocessées (défaut: `dataset/processed`)
- `--size HEIGHT WIDTH` : Taille cible des images (défaut: 224 224)
- `--equalization` : Appliquer histogram equalization
- `--augmentation` : Appliquer augmentation de données

### Résultats

Le script génère :

1. **Images préprocessées** dans `dataset/processed/` (structure de dossiers conservée)
2. **Rapport JSON** : `dataset/processed/preprocessing_report.json`
3. **Log des erreurs** : `dataset/processed/preprocessing_errors.log`

### Exemple de rapport

```json
{
  "total_images": 200,
  "processed": 195,
  "errors": 5,
  "skipped": 0,
  "formats": {
    ".jpg": 150,
    ".png": 45,
    ".webp": 5
  },
  "average_size": {
    "width": 800,
    "height": 600
  },
  "duration_seconds": 45.2
}
```

---

## `validate_dataset.py`

Script de validation du dataset pour vérifier la cohérence entre `metadata.csv` et les images réelles.

### Utilisation

```bash
# Validation complète du dataset
python scripts/validate_dataset.py
```

### Vérifications effectuées

1. **Cohérence metadata ↔ images**
   - Vérifie que chaque image a une entrée dans `metadata.csv`
   - Vérifie que chaque entrée metadata a une image correspondante

2. **Détection des doublons**
   - Utilise le hash MD5 pour détecter les images identiques
   - Signale les groupes de doublons

3. **Validation des images**
   - Vérifie le format (PNG, JPG, JPEG, WebP)
   - Vérifie l'intégrité (images non corrompues)
   - Vérifie la résolution minimale (>= 224x224)

4. **Cohérence des hash MD5**
   - Compare les hash dans `metadata.csv` avec les hash calculés
   - Signale les incohérences

### Résultats

Le script affiche un rapport détaillé avec :

- Statistiques générales (nombre d'images, entrées metadata)
- Liste des problèmes détectés (images sans metadata, doublons, etc.)
- Recommandations pour corriger les problèmes

### Exemple de sortie

```
============================================================
RAPPORT DE VALIDATION
============================================================

[*] STATISTIQUES GENERALES
   Total d'images trouvées : 117
   Total d'entrées metadata : 117

[+] Toutes les images ont une entree dans metadata.csv
[+] Toutes les entrees metadata ont une image correspondante
[+] Toutes les images sont valides
[!] IMAGES TROP PETITES (< 224x224) (73): ...
[+] Aucun doublon detecte
[+] Tous les hash MD5 sont coherents
```

### Code de sortie

- `0` : Dataset valide (aucun problème)
- `1` : Problèmes détectés (voir le rapport)

---

## `extract_features.py`

Script principal pour extraire les features des images avec ResNet50.

### Utilisation

```bash
# Extraire les features depuis data/product_images/
python scripts/extract_features.py
```

### Prérequis

- Les images doivent être préprocessées dans `data/product_images/`
- TensorFlow doit être installé

### Fonctionnalités

1. **Extraction avec ResNet50**
   - Utilise ResNet50 pré-entraîné sur ImageNet
   - Preprocessing simplifié (resize + preprocess_input)
   - Features NON normalisées L2 (cosine_similarity normalise automatiquement)

2. **Sauvegarde en format .npy**
   - Sauvegarde dans `data/product_features_resnet50.npy`
   - Format NumPy pour chargement rapide

### Résultats

Le script :

1. Charge les images depuis `data/product_images/`
2. Preprocesse avec `tf.image.resize` et `preprocess_input`
3. Extrait les features avec ResNet50
4. Sauvegarde dans `data/product_features_resnet50.npy`

### Format des features

- **Dimension** : 2048 (ResNet50)
- **Normalisation** : Aucune (cosine_similarity normalise automatiquement)
- **Format** : NumPy array (.npy)

### Exemple de sortie

```
============================================================
EXTRACTING FEATURES WITH RESNET50
============================================================

 Loading product images...
 Loaded 117 images

 Preprocessing images...
  Shape after resize: (117, 224, 224, 3)

 Loading ResNet50...
 Extracting features...
117/117 [==============================] - 5s 43ms/step
 Features shape: (117, 2048)

 Features saved to data/product_features_resnet50.npy

============================================================
FEATURE EXTRACTION COMPLETE!
 Feature dimension: 2048
============================================================
```

---

## `populate_database.py`

Script de peuplement de la base de données avec les produits du `metadata.csv`.

### Utilisation

```bash
# Peuplement normal (ignore les doublons)
python scripts/populate_database.py

# Supprimer tous les produits existants avant insertion
python scripts/populate_database.py --force

# Ne pas ignorer les doublons (afficher une erreur)
python scripts/populate_database.py --no-skip-duplicates
```

### Prérequis

- La base de données doit être initialisée (Tâche 5)
- Le fichier `dataset/metadata.csv` doit exister (Tâche 4)
- Les images doivent être accessibles dans `dataset/images/`

### Fonctionnalités

1. **Validation des données**
   - Vérifie les champs requis (name, category, price, image_path, image_hash)
   - Valide le format du prix (nombre >= 0)
   - Valide le format du hash MD5 (32 caractères hexadécimaux)
   - Vérifie que les images existent

2. **Gestion des doublons**
   - Utilise `image_hash` UNIQUE pour détecter les doublons
   - Ignore les doublons par défaut (option `--no-skip-duplicates` pour afficher une erreur)

3. **Rapport d'insertion**
   - Statistiques (total, valides, insérés, ignorés, erreurs)
   - Sauvegardé dans `dataset/population_report.json`

### Résultats

Le script :

1. Lit tous les produits depuis `metadata.csv`
2. Valide chaque produit
3. Insère les produits valides dans la table `products`
4. Ignore les doublons (produits avec le même `image_hash`)

### Exemple de sortie

```
============================================================
PEUPLEMENT DE LA BASE DE DONNEES
============================================================

[+] Connexion à la base de données établie

[*] Chargement de metadata.csv...
[+] 117 produit(s) trouvé(s) dans metadata.csv

[*] Insertion des produits en cours...

Insertion: 100%|████████████| 117/117 [00:02<00:00, 45.23it/s]

============================================================
RAPPORT D'INSERTION
============================================================

Total de produits dans CSV: 117
Produits valides: 117
Produits insérés: 117
Produits ignorés (doublons): 0
Erreurs: 0
Temps total: 2.59 secondes

[+] Nombre total de produits en base: 117
[+] Rapport sauvegardé: dataset/population_report.json
[+] Peuplement terminé avec succès !
```

### Code de sortie

- `0` : Peuplement réussi
- `1` : Erreur (connexion DB, fichier CSV introuvable, etc.)
