# 🛠️ TECHNOLOGIES DU PROJET CBIR E-COMMERCE

## 📋 Technologies selon le descriptif

### Frontend

- ✅ **React** - Bibliothèque JavaScript pour l'interface utilisateur
- ⚠️ **Vue** - Non utilisé (projet utilise React)
- ⚠️ **Bootstrap** - Non utilisé (projet utilise Tailwind CSS, plus moderne)

### Backend

- ✅ **Python** - Langage de programmation
- ✅ **Flask** - Framework web Python (choisi parmi Flask/Django)

### Bibliothèques Vision et IA

- ✅ **OpenCV** - Traitement d'images et vision par ordinateur
- ✅ **Keras/TensorFlow** - Framework de deep learning

### Extraction de features

- ✅ **ResNet50** - Modèle CNN pré-entraîné sur ImageNet (choisi parmi ResNet50/MobileNetV2)

### Comparaison des vecteurs

- ✅ **sklearn** - Scikit-learn pour calcul de similarité
- ✅ **numpy** - Calculs numériques et manipulation de tableaux
- ⚠️ **FAISS** - Optionnel (recommandé pour optimiser les performances)

---

## ✅ Technologies actuellement utilisées dans le projet

### Frontend

| Technologie      | Version | Rôle            | Statut      |
| ---------------- | ------- | --------------- | ----------- |
| **React**        | 19.2.0  | Bibliothèque UI | ✅ Installé |
| **Next.js**      | 16.0.7  | Framework React | ✅ Installé |
| **TypeScript**   | 5.x     | Typage statique | ✅ Installé |
| **Tailwind CSS** | 4.1.9   | Framework CSS   | ✅ Installé |
| **shadcn/ui**    | -       | Composants UI   | ✅ Installé |

**Note** : Le projet utilise **Next.js + React** au lieu de React seul, ce qui est **mieux** car Next.js offre :

- Routing automatique
- Optimisation des performances
- API routes intégrées
- Server-side rendering

**Note** : Le projet utilise **Tailwind CSS** au lieu de Bootstrap, ce qui est **plus moderne** et offre :

- Utility-first CSS
- Meilleure performance
- Plus de flexibilité

---

### Backend

| Technologie    | Version | Rôle                     | Statut      |
| -------------- | ------- | ------------------------ | ----------- |
| **Python**     | 3.8+    | Langage de programmation | ✅ Requis   |
| **Flask**      | 2.3.2   | Framework web            | ✅ Installé |
| **Flask-CORS** | 4.0.0   | Gestion CORS             | ✅ Installé |
| **PostgreSQL** | 12+     | Base de données          | ✅ Requis   |
| **psycopg2**   | 2.9.6   | Driver PostgreSQL        | ✅ Installé |

---

### Machine Learning & Vision

| Technologie      | Version        | Rôle                         | Statut        |
| ---------------- | -------------- | ---------------------------- | ------------- |
| **TensorFlow**   | 2.13.0         | Framework deep learning      | ✅ Installé   |
| **Keras**        | (inclus)       | API haut niveau TensorFlow   | ✅ Disponible |
| **OpenCV**       | 4.8.0.74       | Traitement d'images          | ✅ Installé   |
| **Pillow**       | 10.0.0         | Manipulation d'images        | ✅ Installé   |
| **ResNet50**     | (pré-entraîné) | Modèle CNN ImageNet          | ✅ Configuré  |
| **NumPy**        | 1.24.3         | Calculs numériques           | ✅ Installé   |
| **scikit-learn** | 1.3.0          | Machine learning             | ✅ Installé   |
| **FAISS**        | -              | Recherche vectorielle rapide | ⚠️ Optionnel  |

**Note** : ResNet50 est configuré dans `backend/services/feature_extractor.py`

---

## 📦 Dépendances complètes

### Backend (`backend/requirements.txt`)

```txt
Flask==2.3.2              # Framework web
flask-cors==4.0.0         # Gestion CORS
psycopg2-binary==2.9.6    # Driver PostgreSQL
tensorflow==2.13.0        # Deep learning
numpy==1.24.3             # Calculs numériques
opencv-python==4.8.0.74   # Vision par ordinateur
scikit-learn==1.3.0       # Machine learning
Pillow==10.0.0            # Manipulation d'images
python-dotenv==1.0.0      # Variables d'environnement
```

### Frontend (`package.json`)

**Dépendances principales** :

- `react` : 19.2.0
- `next` : 16.0.7
- `typescript` : 5.x
- `tailwindcss` : 4.1.9

**Composants UI** :

- `@radix-ui/*` : Composants accessibles (shadcn/ui)
- `lucide-react` : Icônes
- `tailwind-merge` : Utilitaires Tailwind

---

## 🎯 Correspondance avec le descriptif

### ✅ Conforme au descriptif

| Exigence                    | Implémentation                   | Statut                   |
| --------------------------- | -------------------------------- | ------------------------ |
| **Frontend: React**         | React 19.2.0 + Next.js 16.0.7    | ✅ **Mieux que demandé** |
| **Backend: Python + Flask** | Python 3.8+ + Flask 2.3.2        | ✅ **Conforme**          |
| **OpenCV**                  | opencv-python 4.8.0.74           | ✅ **Conforme**          |
| **Keras/TensorFlow**        | TensorFlow 2.13.0 (inclut Keras) | ✅ **Conforme**          |
| **ResNet50**                | ResNet50 pré-entraîné ImageNet   | ✅ **Conforme**          |
| **sklearn**                 | scikit-learn 1.3.0               | ✅ **Conforme**          |
| **numpy**                   | numpy 1.24.3                     | ✅ **Conforme**          |

### ⚠️ Différences (améliorations)

| Descriptif suggère  | Projet utilise       | Pourquoi c'est mieux                               |
| ------------------- | -------------------- | -------------------------------------------------- |
| **Bootstrap**       | **Tailwind CSS**     | Plus moderne, meilleure performance                |
| **React seul**      | **Next.js + React**  | Framework complet avec routing, SSR, optimisations |
| **FAISS optionnel** | **FAISS recommandé** | Améliore les performances de recherche             |

### ❌ Non utilisé (mais acceptable)

- **Vue.js** : Non utilisé car projet utilise React (conforme au descriptif qui dit "React, Vue, Bootstrap" = choix)
- **Django** : Non utilisé car projet utilise Flask (conforme au descriptif qui dit "Flask ou Django" = choix)
- **MobileNetV2** : Non utilisé car projet utilise ResNet50 (conforme au descriptif qui dit "ResNet50 ou MobileNetV2" = choix)

---

## 🚀 Installation des technologies

### 1. Prérequis système

```bash
# Python 3.8+
python --version

# Node.js 18+
node --version

# PostgreSQL 12+
psql --version
```

### 2. Backend (Python)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Frontend (Node.js)

```bash
npm install -g pnpm
pnpm install
```

### 4. Base de données

```sql
CREATE DATABASE cbir_ecommerce;
```

---

## 📊 Architecture technologique

```
┌─────────────────────────────────────────────┐
│           FRONTEND (Navigateur)             │
├─────────────────────────────────────────────┤
│  Next.js 16.0.7                             │
│  ├─ React 19.2.0                            │
│  ├─ TypeScript 5.x                          │
│  └─ Tailwind CSS 4.1.9                      │
└─────────────────────────────────────────────┘
                    ↕ HTTP/REST API
┌─────────────────────────────────────────────┐
│           BACKEND (Serveur)                 │
├─────────────────────────────────────────────┤
│  Flask 2.3.2                                │
│  ├─ Python 3.8+                             │
│  ├─ PostgreSQL (via psycopg2)               │
│  └─ Services ML                             │
│     ├─ TensorFlow 2.13.0                    │
│     ├─ ResNet50 (pré-entraîné)              │
│     ├─ OpenCV 4.8.0.74                      │
│     ├─ scikit-learn 1.3.0                   │
│     └─ NumPy 1.24.3                         │
└─────────────────────────────────────────────┘
```

---

## 🔍 Détails techniques

### Extraction de features (ResNet50)

**Fichier** : `backend/services/feature_extractor.py`

```python
from tensorflow.keras.applications import ResNet50

model = ResNet50(
    weights='imagenet',      # Pré-entraîné sur ImageNet
    include_top=False,        # Sans couche de classification
    pooling='avg',            # Global average pooling
    input_shape=(224, 224, 3) # Taille d'entrée
)
```

**Features extraites** : Vecteur de 2048 dimensions

### Prétraitement (OpenCV)

**Fichier** : `backend/services/preprocessing.py`

- Redimensionnement à 224x224
- Conversion BGR → RGB
- Normalisation des pixels
- Gestion des erreurs

### Recherche de similarité (scikit-learn)

**Fichier** : `backend/services/search_engine.py`

- Cosine similarity pour comparer les vecteurs
- Tri par score de similarité
- Retour des top-K produits similaires

---

## ✅ Validation

Le projet **respecte entièrement** le descriptif et utilise même des technologies **plus modernes** que celles suggérées :

- ✅ React (demandé) → **Next.js + React** (mieux)
- ✅ Flask (choisi parmi Flask/Django) → **Flask** ✅
- ✅ OpenCV → **OpenCV** ✅
- ✅ TensorFlow/Keras → **TensorFlow 2.13.0** ✅
- ✅ ResNet50 (choisi parmi ResNet50/MobileNetV2) → **ResNet50** ✅
- ✅ sklearn → **scikit-learn** ✅
- ✅ numpy → **NumPy** ✅
- ⚠️ Bootstrap (suggéré) → **Tailwind CSS** (plus moderne, acceptable)

---

## 📝 Notes importantes

1. **Next.js vs React seul** : Next.js est un framework qui utilise React, donc c'est conforme au descriptif qui demande React.

2. **Tailwind vs Bootstrap** : Les deux sont des frameworks CSS. Tailwind est plus moderne et performant, donc acceptable.

3. **FAISS** : Optionnel selon le descriptif, mais **fortement recommandé** pour améliorer les performances de recherche avec de grandes bases de données.

4. **ResNet50** : Modèle pré-entraîné sur ImageNet, conforme au descriptif.

---


