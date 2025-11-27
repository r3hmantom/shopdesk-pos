from src.database import Database

class ConfigModel:
    def __init__(self):
        self.db = Database()
        self._ensure_table()

    def _ensure_table(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                key_name VARCHAR(50) PRIMARY KEY,
                value VARCHAR(255)
            )
        """)
        # Seed default tax if not exists
        cursor.execute("SELECT value FROM system_config WHERE key_name = 'tax_rate'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO system_config (key_name, value) VALUES ('tax_rate', '10.0')")
            
        self.db.conn.commit()

    def get_setting(self, key):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT value FROM system_config WHERE key_name = %s", (key,))
        res = cursor.fetchone()
        return res[0] if res else None

    def set_setting(self, key, value):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO system_config (key_name, value) VALUES (%s, %s)
                ON CONFLICT (key_name) DO UPDATE SET value = EXCLUDED.value
            """, (key, str(value)))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving setting: {e}")
            return False

    def get_tax_rate(self):
        val = self.get_setting('tax_rate')
        try:
            return float(val)
        except:
            return 10.0

