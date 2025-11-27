from src.database import Database

class CustomerModel:
    def __init__(self):
        self.db = Database()

    def create_customer(self, name, phone):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO customers (name, phone, loyalty_points)
                VALUES (%s, %s, 0)
                RETURNING id
            """, (name, phone))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error creating customer: {e}")
            return None

    def get_customer_by_phone(self, phone):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
        return cursor.fetchone()

    def get_customer_by_id(self, customer_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        return cursor.fetchone()

    def update_loyalty_points(self, customer_id, points_change):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE customers 
                SET loyalty_points = loyalty_points + %s 
                WHERE id = %s
            """, (points_change, customer_id))
            return True
        except Exception as e:
            print(f"Error updating loyalty points: {e}")
            return False
