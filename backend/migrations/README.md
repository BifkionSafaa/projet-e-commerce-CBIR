# Migrations de Base de Données

## Structure

Ce dossier contient les scripts de migration SQL pour créer et modifier le schéma de la base de données.

## Fichiers

- `001_create_tables.sql` : Création initiale des tables `products` et `product_features`

## Schéma de la Base de Données

### Table `products`

Stocke les informations sur les produits du catalogue.

| Colonne       | Type           | Contraintes               | Description                                    |
| ------------- | -------------- | ------------------------- | ---------------------------------------------- |
| `id`          | SERIAL         | PRIMARY KEY               | Identifiant unique auto-incrémenté             |
| `name`        | VARCHAR(255)   | NOT NULL                  | Nom du produit                                 |
| `category`    | VARCHAR(100)   | NOT NULL                  | Catégorie (mode/vetements, electronique, etc.) |
| `price`       | DECIMAL(10, 2) | NOT NULL                  | Prix en euros                                  |
| `description` | TEXT           | NULL                      | Description détaillée                          |
| `brand`       | VARCHAR(100)   | NULL                      | Marque (optionnel)                             |
| `color`       | VARCHAR(50)    | NULL                      | Couleur principale (optionnel)                 |
| `image_path`  | VARCHAR(500)   | NOT NULL                  | Chemin relatif vers l'image                    |
| `image_hash`  | VARCHAR(32)    | UNIQUE, NOT NULL          | Hash MD5 de l'image (évite les doublons)       |
| `created_at`  | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP | Date de création                               |
| `updated_at`  | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP | Date de mise à jour                            |

**Index :**

- `idx_products_category` : Sur `category` (recherches par catégorie)
- `idx_products_price` : Sur `price` (recherches par prix)
- `idx_products_image_hash` : Sur `image_hash` (vérification doublons)

### Table `product_features`

Stocke les vecteurs de features extraits par ResNet50 pour la recherche par image.

| Colonne          | Type      | Contraintes               | Description                     |
| ---------------- | --------- | ------------------------- | ------------------------------- |
| `id`             | SERIAL    | PRIMARY KEY               | Identifiant unique              |
| `product_id`     | INT       | NOT NULL, FOREIGN KEY     | Référence vers `products.id`    |
| `feature_vector` | TEXT      | NOT NULL                  | Vecteur JSON de 2048 dimensions |
| `extracted_at`   | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date d'extraction               |

**Index :**

- `idx_product_features_product_id` : Sur `product_id` (jointures)

**Relation :**

- `product_features.product_id` → `products.id` (ON DELETE CASCADE)

## Utilisation

### Créer les tables

```bash
# Utiliser le script Python
python scripts/init_database.py

# Ou avec --force pour recréer les tables existantes
python scripts/init_database.py --force
```

### Exécuter manuellement le SQL

```bash
# Se connecter à PostgreSQL
psql -h localhost -U postgres -d cbir_ecommerce

# Exécuter le script
\i backend/migrations/001_create_tables.sql
```

## Notes

- Le `feature_vector` est stocké en TEXT JSON (format: `[0.123, 0.456, ..., 0.789]`)
- L'extension `pgvector` peut être utilisée plus tard pour optimiser les recherches de similarité
- Le `image_hash` est UNIQUE pour éviter les doublons lors de l'insertion
