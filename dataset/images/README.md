# Structure du Dataset d'Images

## Organisation

```
dataset/images/
├── mode/
│   ├── chaussures/       (5-10 images)
│   ├── vetements/        (5-10 images)
│   └── sacs/             (5-10 images)
├── electronique/          (5-10 images mélangées: téléphones, caméras, machines, etc.)
├── jouets/               (5-10 images: poupées, voitures, puzzles, peluches, robots, etc.)
└── beaute/
    └── cosmétiques/      (5-10 images)
```

## Convention de nommage

Utilisez le format : `{categorie}_{numero}.jpg`

Exemples :

- `chaussures_001.jpg`, `chaussures_002.jpg`, ...
- `electronique_001.jpg`, `electronique_002.jpg`, ... (téléphones, caméras, machines, etc.)
- `jouets_001.jpg`, `jouets_002.jpg`, ... (poupées, voitures, puzzles, peluches, robots, etc.)

## Objectif

- **Minimum** : 5 images par catégorie
- **Recommandé** : 10 images par catégorie pour plus de diversité
- **Total** : 30-60 images (6 catégories × 5-10 images)

## Critères de qualité

- Résolution >= 224x224 pixels
- Images de produits claires et nettes
- Diversité dans chaque catégorie (différents modèles, couleurs, angles)

## Sources

Documenter les sources des images dans `dataset/SOURCES.md`
