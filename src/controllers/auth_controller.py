from src.models.user_model import UserModel
from src.models.logger_model import LoggerModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.logger = LoggerModel()
        self.current_user = None
        self.current_session_id = None

    def login(self, username, password):
        user = self.user_model.authenticate(username, password)
        if user:
            self._set_current_user(user)
            self.logger.log_activity(user[0], "LOGIN", "Login via Username/Password")
            return True, "Login successful"
        return False, "Invalid username or password"

    def login_with_pin(self, pin):
        user = self.user_model.authenticate_pin(pin)
        if user:
            self._set_current_user(user)
            self.logger.log_activity(user[0], "LOGIN", "Login via PIN")
            return True, "Login successful"
        return False, "Invalid PIN"

    def _set_current_user(self, user):
        self.current_user = {
            "id": user[0],
            "username": user[1],
            "role": user[2],
            "first_name": user[3],
            "last_name": user[4]
        }
        self.current_session_id = self.user_model.start_session(user[0])

    def register(self, username, password, role, first_name, last_name, phone, cnic):
        if self.user_model.get_user_by_username(username):
            return False, "Username already exists"
        
        success = self.user_model.create_user(username, password, role, first_name, last_name, phone, cnic)
        if success:
            return True, "Account created successfully"
        return False, "Failed to create account"

    def logout(self):
        if self.current_user:
            self.logger.log_activity(self.current_user['id'], "LOGOUT", "User logged out")
            if self.current_session_id:
                self.user_model.end_session(self.current_session_id)
        self.current_user = None
        self.current_session_id = None

    def set_pin(self, pin):
        if not self.current_user:
            return False, "Not logged in"
        
        success = self.user_model.set_pin(self.current_user['id'], pin)
        if success:
            self.logger.log_activity(self.current_user['id'], "SET_PIN", "User updated PIN")
            return True, "PIN updated successfully"
        return False, "Failed to update PIN"
