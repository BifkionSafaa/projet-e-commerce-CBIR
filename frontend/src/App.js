'use client'

import React from 'react'
import SearchBar from './components/SearchBar.jsx'
import ImageUpload from './components/ImageUpload.jsx'
import ProductGrid from './components/ProductGrid.jsx'

export default function App() {
  const [products, setProducts] = React.useState([])
  const [loading, setLoading] = React.useState(false)

  React.useEffect(() => {
    fetchRandomProducts()
  }, [])

  const fetchRandomProducts = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:5000/api/products/random?count=8')
      const data = await response.json()
      setProducts(data)
    } catch (error) {
      console.error('Error fetching products:', error)
    }
    setLoading(false)
  }

  const handleSearch = query => {
    console.log('Searching for:', query)
  }

  const handleImageUpload = file => {
    console.log('Uploaded file:', file)
  }

  return (
    <div>
      <header>
        <h1>CBIR E-Commerce</h1>
      </header>
      <div className="container">
        <div className="search-section">
          <SearchBar onSearch={handleSearch} />
          <ImageUpload onUpload={handleImageUpload} />
        </div>
        <ProductGrid products={products} loading={loading} />
      </div>
    </div>
  )
}
