import customtkinter as ctk
from tkinter import messagebox

def build_login_frame(root, auth_controller, on_login_success, on_register_click):
    frame = ctk.CTkFrame(root, corner_radius=0)
    
    # Center Box
    login_box = ctk.CTkFrame(frame, width=400, height=500, corner_radius=15)
    login_box.place(relx=0.5, rely=0.5, anchor="center")

    titleLabel = ctk.CTkLabel(login_box, text="Welcome Back", font=("Roboto Medium", 30))
    titleLabel.pack(pady=(40, 30))

    username = ctk.CTkEntry(login_box, placeholder_text="Username", width=300, height=40, font=("Roboto", 14))
    username.pack(pady=(10, 15))

    password = ctk.CTkEntry(login_box, placeholder_text="Password", show="*", width=300, height=40, font=("Roboto", 14))
    password.pack(pady=(0, 20))

    pin_entry = ctk.CTkEntry(login_box, placeholder_text="Enter PIN", show="*", width=300, height=40, font=("Roboto", 14))
    
    mode_var = ctk.StringVar(value="password")

    def handle_login():
        if mode_var.get() == "password":
            user = username.get()
            pwd = password.get()
            success, message = auth_controller.login(user, pwd)
        else:
            pin = pin_entry.get()
            success, message = auth_controller.login_with_pin(pin)
            
        if success:
            on_login_success()
        else:
            messagebox.showerror("Login Failed", message)

    loginButton = ctk.CTkButton(login_box, text="Login", width=300, height=45, font=("Roboto Medium", 16), command=handle_login)
    loginButton.pack(pady=10)
    
    def toggle_mode():
        if mode_var.get() == "password":
            mode_var.set("pin")
            username.pack_forget()
            password.pack_forget()
            pin_entry.pack(pady=(20, 20), before=loginButton)
            toggle_btn.configure(text="Use Username/Password")
            titleLabel.configure(text="Enter PIN")
        else:
            mode_var.set("password")
            pin_entry.pack_forget()
            username.pack(pady=(10, 15), before=loginButton)
            password.pack(pady=(0, 20), before=loginButton)
            toggle_btn.configure(text="Use PIN")
            titleLabel.configure(text="Welcome Back")

    toggle_btn = ctk.CTkButton(login_box, text="Use PIN", fg_color="transparent", text_color="#3B82F6", hover_color="#eee", command=toggle_mode)
    toggle_btn.pack(pady=(0, 10))

    createAccountLabel = ctk.CTkButton(login_box, text="Create an account", 
                                       fg_color="transparent", hover_color="#eee", 
                                       text_color="gray", font=("Roboto", 12),
                                       command=on_register_click)
    createAccountLabel.pack(pady=(10, 20))

    return frame

# -------------------
# Standalone execution
# -------------------
if __name__ == "__main__":
    def dummy_auth_controller():
        class AuthController:
            def login(self, username, password):
                if username == "admin" and password == "password":
                    return True, "Login successful"
                return False, "Invalid credentials"
        return AuthController()

    def dummy_on_login_success():
        print("Login successful (dummy callback)")

    def dummy_on_register_click():
        print("Switch to create account (dummy callback)")

    root = ctk.CTk()
    root.title("Standalone Login Page")
    root.state("zoomed")

    auth_controller = dummy_auth_controller()
    login_frame = build_login_frame(root, auth_controller, dummy_on_login_success, dummy_on_register_click)
    login_frame.pack(fill="both", expand=True)

    root.mainloop()
