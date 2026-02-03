'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { toast } from 'sonner'

interface CartItem {
  productId: number
  name: string
  price: number
  image_path: string
  quantity: number
}

interface CartContextType {
  cartItems: CartItem[]
  cartCount: number
  addToCart: (product: { id: number; name: string; price: number; image_path: string }) => void
  removeFromCart: (productId: number) => void
  clearCart: () => void
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cartItems, setCartItems] = useState<CartItem[]>([])

  // Charger le panier depuis localStorage au démarrage
  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      try {
        setCartItems(JSON.parse(savedCart))
      } catch (e) {
        console.error('Error loading cart from localStorage:', e)
      }
    }
  }, [])

  // Sauvegarder le panier dans localStorage à chaque changement
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cartItems))
  }, [cartItems])

  const addToCart = (product: { id: number; name: string; price: number; image_path: string }) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.productId === product.id)
      
      if (existingItem) {
        // Si le produit existe déjà, augmenter la quantité
        const updatedItems = prevItems.map(item =>
          item.productId === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
        toast.success(`${product.name} ajouté au panier (${existingItem.quantity + 1}x)`)
        return updatedItems
      } else {
        // Nouveau produit
        const newItems = [...prevItems, {
          productId: product.id,
          name: product.name,
          price: product.price,
          image_path: product.image_path,
          quantity: 1
        }]
        toast.success(`${product.name} ajouté au panier`, {
          description: 'Le produit a été ajouté avec succès',
        })
        return newItems
      }
    })
  }

  const removeFromCart = (productId: number) => {
    setCartItems(prevItems => {
      const itemToRemove = prevItems.find(item => item.productId === productId)
      const newItems = prevItems.filter(item => item.productId !== productId)
      if (itemToRemove) {
        toast.success(`${itemToRemove.name} retiré du panier`)
      }
      return newItems
    })
  }

  const clearCart = () => {
    setCartItems([])
  }

  const cartCount = cartItems.reduce((total, item) => total + item.quantity, 0)

  return (
    <CartContext.Provider value={{ cartItems, cartCount, addToCart, removeFromCart, clearCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

