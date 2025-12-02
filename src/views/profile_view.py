import customtkinter as ctk
from tkinter import messagebox

def build_profile_frame(parent, auth_controller):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    user = auth_controller.current_user

    ctk.CTkLabel(frame, text="My Profile", font=("Roboto Medium", 30)).pack(pady=(30, 40))

    info_card = ctk.CTkFrame(frame, width=500, corner_radius=15)
    info_card.pack(pady=10)

    def add_info(label_text, value):
        row = ctk.CTkFrame(info_card, fg_color="transparent")
        row.pack(fill="x", pady=10, padx=40)
        ctk.CTkLabel(row, text=label_text, font=("Roboto Medium", 16), width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=value, font=("Roboto", 16), anchor="w").pack(side="left", padx=10)

    add_info("Username:", user['username'])
    add_info("Role:", user['role'])
    add_info("First Name:", user['first_name'])
    add_info("Last Name:", user['last_name'])
    
    # Password Change Section
    reset_frame = ctk.CTkFrame(frame, fg_color="transparent")
    
    def show_reset():
        reset_frame.pack(pady=10)
        for widget in reset_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(reset_frame, text="Change Password", font=("Roboto Medium", 20)).pack(pady=10)
        
        new_pass_entry = ctk.CTkEntry(reset_frame, placeholder_text="New Password", show="*", width=300)
        new_pass_entry.pack(pady=10)
        
        def change_pass():
            new_pass = new_pass_entry.get()
            if new_pass:
                messagebox.showinfo("Success", "Password changed successfully (Simulation).")
                reset_frame.pack_forget()
            else:
                messagebox.showwarning("Error", "Password cannot be empty.")

        ctk.CTkButton(reset_frame, text="Update Password", command=change_pass).pack(pady=10)

    ctk.CTkButton(frame, text="Change Password", command=show_reset, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).pack(pady=(20, 10))

    # --- Shift History Section ---
    ctk.CTkLabel(frame, text="My Recent Shifts", font=("Roboto Medium", 20)).pack(pady=(30, 10))
    
    shifts_frame = ctk.CTkScrollableFrame(frame, height=200, corner_radius=10)
    shifts_frame.pack(fill="x", padx=40, pady=10)
    
    # Fetch sessions
    sessions = auth_controller.user_model.get_user_sessions(user['id'])
    
    if not sessions:
        ctk.CTkLabel(shifts_frame, text="No shift history found.").pack(pady=20)
    else:
        # Header
        h_row = ctk.CTkFrame(shifts_frame, height=30, fg_color="#e0e0e0")
        h_row.pack(fill="x", pady=2)
        ctk.CTkLabel(h_row, text="Login Time", width=200, anchor="w", font=("Roboto", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(h_row, text="Logout Time", width=200, anchor="w", font=("Roboto", 12, "bold")).pack(side="left", padx=10)
        
        for s in sessions:
            login_t = s[0].strftime("%Y-%m-%d %H:%M:%S") if s[0] else "-"
            logout_t = s[1].strftime("%Y-%m-%d %H:%M:%S") if s[1] else "Active"
            
            row = ctk.CTkFrame(shifts_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=login_t, width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=logout_t, width=200, anchor="w", text_color="green" if logout_t == "Active" else "black").pack(side="left", padx=10)

    return frame
