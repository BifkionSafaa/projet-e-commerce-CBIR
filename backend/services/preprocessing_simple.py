"""
Preprocessing simplifié
- Utilise tf.image.resize
- Preprocess_input de ResNet50
- Pas d'amélioration de qualité complexe
"""
import numpy as np
import tensorflow as tf
import io
from PIL import Image, ImageOps
from tensorflow.keras.applications.resnet50 import preprocess_input

def load_and_preprocess_image_simple(image_path, target_size=(224, 224)):
    """
    Preprocessing simplifié
    - Utilise tf.image.resize
    - Preprocess_input de ResNet50
    - Pas d'amélioration de qualité
    """
    # 1. Ouvrir l'image
    pil_image = Image.open(image_path)
    
    # 2. Corriger l'orientation EXIF
    pil_image = ImageOps.exif_transpose(pil_image)
    
    # 3. Convertir en numpy array
    image = np.array(pil_image.convert('RGB'))
    
    # 4. Resize avec tf.image.resize
    image_resized = tf.image.resize(image, target_size).numpy()
    
    # 5. Appliquer preprocess_input de ResNet50
    # Cela fait la normalisation ImageNet automatiquement
    image_preprocessed = preprocess_input(image_resized)
    
    # 6. Ajouter dimension batch
    image_preprocessed = np.expand_dims(image_preprocessed, axis=0)
    
    return image_preprocessed

def preprocess_from_bytes_simple(file_bytes, target_size=(224, 224)):
    """
    Preprocessing simplifié depuis bytes
    """
    # Ouvrir l'image depuis les bytes
    pil_image = Image.open(io.BytesIO(file_bytes))
    pil_image = ImageOps.exif_transpose(pil_image)
    
    # Convertir en numpy array
    image = np.array(pil_image.convert('RGB'))
    
    # Resize avec tf.image.resize
    image_resized = tf.image.resize(image, target_size).numpy()
    
    # Preprocess_input de ResNet50
    image_preprocessed = preprocess_input(image_resized)
    
    # Ajouter dimension batch
    image_preprocessed = np.expand_dims(image_preprocessed, axis=0)
    
    return image_preprocessed

