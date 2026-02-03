import os

class Config:
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'cbir_ecommerce')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    # Paths
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'user_queries')
    PRODUCT_IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'product_images')
    DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', 'dataset')
    
    # Ensure folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PRODUCT_IMAGES_FOLDER, exist_ok=True)
    
    # Model Configuration
    MODEL_NAME = 'resnet50'
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
