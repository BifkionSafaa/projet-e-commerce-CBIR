# Composants d'affichage des produits

Composants React/Next.js pour afficher les produits dans l'application CBIR E-Commerce.

## Composants

### ProductCard

Composant pour afficher une carte produit individuelle.

#### Props

```typescript
interface ProductCardProps {
  product: Product // Objet produit
  showSimilarity?: boolean // Afficher le score de similarité
  className?: string // Classes CSS supplémentaires
  imageBaseUrl?: string // URL de base pour les images
}
```

#### Interface Product

```typescript
interface Product {
  id: number
  name: string
  category: string
  price: number
  image_path: string
  description?: string
  brand?: string
  color?: string
  similarity_score?: number // Score de similarité (0-1)
}
```

#### Fonctionnalités

- ✅ Image avec lazy loading natif
- ✅ Badge de similarité (si recherche)
- ✅ Badge de catégorie
- ✅ Affichage nom, prix, marque, couleur
- ✅ Boutons "Voir détails" et "Ajouter"
- ✅ Hover effects
- ✅ Gestion d'erreur d'image (placeholder)

#### Exemple

```tsx
import { ProductCard } from '@/components/products'

const product = {
  id: 1,
  name: "AirPods Pro",
  category: "electronique",
  price: 249.99,
  image_path: "electronique/airpods_01.jpg",
  similarity_score: 0.998
}

<ProductCard
  product={product}
  showSimilarity={true}
/>
```

### ProductGrid

Composant pour afficher une grille responsive de produits.

#### Props

```typescript
interface ProductGridProps {
  products: Product[] // Liste des produits
  loading?: boolean // État de chargement
  showSimilarity?: boolean // Afficher les scores de similarité
  columns?: {
    // Nombre de colonnes par breakpoint
    mobile?: number // Défaut: 1
    tablet?: number // Défaut: 2
    desktop?: number // Défaut: 3
    wide?: number // Défaut: 4
  }
  onLoadMore?: () => void // Callback pour infinite scroll
  hasMore?: boolean // Y a-t-il plus de produits ?
  className?: string // Classes CSS supplémentaires
  imageBaseUrl?: string // URL de base pour les images
}
```

#### Fonctionnalités

- ✅ Grille responsive (mobile, tablette, desktop)
- ✅ Lazy loading des images
- ✅ Infinite scroll (optionnel)
- ✅ États de chargement
- ✅ Message si aucun produit

#### Exemple

```tsx
import { ProductGrid } from '@/components/products'

;<ProductGrid
  products={products}
  loading={isLoading}
  showSimilarity={true}
  onLoadMore={handleLoadMore}
  hasMore={hasMoreProducts}
/>
```

### Page de détails produit

Page dédiée pour afficher les détails complets d'un produit.

**Route** : `/products/[id]`

#### Fonctionnalités

- ✅ Affichage image en grand format
- ✅ Toutes les informations du produit
- ✅ Description complète
- ✅ Boutons d'action (Ajouter au panier, Acheter)
- ✅ Navigation retour
- ✅ Gestion d'erreurs (produit non trouvé)
- ✅ État de chargement

#### Exemple d'utilisation

```tsx
// Navigation vers la page de détails
<Link href={`/products/${product.id}`}>Voir détails</Link>
```

## Utilisation complète

```tsx
import { ProductGrid, ProductCard } from '@/components/products'
import { useState, useEffect } from 'react'

function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    setLoading(true)
    const response = await fetch('http://localhost:5000/api/products/random?count=12')
    const data = await response.json()
    setProducts(data)
    setLoading(false)
  }

  return (
    <div>
      <h1>Nos produits</h1>
      <ProductGrid products={products} loading={loading} showSimilarity={false} />
    </div>
  )
}
```

## Infinite Scroll

Pour activer l'infinite scroll :

```tsx
const [page, setPage] = useState(1)
const [hasMore, setHasMore] = useState(true)

const handleLoadMore = async () => {
  const nextPage = page + 1
  const response = await fetch(`/api/products?page=${nextPage}`)
  const data = await response.json()

  if (data.length === 0) {
    setHasMore(false)
  } else {
    setProducts([...products, ...data])
    setPage(nextPage)
  }
}

;<ProductGrid products={products} onLoadMore={handleLoadMore} hasMore={hasMore} />
```

## Responsive Design

La grille s'adapte automatiquement :

- **Mobile** : 1 colonne
- **Tablette** : 2 colonnes
- **Desktop** : 3 colonnes
- **Large** : 4 colonnes

## Lazy Loading

Les images utilisent le lazy loading natif du navigateur (`loading="lazy"`).
Cela améliore les performances en ne chargeant que les images visibles.

## Styles

Les composants utilisent Tailwind CSS et les composants UI de shadcn/ui.
Ils sont entièrement responsive et accessibles.
