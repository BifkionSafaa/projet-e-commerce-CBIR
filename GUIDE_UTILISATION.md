# 📖 GUIDE D'UTILISATION DE L'APPLICATION

## 🎯 Vue d'ensemble

Cette application permet de rechercher des produits similaires dans un catalogue e-commerce en utilisant :
- **Recherche par image** : Uploader une image pour trouver des produits visuellement similaires
- **Recherche par texte** : Rechercher par nom, description, catégorie ou marque

### Personnaliser la bannière promotionnelle

La première section visible sur la page d’accueil est une **bannière promotionnelle**. Pour utiliser votre propre image :

1. Ajoutez une image (JPG ou PNG) dans le dossier **`public/`** du projet.
2. Nommez-la **`banner-promo.jpg`** (ou `.png`).
3. Au prochain chargement de la page, elle remplacera l’image par défaut.

Si `banner-promo.jpg` n’existe pas, l’application affiche une image de remplacement.

---

## 🚀 Démarrage de l'application

### 1. Vérifier que les services sont démarrés

Avant d'utiliser l'application, assurez-vous que :

- ✅ **PostgreSQL** est démarré (service Windows)
- ✅ **Backend Flask** est démarré (terminal 1) → `http://localhost:5000`
- ✅ **Frontend Next.js** est démarré (terminal 2) → `http://localhost:3000`

### 2. Ouvrir l'application

Ouvrez votre navigateur et accédez à : **http://localhost:3000**

---

## 🔍 RECHERCHE PAR IMAGE

### Comment utiliser la recherche par image

1. **Sélectionner une image**
   - Cliquez sur la zone "Glisser-déposer une image" ou cliquez pour parcourir vos fichiers
   - Formats acceptés : JPG, JPEG, PNG, WebP
   - Taille recommandée : moins de 10 MB

2. **Lancer la recherche**
   - Une fois l'image sélectionnée, cliquez sur le bouton **"Rechercher"**
   - L'application va :
     - Préprocesser l'image
     - Extraire les features visuelles avec ResNet50
     - Comparer avec les produits de la base de données
     - Afficher les produits les plus similaires

3. **Consulter les résultats**
   - Les produits sont affichés par ordre de similarité décroissante
   - Chaque produit affiche :
     - **Image** du produit
     - **Nom** du produit
     - **Prix**
     - **Score de similarité** (en pourcentage)
     - **Catégorie**, **Marque**, **Couleur**

### Filtres disponibles pour la recherche par image

Une fois les résultats affichés, vous pouvez filtrer :

- **Catégorie** : Filtrer par catégorie (électronique, vêtements, etc.)
- **Prix minimum** : Définir un prix minimum
- **Prix maximum** : Définir un prix maximum
- **Marque** : Filtrer par marque
- **Couleur** : Filtrer par couleur

### Exemple d'utilisation

1. Vous avez une photo d'un casque audio
2. Vous uploadez cette image
3. L'application trouve tous les casques audio similaires dans le catalogue
4. Vous pouvez filtrer par prix (ex: entre 50€ et 200€)

---

## 📝 RECHERCHE PAR TEXTE

### Comment utiliser la recherche par texte

1. **Taper votre recherche** dans le champ de recherche en haut de la page
   - Vous pouvez rechercher par :
     - **Nom** du produit (ex: "AirPods", "T-shirt")
     - **Description** (ex: "bluetooth", "coton")
     - **Catégorie** (ex: "électronique", "vêtements")
     - **Marque** (ex: "Apple", "Nike")

2. **Appuyer sur Entrée** ou cliquer sur le bouton de recherche

3. **Consulter les résultats**
   - Les résultats sont triés par pertinence
   - Les correspondances exactes dans le nom apparaissent en premier

### Exemples de recherches

- `"casque"` → Trouve tous les casques
- `"blanc"` → Trouve les produits blancs
- `"Apple"` → Trouve tous les produits Apple
- `"électronique"` → Trouve tous les produits électroniques

---

## 🎨 PRODUITS RECOMMANDÉS

Sur la page d'accueil, vous verrez une section **"Produits recommandés"** qui affiche :
- 8 produits aléatoires du catalogue
- Mise à jour automatique au chargement de la page
- Bouton **"Actualiser"** pour obtenir de nouveaux produits

---

## 📊 COMPRENDRE LES RÉSULTATS

### Score de similarité

- **100%** : Produit identique ou très similaire
- **80-99%** : Produit très similaire
- **50-79%** : Produit similaire
- **< 50%** : Produit peu similaire (non affiché par défaut)

### Tri des résultats

Vous pouvez trier les résultats par :
- **Similarité** (par défaut) : Du plus similaire au moins similaire
- **Prix croissant** : Du moins cher au plus cher
- **Prix décroissant** : Du plus cher au moins cher
- **Nom** : Ordre alphabétique

---

## 🔧 FONCTIONNALITÉS AVANCÉES

### Filtres combinés

Vous pouvez combiner plusieurs filtres :
- Exemple : Rechercher des "casques" entre 50€ et 150€ de marque "Sony"

### Réinitialisation des filtres

Cliquez sur le bouton **"Réinitialiser"** pour :
- Effacer tous les filtres
- Réinitialiser les résultats
- Revenir à l'état initial

---

## ❓ QUESTIONS FRÉQUENTES

### Pourquoi ma recherche ne retourne aucun résultat ?

**Causes possibles :**
1. **Seuil de similarité trop élevé** : Essayez avec une image plus similaire
2. **Aucun produit correspondant** : Vérifiez que le catalogue contient des produits similaires
3. **Filtres trop restrictifs** : Essayez de retirer certains filtres

### Pourquoi les résultats ne sont pas pertinents ?

**Explications :**
- Le modèle ResNet50 trouve des **similarités visuelles**, pas sémantiques
- Un plush peut être visuellement similaire à un vêtement (texture, couleur)
- Les résultats sont filtrés par catégorie du premier résultat pour améliorer la pertinence

### Comment améliorer les résultats ?

1. **Utilisez des images de bonne qualité**
2. **Utilisez des images avec un fond uniforme** (blanc de préférence)
3. **Assurez-vous que l'objet est bien visible** dans l'image
4. **Utilisez les filtres** pour affiner les résultats

### Puis-je rechercher plusieurs produits à la fois ?

Non, actuellement vous ne pouvez rechercher qu'un seul produit à la fois. Pour rechercher un autre produit, uploadez une nouvelle image ou effectuez une nouvelle recherche par texte.

---

## 🎯 CONSEILS D'UTILISATION

### Pour de meilleurs résultats avec la recherche par image :

1. ✅ **Utilisez des images claires et nettes**
2. ✅ **Assurez-vous que le produit occupe une grande partie de l'image**
3. ✅ **Évitez les images avec plusieurs produits**
4. ✅ **Utilisez des images avec un fond uniforme**
5. ✅ **Privilégiez les images en format carré (1:1)**

### Pour de meilleurs résultats avec la recherche par texte :

1. ✅ **Utilisez des mots-clés précis** (ex: "AirPods Pro" plutôt que "écouteurs")
2. ✅ **Essayez différentes orthographes** si aucun résultat
3. ✅ **Utilisez les filtres** pour affiner votre recherche
4. ✅ **Combinez plusieurs mots-clés** (ex: "casque bluetooth noir")

---

## 🐛 DÉPANNAGE

### L'application ne charge pas

1. Vérifiez que le backend est démarré : `http://localhost:5000/health`
2. Vérifiez que le frontend est démarré : `http://localhost:3000`
3. Vérifiez la console du navigateur (F12) pour les erreurs

### Les images ne s'affichent pas

1. Vérifiez que les images sont dans `dataset/images/`
2. Vérifiez que le backend sert les images correctement
3. Vérifiez les permissions de fichiers

### La recherche est lente

1. C'est normal pour la première recherche (chargement du modèle ResNet50)
2. Les recherches suivantes sont plus rapides (cache)
3. Si c'est toujours lent, vérifiez les performances de votre machine

---

## 📚 DOCUMENTATION COMPLÉMENTAIRE

Pour plus d'informations techniques :

- **Guide d'installation** : `GUIDE_INSTALLATION.md`
- **Démarrage rapide** : `QUICK_START.md`
- **Architecture** : `docs/ARCHITECTURE_CBIR.md`
- **API** : `docs/API_EXPLANATION.md`

---

## ✅ RÉSUMÉ

**Fonctionnalités principales :**
- 🔍 Recherche par image (upload)
- 📝 Recherche par texte (nom, description, catégorie, marque)
- 🎨 Filtres avancés (catégorie, prix, marque, couleur)
- 📊 Tri des résultats (similarité, prix, nom)
- 🎯 Produits recommandés aléatoires

**Pour commencer :**
1. Démarrer les services (PostgreSQL, Backend, Frontend)
2. Ouvrir `http://localhost:3000`
3. Uploadez une image ou recherchez par texte
4. Explorez les résultats et utilisez les filtres

---

**Besoin d'aide ?** Consultez la section "Dépannage" ci-dessus ou les autres fichiers de documentation.

