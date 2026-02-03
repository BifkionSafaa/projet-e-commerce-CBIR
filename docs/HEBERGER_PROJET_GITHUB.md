# Héberger le projet sur GitHub

Étapes pour mettre le code du projet **ecommerce-cbir** dans un dépôt GitHub.

---

## 1. Créer un dépôt sur GitHub

1. Va sur [github.com](https://github.com) et connecte-toi.
2. Clique sur **"New"** (ou **"+"** → **"New repository"**).
3. Renseigne :
   - **Repository name** : par ex. `ecommerce-cbir` ou `ecommerce-cbir-project`
   - **Description** : optionnel (ex. "E-commerce avec recherche par image CBIR")
   - **Public** ou **Private**
   - **Ne coche pas** "Add a README" (le projet en a déjà un).
4. Clique sur **"Create repository"**.
5. Note l’URL du dépôt : `https://github.com/TON_USERNAME/NOM_DU_REPO.git`

---

## 2. Préparer le projet (fichiers lourds)

GitHub refuse les fichiers **> 100 Mo**. Le dossier `data/` (fichiers `.npy`) et `dataset/images/` peuvent être lourds.

- Si tu veux **tout pousser** et que la taille reste sous 100 Mo par fichier : tu peux ignorer cette étape.
- Si tu dépasses ou veux alléger le repo : ajoute dans `.gitignore` à la fin :
  ```
  # Données lourdes (optionnel)
  data/*.npy
  dataset/images/
  ```
  Puis documente dans le README comment générer ou récupérer ces données (scripts, lien, etc.).

---

## 3. Initialiser Git et faire le premier commit

Ouvre un terminal **à la racine du projet** (`ecommerce-cbir-project`) et exécute :

```bash
# Initialiser Git
git init

# Vérifier que .gitignore est bien pris en compte
git add .
git status

# Premier commit
git commit -m "Initial commit - projet e-commerce CBIR"
```

Si un fichier trop gros apparaît (> 100 Mo), retire-le du suivi, ajoute-le dans `.gitignore`, puis refais `git add .` et `git commit`.

---

## 4. Branche principale

Si Git te demande un nom de branche, utilise `main` :

```bash
git branch -M main
```

---

## 5. Lier le dépôt GitHub et pousser

Remplace `TON_USERNAME` et `NOM_DU_REPO` par les tiens :

```bash
git remote add origin https://github.com/TON_USERNAME/NOM_DU_REPO.git
git push -u origin main
```

Si le dépôt GitHub a été créé avec un README et que tu as des conflits :

```bash
git pull origin main --allow-unrelated-histories
# Résoudre les conflits si demandé, puis :
git push -u origin main
```

---

## 6. Vérification

- Ouvre `https://github.com/TON_USERNAME/NOM_DU_REPO` : tu dois voir le code du projet.
- Pour cloner ailleurs : `git clone https://github.com/TON_USERNAME/NOM_DU_REPO.git`

---

## Résumé des commandes (copier-coller)

```bash
cd c:\Users\espacegamers\ecommerce-cbir-project
git init
git add .
git status
git commit -m "Initial commit - projet e-commerce CBIR"
git branch -M main
git remote add origin https://github.com/TON_USERNAME/NOM_DU_REPO.git
git push -u origin main
```

Remplacer `TON_USERNAME` et `NOM_DU_REPO` par ton compte GitHub et le nom du dépôt.
