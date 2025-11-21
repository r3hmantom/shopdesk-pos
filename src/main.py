import customtkinter as ctk
from src.database import Database
from src.views.login_view import build_login_frame
from src.controllers.auth_controller import AuthController

# Set modern theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDA POS System")
        self.root.geometry("1280x800")
        
        # Initialize Database
        self.db = Database()
        self.db.connect()
        
        # Initialize Controller
        self.auth_controller = AuthController()
        
        # Start with Login Screen
        self.show_login()

    def show_login(self):
        self.clear_window()
        # Pass the app instance to login frame so it can call show_dashboard on success
        login_frame = build_login_frame(self.root, self.auth_controller, self.show_dashboard, self.show_register)
        login_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_window()
        from src.views.register_view import build_register_frame
        register_frame = build_register_frame(self.root, self.auth_controller, self.show_login)
        register_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_window()
        from src.views.dashboard_view import build_dashboard_frame
        dashboard_frame = build_dashboard_frame(self.root, self.auth_controller, self.logout)
        dashboard_frame.pack(fill="both", expand=True)

    def logout(self):
        self.auth_controller.logout()
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
