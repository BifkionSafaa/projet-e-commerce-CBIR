'use client'

import React, { useRef } from 'react'
import { ChevronLeft, ChevronRight, Package, Camera, Headphones, Watch, Smartphone, Laptop, Bot, Shirt, CircleUser } from 'lucide-react'
import { Button } from '@/components/ui/button'

const IMAGE_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export interface SubcategoryItem {
  category: string
  image_path: string | null
}

function getCategoryImageUrl(imagePath: string): string {
  if (imagePath.startsWith('http')) return imagePath
  if (imagePath.startsWith('dataset/images/')) return `${IMAGE_BASE_URL}/${imagePath}`
  return `${IMAGE_BASE_URL}/dataset/images/${imagePath}`
}

const iconClass = 'text-indigo-500'

const IconRobe = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M12 2v4l2 2h-4l2-2V2a2 2 0 0 0-4 0v4l2 2H8l2-2V2z" />
    <path d="M6 8h12l-1 14H7L6 8z" />
  </svg>
)
const IconJeans = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M6 4h4v16H6zM14 4h4v16h-4z" />
    <path d="M6 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2H6V4z" />
  </svg>
)
const IconChemise = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M20 4v16H4V4" />
    <path d="M12 4v6l4 2" />
    <path d="M12 10l-4 2" />
    <path d="M12 4h6l-2 4" />
    <path d="M12 4H6L8 8" />
  </svg>
)
const IconPull = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M6 4h12v4l-2 2H8L6 8V4z" />
    <path d="M6 8v12h12V8" />
    <path d="M10 12h4" />
  </svg>
)
const IconJupe = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M12 4c-4 0-6 8-6 12h12c0-4-2-12-6-12z" />
    <path d="M12 4v16" />
  </svg>
)
const IconShort = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M6 6h4v12H6zM14 6h4v12h-4z" />
    <path d="M6 6a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2H6V6z" />
  </svg>
)
const IconVeste = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M12 2v4l3 2h2l2-4" />
    <path d="M12 2v4l-3 2H7L5 4" />
    <path d="M5 8h14v12H5z" />
    <path d="M12 8v12" />
  </svg>
)

const CATEGORY_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  peluche: Package,
  poupée: CircleUser,
  robot: Bot,
  casque: Headphones,
  airpods: Headphones,
  écouteurs: Headphones,
  caméra: Camera,
  montre: Watch,
  drone: Package,
  ordinateur: Laptop,
  smartphone: Smartphone,
  tablette: Smartphone,
  audio: Headphones,
  électronique: Package,
  robes: IconRobe,
  jeans: IconJeans,
  't-shirt': Shirt,
  chemise: IconChemise,
  pull: IconPull,
  jupe: IconJupe,
  short: IconShort,
  veste: IconVeste,
}

function getIconForCategory(category: string): React.ComponentType<{ className?: string }> {
  const key = category.toLowerCase().trim()
  return CATEGORY_ICONS[key] ?? Package
}

interface CategoryStripProps {
  items: SubcategoryItem[]
  onCategoryClick: (category: string) => void
  loading?: boolean
}

export function CategoryStrip({ items, onCategoryClick, loading }: CategoryStripProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scroll = (dir: 'left' | 'right') => {
    if (!scrollRef.current) return
    const step = scrollRef.current.clientWidth * 0.6
    scrollRef.current.scrollBy({ left: dir === 'left' ? -step : step, behavior: 'smooth' })
  }

  if (loading) {
    return (
      <div className="w-full overflow-hidden rounded-2xl bg-gradient-to-r from-blue-50 via-indigo-50/80 to-violet-50 border-y border-indigo-200 p-4">
        <div className="flex gap-4 animate-pulse max-w-[42rem] mx-auto">
          {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
            <div key={i} className="h-20 w-20 shrink-0 rounded-full bg-white border border-slate-200" />
          ))}
        </div>
      </div>
    )
  }

  if (!items.length) return null

  return (
    <div className="w-full overflow-hidden rounded-2xl bg-gradient-to-r from-blue-50 via-indigo-50/80 to-violet-50 border-y border-indigo-200 p-4">
      <div className="relative max-w-[42rem] mx-auto">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute left-2 top-1/2 z-10 h-8 w-8 -translate-y-1/2 rounded-full bg-white shadow-md hover:bg-indigo-50 border border-slate-200"
          onClick={() => scroll('left')}
          aria-label="Défiler à gauche"
        >
          <ChevronLeft className="h-4 w-4 text-indigo-700" />
        </Button>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute right-2 top-1/2 z-10 h-8 w-8 -translate-y-1/2 rounded-full bg-white shadow-md hover:bg-indigo-50 border border-slate-200"
          onClick={() => scroll('right')}
          aria-label="Défiler à droite"
        >
          <ChevronRight className="h-4 w-4 text-indigo-700" />
        </Button>

        <div
          ref={scrollRef}
          className="flex gap-6 overflow-x-auto scroll-smooth px-10 py-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
          {items.map(({ category, image_path }) => {
            const IconComponent = getIconForCategory(category)
            return (
              <button
                key={category}
                type="button"
                onClick={() => onCategoryClick(category)}
                className="flex shrink-0 flex-col items-center gap-2 transition-transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 rounded-xl p-1"
              >
                <div className="h-16 w-16 overflow-hidden rounded-full border-2 border-slate-200 bg-white shadow-sm flex items-center justify-center">
                  {image_path ? (
                    <img
                      src={getCategoryImageUrl(image_path)}
                      alt={category}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <IconComponent className={`h-8 w-8 ${iconClass}`} />
                  )}
                </div>
                <span className="max-w-[80px] truncate text-center text-sm font-medium text-slate-700 capitalize">
                  {category}
                </span>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
