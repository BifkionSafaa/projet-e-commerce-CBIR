export default function ProductGrid({ products, loading }) {
  if (loading) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Loading products...</div>
  }

  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <div className="product-image">
            <img
              src={`/.jpg?height=250&width=250&query=${product.name}`}
              alt={product.name}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </div>
          <div className="product-info">
            <div className="product-name">{product.name}</div>
            <div style={{ color: '#7f8c8d', fontSize: '0.9rem', marginBottom: '10px' }}>
              {product.category}
            </div>
            <div className="product-price">${product.price.toFixed(2)}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
