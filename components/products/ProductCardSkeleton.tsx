'use client'

import React from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { cn } from '@/lib/utils'

interface ProductCardSkeletonProps {
  className?: string
}

export function ProductCardSkeleton({ className }: ProductCardSkeletonProps) {
  return (
    <Card className={cn('overflow-hidden w-full max-w-[260px] mx-auto bg-gradient-to-br from-blue-100/90 via-indigo-50/95 to-violet-100/90', className)}>
      <div className="relative h-44 w-full bg-blue-50/50">
        <Skeleton className="w-full h-full" />
      </div>

      <CardContent className="p-2">
        <div className="space-y-0.5">
          <Skeleton className="h-3.5 w-3/4" />
          <Skeleton className="h-3 w-1/2" />
          <Skeleton className="h-3 w-2/3" />
          <div className="flex justify-between pt-0.5">
            <Skeleton className="h-4 w-16" />
          </div>
          <div className="flex gap-1 pt-0.5">
            <Skeleton className="h-7 flex-1" />
            <Skeleton className="h-7 flex-1" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}





