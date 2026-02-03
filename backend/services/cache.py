"""
Service de cache en mémoire pour optimiser les performances
"""
import hashlib
import json
import time
import logging
from typing import Optional, Dict, Any
from functools import wraps

logger = logging.getLogger(__name__)


class MemoryCache:
    """
    Cache en mémoire simple avec expiration automatique
    """
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialise le cache
        
        Args:
            default_ttl: Time to live par défaut en secondes (1 heure par défaut)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Génère une clé de cache unique à partir des arguments
        
        Args:
            prefix: Préfixe pour le type de cache
            *args: Arguments positionnels
            **kwargs: Arguments nommés
        
        Returns:
            Clé de cache (hash)
        """
        # Créer une représentation string des arguments
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': sorted(kwargs.items()) if kwargs else {}
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        # Générer un hash MD5
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache
        
        Args:
            key: Clé de cache
        
        Returns:
            Valeur en cache ou None si expirée/inexistante
        """
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Vérifier l'expiration
        if time.time() > entry['expires_at']:
            del self.cache[key]
            self.misses += 1
            return None
        
        self.hits += 1
        logger.debug(f"Cache hit: {key}")
        return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Stocke une valeur dans le cache
        
        Args:
            key: Clé de cache
            value: Valeur à stocker
            ttl: Time to live en secondes (None = utiliser default_ttl)
        """
        if ttl is None:
            ttl = self.default_ttl
        
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl,
            'created_at': time.time()
        }
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> None:
        """Supprime une entrée du cache"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache delete: {key}")
    
    def clear(self) -> None:
        """Vide tout le cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du cache
        
        Returns:
            Dictionnaire avec hits, misses, hit_rate, size
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 2),
            'size': len(self.cache),
            'total_requests': total
        }
    
    def cleanup_expired(self) -> int:
        """
        Nettoie les entrées expirées
        
        Returns:
            Nombre d'entrées supprimées
        """
        now = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)


# Instance globale du cache
_cache_instance: Optional[MemoryCache] = None


def get_cache() -> MemoryCache:
    """
    Retourne l'instance globale du cache (Singleton)
    
    Returns:
        Instance MemoryCache
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = MemoryCache(default_ttl=3600)  # 1 heure par défaut
    return _cache_instance


def cached(prefix: str = "default", ttl: int = 3600):
    """
    Décorateur pour mettre en cache le résultat d'une fonction
    
    Args:
        prefix: Préfixe pour le type de cache
        ttl: Time to live en secondes
    
    Exemple:
        @cached(prefix="search", ttl=1800)
        def search_products(query):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache()
            key = cache._generate_key(prefix, *args, **kwargs)
            
            # Essayer de récupérer depuis le cache
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            
            # Exécuter la fonction
            result = func(*args, **kwargs)
            
            # Mettre en cache le résultat
            cache.set(key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator






