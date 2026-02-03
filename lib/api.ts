/**
 * Services API centralisés pour l'application CBIR E-Commerce
 * Gère toutes les communications avec le backend Flask
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

// Types TypeScript
export interface Product {
  id: number
  name: string
  category: string
  price: number
  description?: string
  brand?: string
  color?: string
  image_path: string
  similarity_score?: number
}

export interface SearchResult {
  results: Product[]
  count: number
  query_time?: number
}

export interface ApiError {
  error: string
  success: boolean
}

/**
 * Gère les erreurs HTTP de manière centralisée
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({
      error: `HTTP ${response.status}: ${response.statusText}`,
      success: false,
    }))
    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Effectue une requête avec timeout et retry
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeout: number = 30000,
  retries: number = 2
): Promise<Response> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    })
    clearTimeout(timeoutId)
    return response
  } catch (error) {
    clearTimeout(timeoutId)

    if (retries > 0 && error instanceof Error && error.name === 'AbortError') {
      // Retry on timeout
      return fetchWithTimeout(url, options, timeout, retries - 1)
    }

    throw error
  }
}

/**
 * Récupère des produits aléatoires
 */
export async function getRandomProducts(count: number = 8): Promise<Product[]> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/products/random?count=${count}`, {
      method: 'GET',
    })
    const data = await handleResponse<{ products: Product[]; count: number }>(response)
    return data.products || (Array.isArray(data) ? data : [])
  } catch (error) {
    console.error('Error fetching random products:', error)
    throw error
  }
}

/**
 * Recherche par image
 */
export async function searchByImage(
  file: File,
  topK: number = 10,
  minSimilarity: number = 0.5  // Par défaut: 50% de similarité minimum
): Promise<SearchResult> {
  try {
    const formData = new FormData()
    formData.append('image', file)

    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/search/image?top_k=${topK}&min_similarity=${minSimilarity}`,
      {
        method: 'POST',
        body: formData,
      },
      60000 // 60 secondes pour l'extraction de features
    )

    const data = await handleResponse<SearchResult>(response)
    return {
      results: data.results || [],
      count: data.count || data.results?.length || 0,
      query_time: data.query_time,
    }
  } catch (error) {
    console.error('Error searching by image:', error)
    throw error
  }
}

/**
 * Recherche par texte
 */
export async function searchByText(query: string, limit: number = 20): Promise<SearchResult> {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/search/text?q=${encodeURIComponent(query)}&limit=${limit}`,
      { method: 'GET' }
    )

    const data = await handleResponse<SearchResult>(response)
    return {
      results: data.results || [],
      count: data.count || data.results?.length || 0,
    }
  } catch (error) {
    console.error('Error searching by text:', error)
    throw error
  }
}

/**
 * Recherche hybride (image + texte)
 */
export async function searchHybrid(
  imageFile: File | null,
  textQuery: string | null,
  topK: number = 10,
  minSimilarity: number = 0.85
): Promise<SearchResult> {
  try {
    const formData = new FormData()
    if (imageFile) {
      formData.append('image', imageFile)
    }
    if (textQuery) {
      formData.append('query', textQuery)
    }

    const response = await fetchWithTimeout(
      `${API_BASE_URL}/api/search/hybrid?top_k=${topK}&min_similarity=${minSimilarity}`,
      {
        method: 'POST',
        body: formData,
      },
      60000
    )

    const data = await handleResponse<SearchResult>(response)
    return {
      results: data.results || [],
      count: data.count || data.results?.length || 0,
      query_time: data.query_time,
    }
  } catch (error) {
    console.error('Error in hybrid search:', error)
    throw error
  }
}

/**
 * Récupère un produit par son ID
 */
export async function getProduct(id: number): Promise<Product> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/products/${id}`, { method: 'GET' })
    return handleResponse<Product>(response)
  } catch (error) {
    console.error(`Error fetching product ${id}:`, error)
    throw error
  }
}

/**
 * Catégorie avec image pour le bandeau
 */
export interface CategoryItem {
  category: string
  image_path: string
}

/**
 * Récupère la liste des catégories avec une image par catégorie
 */
export async function getCategories(): Promise<CategoryItem[]> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/products/categories`, {
      method: 'GET',
    })
    const data = await handleResponse<{ categories: CategoryItem[]; count: number }>(response)
    return data.categories || []
  } catch (error) {
    console.error('Error fetching categories:', error)
    return []
  }
}

/**
 * Récupère des produits avec filtres
 */
export interface ProductFilters {
  category?: string
  minPrice?: number
  maxPrice?: number
  brand?: string
  color?: string
  limit?: number
  offset?: number
}

export async function getProducts(filters: ProductFilters = {}): Promise<SearchResult> {
  try {
    const params = new URLSearchParams()
    if (filters.category) params.append('category', filters.category)
    if (filters.minPrice !== undefined) params.append('min_price', filters.minPrice.toString())
    if (filters.maxPrice !== undefined) params.append('max_price', filters.maxPrice.toString())
    if (filters.brand) params.append('brand', filters.brand)
    if (filters.color) params.append('color', filters.color)
    if (filters.limit) params.append('limit', filters.limit.toString())
    if (filters.offset) params.append('offset', filters.offset.toString())

    const response = await fetchWithTimeout(`${API_BASE_URL}/api/products?${params.toString()}`, {
      method: 'GET',
    })

    const data = await handleResponse<SearchResult>(response)
    return {
      results: data.results || [],
      count: data.count || data.results?.length || 0,
    }
  } catch (error) {
    console.error('Error fetching products:', error)
    throw error
  }
}





