'use client'

import React, { useState, useEffect, useMemo } from 'react'
import { SearchBar } from '@/components/search'
import { ProductGrid, Product } from '@/components/products'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { RefreshCw, Filter, X, ShoppingCart, Image as ImageIcon, Search, Package, Heart, User, Share2, Mail, Phone, Truck, ShieldCheck, Umbrella, Headset } from 'lucide-react'
import { getRandomProducts, getCategories, searchByImage, searchByText } from '@/lib/api'
import type { CategoryItem } from '@/lib/api'
import { SUBCATEGORIES } from '@/lib/subcategories'
import { SITE_CONTACT } from '@/lib/site-config'
import { CategoryStrip } from '@/components/categories'
import { toast } from 'sonner'
import { ProductCardSkeleton } from '@/components/products'
import { useCart } from '@/contexts/CartContext'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { ArrowRight } from 'lucide-react'

// Image de la bannière promo (AirPods / BLACK WEEK) : remplacez public/banner-promo.png pour changer
const PROMO_BANNER_IMAGE = '/banner-promo.png'
const PROMO_BANNER_FALLBACK = '/placeholder.jpg'

export default function Page() {
  const router = useRouter()
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [searchResults, setSearchResults] = useState<Product[]>([])
  const [randomProducts, setRandomProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [loadingRandom, setLoadingRandom] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { cartCount } = useCart()

  // Type de recherche
  const [searchType, setSearchType] = useState<'image' | 'text' | null>(null)

  // Filtres pour les résultats
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [colorFilter, setColorFilter] = useState<string>('all')
  const [minPrice, setMinPrice] = useState<string>('')
  const [maxPrice, setMaxPrice] = useState<string>('')
  const [sortBy, setSortBy] = useState<string>('similarity')
  const [searchResetKey, setSearchResetKey] = useState(0)
  const [promoBannerSrc, setPromoBannerSrc] = useState(PROMO_BANNER_IMAGE)
  const [categories, setCategories] = useState<CategoryItem[]>([])
  const [loadingCategories, setLoadingCategories] = useState(false)

  // Charger les produits et catégories au démarrage
  useEffect(() => {
    fetchRandomProducts()
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    setLoadingCategories(true)
    try {
      const list = await getCategories()
      setCategories(list)
    } catch (err) {
      console.error('Error fetching categories:', err)
    } finally {
      setLoadingCategories(false)
    }
  }

  // Sous-catégories (peluche, poupée, robot...) avec image si dispo depuis l'API
  const subcategoryItems = useMemo(() => {
    const byName = new Map(categories.map(c => [c.category.toLowerCase().trim(), c.image_path]))
    return SUBCATEGORIES.map(cat => ({
      category: cat,
      image_path: byName.get(cat.toLowerCase()) ?? null,
    }))
  }, [categories])

  const fetchRandomProducts = async () => {
    setLoadingRandom(true)
    setError(null)

    try {
      const products = await getRandomProducts(8)
      setRandomProducts(products)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du chargement des produits')
      console.error('Error fetching random products:', err)
    } finally {
      setLoadingRandom(false)
    }
  }


  const handleImageSelect = async (file: File) => {
    setSelectedImage(file)
    setError(null)
    setSearchResults([])
  }

  const handleSearchByText = async (query: string) => {
    if (!query.trim()) {
      toast.error('Veuillez entrer un terme de recherche')
      setError('Veuillez entrer un terme de recherche')
      return
    }

    setLoading(true)
    setError(null)
    setSearchType('text')
    toast.loading('Recherche en cours...', { id: 'text-search' })

    try {
      const result = await searchByText(query, 50)
      setSearchResults(result.results || [])
      toast.success(`${result.results?.length || 0} résultat(s) trouvé(s)`, { id: 'text-search' })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Une erreur est survenue'
      setError(errorMessage)
      toast.error(errorMessage, { id: 'text-search' })
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleImageSearch = async (file?: File) => {
    const imageToSearch = file ?? selectedImage
    if (!imageToSearch) {
      toast.error('Veuillez sélectionner une image')
      setError('Veuillez sélectionner une image')
      return
    }

    setLoading(true)
    setError(null)
    setSearchType('image')
    setCategoryFilter('all')
    toast.loading("Analyse de l'image en cours...", { id: 'image-search' })

    try {
      const result = await searchByImage(imageToSearch, 50, 0.5)
      setSearchResults(result.results || [])
      toast.success(`${result.results?.length || 0} produit(s) similaire(s) trouvé(s)`, {
        id: 'image-search',
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Une erreur est survenue'
      setError(errorMessage)
      toast.error(errorMessage, { id: 'image-search' })
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const resetSearch = () => {
    setSearchResults([])
    setSearchType(null)
    setSelectedImage(null)
    setError(null)
    setCategoryFilter('all')
    setColorFilter('all')
    setMinPrice('')
    setMaxPrice('')
    setSortBy('similarity')
    // Réinitialiser le champ de recherche
    setSearchResetKey(prev => prev + 1)
    // Scroll vers le haut pour voir la section hero
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Calculer les résultats filtrés
  const filteredResults = useMemo(() => {
    let filtered = [...searchResults]

    if (searchType === 'text' && categoryFilter !== 'all') {
      filtered = filtered.filter(p => p.category === categoryFilter)
    }

    if (colorFilter !== 'all') {
      filtered = filtered.filter(
        p => p.color && p.color.toLowerCase() === colorFilter.toLowerCase()
      )
    }

    if (minPrice) {
      const min = parseFloat(minPrice)
      if (!isNaN(min)) filtered = filtered.filter(p => p.price >= min)
    }
    if (maxPrice) {
      const max = parseFloat(maxPrice)
      if (!isNaN(max)) filtered = filtered.filter(p => p.price <= max)
    }

    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'similarity':
          return (b.similarity_score || 0) - (a.similarity_score || 0)
        case 'price-asc':
          return a.price - b.price
        case 'price-desc':
          return b.price - a.price
        case 'name':
          return a.name.localeCompare(b.name)
        default:
          return 0
      }
    })

    return filtered
  }, [searchResults, categoryFilter, colorFilter, minPrice, maxPrice, sortBy, searchType])

  // Fonction pour obtenir l'URL de l'image
  const getImageUrl = (product: Product) => {
    const imageBaseUrl = 'http://localhost:5000'
    if (product.image_path.startsWith('http')) {
      return product.image_path
    } else if (product.image_path.startsWith('dataset/images/')) {
      return `${imageBaseUrl}/${product.image_path}`
    } else {
      return `${imageBaseUrl}/dataset/images/${product.image_path}`
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20">
      {/* Header unifié : plus de hauteur, nav centrée, partage / réseaux / contact à côté de la recherche */}
      <header className="sticky top-0 z-50 bg-gradient-to-r from-blue-100 via-indigo-50 to-violet-100 backdrop-blur-sm border-b border-indigo-200 shadow-sm">
        <div className="container mx-auto px-4 py-3 md:py-4">
          {/* Ligne 1 : Logo | Nav centrée | Connexion */}
          <div className="flex items-center justify-between gap-4 mb-4 md:mb-5">
            <Link href="/" className="flex items-center gap-2 shrink-0">
              <div className="relative h-9 w-9 md:h-10 md:w-10 rounded-lg bg-gradient-to-br from-blue-400 to-purple-400 flex items-center justify-center shadow-md shadow-blue-200">
                <ImageIcon className="h-4 w-4 text-white" />
                <Search className="h-2.5 w-2.5 text-white absolute -bottom-0.5 -right-0.5 bg-blue-500 rounded-full p-0.5" />
                <Package className="h-3 w-3 text-white absolute top-0.5 left-0.5 opacity-80" />
              </div>
              <h1 className="text-lg md:text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hidden sm:block">
                CBIR E-Commerce
              </h1>
            </Link>

            <nav className="absolute left-1/2 -translate-x-1/2 flex items-center gap-4 md:gap-6 text-sm font-medium">
              <Link href="/" className="text-indigo-700 hover:text-indigo-900 transition-colors">Accueil</Link>
              <Link href="/" className="text-indigo-700 hover:text-indigo-900 transition-colors">Boutique</Link>
              <Link href="/" className="text-indigo-700 hover:text-indigo-900 transition-colors">Produits</Link>
            </nav>

            <Link href="/" className="hidden sm:flex items-center gap-2 text-sm font-medium text-indigo-700 hover:text-indigo-900 shrink-0">
              <User className="h-4 w-4" />
              Connexion
            </Link>
          </div>

          {/* Ligne 2 : Recherche au centre | Partager, Réseaux, Contact à côté | Retour/Favoris/Panier — alignés en haut pour ne pas descendre avec l'aperçu image */}
          <div className="flex items-start gap-2 md:gap-3">
            <div className="flex-1 min-w-0 hidden sm:block" aria-hidden />
            <div className="w-full sm:w-auto sm:max-w-sm md:max-w-md flex justify-center shrink-0">
              <SearchBar
                onSearch={handleSearchByText}
                placeholder="Rechercher produit, marque..."
                disabled={loading}
                resetKey={searchResetKey}
                showCameraButton
                onImageSelect={handleImageSelect}
                selectedImage={selectedImage}
                onClearImage={() => { setSelectedImage(null); setError(null) }}
                onImageSearch={handleImageSearch}
                imageSearchLoading={loading}
              />
            </div>
            <div className="flex items-center gap-1 md:gap-0.5 shrink-0 h-12 self-start">
              <Button variant="ghost" size="icon" className="h-9 w-9 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-100" title="Partager">
                <Share2 className="h-4 w-4" />
              </Button>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="inline-flex h-9 w-9 items-center justify-center rounded-md text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800" aria-label="Facebook">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="inline-flex h-9 w-9 items-center justify-center rounded-md text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800" aria-label="Instagram">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="inline-flex h-9 w-9 items-center justify-center rounded-md text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800" aria-label="Twitter">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </a>
              <Button variant="ghost" size="icon" className="h-9 w-9 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-100 hidden sm:flex" title="Contact" asChild>
                <a href={`mailto:${SITE_CONTACT.email}`}><Mail className="h-4 w-4" /></a>
              </Button>
              <Button variant="ghost" size="icon" className="h-9 w-9 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-100 hidden sm:flex" title="Téléphone" asChild>
                <a href={`tel:${SITE_CONTACT.phone.replace(/\s/g, '')}`}><Phone className="h-4 w-4" /></a>
              </Button>
            </div>
            <div className="flex-1 min-w-0 flex justify-end items-center gap-1 self-start">
              {searchResults.length > 0 && (
                <Button onClick={resetSearch} variant="ghost" size="sm" className="text-indigo-700 hover:text-indigo-900 hover:bg-indigo-100">
                  <X className="h-4 w-4 mr-1 sm:mr-2" />
                  <span className="hidden sm:inline">Retour</span>
                </Button>
              )}
              <Button variant="ghost" size="icon" className="h-10 w-10 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-100" title="Favoris">
                <Heart className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" onClick={() => router.push('/cart')} className="relative h-10 w-10 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-100 transition-all">
                <ShoppingCart className="h-5 w-5" />
                {cartCount > 0 && (
                  <span className="absolute -top-0.5 -right-0.5 h-5 w-5 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 text-white text-xs font-bold flex items-center justify-center">
                    {cartCount > 99 ? '99+' : cartCount}
                  </span>
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Section promotionnelle : fond de section inchangé, seule la carte reprend le style du header */}
      <section className="w-full bg-gradient-to-r from-slate-50 to-blue-50/50 border-b border-slate-200">
        <div className="mx-auto w-full max-w-[1400px] px-3 sm:px-5 md:px-6 lg:px-8 py-8 md:py-10">
          <div className="flex flex-col md:flex-row items-center gap-6 md:gap-10 rounded-2xl overflow-hidden bg-gradient-to-r from-blue-100/90 via-indigo-50/95 to-violet-100/90 shadow-lg border border-indigo-200 min-h-[280px] md:min-h-[340px]">
            <div className="flex-1 p-8 md:p-12 order-2 md:order-1">
              <span className="inline-block px-3 py-1 rounded-full bg-indigo-200/80 text-indigo-800 text-sm font-medium mb-4">
                Offre du moment
              </span>
              <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-3">
                Découvrez nos produits avec la recherche visuelle
              </h2>
              <p className="text-slate-700 mb-6 max-w-lg">
                Trouvez en un clic des articles similaires à l&apos;image de votre choix. Recherchez par photo ou par texte.
              </p>
              <Button
                onClick={() => document.getElementById('search-bar')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white shadow-md"
              >
                Rechercher maintenant
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
            <div className="w-full md:w-[45%] min-h-[260px] md:min-h-[340px] relative order-1 md:order-2 bg-slate-100">
              <Image
                src={promoBannerSrc}
                alt="Promotion"
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 45vw"
                onError={() => setPromoBannerSrc(PROMO_BANNER_FALLBACK)}
                priority
              />
            </div>
          </div>
        </div>
      </section>

      <div id="search-bar" className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Bandeau catégories / sous-catégories : clic = recherche par catégorie */}
        {searchResults.length === 0 && (
          <>
            <div className="mb-8">
              <CategoryStrip
                items={subcategoryItems}
                onCategoryClick={handleSearchByText}
                loading={loadingCategories}
              />
            </div>

            {/* Section avantages : livraison, paiement, garantie, support */}
            <section className="w-full mb-10">
              <div className="w-full h-1.5 bg-gradient-to-r from-blue-100 via-indigo-100 to-violet-100" aria-hidden />
              <div className="bg-white py-10 px-4">
                <div className="container mx-auto max-w-6xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-indigo-600">
                      <Truck className="h-6 w-6" />
                    </div>
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-800 mb-1">Livraison gratuite</h3>
                    <p className="text-sm text-slate-600">Pour les commandes au Maroc ou dès un certain montant d&apos;achat.</p>
                  </div>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-indigo-600">
                      <ShieldCheck className="h-6 w-6" />
                    </div>
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-800 mb-1">Paiement sécurisé</h3>
                    <p className="text-sm text-slate-600">Nous acceptons Visa, Mastercard, PayPal et autres moyens de paiement sécurisés.</p>
                  </div>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-indigo-600">
                      <Umbrella className="h-6 w-6" />
                    </div>
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-800 mb-1">Garantie 1 an</h3>
                    <p className="text-sm text-slate-600">Tous nos produits sont couverts un an contre les défauts de fabrication.</p>
                  </div>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-indigo-600">
                      <Headset className="h-6 w-6" />
                    </div>
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-800 mb-1">Support 24/7</h3>
                    <p className="text-sm text-slate-600">Contactez-nous 24h/24, 7j/7. Tél : {SITE_CONTACT.phone}</p>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}

        {error && selectedImage && (
          <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-400 rounded-md">
            <p className="text-sm text-red-700 font-medium">{error}</p>
          </div>
        )}

        {/* Résultats de recherche avec filtres */}
        {searchResults.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold text-slate-700">
                Résultats de recherche
                <span className="text-slate-500 text-xl font-normal ml-2">({searchResults.length})</span>
              </h2>
              <Button
                onClick={resetSearch}
                variant="outline"
                size="sm"
                className="flex items-center gap-2 border-slate-300 text-slate-600 hover:bg-slate-100 hover:border-slate-400"
              >
                <X className="h-4 w-4" />
                Retour à l'accueil
              </Button>
            </div>

            {/* Filtres et tri : fond assorti au thème (bleu-indigo-violet) */}
            <Card className="mb-6 bg-gradient-to-r from-blue-100/90 via-indigo-50/95 to-violet-100/90 border-2 border-indigo-200 shadow-md">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold flex items-center gap-2 text-slate-800">
                    <Filter className="h-5 w-5 text-indigo-600" />
                    Filtres
                  </h3>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setCategoryFilter('all')
                      setColorFilter('all')
                      setMinPrice('')
                      setMaxPrice('')
                      setSortBy('similarity')
                    }}
                    className="text-xs text-slate-700 hover:text-slate-900 hover:bg-indigo-100/80"
                  >
                    <X className="h-4 w-4 mr-1" />
                    Réinitialiser
                  </Button>
                </div>

                <div
                  className={`grid grid-cols-1 ${searchType === 'text' ? 'md:grid-cols-5' : 'md:grid-cols-4'} gap-4`}
                >
                  {searchType === 'text' && (
                    <div>
                      <Label htmlFor="category" className="text-slate-700">Catégorie</Label>
                      <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                        <SelectTrigger id="category" className="bg-white border-slate-300 text-slate-700">
                          <SelectValue placeholder="Toutes" />
                        </SelectTrigger>
                        <SelectContent className="bg-white border-slate-200 shadow-lg">
                          <SelectItem value="all">Toutes les catégories</SelectItem>
                          {Array.from(new Set(searchResults.map(p => p.category)))
                            .sort()
                            .map(cat => (
                              <SelectItem key={cat} value={cat}>
                                {cat}
                              </SelectItem>
                            ))}
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  <div>
                    <Label htmlFor="color" className="text-slate-700">Couleur</Label>
                    <Select value={colorFilter} onValueChange={setColorFilter}>
                      <SelectTrigger id="color" className="bg-white border-slate-300 text-slate-700">
                        <SelectValue placeholder="Toutes" />
                      </SelectTrigger>
                      <SelectContent className="bg-white border-slate-200 shadow-lg">
                        <SelectItem value="all">Toutes les couleurs</SelectItem>
                        {Array.from(new Set(searchResults.map(p => p.color).filter(c => c)))
                          .sort()
                          .map(color => (
                            <SelectItem key={color} value={color || ''}>
                              {color}
                            </SelectItem>
                          ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="minPrice" className="text-slate-700">Prix min</Label>
                    <Input
                      id="minPrice"
                      type="number"
                      placeholder="0"
                      value={minPrice}
                      onChange={e => setMinPrice(e.target.value)}
                      className="bg-white border-slate-300 text-slate-700"
                    />
                  </div>

                  <div>
                    <Label htmlFor="maxPrice" className="text-slate-700">Prix max</Label>
                    <Input
                      id="maxPrice"
                      type="number"
                      placeholder="1000"
                      value={maxPrice}
                      onChange={e => setMaxPrice(e.target.value)}
                      className="bg-white border-slate-300 text-slate-700"
                    />
                  </div>

                  <div>
                    <Label htmlFor="sort" className="text-slate-700">Trier par</Label>
                    <Select value={sortBy} onValueChange={setSortBy}>
                      <SelectTrigger id="sort" className="bg-white border-slate-300 text-slate-700">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-white border-slate-200 shadow-lg">
                        <SelectItem value="similarity">Pertinence</SelectItem>
                        <SelectItem value="price-asc">Prix croissant</SelectItem>
                        <SelectItem value="price-desc">Prix décroissant</SelectItem>
                        <SelectItem value="name">Nom (A-Z)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Résultats filtrés */}
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {Array.from({ length: 8 }).map((_, i) => (
                  <ProductCardSkeleton key={i} />
                ))}
              </div>
            ) : (
              <ProductGrid products={filteredResults} showSimilarity={false} loading={false} />
            )}
          </div>
        )}

        {/* Produits recommandés (affichés quand il n'y a pas de résultats de recherche) */}
        {searchResults.length === 0 && (
          <div className="mb-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-slate-700">Produits recommandés</h2>
              <Button
                onClick={fetchRandomProducts}
                disabled={loadingRandom}
                variant="outline"
                size="sm"
                className="flex items-center gap-2 border-slate-300 text-slate-600 hover:bg-slate-100 hover:border-slate-400"
              >
                <RefreshCw className={`h-4 w-4 ${loadingRandom ? 'animate-spin' : ''}`} />
                Rafraîchir
              </Button>
            </div>

            {loadingRandom ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {Array.from({ length: 8 }).map((_, i) => (
                  <ProductCardSkeleton key={i} />
                ))}
              </div>
            ) : randomProducts.length > 0 ? (
              <ProductGrid products={randomProducts} showSimilarity={false} loading={false} />
            ) : (
              <Card className="bg-white border-2 border-slate-200 shadow-md">
                <CardContent className="p-6 text-center">
                  <p className="text-slate-600">Aucun produit disponible</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
