"""
Script pour mettre à jour les produits depuis un fichier CSV
Utile pour corriger les noms, couleurs, marques en masse
"""
import sys
import csv
from pathlib import Path

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / '.env')

from models.database import DatabaseConnection

def update_from_csv(csv_file):
    """
    Met à jour les produits depuis un fichier CSV
    
    Format du CSV:
    id,name,color,brand,description,price
    1,Nouveau nom,noir,Apple,Nouvelle description,99.99
    """
    db = DatabaseConnection()
    try:
        db.connect()
        
        updated = 0
        errors = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                product_id = row.get('id')
                if not product_id:
                    print(f"[!] Ligne sans ID, ignorée")
                    continue
                
                try:
                    product_id = int(product_id)
                except ValueError:
                    print(f"[!] ID invalide: {product_id}")
                    errors += 1
                    continue
                
                # Construire la requête UPDATE
                updates = []
                values = []
                
                if 'name' in row and row['name']:
                    updates.append("name = %s")
                    values.append(row['name'].strip())
                
                if 'color' in row:
                    color = row['color'].strip() if row['color'] else None
                    updates.append("color = %s")
                    values.append(color if color and color.upper() != 'NULL' else None)
                
                if 'brand' in row:
                    brand = row['brand'].strip() if row['brand'] else None
                    updates.append("brand = %s")
                    values.append(brand if brand and brand.upper() != 'NULL' else None)
                
                if 'description' in row and row['description']:
                    updates.append("description = %s")
                    values.append(row['description'].strip())
                
                if 'price' in row and row['price']:
                    try:
                        price = float(row['price'])
                        updates.append("price = %s")
                        values.append(price)
                    except ValueError:
                        print(f"[!] Prix invalide pour produit {product_id}: {row['price']}")
                
                if not updates:
                    continue
                
                updates.append("updated_at = CURRENT_TIMESTAMP")
                values.append(product_id)
                
                try:
                    cursor = db.conn.cursor()
                    query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
                    cursor.execute(query, values)
                    db.conn.commit()
                    cursor.close()
                    updated += 1
                    print(f"[+] Produit {product_id} mis à jour")
                except Exception as e:
                    print(f"[!] Erreur pour produit {product_id}: {e}")
                    errors += 1
        
        print(f"\n{'='*60}")
        print(f"RÉSUMÉ")
        print(f"{'='*60}")
        print(f"Produits mis à jour: {updated}")
        print(f"Erreurs: {errors}")
        
    except Exception as e:
        print(f"[!] Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.disconnect()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Met à jour les produits depuis un CSV')
    parser.add_argument('csv_file', type=str, help='Fichier CSV avec les modifications')
    args = parser.parse_args()
    
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"[!] Fichier introuvable: {csv_path}")
        sys.exit(1)
    
    update_from_csv(csv_path)

