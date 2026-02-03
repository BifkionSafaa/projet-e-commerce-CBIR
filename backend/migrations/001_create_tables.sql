-- Migration 001: Création des tables pour le système CBIR e-commerce
-- Date: 2025-12-14
-- Description: Création des tables products et product_features

-- Supprimer les tables si elles existent (pour réinitialisation)
DROP TABLE IF EXISTS product_features CASCADE;
DROP TABLE IF EXISTS products CASCADE;

-- Table products: Stocke les informations sur les produits
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    brand VARCHAR(100),
    color VARCHAR(50),
    image_path VARCHAR(500) NOT NULL,
    image_hash VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table product_features: Stocke les vecteurs de features extraits par ResNet50
CREATE TABLE product_features (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    feature_vector TEXT NOT NULL,  -- JSON array de 2048 dimensions
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Index pour améliorer les performances des requêtes

-- Index sur category pour les recherches par catégorie
CREATE INDEX idx_products_category ON products(category);

-- Index sur price pour les recherches par prix
CREATE INDEX idx_products_price ON products(price);

-- Index sur product_id pour les jointures avec product_features
CREATE INDEX idx_product_features_product_id ON product_features(product_id);

-- Index sur image_hash pour les vérifications de doublons
CREATE INDEX idx_products_image_hash ON products(image_hash);

-- Commentaires sur les tables
COMMENT ON TABLE products IS 'Table stockant les informations sur les produits du catalogue';
COMMENT ON TABLE product_features IS 'Table stockant les vecteurs de features extraits par ResNet50 pour la recherche par image';

-- Commentaires sur les colonnes importantes
COMMENT ON COLUMN products.image_hash IS 'Hash MD5 unique de l''image pour éviter les doublons';
COMMENT ON COLUMN product_features.feature_vector IS 'Vecteur de features JSON de 2048 dimensions extrait par ResNet50';

