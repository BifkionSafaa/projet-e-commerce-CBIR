'use client'

import React, { useState, useEffect, useMemo } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
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
import { ArrowLeft, Filter, X } from 'lucide-react'
import { searchByImage, searchByText, ProductFilters, getProducts } from '@/lib/api'
import Image from 'next/image'

export default function SearchPage() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const [results, setResults] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [queryImage, setQueryImage] = useState<string | null>(null)

  // Filtres
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [minPrice, setMinPrice] = useState<string>('')
  const [maxPrice, setMaxPrice] = useState<string>('')
  const [sortBy, setSortBy] = useState<string>('similarity')

  // Pagination
  const [currentPage, setCurrentPage] = useState<number>(1)
  const itemsPerPage = 12

  // Extraire les paramètres de l'URL
  const searchType = searchParams.get('type') // 'image' ou 'text'
  const searchQuery = searchParams.get('query') // texte ou image data URL

  // Catégories uniques pour le filtre
  const categories = useMemo(() => {
    const cats = new Set(results.map(p => p.category))
    return Array.from(cats).sort()
  }, [results])

  // Charger les résultats au montage
  useEffect(() => {
    if (searchType === 'image' && searchQuery) {
      // Recherche par image - l'image est stockée dans sessionStorage
      const imageData = sessionStorage.getItem('searchImage')
      if (imageData) {
        setQueryImage(imageData)
        // Convertir data URL en File pour la recherche
        fetch(imageData)
          .then(res => res.blob())
          .then(blob => {
            const file = new File([blob], 'search.jpg', { type: 'image/jpeg' })
            performImageSearch(file)
          })
          .catch(err => {
            setError("Erreur lors du chargement de l'image")
            console.error(err)
          })
      }
    } else if (searchType === 'text' && searchQuery) {
      performTextSearch(searchQuery)
    }
  }, [searchType, searchQuery])

  const performImageSearch = async (file: File) => {
    setLoading(true)
    setError(null)

    try {
      const result = await searchByImage(file, 50, 0.85)
      setResults(result.results || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la recherche')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const performTextSearch = async (query: string) => {
    setLoading(true)
    setError(null)

    try {
      const result = await searchByText(query, 50)
      setResults(result.results || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la recherche')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  // Appliquer les filtres
  const filteredResults = useMemo(() => {
    let filtered = [...results]

    // Filtre par catégorie
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(p => p.category === categoryFilter)
    }

    // Filtre par prix
    if (minPrice) {
      const min = parseFloat(minPrice)
      if (!isNaN(min)) {
        filtered = filtered.filter(p => p.price >= min)
      }
    }

    if (maxPrice) {
      const max = parseFloat(maxPrice)
      if (!isNaN(max)) {
        filtered = filtered.filter(p => p.price <= max)
      }
    }

    // Tri
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'similarity':
          // Trier par score de similarité décroissant (si disponible)
          const scoreA = a.similarity_score || 0
          const scoreB = b.similarity_score || 0
          return scoreB - scoreA
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
  }, [results, categoryFilter, minPrice, maxPrice, sortBy])

  // Pagination
  const totalPages = Math.ceil(filteredResults.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedResults = filteredResults.slice(startIndex, endIndex)

  // Réinitialiser la page quand les filtres changent
  useEffect(() => {
    setCurrentPage(1)
  }, [categoryFilter, minPrice, maxPrice, sortBy])

  const clearFilters = () => {
    setCategoryFilter('all')
    setMinPrice('')
    setMaxPrice('')
    setSortBy('similarity')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-gray-900 text-white py-4">
        <div className="container mx-auto px-4">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => router.push('/')}
              className="text-white hover:bg-gray-800"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour
            </Button>
            <h1 className="text-2xl font-bold">Résultats de recherche</h1>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Filtres */}
          <aside className="lg:col-span-1">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold flex items-center gap-2">
                    <Filter className="h-5 w-5" />
                    Filtres
                  </h2>
                  <Button variant="ghost" size="sm" onClick={clearFilters} className="text-xs">
                    <X className="h-4 w-4 mr-1" />
                    Réinitialiser
                  </Button>
                </div>

                <div className="space-y-4">
                  {/* Filtre catégorie */}
                  <div>
                    <Label htmlFor="category">Catégorie</Label>
                    <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                      <SelectTrigger id="category">
                        <SelectValue placeholder="Toutes les catégories" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Toutes les catégories</SelectItem>
                        {categories.map(cat => (
                          <SelectItem key={cat} value={cat}>
                            {cat}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Filtre prix */}
                  <div>
                    <Label htmlFor="minPrice">Prix minimum</Label>
                    <Input
                      id="minPrice"
                      type="number"
                      placeholder="0"
                      value={minPrice}
                      onChange={e => setMinPrice(e.target.value)}
                    />
                  </div>

                  <div>
                    <Label htmlFor="maxPrice">Prix maximum</Label>
                    <Input
                      id="maxPrice"
                      type="number"
                      placeholder="1000"
                      value={maxPrice}
                      onChange={e => setMaxPrice(e.target.value)}
                    />
                  </div>

                  {/* Tri */}
                  <div>
                    <Label htmlFor="sort">Trier par</Label>
                    <Select value={sortBy} onValueChange={setSortBy}>
                      <SelectTrigger id="sort">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
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
          </aside>

          {/* Contenu principal */}
          <main className="lg:col-span-3">
            {/* Image de recherche (si recherche par image) */}
            {queryImage && (
              <Card className="mb-6">
                <CardContent className="p-4">
                  <h3 className="text-sm font-medium mb-2">Image recherchée :</h3>
                  <div className="relative w-32 h-32 border rounded-md overflow-hidden">
                    <Image
                      src={queryImage}
                      alt="Image de recherche"
                      fill
                      className="object-cover"
                    />
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Statistiques */}
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-gray-600">
                {loading
                  ? 'Recherche en cours...'
                  : filteredResults.length > 0
                    ? `${filteredResults.length} résultat${filteredResults.length > 1 ? 's' : ''} trouvé${filteredResults.length > 1 ? 's' : ''}`
                    : 'Aucun résultat'}
              </p>
              {filteredResults.length > itemsPerPage && (
                <p className="text-sm text-gray-500">
                  Page {currentPage} sur {totalPages}
                </p>
              )}
            </div>

            {/* Erreur */}
            {error && (
              <Card className="mb-6 border-red-200 bg-red-50">
                <CardContent className="p-4">
                  <p className="text-sm text-red-600">{error}</p>
                </CardContent>
              </Card>
            )}

            {/* Résultats */}
            {loading ? (
              <div className="text-center py-12">
                <p className="text-gray-500">Chargement des résultats...</p>
              </div>
            ) : filteredResults.length > 0 ? (
              <>
                <ProductGrid products={paginatedResults} />

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="mt-8 flex items-center justify-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                      disabled={currentPage === 1}
                    >
                      Précédent
                    </Button>

                    {/* Numéros de page */}
                    <div className="flex gap-1">
                      {Array.from({ length: totalPages }, (_, i) => i + 1)
                        .filter(page => {
                          // Afficher la première page, la dernière, la page actuelle et les pages adjacentes
                          return (
                            page === 1 ||
                            page === totalPages ||
                            (page >= currentPage - 1 && page <= currentPage + 1)
                          )
                        })
                        .map((page, index, array) => {
                          // Ajouter des ellipses si nécessaire
                          const showEllipsisBefore = index > 0 && array[index - 1] !== page - 1
                          const showEllipsisAfter =
                            index < array.length - 1 && array[index + 1] !== page + 1

                          return (
                            <React.Fragment key={page}>
                              {showEllipsisBefore && (
                                <span className="px-2 text-gray-500">...</span>
                              )}
                              <Button
                                variant={currentPage === page ? 'default' : 'outline'}
                                size="sm"
                                onClick={() => setCurrentPage(page)}
                                className="min-w-[40px]"
                              >
                                {page}
                              </Button>
                              {showEllipsisAfter && <span className="px-2 text-gray-500">...</span>}
                            </React.Fragment>
                          )
                        })}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Suivant
                    </Button>
                  </div>
                )}
              </>
            ) : (
              <Card>
                <CardContent className="p-12 text-center">
                  <p className="text-gray-500 mb-4">Aucun produit ne correspond à vos critères</p>
                  <Button onClick={clearFilters} variant="outline">
                    Réinitialiser les filtres
                  </Button>
                </CardContent>
              </Card>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}
