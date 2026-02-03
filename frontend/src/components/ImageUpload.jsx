'use client'

import React from 'react'

export default function ImageUpload({ onUpload }) {
  const [dragActive, setDragActive] = React.useState(false)
  const fileInputRef = React.useRef(null)

  const handleDrag = e => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = e => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      onUpload(files[0])
    }
  }

  const handleChange = e => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0])
    }
  }

  return (
    <div
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
      style={{
        border: dragActive ? '2px solid #3498db' : '2px dashed #bdc3c7',
        borderRadius: '4px',
        padding: '30px',
        textAlign: 'center',
        cursor: 'pointer',
        backgroundColor: dragActive ? '#ecf0f1' : 'transparent',
        transition: 'all 0.3s ease',
      }}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        style={{ display: 'none' }}
      />
      <p style={{ margin: 0, color: '#7f8c8d' }}>Drag and drop an image here, or click to select</p>
    </div>
  )
}
