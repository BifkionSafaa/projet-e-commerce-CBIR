# 🏗️ Architecture Détaillée du Système CBIR

## Vue d'ensemble

Le système est composé de trois couches principales :

1. **Frontend** (Next.js) : Interface utilisateur
2. **Backend** (Flask) : API REST et logique métier
3. **Base de données** (PostgreSQL) : Stockage des données

## Architecture Backend

### Services (Singleton Pattern)

#### 1. FeatureExtractor

**Responsabilité** : Extraction de features visuelles avec ResNet50

```python
from services.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()  # Singleton
features = extractor.extract_features(image)  # Shape: (2048,)
```

**Caractéristiques** :

- Modèle ResNet50 pré-entraîné sur ImageNet
- Extraction de la couche avant la classification (2048 dimensions)
- Normalisation ImageNet appliquée
- Cache du modèle en mémoire

#### 2. SearchEngine

**Responsabilité** : Recherche de similarité avec FAISS

```python
from services.search_engine import SearchEngine

engine = SearchEngine()  # Singleton
results = engine.search_similar(query_features, top_k=10)
```

**Caractéristiques** :

- Index FAISS Flat (L2 distance)
- Conversion distance → score de similarité (0-1)
- Chargement depuis la base de données au démarrage

#### 3. Preprocessing

**Responsabilité** : Prétraitement des images

```python
from services.preprocessing import load_and_preprocess_image

image = load_and_preprocess_image('path/to/image.jpg')
# Shape: (224, 224, 3), normalisé ImageNet
```

**Pipeline** :

1. Validation format
2. Vérification intégrité
3. Correction EXIF
4. Gestion alpha channel
5. Smart resize (crop)
6. Normalisation ImageNet
7. Amélioration qualité

#### 4. CategoryClassifier

**Responsabilité** : Classification de catégorie (optionnel)

```python
from services.category_classifier import CategoryClassifier

classifier = CategoryClassifier()
category = classifier.predict_category(image_features)
```

**Note** : Actuellement désactivé (faible précision)

#### 5. MemoryCache

**Responsabilité** : Cache en mémoire pour les recherches fréquentes

```python
from services.cache import get_cache

cache = get_cache()  # Singleton
cache.set('key', data, ttl=3600)
data = cache.get('key')
```

**Caractéristiques** :

- TTL (Time To Live) configurable
- Thread-safe
- Statistiques (hits, misses)

### Routes API

#### `/api/products`

- `GET /random` : Produits aléatoires
- `GET /{id}` : Détails d'un produit

#### `/api/search`

- `POST /image` : Recherche par image
- `GET|POST /text` : Recherche par texte

#### `/api/upload`

- `POST /` : Upload d'image

## Flux de recherche par image

```
1. User upload image
   ↓
2. Frontend → POST /api/search/image
   ↓
3. Backend: Preprocessing
   - Validation format
   - Correction EXIF
   - Smart resize
   - Normalisation ImageNet
   ↓
4. Feature Extraction (ResNet50)
   - Extract 2048-dim vector
   ↓
5. Search Engine (FAISS)
   - Calculate distances
   - Convert to similarity scores
   - Filter by min_similarity
   ↓
6. Database Query
   - Get product details
   - Apply filters (category, price, etc.)
   ↓
7. Response JSON
   - List of products with similarity scores
```

## Flux de recherche par texte

```
1. User enters query
   ↓
2. Frontend → GET /api/search/text?q=...
   ↓
3. Backend: SQL Query
   - LIKE search in name, description, brand, category, color
   - Apply filters (category, price, brand, color)
   - ORDER BY relevance
   ↓
4. Response JSON
   - List of matching products
```

## Base de données

### Schéma relationnel

```
products (1) ────< (N) product_features
```

- **products** : Métadonnées produits
- **product_features** : Vecteurs de features (1 par produit)

### Index

- `idx_products_category` : Recherche par catégorie
- `idx_products_price` : Recherche par prix
- `idx_products_brand` : Recherche par marque
- `idx_products_color` : Recherche par couleur
- `idx_products_category_price` : Composite (catégorie + prix)

## Optimisations

### Cache

- **Recherche par image** : TTL 1 heure (hash image + filtres)
- **Recherche par texte** : TTL 30 minutes (query + filtres)

### Compression

- **Gzip** : Réponses API compressées (flask-compress)

### Logging

- **Structured logging** : JSON format pour parsing facile

## Sécurité

- **CORS** : Configuré pour frontend
- **File validation** : Formats autorisés uniquement
- **Size limits** : 16 MB max pour uploads
- **SQL injection** : Paramètres préparés

## Performance

- **Feature extraction** : ~100-200ms par image
- **Search** : < 100ms avec FAISS
- **Database queries** : < 50ms avec index

## Scalabilité

- **Horizontal scaling** : Stateless backend
- **Database** : Index optimisés
- **Cache** : Réduit charge DB
- **FAISS** : Supporte millions de vecteurs





