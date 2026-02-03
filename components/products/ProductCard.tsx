'use client'

import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Eye, ShoppingCart } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useCart } from '@/contexts/CartContext'

export interface Product {
  id: number
  name: string
  category: string
  price: number
  image_path: string
  description?: string
  brand?: string
  color?: string
  similarity_score?: number
}

interface ProductCardProps {
  product: Product
  showSimilarity?: boolean
  className?: string
  imageBaseUrl?: string
}

export function ProductCard({
  product,
  showSimilarity = false,
  className,
  imageBaseUrl = 'http://localhost:5000',
}: ProductCardProps) {
  const { addToCart } = useCart()
  
  // Construire l'URL de l'image
  // Les chemins dans la BDD sont comme "electronique/airpods_01.jpg"
  // On doit construire: http://localhost:5000/dataset/images/electronique/airpods_01.jpg
  let imageUrl: string
  if (product.image_path.startsWith('http')) {
    imageUrl = product.image_path
  } else if (product.image_path.startsWith('dataset/images/')) {
    // Chemin avec dataset/images/ déjà inclus
    imageUrl = `${imageBaseUrl}/${product.image_path}`
  } else {
    // Chemin relatif simple (ex: "electronique/airpods_01.jpg")
    // Ajouter dataset/images/ devant
    imageUrl = `${imageBaseUrl}/dataset/images/${product.image_path}`
  }

  return (
    <Card
      className={cn(
        'group overflow-hidden hover:shadow-xl transition-all duration-300 ease-in-out',
        'hover:-translate-y-1 border-2 hover:border-primary/20',
        'w-full max-w-[260px] mx-auto',
        'bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90',
        className
      )}
    >
      <div className="relative h-44 w-full bg-gradient-to-br from-blue-50/80 to-indigo-50/80 overflow-hidden">
        {/* Image : pleine largeur de la carte */}
        <Image
          src={imageUrl}
          alt={product.name}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500 ease-out"
          loading="lazy"
          quality={85}
          unoptimized={
            imageUrl.startsWith('http://localhost:5000') ||
            imageUrl.startsWith('http://127.0.0.1:5000')
          } // Désactiver l'optimisation pour les images externes
        />

        {/* Badge de similarité */}
        {showSimilarity && product.similarity_score !== undefined && (
          <Badge
            variant="secondary"
            className="absolute top-2 right-2 bg-black/70 text-white backdrop-blur-sm"
          >
            {(product.similarity_score * 100).toFixed(1)}% similaire
          </Badge>
        )}
      </div>

      <CardContent className="p-2">
        <div className="space-y-0.5">
          {/* Catégorie */}
          {product.category && (
            <p className="text-[10px] uppercase tracking-wide text-gray-400 truncate">
              {product.category}
            </p>
          )}
          {/* Nom du produit */}
          <h3 className="font-semibold text-xs line-clamp-2 min-h-[1.75rem]">{product.name}</h3>

          {/* Marque et couleur (si disponibles) */}
          {(product.brand || product.color) && (
            <div className="flex gap-1 text-[11px] text-gray-500">
              {product.brand && <span>{product.brand}</span>}
              {product.color && (
                <>
                  {product.brand && <span>•</span>}
                  <span>{product.color}</span>
                </>
              )}
            </div>
          )}

          {/* Prix */}
          <div className="flex items-center justify-between pt-0.5">
            <p className="text-base font-bold text-green-600">
              ${product.price?.toFixed(2) || '0.00'}
            </p>
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-1 pt-0.5">
            <Link href={`/products/${product.id}`} className="flex-1">
              <Button
                variant="outline"
                className="w-full transition-all duration-200 text-[11px] h-7 border-indigo-200 text-indigo-700 hover:bg-gradient-to-r hover:from-blue-500 hover:to-indigo-500 hover:text-white hover:border-transparent"
                size="sm"
              >
                <Eye className="h-2.5 w-2.5 mr-0.5" />
                Détails
              </Button>
            </Link>
            <Button
              variant="default"
              size="sm"
              onClick={(e) => {
                e.preventDefault()
                addToCart({
                  id: product.id,
                  name: product.name,
                  price: product.price,
                  image_path: product.image_path
                })
              }}
              className="flex-1 transition-all duration-200 hover:bg-primary/90 hover:scale-105 active:scale-95 text-[11px] h-7 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white"
            >
              <ShoppingCart className="h-2.5 w-2.5 mr-0.5" />
              Ajouter
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
