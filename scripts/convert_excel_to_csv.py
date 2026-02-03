"""
Script pour convertir metadata.xlsx en metadata.csv
"""
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("[!] pandas n'est pas installé")
    print("[!] Installez-le avec: pip install pandas openpyxl")
    sys.exit(1)

DATASET_DIR = Path(__file__).parent.parent / 'dataset'
EXCEL_FILE = DATASET_DIR / 'metadata.xlsx'
CSV_FILE = DATASET_DIR / 'metadata.csv'

def convert_excel_to_csv():
    """Convertit metadata.xlsx en metadata.csv"""
    
    if not EXCEL_FILE.exists():
        print(f"[!] Fichier Excel introuvable: {EXCEL_FILE}")
        return False
    
    print(f"[*] Lecture du fichier Excel: {EXCEL_FILE}")
    
    try:
        # Lire le fichier Excel
        df = pd.read_excel(EXCEL_FILE)
        
        print(f"[+] {len(df)} lignes trouvées")
        print(f"[+] Colonnes: {', '.join(df.columns.tolist())}")
        print()
        
        # Sauvegarder en CSV UTF-8
        print(f"[*] Conversion en CSV: {CSV_FILE}")
        df.to_csv(CSV_FILE, index=False, encoding='utf-8')
        
        print(f"[+] Conversion réussie !")
        print(f"[+] Fichier CSV créé: {CSV_FILE}")
        print()
        print("[*] Vous pouvez maintenant exécuter:")
        print("    python scripts/populate_database.py --force")
        
        return True
        
    except Exception as e:
        print(f"[!] Erreur lors de la conversion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    convert_excel_to_csv()

