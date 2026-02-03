'use client'

import React, { useState, useEffect, useRef } from 'react'
import { ProductCard, Product } from './ProductCard'
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-react'

interface ProductGridProps {
  products: Product[]
  loading?: boolean
  showSimilarity?: boolean
  columns?: {
    mobile?: number
    tablet?: number
    desktop?: number
    wide?: number
  }
  onLoadMore?: () => void
  hasMore?: boolean
  className?: string
  imageBaseUrl?: string
}

export function ProductGrid({
  products,
  loading = false,
  showSimilarity = false,
  columns = {
    mobile: 1,
    tablet: 2,
    desktop: 3,
    wide: 4,
  },
  onLoadMore,
  hasMore = false,
  className,
  imageBaseUrl,
}: ProductGridProps) {
  const [isIntersecting, setIsIntersecting] = useState(false)
  const loadMoreRef = useRef<HTMLDivElement>(null)

  // Infinite scroll avec Intersection Observer
  useEffect(() => {
    if (!onLoadMore || !hasMore || loading) return

    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) {
          setIsIntersecting(true)
          onLoadMore?.()
        } else {
          setIsIntersecting(false)
        }
      },
      { threshold: 0.1 }
    )

    if (loadMoreRef.current) {
      observer.observe(loadMoreRef.current)
    }

    return () => {
      if (loadMoreRef.current) {
        observer.unobserve(loadMoreRef.current)
      }
    }
  }, [onLoadMore, hasMore, loading])

  if (loading && products.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
        <span className="ml-2 text-gray-500">Chargement des produits...</span>
      </div>
    )
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">Aucun produit trouvé</p>
      </div>
    )
  }

  return (
    <div className={cn('w-full', className)}>
      {/* Grille responsive */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 md:gap-4">
        {products.map((product, index) => (
          <div
            key={product.id}
            className="animate-in fade-in slide-in-from-bottom-4"
            style={{
              animationDelay: `${index * 50}ms`,
              animationFillMode: 'both',
            }}
          >
            <ProductCard
              product={product}
              showSimilarity={showSimilarity}
              imageBaseUrl={imageBaseUrl}
            />
          </div>
        ))}
      </div>

      {/* Infinite scroll trigger */}
      {onLoadMore && hasMore && (
        <div ref={loadMoreRef} className="h-20 flex items-center justify-center">
          {loading && (
            <div className="flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin text-gray-400" />
              <span className="text-sm text-gray-500">Chargement...</span>
            </div>
          )}
        </div>
      )}

      {/* Message si plus de produits */}
      {!hasMore && products.length > 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500 text-sm">Tous les produits ont été chargés</p>
        </div>
      )}
    </div>
  )
}
