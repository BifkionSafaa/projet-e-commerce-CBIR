'use client'

import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { ArrowLeft, ShoppingCart, Trash2 } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { useCart } from '@/contexts/CartContext'

export default function CartPage() {
  const { cartItems, cartCount, removeFromCart, clearCart } = useCart()

  // Calculer le total
  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)

  // Construire l'URL de l'image
  const getImageUrl = (imagePath: string) => {
    const imageBaseUrl = 'http://localhost:5000'
    if (imagePath.startsWith('http')) {
      return imagePath
    } else if (imagePath.startsWith('dataset/images/')) {
      return `${imageBaseUrl}/${imagePath}`
    } else {
      return `${imageBaseUrl}/dataset/images/${imagePath}`
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Link href="/">
            <Button variant="ghost" className="text-indigo-700 hover:text-indigo-900 hover:bg-indigo-100">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Retour
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-slate-700">Panier</h1>
          {cartCount > 0 && (
            <Button
              onClick={clearCart}
              variant="outline"
              size="sm"
              className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-300"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Vider le panier
            </Button>
          )}
        </div>

        {cartCount === 0 ? (
          <Card className="bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90 border-2 border-indigo-200 shadow-md">
            <CardContent className="p-12 text-center">
              <ShoppingCart className="h-16 w-16 mx-auto text-indigo-300 mb-4" />
              <h2 className="text-2xl font-semibold text-slate-700 mb-2">Votre panier est vide</h2>
              <p className="text-slate-600 mb-6">Ajoutez des produits pour commencer vos achats</p>
              <Link href="/">
                <Button className="bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white">
                  Continuer les achats
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Liste des produits */}
            <div className="lg:col-span-2 space-y-4">
              {cartItems.map((item) => (
                <Card key={item.productId} className="bg-white border-2 border-slate-200 shadow-md">
                  <CardContent className="p-4">
                    <div className="flex gap-4">
                      {/* Image */}
                      <div className="relative w-24 h-24 bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg overflow-hidden flex-shrink-0">
                        <Image
                          src={getImageUrl(item.image_path)}
                          alt={item.name}
                          fill
                          className="object-contain"
                          sizes="96px"
                          unoptimized={
                            getImageUrl(item.image_path).startsWith('http://localhost:5000') ||
                            getImageUrl(item.image_path).startsWith('http://127.0.0.1:5000')
                          }
                        />
                      </div>

                      {/* Informations */}
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-slate-700 mb-1 line-clamp-2">{item.name}</h3>
                        <p className="text-lg font-bold text-indigo-600 mb-2">
                          ${(item.price * item.quantity).toFixed(2)}
                        </p>
                        <div className="flex items-center gap-4">
                          <span className="text-sm text-slate-500">
                            Quantité: <span className="font-semibold text-slate-700">{item.quantity}</span>
                          </span>
                          <span className="text-sm text-slate-500">
                            Prix unitaire: <span className="font-semibold text-slate-700">${item.price.toFixed(2)}</span>
                          </span>
                        </div>
                      </div>

                      {/* Bouton supprimer */}
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeFromCart(item.productId)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50 flex-shrink-0"
                      >
                        <Trash2 className="h-5 w-5" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Résumé */}
            <div className="lg:col-span-1">
              <Card className="bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90 border-2 border-indigo-200 shadow-md sticky top-24">
                <CardHeader>
                  <h2 className="text-xl font-semibold text-slate-700">Résumé</h2>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between text-slate-600">
                    <span>Articles ({cartCount})</span>
                    <span className="font-semibold text-indigo-700">${total.toFixed(2)}</span>
                  </div>
                  <Separator className="bg-indigo-200" />
                  <div className="flex justify-between text-lg font-bold text-slate-700">
                    <span>Total</span>
                    <span className="text-indigo-600">${total.toFixed(2)}</span>
                  </div>
                  <Button
                    className="w-full bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white shadow-md"
                    size="lg"
                  >
                    Passer la commande
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

