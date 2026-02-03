import cv2
import numpy as np
from PIL import Image, ImageOps
import io
import os
import random

# Configuration
ALLOWED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG', '.WEBP'}


def validate_image_format(image_path):
    """
    Vérifie que le fichier est un format d'image valide
    
    Args:
        image_path: Chemin vers l'image
    
    Returns:
        bool: True si le format est valide
    """
    if not os.path.exists(image_path):
        return False
    
    ext = os.path.splitext(image_path)[1]
    return ext in ALLOWED_FORMATS


def is_image_valid(image_path):
    """
    Vérifie si l'image n'est pas corrompue
    
    Args:
        image_path: Chemin vers l'image
    
    Returns:
        bool: True si l'image est valide
    """
    try:
        # Essayer d'ouvrir avec PIL
        img = Image.open(image_path)
        img.verify()  # Vérifie l'intégrité du fichier
        
        # Essayer aussi avec OpenCV
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            return False
        
        return True
    except Exception:
        return False


def correct_image_orientation(image_path):
    """
    Corrige l'orientation de l'image selon les données EXIF
    
    Args:
        image_path: Chemin vers l'image
    
    Returns:
        PIL.Image: Image corrigée
    """
    try:
        image = Image.open(image_path)
        # Utiliser ImageOps pour auto-orientation (plus simple)
        image = ImageOps.exif_transpose(image)
        return image
    except Exception:
        # Retourner l'image originale si erreur
        return Image.open(image_path)


def handle_alpha_channel(image):
    """
    Gère les images avec canal alpha (transparence)
    Convertit RGBA en RGB avec fond blanc
    
    Args:
        image: Image numpy array (peut être RGBA)
    
    Returns:
        numpy.ndarray: Image RGB
    """
    if len(image.shape) == 2:
        # Image en niveaux de gris, convertir en RGB
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        # Image RGBA, convertir en RGB avec fond blanc
        # Séparer les canaux
        rgb = image[:, :, :3]
        alpha = image[:, :, 3] / 255.0
        
        # Créer un fond blanc
        white_background = np.ones_like(rgb) * 255
        
        # Combiner avec transparence
        image = (rgb * alpha[:, :, np.newaxis] + white_background * (1 - alpha[:, :, np.newaxis])).astype(np.uint8)
    elif image.shape[2] == 3:
        # Déjà en RGB, rien à faire
        pass
    
    return image


def smart_resize(image, target_size=(224, 224), padding_color=None, use_crop=False):
    """
    Redimensionne l'image en gardant le ratio d'aspect
    Ajoute du padding si nécessaire, ou fait un crop intelligent
    
    IMPORTANT: Si use_crop=True, fait un crop au lieu d'un padding pour éviter
    les fonds uniformes qui créent des similarités artificielles entre images différentes
    
    Args:
        image: Image numpy array
        target_size: Taille cible (height, width)
        padding_color: Couleur du padding (RGB). Si None, utilise la couleur moyenne de l'image
        use_crop: Si True, fait un crop au lieu d'un padding (recommandé pour éviter les similarités)
    
    Returns:
        numpy.ndarray: Image redimensionnée
    """
    h, w = image.shape[:2]
    target_h, target_w = target_size
    
    # Si on utilise le crop, redimensionner pour remplir toute l'image (sans padding)
    if use_crop:
        # Calculer le ratio pour remplir toute l'image (crop)
        ratio = max(target_h / h, target_w / w)
        new_h, new_w = int(h * ratio), int(w * ratio)
        
        # S'assurer que les dimensions sont au moins égales à la taille cible
        if new_h < target_h:
            new_h = target_h
        if new_w < target_w:
            new_w = target_w
        
        # Redimensionner
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Crop au centre pour obtenir la taille exacte
        start_y = (new_h - target_h) // 2
        start_x = (new_w - target_w) // 2
        cropped = resized[start_y:start_y+target_h, start_x:start_x+target_w]
        
        # Vérifier que le crop a la bonne taille
        if cropped.shape[:2] != (target_h, target_w):
            # Si le crop échoue (image trop petite), utiliser le padding à la place
            return smart_resize(image, target_size, padding_color=padding_color, use_crop=False)
        
        return cropped
    
    # Sinon, utiliser le padding (comportement original)
    # Calculer le ratio pour garder l'aspect
    ratio = min(target_h / h, target_w / w)
    new_h, new_w = int(h * ratio), int(w * ratio)
    
    # Redimensionner
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Déterminer la couleur du padding
    if padding_color is None:
        # Utiliser la couleur moyenne de l'image au lieu de noir/blanc
        # Cela préserve mieux les différences entre images
        if len(image.shape) == 2:
            # Image en niveaux de gris
            mean_color = int(np.mean(image))
            padding_color = (mean_color,)
        else:
            # Image couleur - utiliser la couleur moyenne
            mean_color = tuple(int(c) for c in np.mean(image, axis=(0, 1)))
            padding_color = mean_color
    elif isinstance(padding_color, (int, float)) or (isinstance(padding_color, tuple) and len(padding_color) == 1):
        # Si une seule valeur, utiliser pour tous les canaux
        if isinstance(padding_color, tuple):
            padding_color = (padding_color[0],)
        else:
            padding_color = (int(padding_color),)
    
    # Créer l'image finale avec padding
    if len(resized.shape) == 2:
        # Image en niveaux de gris
        if isinstance(padding_color, tuple) and len(padding_color) == 1:
            final_image = np.full((target_h, target_w), padding_color[0], dtype=np.uint8)
        else:
            final_image = np.full((target_h, target_w), int(padding_color), dtype=np.uint8)
    else:
        # Image couleur
        if isinstance(padding_color, tuple) and len(padding_color) == 3:
            final_image = np.full((target_h, target_w, 3), padding_color, dtype=np.uint8)
        else:
            # Si une seule valeur, répéter pour les 3 canaux
            color_val = padding_color[0] if isinstance(padding_color, tuple) else int(padding_color)
            final_image = np.full((target_h, target_w, 3), (color_val, color_val, color_val), dtype=np.uint8)
    
    # Calculer la position pour centrer l'image
    top = (target_h - new_h) // 2
    left = (target_w - new_w) // 2
    
    # Placer l'image redimensionnée au centre
    if len(resized.shape) == 2:
        final_image[top:top+new_h, left:left+new_w] = resized
    else:
        final_image[top:top+new_h, left:left+new_w, :] = resized
    
    return final_image


def reduce_noise(image, method='bilateral'):
    """
    Réduit le bruit dans l'image
    
    Args:
        image: Image numpy array (RGB)
        method: Méthode de réduction de bruit ('bilateral', 'gaussian', 'median')
    
    Returns:
        numpy.ndarray: Image avec bruit réduit
    """
    if method == 'bilateral':
        # Filtre bilatéral : préserve les bords tout en réduisant le bruit
        denoised = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    elif method == 'gaussian':
        # Filtre gaussien : simple mais efficace
        denoised = cv2.GaussianBlur(image, (5, 5), 0)
    elif method == 'median':
        # Filtre médian : bon pour bruit impulsionnel
        denoised = cv2.medianBlur(image, 5)
    else:
        # Par défaut : filtre bilatéral
        denoised = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    
    return denoised


def enhance_sharpness(image, strength=1.0):
    """
    Améliore la netteté de l'image
    
    Args:
        image: Image numpy array (RGB)
        strength: Force de l'amélioration (0.0 à 2.0)
    
    Returns:
        numpy.ndarray: Image avec netteté améliorée
    """
    # Créer un noyau de sharpening
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]]) * strength
    
    # Appliquer le filtre
    sharpened = cv2.filter2D(image, -1, kernel)
    
    # Clipper les valeurs entre 0 et 255
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    
    return sharpened


def enhance_contrast(image, alpha=1.2, beta=10):
    """
    Améliore le contraste de l'image
    
    Args:
        image: Image numpy array (RGB)
        alpha: Contrôle du contraste (1.0 = pas de changement, >1.0 = plus de contraste)
        beta: Contrôle de la luminosité (0 = pas de changement)
    
    Returns:
        numpy.ndarray: Image avec contraste amélioré
    """
    # Appliquer la transformation : new_image = alpha * image + beta
    enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    return enhanced


def remove_background_simple(image, threshold=240):
    """
    Supprime le fond blanc simple (méthode basique)
    
    Args:
        image: Image numpy array (RGB)
        threshold: Seuil pour détecter le fond blanc (0-255)
    
    Returns:
        numpy.ndarray: Image avec fond supprimé (remplacé par fond transparent ou noir)
    """
    # Convertir en grayscale pour la détection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Créer un masque pour les pixels blancs/clairs
    mask = gray > threshold
    
    # Option 1: Remplacer par fond noir
    result = image.copy()
    result[mask] = [0, 0, 0]
    
    # Option 2: Remplacer par la couleur moyenne de l'image (moins agressif)
    # mean_color = np.mean(image[~mask], axis=0) if np.any(~mask) else [128, 128, 128]
    # result[mask] = mean_color
    
    return result


def improve_image_quality(image, reduce_noise_enabled=True, enhance_sharpness_enabled=True,
                          enhance_contrast_enabled=True, remove_background_enabled=False):
    """
    Améliore la qualité globale de l'image avec plusieurs techniques
    
    Args:
        image: Image numpy array (RGB)
        reduce_noise_enabled: Activer la réduction de bruit
        enhance_sharpness_enabled: Activer l'amélioration de netteté
        enhance_contrast_enabled: Activer l'amélioration de contraste
        remove_background_enabled: Activer la suppression de fond (expérimental)
    
    Returns:
        numpy.ndarray: Image améliorée
    """
    improved = image.copy()
    
    # 1. Réduction du bruit (en premier pour nettoyer l'image)
    if reduce_noise_enabled:
        improved = reduce_noise(improved, method='bilateral')
    
    # 2. Suppression de fond (si activé)
    if remove_background_enabled:
        improved = remove_background_simple(improved, threshold=240)
    
    # 3. Amélioration du contraste
    if enhance_contrast_enabled:
        improved = enhance_contrast(improved, alpha=1.1, beta=5)
    
    # 4. Amélioration de la netteté (en dernier pour accentuer les détails)
    if enhance_sharpness_enabled:
        improved = enhance_sharpness(improved, strength=0.5)  # Force modérée
    
    return improved


def apply_histogram_equalization(image):
    """
    Améliore le contraste avec histogram equalization
    
    Args:
        image: Image numpy array (RGB)
    
    Returns:
        numpy.ndarray: Image avec contraste amélioré
    """
    # Convertir en YUV
    yuv = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    
    # Appliquer equalization sur le canal Y (luminosité)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    
    # Reconvertir en RGB
    equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)
    
    return equalized


def augment_image(image, rotation_range=15, flip_prob=0.5, brightness_range=0.2):
    """
    Applique des transformations d'augmentation de données
    
    Args:
        image: Image numpy array (RGB)
        rotation_range: Angle de rotation max en degrés
        flip_prob: Probabilité de flip horizontal
        brightness_range: Variation de luminosité (0-1)
    
    Returns:
        numpy.ndarray: Image augmentée
    """
    augmented = image.copy()
    
    # 1. Rotation aléatoire
    angle = random.uniform(-rotation_range, rotation_range)
    h, w = augmented.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    augmented = cv2.warpAffine(augmented, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    # 2. Flip horizontal (avec probabilité)
    if random.random() < flip_prob:
        augmented = cv2.flip(augmented, 1)
    
    # 3. Ajustement de luminosité
    brightness_factor = 1 + random.uniform(-brightness_range, brightness_range)
    augmented = cv2.convertScaleAbs(augmented, alpha=1, beta=(brightness_factor - 1) * 128)
    
    return augmented


def load_and_preprocess_image(image_path, target_size=(224, 224), 
                               apply_equalization=False, 
                               apply_augmentation=False):
    """
    Fonction complète de prétraitement avec toutes les améliorations
    
    Args:
        image_path: Chemin vers l'image
        target_size: Taille cible
        apply_equalization: Appliquer histogram equalization
        apply_augmentation: Appliquer augmentation de données
    
    Returns:
        numpy.ndarray: Image préprocessée (normalisée 0-1) avec dimension batch
    """
    # 1. Valider le format
    if not validate_image_format(image_path):
        raise ValueError(f"Format d'image non supporté : {image_path}")
    
    # 2. Vérifier l'intégrité
    if not is_image_valid(image_path):
        raise ValueError(f"Image corrompue : {image_path}")
    
    # 3. Corriger l'orientation EXIF
    pil_image = correct_image_orientation(image_path)
    
    # 4. Convertir PIL en numpy array
    image = np.array(pil_image)
    
    # 5. Gérer la transparence
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = handle_alpha_channel(image)
    
    # 6. Convertir en RGB si nécessaire (PIL retourne déjà RGB)
    
    # 7. Redimensionnement intelligent
    # Utiliser padding avec fond blanc uniforme pour cohérence (comme les screenshots)
    # Cela uniformise toutes les images et améliore la discrimination
    image = smart_resize(image, target_size, padding_color=(255, 255, 255), use_crop=False)
    
    # 7.5. Amélioration de la qualité de l'image (NOUVEAU)
    # Réduire le bruit, améliorer la netteté et le contraste
    # Cela améliore la discrimination des features entre catégories
    image = improve_image_quality(
        image,
        reduce_noise_enabled=True,      # Réduire le bruit
        enhance_sharpness_enabled=True,  # Améliorer la netteté
        enhance_contrast_enabled=True,   # Améliorer le contraste
        remove_background_enabled=False  # Désactivé par défaut (expérimental)
    )
    
    # 8. Histogram equalization (optionnel)
    if apply_equalization:
        image = apply_histogram_equalization(image)
    
    # 9. Augmentation (optionnel)
    if apply_augmentation:
        image = augment_image(image)
    
    # 10. Normalisation ImageNet (OBLIGATOIRE pour ResNet50)
    # ResNet50 pré-entraîné attend cette normalisation spécifique
    # Mean et std utilisés lors de l'entraînement sur ImageNet
    image = image.astype('float32') / 255.0
    
    # Normalisation ImageNet (mean et std d'ImageNet)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    image = (image - mean) / std
    
    # 11. Ajouter dimension batch
    image = np.expand_dims(image, axis=0)
    
    return image


def preprocess_from_bytes(file_bytes, target_size=(224, 224), 
                          apply_equalization=False):
    """
    Preprocess image from bytes (pour les uploads)
    
    Args:
        file_bytes: Bytes de l'image
        target_size: Taille cible
        apply_equalization: Appliquer histogram equalization
    
    Returns:
        numpy.ndarray: Image préprocessée (normalisée 0-1) avec dimension batch
    """
    try:
        # Ouvrir l'image depuis les bytes
        pil_image = Image.open(io.BytesIO(file_bytes))
        
        # Corriger l'orientation EXIF
        pil_image = ImageOps.exif_transpose(pil_image)
        
        # Convertir en numpy array
        image = np.array(pil_image)
        
        # Gérer la transparence
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = handle_alpha_channel(image)
        
        # Redimensionnement intelligent
        # Utiliser padding avec fond blanc uniforme pour cohérence (comme les screenshots)
        image = smart_resize(image, target_size, padding_color=(255, 255, 255), use_crop=False)
        
        # Amélioration de la qualité de l'image (NOUVEAU)
        # Réduire le bruit, améliorer la netteté et le contraste
        image = improve_image_quality(
            image,
            reduce_noise_enabled=True,      # Réduire le bruit
            enhance_sharpness_enabled=True,  # Améliorer la netteté
            enhance_contrast_enabled=True,   # Améliorer le contraste
            remove_background_enabled=False  # Désactivé par défaut (expérimental)
        )
        
        # Histogram equalization (optionnel)
        if apply_equalization:
            image = apply_histogram_equalization(image)
        
        # Normalisation ImageNet (OBLIGATOIRE pour ResNet50)
        # ResNet50 pré-entraîné attend cette normalisation spécifique
        # Mean et std utilisés lors de l'entraînement sur ImageNet
        image = image.astype('float32') / 255.0
        
        # Normalisation ImageNet (mean et std d'ImageNet)
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        image = (image - mean) / std
        
        # Ajouter dimension batch
        image = np.expand_dims(image, axis=0)
        
        return image
    except Exception as e:
        raise ValueError(f"Erreur lors du prétraitement depuis bytes : {e}")


def normalize_features(features):
    """Normalize feature vectors"""
    return features / (np.linalg.norm(features, axis=1, keepdims=True) + 1e-7)
