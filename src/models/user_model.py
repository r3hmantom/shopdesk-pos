from src.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def authenticate(self, username, password):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, username, role, first_name, last_name FROM users WHERE username = %s AND password_hash = %s", (username, password))
        return cursor.fetchone()

    def create_user(self, username, password, role, first_name, last_name, phone, cnic):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, phone, cnic)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, password, role, first_name, last_name, phone, cnic))
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def get_user_by_username(self, username):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()

    def authenticate_pin(self, pin):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, username, role, first_name, last_name FROM users WHERE pin_hash = %s", (pin,))
        return cursor.fetchone()

    def set_pin(self, user_id, pin):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("UPDATE users SET pin_hash = %s WHERE id = %s", (pin, user_id))
            return True
        except Exception as e:
            print(f"Error setting PIN: {e}")
            return False

    def start_session(self, user_id):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO user_sessions (user_id) VALUES (%s) RETURNING id
            """, (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error starting session: {e}")
            return None

    def end_session(self, session_id):
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                UPDATE user_sessions SET logout_time = CURRENT_TIMESTAMP, is_active = FALSE WHERE id = %s
            """, (session_id,))
            return True
        except Exception as e:
            print(f"Error ending session: {e}")
            return False

    def get_user_sessions(self, user_id, limit=10):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT login_time, logout_time 
            FROM user_sessions 
            WHERE user_id = %s 
            ORDER BY login_time DESC 
            LIMIT %s
        """, (user_id, limit))
        return cursor.fetchall()

    def get_all_users_with_shifts(self):
        cursor = self.db.get_cursor()
        # Fetch users
        cursor.execute("SELECT id, username, role, first_name, last_name FROM users ORDER BY role, username")
        users = cursor.fetchall()
        
        results = []
        for u in users:
            uid = u[0]
            # Fetch last shift
            cursor.execute("SELECT login_time, logout_time FROM user_sessions WHERE user_id = %s ORDER BY login_time DESC LIMIT 1", (uid,))
            shift = cursor.fetchone()
            results.append({
                'id': u[0],
                'username': u[1],
                'role': u[2],
                'name': f"{u[3]} {u[4]}",
                'last_login': shift[0] if shift else None,
                'last_logout': shift[1] if shift else None
            })
        return results
