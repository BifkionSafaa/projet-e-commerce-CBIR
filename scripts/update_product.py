"""
Script pour mettre à jour les informations d'un produit dans la base de données
"""
import sys
from pathlib import Path

# Ajouter le dossier backend au path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
load_dotenv(dotenv_path=backend_path / '.env')

from models.database import DatabaseConnection

def update_product(product_id, name=None, color=None, brand=None, description=None, price=None):
    """
    Met à jour les informations d'un produit
    
    Args:
        product_id: ID du produit à modifier
        name: Nouveau nom (optionnel)
        color: Nouvelle couleur (optionnel)
        brand: Nouvelle marque (optionnel)
        description: Nouvelle description (optionnel)
        price: Nouveau prix (optionnel)
    """
    db = DatabaseConnection()
    try:
        db.connect()
        
        # Construire la requête UPDATE dynamiquement
        updates = []
        values = []
        
        if name is not None:
            updates.append("name = %s")
            values.append(name)
        
        if color is not None:
            updates.append("color = %s")
            values.append(color if color else None)  # Permettre de mettre None
        
        if brand is not None:
            updates.append("brand = %s")
            values.append(brand if brand else None)
        
        if description is not None:
            updates.append("description = %s")
            values.append(description)
        
        if price is not None:
            updates.append("price = %s")
            values.append(float(price))
        
        if not updates:
            print("[!] Aucune modification à effectuer")
            return False
        
        # Ajouter updated_at
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        # Ajouter product_id pour le WHERE
        values.append(product_id)
        
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        
        cursor = db.conn.cursor()
        cursor.execute(query, values)
        db.conn.commit()
        cursor.close()
        
        print(f"[+] Produit ID {product_id} mis à jour avec succès")
        return True
        
    except Exception as e:
        print(f"[!] Erreur: {e}")
        db.conn.rollback()
        return False
    finally:
        db.disconnect()

def show_product(product_id):
    """Affiche les informations d'un produit"""
    db = DatabaseConnection()
    try:
        db.connect()
        
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT id, name, category, price, description, brand, color, image_path
            FROM products
            WHERE id = %s
        """, (product_id,))
        
        product = cursor.fetchone()
        cursor.close()
        
        if not product:
            print(f"[!] Produit ID {product_id} introuvable")
            return
        
        print(f"\n{'='*60}")
        print(f"PRODUIT ID {product[0]}")
        print(f"{'='*60}")
        print(f"Nom: {product[1]}")
        print(f"Catégorie: {product[2]}")
        print(f"Prix: {product[3]:.2f} €")
        print(f"Description: {product[4] or '(vide)'}")
        print(f"Marque: {product[5] or '(vide)'}")
        print(f"Couleur: {product[6] or '(vide)'}")
        print(f"Image: {product[7]}")
        print()
        
    except Exception as e:
        print(f"[!] Erreur: {e}")
    finally:
        db.disconnect()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Met à jour les informations d\'un produit')
    parser.add_argument('product_id', type=int, help='ID du produit à modifier')
    parser.add_argument('--name', type=str, help='Nouveau nom')
    parser.add_argument('--color', type=str, help='Nouvelle couleur (ou "NULL" pour vider)')
    parser.add_argument('--brand', type=str, help='Nouvelle marque (ou "NULL" pour vider)')
    parser.add_argument('--description', type=str, help='Nouvelle description')
    parser.add_argument('--price', type=float, help='Nouveau prix')
    parser.add_argument('--show', action='store_true', help='Afficher les informations actuelles')
    
    args = parser.parse_args()
    
    if args.show:
        show_product(args.product_id)
    
    # Convertir "NULL" en None
    color = None if args.color == "NULL" else args.color
    brand = None if args.brand == "NULL" else args.brand
    
    if args.name or color is not None or brand is not None or args.description or args.price:
        update_product(
            args.product_id,
            name=args.name,
            color=color,
            brand=args.brand,
            description=args.description,
            price=args.price
        )
        show_product(args.product_id)
    elif not args.show:
        print("[!] Spécifiez au moins une option (--name, --color, --brand, --description, --price)")
        print("[!] Ou utilisez --show pour afficher les informations actuelles")

