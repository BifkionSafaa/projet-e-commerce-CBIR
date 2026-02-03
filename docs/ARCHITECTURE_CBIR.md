# 🏗️ Architecture CBIR : Features vs Classifieur

## 📚 Principe fondamental du CBIR

Dans un projet **CBIR (Content-Based Image Retrieval)**, la méthode principale est :

### ✅ **Recherche par similarité de FEATURES** (Méthode principale)

1. **Extraction de features** : ResNet50 extrait des vecteurs de features (2048 dimensions)
2. **Recherche par similarité** : Comparaison cosinus/Euclidienne entre features
3. **Résultats** : Produits avec features les plus similaires

**C'est la méthode CBIR classique et correcte.**

---

## 🤔 Pourquoi avons-nous ajouté un classifieur ?

### Problème identifié

Les **features ResNet50 pré-entraînées** ne sont **pas assez discriminantes** pour distinguer les catégories de produits e-commerce :

- Similarité intra-catégorie : 0.8169
- Similarité inter-catégorie : 0.8087
- **Différence : 0.0082** (très faible !)

**Conséquence** : Un casque peut avoir 99.9% de similarité avec un vêtement (fond blanc similaire).

---

### Solution temporaire : Classifieur

Le classifieur a été ajouté comme **solution de contournement** pour :

- Prédire la catégorie de l'image uploadée
- Filtrer les résultats par cette catégorie
- Compenser le manque de discrimination des features

**Mais ce n'est PAS la méthode CBIR classique.**

---

## 🎯 Méthode CBIR idéale (sans classifieur)

### Architecture correcte :

```
Image uploadée
    ↓
Extraction features (ResNet50)
    ↓
Recherche par similarité (cosinus/Euclidienne)
    ↓
Résultats : Produits avec features les plus similaires
```

**Pas besoin de classifieur** si les features sont discriminantes.

---

## ❌ Problème actuel

### Pourquoi le classifieur est nécessaire ?

1. **Features pas assez discriminantes** :
   - ResNet50 pré-entraîné sur ImageNet (généraliste)
   - Pas adapté aux produits e-commerce spécifiques
   - Fond blanc similaire entre catégories

2. **Résultats incorrects** :
   - Casque → Résultats vêtements (99.9% similarité)
   - Peluche → Résultats AirPods (99.8% similarité)

3. **Solution de contournement** :
   - Classifieur prédit la catégorie
   - Filtre les résultats par catégorie
   - Compense le manque de discrimination

---

## ✅ Solutions à long terme (sans classifieur)

### 1. **Fine-tuning ResNet50**

**Entraîner ResNet50 sur un dataset de produits e-commerce** :

- Dataset avec produits e-commerce
- Fine-tuning des dernières couches
- Features plus discriminantes pour le domaine

**Avantages** :

- ✅ Features discriminantes naturellement
- ✅ Pas besoin de classifieur
- ✅ Méthode CBIR pure

**Inconvénients** :

- ⚠️ Nécessite beaucoup de données
- ⚠️ Temps d'entraînement

---

### 2. **Modèle spécialisé e-commerce**

**Utiliser un modèle pré-entraîné sur produits e-commerce** :

- Modèles spécialisés (ex: Fashion-MNIST, ProductNet)
- Features déjà adaptées au domaine

**Avantages** :

- ✅ Features discriminantes
- ✅ Pas d'entraînement nécessaire

**Inconvénients** :

- ⚠️ Moins de modèles disponibles
- ⚠️ Peut nécessiter adaptation

---

### 3. **Améliorer le preprocessing**

**Techniques avancées** :

- Background removal (suppression du fond)
- Segmentation d'objet
- Augmentation de données

**Avantages** :

- ✅ Améliore la discrimination
- ✅ Pas de changement de modèle

**Inconvénients** :

- ⚠️ Complexité accrue
- ⚠️ Peut ne pas suffire

---

## 📊 Comparaison : Avec vs Sans classifieur

### Avec classifieur (solution actuelle) :

```
Image uploadée
    ↓
Extraction features
    ↓
Classifieur → Prédit catégorie
    ↓
Recherche par similarité
    ↓
Filtre par catégorie prédite
    ↓
Résultats
```

**Avantages** :

- ✅ Compense le manque de discrimination
- ✅ Résultats plus pertinents

**Inconvénients** :

- ❌ Dépend de la précision du classifieur (62.5%)
- ❌ Pas la méthode CBIR pure
- ❌ Deux modèles à maintenir

---

### Sans classifieur (méthode CBIR pure) :

```
Image uploadée
    ↓
Extraction features (fine-tunées)
    ↓
Recherche par similarité
    ↓
Résultats (déjà pertinents)
```

**Avantages** :

- ✅ Méthode CBIR pure
- ✅ Un seul modèle
- ✅ Plus simple

**Inconvénients** :

- ⚠️ Nécessite fine-tuning ou meilleur modèle
- ⚠️ Features doivent être discriminantes

---

## 🎯 Recommandation

### Pour un projet académique/démo (actuel) :

**Garder le classifieur** comme solution de contournement :

- ✅ Fonctionne avec les features actuelles
- ✅ Résultats acceptables
- ✅ Pas besoin de fine-tuning

### Pour un projet production :

**Fine-tuner ResNet50** ou utiliser un modèle spécialisé :

- ✅ Features discriminantes naturellement
- ✅ Pas besoin de classifieur
- ✅ Méthode CBIR pure
- ✅ Meilleure performance

---

## 📝 Résumé

### Question : Features ou Classifieur ?

**Réponse** : **FEATURES** (méthode CBIR principale)

**Le classifieur est un ajout** pour compenser le manque de discrimination des features ResNet50 pré-entraînées.

**Méthode CBIR idéale** :

- Features discriminantes → Recherche par similarité → Résultats pertinents
- **Pas besoin de classifieur**

**Méthode actuelle (contournement)** :

- Features peu discriminantes → Classifieur → Filtre → Résultats pertinents
- **Classifieur nécessaire pour compenser**

---

## ✅ Conclusion

**Dans un projet CBIR, on utilise les FEATURES pour la recherche.**

Le classifieur est une **solution de contournement** pour compenser le manque de discrimination des features ResNet50 pré-entraînées.

**Pour améliorer à long terme** : Fine-tuner ResNet50 ou utiliser un modèle spécialisé e-commerce.





