# Composants de recherche

Composants React/Next.js pour la recherche par image dans l'application CBIR E-Commerce.

## Composants

### ImageUpload

Composant pour uploader une image avec plusieurs méthodes :

- **Drag & drop** : Glisser-déposer une image
- **Sélection fichier** : Cliquer pour choisir un fichier
- **Caméra** : Prendre une photo (mobile/desktop)
- **Prévisualisation** : Affiche l'image sélectionnée
- **Validation** : Vérifie le format et la taille

#### Props

```typescript
interface ImageUploadProps {
  onImageSelect: (file: File) => void // Callback appelé quand une image est sélectionnée
  maxSizeMB?: number // Taille max en MB (défaut: 16)
  acceptedFormats?: string[] // Formats acceptés (défaut: jpeg, jpg, png, webp)
  className?: string // Classes CSS supplémentaires
}
```

#### Exemple

```tsx
<ImageUpload
  onImageSelect={file => {
    console.log('Image sélectionnée:', file.name)
  }}
  maxSizeMB={16}
/>
```

### SearchBar

Composant de barre de recherche par texte.

#### Props

```typescript
interface SearchBarProps {
  onSearch: (query: string) => void // Callback appelé lors de la recherche
  placeholder?: string // Texte du placeholder
  className?: string // Classes CSS supplémentaires
  disabled?: boolean // Désactiver la recherche
}
```

#### Exemple

```tsx
<SearchBar
  onSearch={query => {
    console.log('Recherche:', query)
  }}
  placeholder="Rechercher un produit..."
/>
```

### SearchButton

Bouton de recherche avec état de chargement.

#### Props

```typescript
interface SearchButtonProps {
  onClick: () => void // Callback appelé au clic
  loading?: boolean // Afficher l'état de chargement
  disabled?: boolean // Désactiver le bouton
  children?: React.ReactNode // Contenu du bouton
  className?: string // Classes CSS supplémentaires
}
```

#### Exemple

```tsx
<SearchButton onClick={handleSearch} loading={isSearching} disabled={!imageSelected}>
  Rechercher
</SearchButton>
```

## Utilisation complète

```tsx
import { ImageUpload, SearchBar, SearchButton } from '@/components/search'

function SearchPage() {
  const [image, setImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!image) return

    setLoading(true)
    const formData = new FormData()
    formData.append('image', image)

    const response = await fetch('http://localhost:5000/api/search/image', {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()
    console.log('Résultats:', data.results)
    setLoading(false)
  }

  return (
    <div>
      <ImageUpload onImageSelect={setImage} />
      <SearchButton onClick={handleSearch} loading={loading} />
    </div>
  )
}
```

## Validation des fichiers

Le composant `ImageUpload` valide automatiquement :

- **Format** : JPG, JPEG, PNG, WEBP uniquement
- **Taille** : Maximum 16MB par défaut (configurable)
- **Fichier vide** : Rejeté automatiquement

## Accès caméra

Sur mobile, le bouton "Prendre une photo" ouvre directement la caméra.
Sur desktop, il ouvre le sélecteur de fichier avec option caméra (si disponible).

## Styles

Les composants utilisent Tailwind CSS et les composants UI de shadcn/ui.
Ils sont responsive et s'adaptent automatiquement aux différentes tailles d'écran.
