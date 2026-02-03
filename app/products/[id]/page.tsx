'use client'

import React, { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, ShoppingCart, Loader2 } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { useCart } from '@/contexts/CartContext'

interface Product {
  id: number
  name: string
  category: string
  price: number
  description: string
  brand: string | null
  color: string | null
  image_path: string
}

export default function ProductDetailPage() {
  const params = useParams()
  const router = useRouter()
  const productId = params.id as string
  const { addToCart } = useCart()

  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProduct = async () => {
      if (!productId) return

      setLoading(true)
      setError(null)

      try {
        const response = await fetch(`http://localhost:5000/api/products/${productId}`)

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Produit non trouvé')
          }
          throw new Error('Erreur lors du chargement du produit')
        }

        const data = await response.json()
        setProduct(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Une erreur est survenue')
      } finally {
        setLoading(false)
      }
    }

    fetchProduct()
  }, [productId])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-500" />
          <p className="mt-4 text-slate-600">Chargement du produit...</p>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 flex items-center justify-center">
        <Card className="max-w-md bg-white border-2 border-slate-200 shadow-md">
          <CardContent className="p-6 text-center">
            <p className="text-red-600 mb-4">{error || 'Produit non trouvé'}</p>
            <Button onClick={() => router.push('/')} variant="outline" className="border-slate-300 text-slate-600 hover:bg-slate-100">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Retour à l'accueil
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Construire l'URL de l'image
  // Les chemins dans la BDD sont comme "electronique/airpods_01.jpg"
  let imageUrl: string
  if (product.image_path.startsWith('http')) {
    imageUrl = product.image_path
  } else if (product.image_path.startsWith('dataset/images/')) {
    imageUrl = `http://localhost:5000/${product.image_path}`
  } else {
    // Chemin relatif simple, ajouter dataset/images/
    imageUrl = `http://localhost:5000/dataset/images/${product.image_path}`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Bouton retour */}
        <Link href="/">
          <Button variant="ghost" className="mb-6 text-slate-600 hover:text-slate-800 hover:bg-slate-100">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Retour
          </Button>
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Image du produit */}
          <Card className="overflow-hidden bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90 border-2 border-indigo-200 shadow-md">
            <div className="relative aspect-square bg-gradient-to-br from-blue-50/80 to-indigo-50/80">
              <Image
                src={imageUrl}
                alt={product.name}
                fill
                sizes="(max-width: 1024px) 100vw, min(90vw, 900px)"
                className="object-contain"
                priority
                quality={95}
                unoptimized={
                  imageUrl.startsWith('http://localhost:5000') ||
                  imageUrl.startsWith('http://127.0.0.1:5000')
                }
              />
            </div>
          </Card>

          {/* Informations du produit */}
          <div className="space-y-6">
            <Card className="bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90 border-2 border-indigo-200 shadow-md">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h1 className="text-3xl font-semibold mb-2 text-slate-700">{product.name}</h1>
                    <div className="flex gap-2 items-center">
                      <Badge variant="outline" className="border-blue-300 text-blue-700 bg-blue-50">{product.category}</Badge>
                      {product.brand && <Badge variant="secondary" className="bg-indigo-100 text-indigo-700 border-indigo-200">{product.brand}</Badge>}
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <Separator className="bg-slate-200" />

                {/* Prix */}
                <div>
                  <p className="text-sm text-slate-500 mb-1">Prix</p>
                  <p className="text-4xl font-bold text-green-600">${product.price.toFixed(2)}</p>
                </div>

                <Separator className="bg-slate-200" />

                {/* Description */}
                {product.description && (
                  <div>
                    <p className="text-sm text-slate-500 mb-2">Description</p>
                    <p className="text-slate-700 leading-relaxed">{product.description}</p>
                  </div>
                )}

                {/* Détails supplémentaires */}
                <div className="grid grid-cols-2 gap-4 pt-4">
                  {product.color && (
                    <div>
                      <p className="text-sm text-slate-500 mb-1">Couleur</p>
                      <p className="font-medium text-slate-700">{product.color}</p>
                    </div>
                  )}
                  {product.brand && (
                    <div>
                      <p className="text-sm text-slate-500 mb-1">Marque</p>
                      <p className="font-medium text-slate-700">{product.brand}</p>
                    </div>
                  )}
                </div>

                <Separator className="bg-slate-200" />

                {/* Boutons d'action */}
                <div className="flex gap-4 pt-4">
                  <Button 
                    size="lg" 
                    onClick={() => {
                      if (product) {
                        addToCart({
                          id: product.id,
                          name: product.name,
                          price: product.price,
                          image_path: product.image_path
                        })
                      }
                    }}
                    className="flex-1 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white shadow-md"
                  >
                    <ShoppingCart className="h-5 w-5 mr-2" />
                    Ajouter au panier
                  </Button>
                  <Button 
                    size="lg" 
                    variant="outline" 
                    className="flex-1 border-2 border-blue-300 text-blue-600 hover:bg-blue-50 hover:border-blue-400"
                  >
                    Acheter maintenant
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
