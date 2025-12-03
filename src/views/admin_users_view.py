import customtkinter as ctk
from tkinter import ttk, messagebox
from src.models.user_model import UserModel

def build_admin_users_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    user_model = UserModel()
    
    ctk.CTkLabel(frame, text="Admin - User Management", font=("Roboto Medium", 24)).pack(pady=(20, 10))

    # Table
    cols = ("Username", "Role", "Name", "Last Login", "Status")
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    def load_users():
        for item in tree.get_children():
            tree.delete(item)
            
        users = user_model.get_all_users_with_shifts()
        for u in users:
            status = "Offline"
            if u['last_login'] and not u['last_logout']:
                status = "Active"
            
            login_str = u['last_login'].strftime("%Y-%m-%d %H:%M") if u['last_login'] else "Never"
            
            tree.insert("", "end", values=(
                u['username'], 
                u['role'], 
                u['name'], 
                login_str,
                status
            ))
            
    ctk.CTkButton(frame, text="Refresh List", command=load_users).pack(pady=10)
    load_users()
    
    return frame

