import io
import os
import tempfile
import unittest

import cv2
import numpy as np
from PIL import Image

from services.preprocessing import (
    ALLOWED_FORMATS,
    apply_histogram_equalization,
    augment_image,
    correct_image_orientation,
    handle_alpha_channel,
    is_image_valid,
    load_and_preprocess_image,
    preprocess_from_bytes,
    smart_resize,
    validate_image_format,
)


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        # Image RGB simple pour la plupart des tests (100x50, fond blanc + rectangle rouge)
        self.rgb_image = np.ones((50, 100, 3), dtype=np.uint8) * 255
        self.rgb_image[10:40, 30:70] = [255, 0, 0]  # rectangle rouge

    def test_validate_image_format(self):
        # Créer un fichier temporaire avec delete=False pour Windows
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        try:
            Image.fromarray(self.rgb_image).save(tmp.name)
            self.assertTrue(validate_image_format(tmp.name))
        finally:
            os.remove(tmp.name)
        # Mauvaise extension
        tmp2 = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        tmp2.close()
        try:
            self.assertFalse(validate_image_format(tmp2.name))
        finally:
            os.remove(tmp2.name)
        # Fichier inexistant
        self.assertFalse(validate_image_format("not_exists.jpg"))

    def test_is_image_valid(self):
        # Créer un fichier temporaire valide
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.close()
        try:
            Image.fromarray(self.rgb_image).save(tmp.name)
            self.assertTrue(is_image_valid(tmp.name))
        finally:
            os.remove(tmp.name)
        # Fichier corrompu
        tmp2 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp2.write(b"not an image")
        tmp2.close()
        corrupted_path = tmp2.name
        try:
            self.assertFalse(is_image_valid(corrupted_path))
        finally:
            os.remove(corrupted_path)

    def test_handle_alpha_channel_rgba(self):
        h, w = self.rgb_image.shape[:2]
        alpha = np.ones((h, w), dtype=np.uint8) * 128  # semi-transparent
        rgba = np.dstack([self.rgb_image, alpha])
        processed = handle_alpha_channel(rgba)
        self.assertEqual(processed.shape, (h, w, 3))
        self.assertTrue(processed.dtype == np.uint8)

    def test_handle_alpha_channel_grayscale(self):
        gray = np.ones((20, 30), dtype=np.uint8) * 100
        processed = handle_alpha_channel(gray)
        self.assertEqual(processed.shape, (20, 30, 3))

    def test_smart_resize_preserves_aspect(self):
        target_size = (224, 224)
        # Test avec use_crop=True (comportement par défaut maintenant)
        resized = smart_resize(self.rgb_image, target_size, use_crop=True)
        self.assertEqual(resized.shape, (224, 224, 3))
        
        # Test avec use_crop=False (padding)
        resized_padding = smart_resize(self.rgb_image, target_size, use_crop=False)
        self.assertEqual(resized_padding.shape, (224, 224, 3))

    def test_apply_histogram_equalization(self):
        # Image sombre + zone claire pour vérifier la redistribution
        dark = np.ones((50, 50, 3), dtype=np.uint8) * 30
        dark[10:40, 10:40] = 200
        equalized = apply_histogram_equalization(dark)
        self.assertEqual(equalized.shape, dark.shape)
        # Vérifie que la dynamique a changé (pas tout à la même valeur)
        self.assertGreater(equalized.max() - equalized.min(), 0)

    def test_augment_image_shape(self):
        np.random.seed(0)
        img = self.rgb_image
        augmented = augment_image(img)
        self.assertEqual(augmented.shape, img.shape)
        self.assertTrue(augmented.dtype == np.uint8)

    def test_load_and_preprocess_image(self):
        # Créer un fichier temporaire avec delete=False pour Windows
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        try:
            Image.fromarray(self.rgb_image).save(tmp.name, format="JPEG")
            processed = load_and_preprocess_image(tmp.name, target_size=(224, 224))
            # load_and_preprocess_image retourne (1, 224, 224, 3) avec dimension batch
            self.assertEqual(processed.shape, (1, 224, 224, 3))
            self.assertTrue(processed.dtype == np.float32)
            # Vérifier que l'image est normalisée ImageNet (valeurs peuvent être négatives)
            # Les valeurs normalisées ImageNet peuvent être en dehors de [0, 1]
        finally:
            os.remove(tmp.name)

    def test_preprocess_from_bytes(self):
        buf = io.BytesIO()
        Image.fromarray(self.rgb_image).save(buf, format="PNG")
        image_bytes = buf.getvalue()
        processed = preprocess_from_bytes(image_bytes, target_size=(224, 224))
        self.assertEqual(processed.shape, (1, 224, 224, 3))
        self.assertTrue(processed.dtype == np.float32)
        # Avec normalisation ImageNet, les valeurs peuvent être négatives
        # On vérifie juste que l'image est bien normalisée (pas de valeurs extrêmes)
        self.assertTrue(np.isfinite(processed).all())


if __name__ == "__main__":
    unittest.main()

