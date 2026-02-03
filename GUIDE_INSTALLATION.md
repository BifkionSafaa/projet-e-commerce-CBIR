# 🚀 GUIDE D'INSTALLATION ET CONFIGURATION VS CODE

## 📋 PRÉREQUIS SYSTÈME

### 1. Logiciels à installer

#### Python (Backend)

- **Version requise** : Python 3.8 ou supérieur
- **Téléchargement** : [python.org/downloads](https://www.python.org/downloads/)
- **Vérification** : Ouvrir terminal et taper `python --version` ou `python3 --version`

#### Node.js et npm/pnpm (Frontend)

- **Version requise** : Node.js 18.x ou supérieur
- **Téléchargement** : [nodejs.org](https://nodejs.org/)
- **Vérification** :
  ```bash
  node --version
  npm --version
  ```
- **Note** : Le projet utilise `pnpm`, installer avec :
  ```bash
  npm install -g pnpm
  ```

#### PostgreSQL (Base de données)

- **Version requise** : PostgreSQL 12 ou supérieur
- **Téléchargement** : [postgresql.org/download](https://www.postgresql.org/download/)
- **Alternative** : Docker avec image PostgreSQL
- **Outils graphiques** (optionnel) :
  - pgAdmin : [pgadmin.org](https://www.pgadmin.org/)
  - DBeaver : [dbeaver.io](https://dbeaver.io/)

#### Git (Version control)

- **Téléchargement** : [git-scm.com](https://git-scm.com/)
- **Vérification** : `git --version`

---

## 🔧 INSTALLATION DES EXTENSIONS VS CODE

### Extensions Python (Backend)

1. **Python** (Microsoft)
   - ID : `ms-python.python`
   - Fonctionnalités : IntelliSense, debugging, linting

2. **Pylance** (Microsoft)
   - ID : `ms-python.vscode-pylance`
   - Fonctionnalités : Analyseur de code Python avancé

3. **Python Debugger** (Microsoft)
   - ID : `ms-python.debugpy`
   - Fonctionnalités : Débogage Python

4. **Python Test Explorer** (optionnel)
   - ID : `littlefoxteam.vscode-python-test-adapter`
   - Fonctionnalités : Exécution de tests pytest

5. **Python Docstring Generator** (optionnel)
   - ID : `njpwerner.autodocstring`
   - Fonctionnalités : Génération automatique de docstrings

### Extensions TypeScript/React (Frontend)

1. **ES7+ React/Redux/React-Native snippets**
   - ID : `dsznajder.es7-react-js-snippets`
   - Fonctionnalités : Snippets React

2. **TypeScript Importer** (optionnel)
   - ID : `pmneo.tsimporter`
   - Fonctionnalités : Import automatique TypeScript

3. **Tailwind CSS IntelliSense**
   - ID : `bradlc.vscode-tailwindcss`
   - Fonctionnalités : Autocomplétion Tailwind CSS

### Extensions Générales

1. **Prettier - Code formatter**
   - ID : `esbenp.prettier-vscode`
   - Fonctionnalités : Formatage automatique

2. **ESLint**
   - ID : `dbaeumer.vscode-eslint`
   - Fonctionnalités : Linting JavaScript/TypeScript

3. **Black Formatter** (Python)
   - ID : `ms-python.black-formatter`
   - Fonctionnalités : Formatage Python avec Black

4. **GitLens** (optionnel)
   - ID : `eamodio.gitlens`
   - Fonctionnalités : Visualisation Git avancée

5. **Error Lens** (optionnel)
   - ID : `usernamehw.errorlens`
   - Fonctionnalités : Affichage des erreurs inline

6. **Thunder Client** (optionnel)
   - ID : `rangav.vscode-thunder-client`
   - Fonctionnalités : Test d'API REST (alternative à Postman)

7. **PostgreSQL** (optionnel)
   - ID : `ckolkman.vscode-postgres`
   - Fonctionnalités : Gestion PostgreSQL depuis VS Code

---

## ⚙️ CONFIGURATION VS CODE

### 1. Créer le dossier `.vscode`

Créer un dossier `.vscode` à la racine du projet avec les fichiers de configuration suivants :

### 2. Fichier `settings.json`

Créer `.vscode/settings.json` :

```json
{
  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.analysis.typeCheckingMode": "basic",

  // TypeScript/JavaScript
  "typescript.preferences.importModuleSpecifier": "relative",
  "javascript.preferences.importModuleSpecifier": "relative",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "javascript.updateImportsOnFileMove.enabled": "always",

  // Formatage
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },

  // Fichiers à exclure
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.venv": false
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/__pycache__": true,
    "**/.next": true,
    "**/.venv": true,
    "**/dist": true
  },

  // Tailwind CSS
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^\"'`]*)(?:'|\"|`)"]
  ],

  // Autres
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

### 3. Fichier `launch.json` (Débogage)

Créer `.vscode/launch.json` :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask Backend",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/app.py",
      "console": "integratedTerminal",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
      },
      "cwd": "${workspaceFolder}/backend",
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend",
      "justMyCode": false
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["${workspaceFolder}/backend/tests", "-v"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend",
      "justMyCode": false
    }
  ]
}
```

### 4. Fichier `tasks.json` (Tâches automatiques)

Créer `.vscode/tasks.json` :

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Backend: Install Dependencies",
      "type": "shell",
      "command": "pip install -r requirements.txt",
      "options": {
        "cwd": "${workspaceFolder}/backend"
      },
      "problemMatcher": []
    },
    {
      "label": "Backend: Run Flask",
      "type": "shell",
      "command": "python app.py",
      "options": {
        "cwd": "${workspaceFolder}/backend"
      },
      "problemMatcher": [],
      "isBackground": true,
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Frontend: Install Dependencies",
      "type": "shell",
      "command": "pnpm install",
      "problemMatcher": []
    },
    {
      "label": "Frontend: Run Dev Server",
      "type": "shell",
      "command": "pnpm dev",
      "problemMatcher": [],
      "isBackground": true,
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Backend: Run Tests",
      "type": "shell",
      "command": "pytest",
      "options": {
        "cwd": "${workspaceFolder}/backend"
      },
      "problemMatcher": []
    },
    {
      "label": "Frontend: Run Linter",
      "type": "shell",
      "command": "pnpm lint",
      "problemMatcher": []
    }
  ]
}
```

### 5. Fichier `env.example`

Le fichier `backend/env.example` est déjà créé. Pour l'utiliser :

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cbir_ecommerce
DB_USER=postgres
DB_PASSWORD=your_password_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Paths (optional, defaults are set in config.py)
# UPLOAD_FOLDER=backend/uploads/user_queries
# PRODUCT_IMAGES_FOLDER=backend/static/product_images
# DATASET_PATH=dataset
```

### 6. Fichier `.gitignore`

Créer `.gitignore` à la racine (s'il n'existe pas) :

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
backend/.venv/
backend/venv/
backend/env/
backend/.env
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/

# Node.js
node_modules/
.next/
out/
dist/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
.pnpm-debug.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
backend/uploads/
backend/static/product_images/
dataset/processed/
*.db
*.sqlite
```

---

## 📦 INSTALLATION DES DÉPENDANCES

### Backend (Python/Flask)

1. **Créer un environnement virtuel** :

   ```bash
   cd backend
   python -m venv .venv
   ```

2. **Activer l'environnement virtuel** :
   - **Windows** :
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/Mac** :
     ```bash
     source .venv/bin/activate
     ```

3. **Installer les dépendances** :

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Vérifier l'installation** :
   ```bash
   python -c "import flask; import tensorflow; print('OK')"
   ```

### Frontend (Next.js/React)

1. **Installer pnpm** (si pas déjà installé) :

   ```bash
   npm install -g pnpm
   ```

2. **Installer les dépendances** :

   ```bash
   pnpm install
   ```

3. **Vérifier l'installation** :
   ```bash
   pnpm --version
   node --version
   ```

---

## 🗄️ CONFIGURATION POSTGRESQL

### 1. Créer la base de données

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE cbir_ecommerce;

-- Créer un utilisateur (optionnel)
CREATE USER cbir_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE cbir_ecommerce TO cbir_user;

-- Se connecter à la base
\c cbir_ecommerce
```

### 2. Créer le fichier `.env`

Copier `backend/env.example` vers `backend/.env` et remplir les valeurs :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cbir_ecommerce
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 3. Initialiser la base de données

```bash
cd backend
python scripts/init_database.py
```

---

## 🚀 DÉMARRAGE DU PROJET

### Terminal 1 : Backend Flask

```bash
cd backend
# Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Lancer Flask
python app.py
```

Le backend sera accessible sur : `http://localhost:5000`

### Terminal 2 : Frontend Next.js

```bash
# À la racine du projet
pnpm dev
```

Le frontend sera accessible sur : `http://localhost:3000`

---

## 🧪 VÉRIFICATION DE L'INSTALLATION

### Tester le Backend

1. Ouvrir un navigateur ou utiliser Thunder Client/Postman
2. Tester l'endpoint de santé :
   ```
   GET http://localhost:5000/health
   ```
3. Devrait retourner : `{"status": "ok"}`

### Tester le Frontend

1. Ouvrir le navigateur : `http://localhost:3000`
2. La page d'accueil devrait s'afficher

---

## 🔍 COMMANDES UTILES

### Backend

```bash
# Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Lancer Flask
python app.py

# Lancer les tests
pytest
pytest -v  # Mode verbeux
pytest tests/test_preprocessing.py  # Test spécifique

# Formatter le code
black backend/
```

### Frontend

```bash
# Développement
pnpm dev

# Build de production
pnpm build

# Lancer en production
pnpm start

# Linter
pnpm lint

# Installer une nouvelle dépendance
pnpm add package-name
pnpm add -D package-name  # Dev dependency
```

---

## 🐛 DÉPANNAGE

### Problème : Python non trouvé

**Solution** :

- Vérifier que Python est dans le PATH
- Redémarrer VS Code après installation Python
- Vérifier l'interpréteur Python dans VS Code : `Ctrl+Shift+P` → "Python: Select Interpreter"

### Problème : Module non trouvé (Python)

**Solution** :

- Vérifier que l'environnement virtuel est activé
- Réinstaller les dépendances : `pip install -r requirements.txt`
- Vérifier que VS Code utilise le bon interpréteur Python

### Problème : Erreur de connexion PostgreSQL

**Solution** :

- Vérifier que PostgreSQL est démarré
- Vérifier les credentials dans `.env`
- Tester la connexion : `psql -U postgres -d cbir_ecommerce`

### Problème : Port déjà utilisé

**Solution** :

- Backend (5000) : Changer le port dans `backend/app.py`
- Frontend (3000) : Changer le port avec `pnpm dev -- -p 3001`

### Problème : TensorFlow ne s'installe pas

**Solution** :

- Vérifier la version de Python (3.8-3.11 recommandé)
- Installer manuellement : `pip install tensorflow==2.13.0`
- Pour Windows, peut nécessiter Visual C++ Redistributable

---

## 📚 RESSOURCES UTILES

- **Documentation Flask** : https://flask.palletsprojects.com/
- **Documentation Next.js** : https://nextjs.org/docs
- **Documentation TensorFlow** : https://www.tensorflow.org/api_docs
- **Documentation PostgreSQL** : https://www.postgresql.org/docs/

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Python 3.8+ installé
- [ ] Node.js 18+ installé
- [ ] pnpm installé
- [ ] PostgreSQL installé et démarré
- [ ] Git installé
- [ ] VS Code installé
- [ ] Extensions VS Code installées
- [ ] Fichiers de configuration VS Code créés (`.vscode/`)
- [ ] Environnement virtuel Python créé et activé
- [ ] Dépendances backend installées
- [ ] Dépendances frontend installées
- [ ] Base de données PostgreSQL créée
- [ ] Fichier `.env` configuré
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] Tests de connexion réussis

---

**Bon développement ! 🚀**
