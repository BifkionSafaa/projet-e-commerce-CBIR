'use client'

import React, { useState, useRef, FormEvent } from 'react'
import { Search, Camera, X } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const ACCEPTED_FORMATS = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
const MAX_SIZE_MB = 16

interface SearchBarProps {
  onSearch: (query: string) => void
  placeholder?: string
  className?: string
  disabled?: boolean
  resetKey?: number
  /** Icône caméra dans le champ pour recherche par image */
  showCameraButton?: boolean
  onImageSelect?: (file: File) => void
  selectedImage?: File | null
  onClearImage?: () => void
  /** Appelé automatiquement à la sélection d'une image (recherche immédiate) */
  onImageSearch?: (file: File) => void
  imageSearchLoading?: boolean
}

export function SearchBar({
  onSearch,
  placeholder = 'Rechercher par nom, description, catégorie ou marque...',
  className,
  disabled = false,
  resetKey = 0,
  showCameraButton = false,
  onImageSelect,
  selectedImage,
  onClearImage,
  onImageSearch,
  imageSearchLoading = false,
}: SearchBarProps) {
  const [query, setQuery] = useState('')
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [imageError, setImageError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  React.useEffect(() => {
    if (resetKey > 0) {
      setQuery('')
      setImagePreview(null)
      setImageError(null)
    }
  }, [resetKey])

  React.useEffect(() => {
    if (!selectedImage) {
      setImagePreview(null)
      setImageError(null)
    }
  }, [selectedImage])

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (query.trim() && !disabled) {
      onSearch(query.trim())
    }
  }

  const validateFile = (file: File): string | null => {
    if (!ACCEPTED_FORMATS.includes(file.type)) {
      return `Format non supporté. Utilisez: ${ACCEPTED_FORMATS.map(f => f.split('/')[1]).join(', ')}`
    }
    const maxBytes = MAX_SIZE_MB * 1024 * 1024
    if (file.size > maxBytes) return `Fichier trop volumineux (max ${MAX_SIZE_MB}MB)`
    if (file.size === 0) return 'Fichier vide'
    return null
  }

  const handleCameraClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file || !onImageSelect) return
    setImageError(null)
    const err = validateFile(file)
    if (err) {
      setImageError(err)
      return
    }
    const reader = new FileReader()
    reader.onloadend = () => setImagePreview(reader.result as string)
    reader.readAsDataURL(file)
    onImageSelect(file)
    onImageSearch?.(file)
    e.target.value = ''
  }

  const handleClearImage = () => {
    setImagePreview(null)
    setImageError(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
    onClearImage?.()
  }

  return (
    <div className={cn('w-full', className)}>
      <form onSubmit={handleSubmit} className="w-full">
        <div className="flex rounded-lg overflow-hidden border border-slate-300 bg-white shadow-sm">
          <div className="relative flex-1 flex items-center">
            <Search className="absolute left-4 h-5 w-5 text-slate-400 pointer-events-none" />
            <Input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder={placeholder}
              disabled={disabled}
              className="pl-12 pr-4 border-0 rounded-none focus-visible:ring-0 focus-visible:ring-offset-0 h-12 bg-transparent text-slate-700 placeholder:text-slate-400"
            />
          </div>
          <Button
            type="submit"
            disabled={disabled || !query.trim()}
            variant="secondary"
            size="icon"
            className="h-12 w-12 rounded-none border-l border-slate-200 bg-white hover:bg-slate-50 text-slate-700"
            title="Rechercher par texte"
          >
            <Search className="h-5 w-5" />
          </Button>
          {showCameraButton && (
            <>
              <input
                ref={fileInputRef}
                type="file"
                accept={ACCEPTED_FORMATS.join(',')}
                onChange={handleFileChange}
                className="hidden"
              />
              <Button
                type="button"
                variant="secondary"
                size="icon"
                onClick={handleCameraClick}
                disabled={disabled}
                className="h-12 w-12 rounded-none border-l border-slate-200 bg-slate-100 hover:bg-slate-200 text-slate-700"
                title="Rechercher par image"
              >
                <Camera className="h-5 w-5" />
              </Button>
            </>
          )}
        </div>
      </form>

      {/* Aperçu : uniquement l'image avec X pour supprimer (recherche lancée automatiquement) */}
      {showCameraButton && (selectedImage || imagePreview) && (
        <div className="mt-2 flex items-center gap-2 flex-wrap">
          {imagePreview && (
            <div className="relative inline-flex items-center rounded-lg border border-slate-200 bg-slate-50 overflow-hidden">
              <img
                src={imagePreview}
                alt=""
                className="h-10 w-10 object-cover"
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={handleClearImage}
                className="h-7 w-7 absolute top-0.5 right-0.5 rounded-full bg-white/90 hover:bg-white text-slate-600 shadow-sm"
                title="Supprimer l'image"
              >
                <X className="h-3.5 w-3.5" />
              </Button>
            </div>
          )}
          {imageSearchLoading && (
            <span className="text-sm text-slate-500">Recherche en cours...</span>
          )}
          {imageError && (
            <p className="text-sm text-red-600">{imageError}</p>
          )}
        </div>
      )}
    </div>
  )
}
