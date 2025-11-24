from src.database import Database

class SupplierModel:
    def __init__(self):
        self.db = Database()

    def get_all_suppliers(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM suppliers ORDER BY name")
        return cursor.fetchall()

    def add_supplier(self, name, contact, phone, email):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO suppliers (name, contact_person, phone, email)
                VALUES (%s, %s, %s, %s)
            """, (name, contact, phone, email))
            return True
        except Exception as e:
            print(f"Error adding supplier: {e}")
            return False

    def create_restock_order(self, supplier_id, product_id, quantity):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO restock_orders (supplier_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (supplier_id, product_id, quantity))
            # Also update actual stock
            cursor.execute("""
                UPDATE products SET stock_quantity = stock_quantity + %s WHERE id = %s
            """, (quantity, product_id))
            return True
        except Exception as e:
            print(f"Error creating restock order: {e}")
            return False

