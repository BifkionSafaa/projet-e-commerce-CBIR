"""
Script pour créer automatiquement la base de données PostgreSQL
si elle n'existe pas déjà
"""
import sys
import os
from pathlib import Path

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config

def database_exists(db_name, user, password, host='localhost', port=5432):
    """Vérifie si la base de données existe"""
    try:
        # Se connecter à la base 'postgres' (base par défaut)
        conn = psycopg2.connect(
            host=host,
            port=port,
            database='postgres',
            user=user,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        
        return exists
    except Exception as e:
        print(f"[!] Erreur lors de la verification: {e}")
        return False

def create_database(db_name, user, password, host='localhost', port=5432):
    """Crée la base de données si elle n'existe pas"""
    try:
        # Se connecter à la base 'postgres' (base par défaut)
        conn = psycopg2.connect(
            host=host,
            port=port,
            database='postgres',
            user=user,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Vérifier si la base existe déjà
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        
        if cursor.fetchone():
            print(f"[*] La base de donnees '{db_name}' existe deja")
            cursor.close()
            conn.close()
            return True
        
        # Créer la base de données
        print(f"[*] Creation de la base de donnees '{db_name}'...")
        cursor.execute(f'CREATE DATABASE {db_name}')
        cursor.close()
        conn.close()
        
        print(f"[+] Base de donnees '{db_name}' creee avec succes !")
        return True
        
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print(f"[!] Erreur d'authentification: Mot de passe incorrect")
            print(f"[*] Verifiez votre mot de passe PostgreSQL dans backend/.env")
        elif "could not connect" in str(e):
            print(f"[!] Erreur de connexion: Impossible de se connecter a PostgreSQL")
            print(f"[*] Verifiez que PostgreSQL est demarre et accessible")
        else:
            print(f"[!] Erreur: {e}")
        return False
    except Exception as e:
        print(f"[!] Erreur lors de la creation de la base de donnees: {e}")
        return False

def main():
    print("=" * 60)
    print("CREATION DE LA BASE DE DONNEES POSTGRESQL")
    print("=" * 60)
    
    # Récupérer les paramètres depuis la config
    db_name = Config.DB_NAME
    db_user = Config.DB_USER
    db_password = Config.DB_PASSWORD
    db_host = Config.DB_HOST
    db_port = Config.DB_PORT
    
    print(f"\n[*] Parametres de connexion:")
    print(f"    Host: {db_host}")
    print(f"    Port: {db_port}")
    print(f"    User: {db_user}")
    print(f"    Database: {db_name}")
    
    # Vérifier si la base existe déjà
    if database_exists(db_name, db_user, db_password, db_host, db_port):
        print(f"\n[+] La base de donnees '{db_name}' existe deja")
        print(f"[*] Vous pouvez maintenant executer: python scripts/init_database.py")
        return True
    
    # Demander confirmation
    print(f"\n[*] La base de donnees '{db_name}' n'existe pas")
    print(f"[*] Creation en cours...")
    
    # Créer la base de données
    if create_database(db_name, db_user, db_password, db_host, db_port):
        print(f"\n[+] Base de donnees creee avec succes !")
        print(f"[*] Prochaine etape: python scripts/init_database.py")
        return True
    else:
        print(f"\n[!] Echec de la creation de la base de donnees")
        print(f"[*] Voir les instructions manuelles ci-dessous")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

