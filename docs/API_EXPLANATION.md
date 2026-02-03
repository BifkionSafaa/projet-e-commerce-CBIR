# 🔌 EXPLICATION DE L'API (Application Programming Interface)

## 📖 Qu'est-ce qu'une API ?

Une **API (Application Programming Interface)** est un ensemble de règles et de protocoles qui permet à deux applications différentes de communiquer entre elles.

Dans notre projet :

- **Frontend (Next.js)** = Application client (navigateur web)
- **Backend (Flask)** = Application serveur (serveur Python)

L'API est le **pont de communication** entre ces deux applications.

---

## 🏗️ Architecture Client-Serveur

```
┌─────────────────┐         HTTP Request          ┌─────────────────┐
│                 │  ───────────────────────────> │                 │
│   FRONTEND      │                                 │    BACKEND      │
│   (Next.js)     │  <───────────────────────────  │    (Flask)       │
│                 │         HTTP Response          │                 │
└─────────────────┘                                 └─────────────────┘
     Navigateur                                          Serveur
```

### Flux de communication :

1. **Le Frontend envoie une requête HTTP** (GET, POST, PUT, DELETE)
   - Exemple : `GET http://localhost:5000/api/products/random?count=8`

2. **Le Backend reçoit la requête** et la traite
   - Interroge la base de données PostgreSQL
   - Traite les données
   - Prépare une réponse

3. **Le Backend renvoie une réponse HTTP** (JSON)
   - Exemple : `[{id: 1, name: "AirPods", price: 199.99, ...}]`

4. **Le Frontend reçoit la réponse** et met à jour l'interface
   - Affiche les produits dans la grille

---

## 🔄 Comment l'API fonctionne dans notre projet

### 1. **Route API** (`backend/routes/products.py`)

```python
@products_bp.route('/random', methods=['GET'])
def get_random_products():
    # 1. Récupérer le paramètre 'count' de la requête
    count = request.args.get('count', 4, type=int)

    # 2. Interroger la base de données
    query = "SELECT * FROM products ORDER BY RANDOM() LIMIT %s"
    products = db.execute_query(query, (count,))

    # 3. Retourner les données en JSON
    return jsonify(products), 200
```

**Explication ligne par ligne :**

- `@products_bp.route('/random', methods=['GET'])` : Définit l'URL `/api/products/random` et la méthode HTTP (GET)
- `request.args.get('count', 4, type=int)` : Récupère le paramètre `count` de l'URL (ex: `?count=8`)
- `db.execute_query(...)` : Exécute une requête SQL pour récupérer les produits
- `return jsonify(products), 200` : Retourne les données en format JSON avec le code HTTP 200 (succès)

### 2. **Appel API depuis le Frontend** (`app/page.tsx`)

```typescript
const fetchRandomProducts = async () => {
  setLoading(true)
  try {
    // 1. Envoyer une requête HTTP GET
    const response = await fetch('http://localhost:5000/api/products/random?count=8')

    // 2. Vérifier si la réponse est OK
    if (!response.ok) {
      throw new Error('Erreur lors du chargement')
    }

    // 3. Convertir la réponse JSON en objet JavaScript
    const data = await response.json()

    // 4. Mettre à jour l'état React
    setProducts(data)
  } catch (error) {
    setError(error.message)
  } finally {
    setLoading(false)
  }
}
```

**Explication ligne par ligne :**

- `fetch(...)` : Fonction JavaScript native pour envoyer une requête HTTP
- `await response.json()` : Convertit la réponse JSON en objet JavaScript
- `setProducts(data)` : Met à jour l'état React avec les produits reçus

---

## 📡 Types de requêtes HTTP

### GET : Récupérer des données

```
GET /api/products/random?count=8
→ Retourne une liste de produits
```

### POST : Envoyer des données

```
POST /api/search/image
Body: FormData avec une image
→ Retourne des produits similaires
```

### PUT : Mettre à jour des données

```
PUT /api/products/123
Body: JSON avec nouvelles données
→ Met à jour le produit
```

### DELETE : Supprimer des données

```
DELETE /api/products/123
→ Supprime le produit
```

---

## 🎯 Rôle de l'API dans notre projet

### 1. **Séparation des responsabilités**

- **Frontend** : Affiche l'interface utilisateur
- **Backend** : Gère la logique métier et la base de données
- **API** : Permet la communication entre les deux

### 2. **Sécurité**

- Le Frontend ne peut pas accéder directement à la base de données
- Le Backend valide et sécurise toutes les requêtes
- Protection contre les injections SQL, XSS, etc.

### 3. **Réutilisabilité**

- L'API peut être utilisée par :
  - Une application web (Next.js)
  - Une application mobile (React Native)
  - Un autre service backend
  - Un script Python

### 4. **Scalabilité**

- Le Backend peut être déployé sur plusieurs serveurs
- Le Frontend peut être déployé sur un CDN
- L'API permet la communication entre services distribués

---

## 🔍 Exemple concret : Tâche 15

### Objectif : Afficher des produits aléatoires sur la page d'accueil

**Étape 1 : Backend** (`backend/routes/products.py`)

```python
@products_bp.route('/random', methods=['GET'])
def get_random_products():
    count = request.args.get('count', 8, type=int)
    # Récupérer produits aléatoires depuis PostgreSQL
    query = """
        SELECT id, name, category, price, description, brand, color, image_path
        FROM products
        ORDER BY RANDOM()
        LIMIT %s
    """
    db = get_db()
    products = db.execute_query(query, (count,))
    return jsonify(products), 200
```

**Étape 2 : Frontend** (`app/page.tsx`)

```typescript
useEffect(() => {
  fetchRandomProducts()
}, [])

const fetchRandomProducts = async () => {
  const response = await fetch('http://localhost:5000/api/products/random?count=8')
  const data = await response.json()
  setProducts(data)
}
```

**Résultat :**

- Au chargement de la page, le Frontend appelle l'API
- L'API interroge la base de données
- Les produits sont retournés en JSON
- Le Frontend affiche les produits dans une grille

---

## 🛠️ Outils pour tester l'API

### 1. **Navigateur** (Console JavaScript)

```javascript
fetch('http://localhost:5000/api/products/random?count=5')
  .then(res => res.json())
  .then(data => console.log(data))
```

### 2. **Postman** (Application dédiée)

- Interface graphique pour tester les APIs
- Permet d'envoyer des requêtes GET, POST, etc.

### 3. **curl** (Ligne de commande)

```bash
curl http://localhost:5000/api/products/random?count=5
```

### 4. **Script Python** (`scripts/test_search_api.py`)

```python
import requests
response = requests.get('http://localhost:5000/api/products/random?count=5')
print(response.json())
```

---

## ✅ Résumé

**L'API est le pont de communication entre :**

- Le **Frontend** (ce que l'utilisateur voit)
- Le **Backend** (la logique et les données)

**Avantages :**

- ✅ Séparation claire des responsabilités
- ✅ Sécurité renforcée
- ✅ Réutilisabilité
- ✅ Scalabilité

**Dans notre projet :**

- L'API Flask expose des routes (`/api/products/random`, `/api/search/image`)
- Le Frontend Next.js appelle ces routes avec `fetch()`
- Les données sont échangées en format JSON





