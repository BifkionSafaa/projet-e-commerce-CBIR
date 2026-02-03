'use client'

import React, { useRef, useState, useCallback } from 'react'
import { Upload, X, FileImage } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface ImageUploadProps {
  onImageSelect: (file: File) => void
  maxSizeMB?: number
  acceptedFormats?: string[]
  className?: string
}

export function ImageUpload({
  onImageSelect,
  maxSizeMB = 16,
  acceptedFormats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
  className,
}: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = (file: File): string | null => {
    // Vérifier le format
    if (!acceptedFormats.includes(file.type)) {
      return `Format non supporté. Formats acceptés: ${acceptedFormats.map(f => f.split('/')[1]).join(', ')}`
    }

    // Vérifier la taille
    const maxSizeBytes = maxSizeMB * 1024 * 1024
    if (file.size > maxSizeBytes) {
      return `Fichier trop volumineux. Taille maximum: ${maxSizeMB}MB`
    }

    if (file.size === 0) {
      return 'Le fichier est vide'
    }

    return null
  }

  const handleFile = useCallback(
    (file: File) => {
      setError(null)

      const validationError = validateFile(file)
      if (validationError) {
        setError(validationError)
        return
      }

      // Créer une prévisualisation
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)

      // Appeler le callback
      onImageSelect(file)
    },
    [onImageSelect, maxSizeMB, acceptedFormats]
  )

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  const handleRemove = () => {
    setPreview(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className={cn('w-full', className)}>
      {preview ? (
        <div className="relative rounded-lg border-2 border-dashed border-blue-300 bg-blue-50/50 p-3">
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-auto max-h-64 object-contain rounded-lg"
            />
            <Button
              type="button"
              variant="destructive"
              size="icon"
              className="absolute top-2 right-2 bg-red-400 hover:bg-red-500 border-red-300"
              onClick={handleRemove}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ) : (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
          className={cn(
            'relative rounded-lg border-2 border-dashed transition-all duration-300 cursor-pointer',
            isDragging 
              ? 'border-blue-400 bg-blue-100 shadow-lg shadow-blue-200' 
              : 'border-blue-300 bg-blue-50/50 hover:border-blue-400 hover:bg-blue-100',
            error && 'border-red-400 bg-red-50'
          )}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={acceptedFormats.join(',')}
            onChange={handleFileSelect}
            className="hidden"
          />

          <div className="flex flex-col items-center justify-center p-6 text-center">
            <div className="mb-3">
              {isDragging ? (
                <Upload className="h-10 w-10 mx-auto text-blue-500 drop-shadow-lg" />
              ) : (
                <FileImage className="h-10 w-10 mx-auto text-blue-400" />
              )}
            </div>

            <p className="text-base font-semibold text-slate-700 mb-1">
              {isDragging ? "Déposez l'image ici" : 'Glissez-déposez une image ici'}
            </p>

            <p className="text-xs text-slate-600 mb-3">ou cliquez pour sélectionner un fichier</p>

            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={e => {
                e.stopPropagation()
                handleClick()
              }}
              className="border-blue-300 text-blue-600 hover:bg-blue-100 hover:border-blue-400 hover:text-blue-700"
            >
              <FileImage className="h-4 w-4 mr-2" />
              Choisir un fichier
            </Button>

            <p className="text-xs text-slate-500 mt-3">
              Formats acceptés: JPG, PNG, WEBP (max {maxSizeMB}MB)
            </p>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-2 p-3 bg-red-50 border border-red-300 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
    </div>
  )
}
