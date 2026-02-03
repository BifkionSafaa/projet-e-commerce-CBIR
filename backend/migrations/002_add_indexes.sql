-- Migration 002: Ajout d'index pour optimiser les requêtes SQL
-- Date: 2025-01-XX
-- Description: Création d'index sur les colonnes fréquemment utilisées pour améliorer les performances

-- Index sur category (utilisé dans les filtres et recherches)
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- Index sur brand (utilisé dans les filtres et recherches)
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);

-- Index sur color (utilisé dans les filtres et recherches)
CREATE INDEX IF NOT EXISTS idx_products_color ON products(color);

-- Index sur price (utilisé dans les filtres min_price/max_price)
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);

-- Index composite sur category et price (pour filtres combinés)
CREATE INDEX IF NOT EXISTS idx_products_category_price ON products(category, price);

-- Index sur name (utilisé dans les recherches LIKE)
-- Note: Pour PostgreSQL, on peut utiliser un index GIN pour les recherches textuelles
-- mais pour l'instant, un index B-tree standard suffit
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);

-- Index sur image_path (utilisé pour servir les images)
CREATE INDEX IF NOT EXISTS idx_products_image_path ON products(image_path);

-- Index sur created_at (pour tri chronologique si nécessaire)
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

-- Commentaires pour documentation
COMMENT ON INDEX idx_products_category IS 'Index pour optimiser les filtres par catégorie';
COMMENT ON INDEX idx_products_brand IS 'Index pour optimiser les filtres par marque';
COMMENT ON INDEX idx_products_color IS 'Index pour optimiser les filtres par couleur';
COMMENT ON INDEX idx_products_price IS 'Index pour optimiser les filtres par prix';
COMMENT ON INDEX idx_products_category_price IS 'Index composite pour optimiser les filtres combinés category + price';
COMMENT ON INDEX idx_products_name IS 'Index pour optimiser les recherches par nom';
COMMENT ON INDEX idx_products_image_path IS 'Index pour optimiser les requêtes sur image_path';






