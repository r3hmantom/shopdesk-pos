from src.database import Database

class ProductModel:
    def __init__(self):
        self.db = Database()

    def add_product(self, name, price, stock_quantity, barcode, category, loyalty_points=0):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO products (name, price, stock_quantity, barcode, category, loyalty_points)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, price, stock_quantity, barcode, category, loyalty_points))
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    def get_product_by_barcode(self, barcode):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
        return cursor.fetchone()

    def get_all_products(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM products ORDER BY name")
        return cursor.fetchall()

    def update_stock(self, product_id, quantity_change):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity + %s 
                WHERE id = %s
            """, (quantity_change, product_id))
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False

    def get_low_stock_items(self, threshold=10):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM products WHERE stock_quantity < %s", (threshold,))
        return cursor.fetchall()

    def update_product(self, product_id, name, price, stock_quantity, barcode, category, loyalty_points):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE products 
                SET name=%s, price=%s, stock_quantity=%s, barcode=%s, category=%s, loyalty_points=%s
                WHERE id=%s
            """, (name, price, stock_quantity, barcode, category, loyalty_points, product_id))
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def get_product_by_id(self, product_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return cursor.fetchone()
