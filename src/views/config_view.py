import customtkinter as ctk
from tkinter import messagebox
from src.models.config_model import ConfigModel

def build_config_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    config_model = ConfigModel()
    
    ctk.CTkLabel(frame, text="System Configuration", font=("Roboto Medium", 24)).pack(pady=(30, 20))
    
    # Settings Container
    card = ctk.CTkFrame(frame, corner_radius=10)
    card.pack(pady=20, padx=20, fill="x")

    # Tax Rate Setting
    row_tax = ctk.CTkFrame(card, fg_color="transparent")
    row_tax.pack(fill="x", padx=20, pady=20)
    
    ctk.CTkLabel(row_tax, text="Tax Rate (%):", font=("Roboto", 16), width=150, anchor="w").pack(side="left")
    
    tax_entry = ctk.CTkEntry(row_tax, width=100)
    tax_entry.pack(side="left", padx=10)
    
    current_tax = config_model.get_tax_rate()
    tax_entry.insert(0, str(current_tax))
    
    def save_settings():
        new_tax = tax_entry.get()
        try:
            val = float(new_tax)
            if val < 0: raise ValueError
            
            if config_model.set_setting('tax_rate', val):
                messagebox.showinfo("Success", "Settings saved successfully.")
            else:
                messagebox.showerror("Error", "Database error.")
        except ValueError:
            messagebox.showerror("Error", "Invalid tax rate. Must be a positive number.")

    ctk.CTkButton(card, text="Save Changes", command=save_settings, height=40).pack(pady=20)

    return frame

