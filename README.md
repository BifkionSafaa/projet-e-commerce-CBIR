# 🛍️ E-Commerce CBIR - Recherche Visuelle de Produits

Système de recherche visuelle de produits basé sur le Content-Based Image Retrieval (CBIR) utilisant l'apprentissage profond. Les utilisateurs peuvent rechercher des produits similaires en uploadant une image.

## 📋 Table des matières

- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Structure du projet](#-structure-du-projet)
- [Guide de démarrage](#-guide-de-démarrage)
- [Architecture](#-architecture)
- [API Endpoints](#-api-endpoints)
- [Prétraitement](#-prétraitement)
- [Tests](#-tests)
- [Documentation](#-documentation)
- [Dépannage](#-dépannage)

## 🎯 Description

Ce projet implémente un système de recherche visuelle de produits pour un site e-commerce. Il utilise :

- **ResNet50** (pré-entraîné sur ImageNet) pour extraire des features visuelles
- **FAISS** pour la recherche rapide de similarité
- **PostgreSQL** pour stocker les métadonnées et features
- **Flask** (backend) et **Next.js** (frontend) pour l'interface

### Fonctionnalités principales

- 🔍 **Recherche par image** : Upload d'une image pour trouver des produits similaires
- 📝 **Recherche par texte** : Recherche dans les noms, descriptions, catégories, marques, couleurs
- 🎨 **Filtres avancés** : Filtrage par catégorie, prix, marque, couleur
- 📊 **Affichage de similarité** : Score de similarité pour chaque résultat
- 🖼️ **Interface moderne** : UI responsive avec animations et optimisations

## 🚀 Technologies

### Backend

- **Python 3.8+**
- **Flask** : Framework web
- **TensorFlow/Keras** : ResNet50 pour extraction de features
- **FAISS** : Recherche de similarité rapide
- **PostgreSQL** : Base de données
- **OpenCV, PIL** : Traitement d'images
- **pytest** : Tests unitaires

### Frontend

- **Next.js 16** : Framework React
- **TypeScript** : Typage statique
- **Tailwind CSS** : Styling
- **shadcn/ui** : Composants UI
- **Sonner** : Notifications toast

## 📦 Prérequis

- **Python 3.8+** : [python.org](https://www.python.org/downloads/)
- **Node.js 18+** : [nodejs.org](https://nodejs.org/)
- **pnpm** : `npm install -g pnpm`
- **PostgreSQL 12+** : [postgresql.org](https://www.postgresql.org/download/)

## 🔧 Installation

### 1. Cloner le repository

```bash
git clone <repository-url>
cd ecommerce-cbir-project
```

### 2. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Frontend

```bash
# À la racine du projet
pnpm install
```

### 4. Base de données

```sql
-- Dans psql ou pgAdmin
CREATE DATABASE cbir_ecommerce;
```

### 5. Configuration

```bash
cd backend
copy env.example .env  # Windows
# ou cp env.example .env  # Linux/Mac
```

Éditer `.env` et remplir les valeurs :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cbir_ecommerce
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

### 6. Initialiser la base de données

```bash
cd backend
.venv\Scripts\activate  # Windows
python scripts/init_database.py
```

### 7. Peupler la base de données

```bash
python scripts/populate_database.py
```

### 8. Extraire les features

```bash
python scripts/extract_all_features.py
```

## ▶️ Guide de démarrage

### Terminal 1 : Backend

```bash
cd backend
.venv\Scripts\activate  # Windows
python app.py
```

→ Backend accessible sur : `http://localhost:5000`

### Terminal 2 : Frontend

```bash
pnpm dev
```

→ Frontend accessible sur : `http://localhost:3000`

### Vérification

1. **Backend** : `http://localhost:5000/health` → `{"status": "ok"}`
2. **Frontend** : `http://localhost:3000` → Page d'accueil s'affiche

## 📁 Structure du projet

```
ecommerce-cbir-project/
├── backend/                 # Backend Flask
│   ├── app.py              # Application Flask principale
│   ├── config.py           # Configuration
│   ├── models/             # Modèles de données
│   │   ├── database.py     # Connexion PostgreSQL
│   │   └── product_model.py
│   ├── routes/             # Routes API
│   │   ├── products.py     # Routes produits
│   │   ├── search.py      # Routes recherche
│   │   └── upload.py      # Routes upload
│   ├── services/          # Services métier
│   │   ├── preprocessing.py      # Prétraitement images
│   │   ├── feature_extractor.py  # Extraction features ResNet50
│   │   ├── search_engine.py      # Moteur de recherche FAISS
│   │   ├── category_classifier.py
│   │   └── cache.py        # Cache mémoire
│   ├── migrations/         # Migrations SQL
│   ├── tests/              # Tests unitaires
│   └── requirements.txt
├── app/                    # Frontend Next.js
│   ├── page.tsx           # Page d'accueil
│   ├── products/[id]/     # Page détail produit
│   └── layout.tsx
├── components/            # Composants React
│   ├── products/          # Composants produits
│   ├── search/            # Composants recherche
│   └── ui/               # Composants UI (shadcn)
├── lib/                   # Utilitaires
│   ├── api.ts            # Appels API centralisés
│   └── utils.ts
├── scripts/               # Scripts utilitaires
│   ├── init_database.py
│   ├── populate_database.py
│   ├── extract_all_features.py
│   └── preprocess_dataset.py
├── dataset/               # Dataset d'images
│   ├── images/           # Images originales
│   ├── processed/       # Images prétraitées
│   └── metadata.csv      # Métadonnées produits
└── docs/                 # Documentation
```

## 🏗️ Architecture

### Diagramme de flux

```
┌─────────────┐
│   Frontend  │
│  (Next.js)  │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │
│   (Flask)   │
└──────┬──────┘
       │
       ├──► Preprocessing ──► Feature Extraction (ResNet50)
       │                           │
       │                           ▼
       │                    ┌──────────────┐
       │                    │   Features   │
       │                    │  (2048 dim)  │
       │                    └──────┬───────┘
       │                           │
       │                           ▼
       │                    ┌──────────────┐
       │                    │     FAISS    │
       │                    │  Index Search │
       │                    └──────┬───────┘
       │                           │
       └───────────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   PostgreSQL    │
         │  - products     │
         │  - features     │
         └─────────────────┘
```

### Schéma de base de données

#### Table `products`

| Colonne       | Type          | Description                   |
| ------------- | ------------- | ----------------------------- |
| `id`          | SERIAL        | Identifiant unique            |
| `name`        | VARCHAR(255)  | Nom du produit                |
| `category`    | VARCHAR(100)  | Catégorie                     |
| `price`       | DECIMAL(10,2) | Prix                          |
| `description` | TEXT          | Description                   |
| `brand`       | VARCHAR(100)  | Marque                        |
| `color`       | VARCHAR(50)   | Couleur                       |
| `image_path`  | VARCHAR(500)  | Chemin image                  |
| `image_hash`  | VARCHAR(32)   | Hash MD5 (détection doublons) |
| `created_at`  | TIMESTAMP     | Date création                 |
| `updated_at`  | TIMESTAMP     | Date mise à jour              |

#### Table `product_features`

| Colonne          | Type      | Description                    |
| ---------------- | --------- | ------------------------------ |
| `id`             | SERIAL    | Identifiant unique             |
| `product_id`     | INT       | FK vers products               |
| `feature_vector` | TEXT      | Vecteur JSON (2048 dimensions) |
| `extracted_at`   | TIMESTAMP | Date extraction                |

**Index** :

- `idx_products_category` : Recherche par catégorie
- `idx_products_price` : Recherche par prix
- `idx_products_brand` : Recherche par marque
- `idx_products_color` : Recherche par couleur
- `idx_product_features_product_id` : Jointure rapide

## 🔌 API Endpoints

### Health Check

```
GET /health
```

**Réponse** :

```json
{ "status": "ok" }
```

### Produits

#### Récupérer des produits aléatoires

```
GET /api/products/random?count=8
```

**Paramètres** :

- `count` (int, optionnel) : Nombre de produits (défaut: 8, max: 50)

**Réponse** :

```json
[
  {
    "id": 1,
    "name": "AirPods Pro",
    "category": "electronique",
    "price": 249.99,
    "description": "...",
    "brand": "Apple",
    "color": "Blanc",
    "image_path": "electronique/airpods_01.jpg"
  }
]
```

#### Récupérer un produit par ID

```
GET /api/products/{id}
```

**Réponse** :

```json
{
  "id": 1,
  "name": "AirPods Pro",
  ...
}
```

### Recherche

#### Recherche par image

```
POST /api/search/image
Content-Type: multipart/form-data

file: [image file]
top_k: 10 (optionnel, défaut: 10)
min_similarity: 0.85 (optionnel, défaut: 0.85)
category: "electronique" (optionnel)
min_price: 0 (optionnel)
max_price: 1000 (optionnel)
brand: "Apple" (optionnel)
color: "Blanc" (optionnel)
```

**Réponse** :

```json
{
  "results": [
    {
      "id": 1,
      "name": "AirPods Pro",
      "category": "electronique",
      "price": 249.99,
      "image_path": "electronique/airpods_01.jpg",
      "similarity_score": 0.98
    }
  ],
  "total": 10
}
```

#### Recherche par texte

```
GET /api/search/text?q=casque&limit=20
POST /api/search/text
Content-Type: application/json

{
  "query": "casque",
  "limit": 20
}
```

**Filtres (query params)** :

- `category` : Filtrer par catégorie
- `min_price`, `max_price` : Filtrer par prix
- `brand` : Filtrer par marque
- `color` : Filtrer par couleur

**Réponse** :

```json
{
  "results": [
    {
      "id": 5,
      "name": "Casque Bluetooth",
      "category": "electronique",
      "price": 79.99,
      ...
    }
  ],
  "total": 3
}
```

### Upload

```
POST /api/upload
Content-Type: multipart/form-data

file: [image file]
```

**Réponse** :

```json
{
  "message": "File uploaded successfully",
  "filename": "image.jpg"
}
```

### Cache (Admin)

```
GET /api/cache/stats
POST /api/cache/clear
```

## 🖼️ Prétraitement

Le prétraitement des images est une étape cruciale pour améliorer la qualité des features extraites.

### Pipeline de prétraitement

1. **Validation du format** : Vérification PNG, JPG, JPEG, WebP
2. **Vérification d'intégrité** : Détection d'images corrompues
3. **Correction EXIF** : Correction de l'orientation automatique
4. **Gestion des canaux alpha** : Conversion RGBA → RGB si nécessaire
5. **Redimensionnement intelligent** : Crop intelligent (pas de padding) pour 224x224
6. **Normalisation ImageNet** : Normalisation avec moyennes ImageNet
7. **Amélioration qualité** :
   - Réduction de bruit (bilateral filter)
   - Amélioration de la netteté
   - Amélioration du contraste

### Paramètres configurables

- **Taille cible** : 224x224 (requis par ResNet50)
- **Méthode de redimensionnement** : Crop intelligent (évite les fonds uniformes)
- **Normalisation** : Moyennes ImageNet (RGB: [0.485, 0.456, 0.408], std: [0.229, 0.224, 0.225])

### Utilisation

```python
from services.preprocessing import load_and_preprocess_image, preprocess_from_bytes

# Depuis un fichier
image = load_and_preprocess_image('path/to/image.jpg')
# Shape: (224, 224, 3)

# Depuis des bytes (upload)
image = preprocess_from_bytes(image_bytes)
# Shape: (1, 224, 224, 3)
```

Voir `docs/AMELIORATION_PREPROCESSING.md` pour plus de détails.

## 🧪 Tests

### Backend

```bash
cd backend
.venv\Scripts\activate
pytest
pytest -v  # Mode verbeux
pytest tests/test_preprocessing.py  # Test spécifique
pytest --cov  # Avec couverture
```

### Frontend

```bash
pnpm lint
```

## 📚 Documentation

- **Guide d'installation** : `GUIDE_INSTALLATION.md`
- **Démarrage rapide** : `QUICK_START.md`
- **Architecture CBIR** : `docs/ARCHITECTURE_CBIR.md`
- **API** : `docs/API_EXPLANATION.md`
- **Prétraitement** : `docs/AMELIORATION_PREPROCESSING.md`

## 🐛 Dépannage

### Backend ne démarre pas

- Vérifier que PostgreSQL est démarré
- Vérifier les variables d'environnement dans `.env`
- Vérifier que l'environnement virtuel est activé

### Erreur "Failed to fetch"

- Vérifier que le backend est démarré sur `http://localhost:5000`
- Vérifier CORS dans `backend/app.py`
- Vérifier que le frontend est sur `http://localhost:3000`

### Images ne s'affichent pas

- Vérifier que les images sont dans `dataset/images/`
- Vérifier que le backend sert les images via `/dataset/images/`
- Vérifier les permissions de fichiers

### Recherche retourne 0 résultats

- Vérifier que les features sont extraites : `python scripts/extract_all_features.py`
- Vérifier que l'index FAISS est chargé
- Vérifier le seuil `min_similarity` (essayer 0.85)

Voir `docs/DEPANNAGE_FAILED_TO_FETCH.md` pour plus de solutions.

## 📝 Licence

Ce projet est un projet académique.

## 👥 Auteurs

Projet développé dans le cadre d'un cours sur le CBIR et l'apprentissage profond.

---

**Besoin d'aide ?** Consultez la documentation dans le dossier `docs/` ou ouvrez une issue.





