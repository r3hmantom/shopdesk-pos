from src.database import Database

class LoggerModel:
    def __init__(self):
        self.db = Database()

    def log_activity(self, user_id, action, details=None):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO activity_logs (user_id, action, details)
                VALUES (%s, %s, %s)
            """, (user_id, action, details))
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False

