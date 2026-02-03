"""
Script pour initialiser la base de données PostgreSQL
Crée les tables nécessaires pour le système CBIR e-commerce
"""
import sys
import os
from pathlib import Path

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / 'backend' / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"[!] Attention: Le fichier {env_path} n'existe pas")
    print(f"[*] Copiez backend/env.example vers backend/.env et remplissez les valeurs")

# Ajouter le dossier backend au path pour importer les modules
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from models.database import DatabaseConnection
from config import Config
import psycopg2
from psycopg2 import errors as psycopg2_errors

def read_sql_file(file_path):
    """Lit un fichier SQL et retourne son contenu"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[!] Erreur lors de la lecture du fichier SQL {file_path}: {e}")
        return None

def execute_sql_script(db, sql_script):
    """Exécute un script SQL (peut contenir plusieurs commandes)"""
    try:
        if not db.conn:
            db.connect()
        
        cursor = db.conn.cursor()
        
        # Nettoyer le script : enlever les commentaires et lignes vides
        cleaned_lines = []
        for line in sql_script.split('\n'):
            stripped = line.strip()
            # Ignorer les lignes vides
            if not stripped:
                continue
            # Enlever les commentaires (-- jusqu'à la fin de la ligne)
            if '--' in stripped:
                # Prendre seulement la partie avant le commentaire
                stripped = stripped.split('--')[0].strip()
                if not stripped:
                    continue
            cleaned_lines.append(stripped)
        
        # Rejoindre toutes les lignes avec des espaces
        full_script = ' '.join(cleaned_lines)
        
        # Exécuter chaque commande séparément en utilisant une approche plus robuste
        # On va splitter par ';' mais en s'assurant que chaque commande est complète
        import re
        # Utiliser une regex pour trouver les commandes SQL complètes
        # Pattern: trouver tout jusqu'à un ';' qui n'est pas dans une chaîne
        commands = re.split(r';(?=\s|$)', full_script)
        
        for command in commands:
            command = command.strip()
            if not command:
                continue
            
            # S'assurer que la commande se termine par ';'
            if not command.endswith(';'):
                command += ';'
            
            try:
                cursor.execute(command)
            except psycopg2_errors.UndefinedTable as e:
                # Ignorer les erreurs "table does not exist" pour DROP TABLE
                if 'DROP' in command.upper():
                    db.conn.rollback()
                    continue
                raise e
            except Exception as e:
                # Afficher la commande qui a échoué pour debug
                print(f"[!] Erreur avec la commande: {command[:150]}...")
                raise e
        
        db.conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        print(f"[!] Erreur lors de l'execution du script SQL: {e}")
        if db.conn:
            db.conn.rollback()
        return False

def check_tables_exist(db):
    """Vérifie si les tables existent déjà"""
    try:
        if not db.conn:
            db.connect()
        
        cursor = db.conn.cursor()
        
        # Vérifier si les tables existent
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('products', 'product_features')
        """)
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        return existing_tables
    except Exception as e:
        print(f"[!] Erreur lors de la verification des tables: {e}")
        return []

def init_database(force=False):
    """Initialise la base de données"""
    print("=" * 60)
    print("INITIALISATION DE LA BASE DE DONNEES")
    print("=" * 60)
    
    # Chemin vers le fichier SQL
    sql_file = Path(__file__).parent.parent / 'backend' / 'migrations' / '001_create_tables.sql'
    
    if not sql_file.exists():
        print(f"[!] Erreur : Le fichier {sql_file} n'existe pas")
        return False
    
    # Lire le script SQL
    print(f"[*] Lecture du script SQL: {sql_file}")
    sql_script = read_sql_file(sql_file)
    
    if not sql_script:
        return False
    
    # Connexion à la base de données
    print(f"[*] Connexion à la base de données...")
    print(f"    Host: {Config.DB_HOST}")
    print(f"    Port: {Config.DB_PORT}")
    print(f"    Database: {Config.DB_NAME}")
    print(f"    User: {Config.DB_USER}")
    
    db = DatabaseConnection()
    
    try:
        if not db.connect():
            print("[!] Erreur : Impossible de se connecter à la base de données")
            print("[*] Verifiez vos parametres de connexion dans .env")
            return False
        
        # Vérifier si les tables existent déjà
        existing_tables = check_tables_exist(db)
        
        if existing_tables and not force:
            print(f"\n[!] Les tables suivantes existent deja: {', '.join(existing_tables)}")
            print("[*] Utilisez --force pour les recréer")
            return False
        
        if existing_tables and force:
            print(f"\n[*] Suppression des tables existantes...")
        
        # Exécuter le script SQL
        print(f"\n[*] Execution du script SQL...")
        if execute_sql_script(db, sql_script):
            print("[+] Tables creees avec succes !")
            
            # Vérifier que les tables ont été créées
            new_tables = check_tables_exist(db)
            print(f"\n[*] Tables existantes: {', '.join(new_tables)}")
            
            # Vérifier les index
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename IN ('products', 'product_features')
            """)
            indexes = [row[0] for row in cursor.fetchall()]
            cursor.close()
            
            print(f"[*] Index crees: {len(indexes)}")
            for idx in indexes:
                print(f"    - {idx}")
            
            print("\n[+] Initialisation terminee avec succes !")
            return True
        else:
            print("[!] Erreur lors de la creation des tables")
            return False
            
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return False
    finally:
        db.disconnect()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialise la base de donnees PostgreSQL')
    parser.add_argument('--force', action='store_true',
                       help='Recree les tables meme si elles existent deja')
    
    args = parser.parse_args()
    
    success = init_database(force=args.force)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

