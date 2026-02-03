"""
Extract features using ResNet50 
- Charge depuis data/product_images/
- Utilise tf.image.resize
- Preprocess_input de ResNet50
- Features NON normalisées L2
"""
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import os

backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

def load_product_images():
    """Load processed product images """
    print(" Loading product images...")
    
    image_dir = Path(__file__).parent.parent / 'data' / 'product_images'
    
    if not image_dir.exists():
        print(f"[ERREUR] Dossier non trouve: {image_dir}")
        print("   Executez d'abord le script de preprocessing pour creer data/product_images/")
        return None
    
    images = []
    num_products = len([f for f in os.listdir(image_dir) if f.endswith('.jpg')])
    
    for i in range(num_products):
        img_path = image_dir / f"product_{i}.jpg"
        if img_path.exists():
            img = Image.open(img_path).convert('RGB')
            images.append(np.array(img))
        else:
            print(f"  [ATTENTION] Image non trouvee: {img_path}")
    
    print(f" Loaded {len(images)} images")
    return images

def preprocess_for_resnet(images):
    """Preprocess images for ResNet50"""
    print("\n Preprocessing images...")
    preprocessed = []
    for img in images:
        # Resize to 224x224
        img_resized = tf.image.resize(img, (224, 224))
        preprocessed.append(img_resized.numpy())
    preprocessed = np.array(preprocessed)
    print(f" Shape after resize: {preprocessed.shape}")
    # Apply ResNet50 preprocessing
    preprocessed = preprocess_input(preprocessed)
    return preprocessed

def extract_features(images_preprocessed):
    """Extract features using ResNet50"""
    print("\n Loading ResNet50 (more accurate than MobileNetV2)...")
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    print(" Extracting features...")
    features = model.predict(images_preprocessed, verbose=1)
    print(f" Features shape: {features.shape}")
    return features

def main():
    print("=" * 60)
    print("EXTRACTING FEATURES WITH RESNET50")
    print("=" * 60 + "\n")
    # Load images
    images = load_product_images()
    if images is None:
        return
    # Preprocess
    images_preprocessed = preprocess_for_resnet(images)
    # Extract features
    features = extract_features(images_preprocessed)
    # Save with different name
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    np.save(data_dir / "product_features_resnet50.npy", features)
    print("\n Features saved to data/product_features_resnet50.npy")
    print("\n" + "=" * 60)
    print("FEATURE EXTRACTION COMPLETE!")
    print(f" Feature dimension: {features.shape[1]}")
    print("=" * 60)

if __name__ == "__main__":
    main()

