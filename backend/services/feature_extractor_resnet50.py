"""
Extracteur de features avec ResNet50
Utilise preprocessing simplifié + cosine similarity
"""
import numpy as np
import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from tensorflow.keras.applications import ResNet50
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logger.warning("TensorFlow not available. Feature extraction will not work.")


class ResNet50FeatureExtractor:
    """
    Extracteur de features utilisant ResNet50
    Pattern Singleton : le modèle est chargé une seule fois
    """
    
    _instance = None
    _model = None
    _model_loaded = False
    
    def __new__(cls):
        """Pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(ResNet50FeatureExtractor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise l'extracteur et charge le modèle si nécessaire"""
        if not self._model_loaded:
            self._load_model()
    
    def _load_model(self):
        """Charge ResNet50 une seule fois"""
        if self._model is not None:
            logger.info("ResNet50 model already loaded, reusing existing instance")
            return True
        
        if not TENSORFLOW_AVAILABLE:
            logger.error("TensorFlow is not available. Cannot load ResNet50 model.")
            self._model_loaded = False
            return False
        
        try:
            logger.info("Loading ResNet50 model...")
            start_time = time.time()
            
            # ResNet50 avec pooling='avg'
            self._model = ResNet50(
                weights='imagenet',
                include_top=False,
                pooling='avg',  # Global average pooling
                input_shape=(224, 224, 3)
            )
            
            load_time = time.time() - start_time
            self._model_loaded = True
            
            logger.info(f"ResNet50 model loaded successfully in {load_time:.2f} seconds")
            logger.info(f"Model output shape: {self._model.output_shape}")
            logger.info(f"Feature dimension: 2048 (ResNet50)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading ResNet50 model: {e}")
            self._model = None
            self._model_loaded = False
            return False
    
    def is_model_loaded(self) -> bool:
        """Vérifie si le modèle est chargé"""
        return self._model is not None and self._model_loaded
    
    def extract_features(self, image_array: np.ndarray, normalize: bool = False) -> np.ndarray:
        """
        Extrait les features d'une image préprocessée
        
        Args:
            image_array: Image préprocessée (shape: (1, 224, 224, 3))
            normalize: Si True, normalise L2 (par défaut False car cosine_similarity normalise automatiquement)
        
        Returns:
            np.ndarray: Vecteur de features (shape: (1, 2048) ou (2048,))
        """
        if not self.is_model_loaded():
            raise ValueError("ResNet50 model is not loaded. Cannot extract features.")
        
        # Valider la forme
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        elif len(image_array.shape) != 4:
            raise ValueError(f"Invalid image shape: {image_array.shape}. Expected (224, 224, 3) or (1, 224, 224, 3)")
        
        if image_array.shape[1:] != (224, 224, 3):
            raise ValueError(f"Invalid image dimensions: {image_array.shape[1:]}. Expected (224, 224, 3)")
        
        try:
            # Extraire les features
            features = self._model.predict(image_array, verbose=0)
            
            # IMPORTANT: Pas de normalisation L2 par défaut
            # cosine_similarity de sklearn normalise automatiquement
            # Mais on peut normaliser si demandé (pour compatibilité)
            if normalize:
                norm = np.linalg.norm(features, axis=1, keepdims=True)
                norm = np.where(norm > 0, norm, 1)  # Éviter division par zéro
                features = features / norm
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            raise ValueError(f"Failed to extract features: {e}")
    
    def get_model_info(self) -> dict:
        """Retourne des informations sur le modèle"""
        info = {
            'model_loaded': self.is_model_loaded(),
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'output_shape': None,
            'num_parameters': None
        }
        
        if self.is_model_loaded():
            info['output_shape'] = self._model.output_shape
            info['num_parameters'] = self._model.count_params()
        
        return info

