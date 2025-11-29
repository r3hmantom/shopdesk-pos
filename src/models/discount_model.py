from src.database import Database

class DiscountModel:
    def __init__(self):
        self.db = Database()

    def create_discount(self, code, discount_type, value):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO discounts (code, discount_type, value)
                VALUES (%s, %s, %s)
            """, (code.upper(), discount_type, value))
            return True
        except Exception as e:
            print(f"Error creating discount: {e}")
            return False

    def get_discount_by_code(self, code):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM discounts WHERE code = %s AND is_active = TRUE", (code.upper(),))
        return cursor.fetchone()

    def get_all_discounts(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM discounts ORDER BY id DESC")
        return cursor.fetchall()

    def delete_discount(self, discount_id):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("DELETE FROM discounts WHERE id = %s", (discount_id,))
            return True
        except Exception as e:
            print(f"Error deleting discount: {e}")
            return False

    def toggle_active(self, discount_id, current_status):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("UPDATE discounts SET is_active = %s WHERE id = %s", (not current_status, discount_id))
            return True
        except Exception as e:
            print(f"Error toggling discount status: {e}")
            return False
