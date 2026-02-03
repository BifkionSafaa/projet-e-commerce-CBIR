'use client'

import React from 'react'
import { Search, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface SearchButtonProps {
  onClick: () => void
  loading?: boolean
  disabled?: boolean
  children?: React.ReactNode
  className?: string
}

export function SearchButton({
  onClick,
  loading = false,
  disabled = false,
  children,
  className,
}: SearchButtonProps) {
  return (
    <Button
      onClick={onClick}
      disabled={disabled || loading}
      className={cn(
        'min-w-[140px] bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold shadow-md shadow-blue-200 disabled:opacity-50 disabled:cursor-not-allowed h-11 px-6',
        className
      )}
    >
      {loading ? (
        <>
          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
          Recherche...
        </>
      ) : (
        <>
          <Search className="h-4 w-4 mr-2" />
          {children || 'Rechercher'}
        </>
      )}
    </Button>
  )
}
