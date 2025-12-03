import customtkinter as ctk
from src.views.sales_view import build_sales_frame
from src.views.inventory_view import build_inventory_frame
from src.views.restock_view import build_restock_frame
from src.views.loyalty_view import build_loyalty_frame
from src.views.refund_view import build_refund_frame
from src.views.profile_view import build_profile_frame
from src.views.reports_view import build_reports_frame
from src.views.discount_view import build_discount_frame
from src.views.admin_users_view import build_admin_users_frame
from src.views.config_view import build_config_frame

def build_dashboard_frame(root, auth_controller, on_logout):
    # Main container
    dashboard_frame = ctk.CTkFrame(root, corner_radius=0)
    
    # Sidebar
    sidebar = ctk.CTkFrame(dashboard_frame, width=250, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    # App Logo / Title
    logo_label = ctk.CTkLabel(sidebar, text="SDA POS", font=("Roboto Medium", 24))
    logo_label.pack(pady=(40, 30), padx=20)

    # User Info
    user_info = f"Hello, {auth_controller.current_user['username']}\n({auth_controller.current_user['role']})"
    user_label = ctk.CTkLabel(sidebar, text=user_info, font=("Roboto", 14), text_color="gray")
    user_label.pack(pady=(0, 30), padx=20)

    # Content Area
    content_area = ctk.CTkFrame(dashboard_frame, corner_radius=0, fg_color="transparent")
    content_area.pack(side="right", fill="both", expand=True)

    def load_view(view_builder):
        for widget in content_area.winfo_children():
            widget.destroy()
        if view_builder:
            frame = view_builder(content_area)
            frame.pack(fill="both", expand=True)

    # Navigation Buttons
    role = auth_controller.current_user['role'].lower()
    
    buttons = []
    
    # Everyone gets Sales and Profile
    buttons.append(("Sales / POS", lambda: load_view(lambda p: build_sales_frame(p, auth_controller))))
    
    if role in ["admin", "manager"]:
        buttons.append(("Inventory", lambda: load_view(lambda p: build_inventory_frame(p))))
        buttons.append(("Restock", lambda: load_view(lambda p: build_restock_frame(p))))
    
    # Everyone gets Customers (Cashiers need it for loyalty)
    buttons.append(("Customers", lambda: load_view(lambda p: build_loyalty_frame(p))))
    
    if role in ["admin", "manager"]:
        buttons.append(("Discounts", lambda: load_view(lambda p: build_discount_frame(p))))
        buttons.append(("Refunds", lambda: load_view(lambda p: build_refund_frame(p))))
        buttons.append(("Reports", lambda: load_view(lambda p: build_reports_frame(p))))

    if role == "admin":
        buttons.append(("Users/Shifts", lambda: load_view(lambda p: build_admin_users_frame(p))))
        buttons.append(("Settings", lambda: load_view(lambda p: build_config_frame(p))))

    buttons.append(("Profile", lambda: load_view(lambda p: build_profile_frame(p, auth_controller))))

    for text, cmd in buttons:
        btn = ctk.CTkButton(sidebar, text=text, command=cmd, 
                            height=40, corner_radius=5, 
                            fg_color="transparent", hover_color="#444", 
                            anchor="w", font=("Roboto", 14))
        btn.pack(fill="x", padx=10, pady=5)

    # Logout at bottom
    logout_btn = ctk.CTkButton(sidebar, text="Logout", command=on_logout, 
                               fg_color="#d9534f", hover_color="#c9302c", 
                               height=40, font=("Roboto Medium", 14))
    logout_btn.pack(side="bottom", fill="x", padx=20, pady=30)

    # Load default
    load_view(lambda p: build_sales_frame(p, auth_controller))

    return dashboard_frame
