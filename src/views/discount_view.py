import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.discount_model import DiscountModel

def build_discount_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    discount_model = DiscountModel()

    # Header
    ctk.CTkLabel(frame, text="Discount Management", font=("Roboto Medium", 24)).pack(pady=(30, 20))

    # --- Create New Discount Section ---
    create_frame = ctk.CTkFrame(frame, corner_radius=10)
    create_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(create_frame, text="Create New Code", font=("Roboto Medium", 16)).pack(anchor="w", padx=20, pady=10)
    
    form_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
    form_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    code_entry = ctk.CTkEntry(form_frame, placeholder_text="Code (e.g. SAVE10)", width=150)
    code_entry.pack(side="left", padx=5)
    
    type_var = ctk.StringVar(value="PERCENTAGE")
    type_combo = ctk.CTkComboBox(form_frame, values=["PERCENTAGE", "FIXED"], variable=type_var, width=120)
    type_combo.pack(side="left", padx=5)
    
    val_entry = ctk.CTkEntry(form_frame, placeholder_text="Value (e.g. 10)", width=100)
    val_entry.pack(side="left", padx=5)
    
    def add_discount():
        code = code_entry.get()
        dtype = type_var.get()
        val = val_entry.get()
        
        if not code or not val:
            messagebox.showerror("Error", "Code and Value are required.")
            return
            
        try:
            val_float = float(val)
        except ValueError:
            messagebox.showerror("Error", "Value must be a number.")
            return
            
        if discount_model.create_discount(code, dtype, val_float):
            messagebox.showinfo("Success", "Discount created!")
            code_entry.delete(0, tk.END)
            val_entry.delete(0, tk.END)
            load_discounts()
        else:
            messagebox.showerror("Error", "Failed to create discount (Code might exist).")

    ctk.CTkButton(form_frame, text="Create", command=add_discount, width=100).pack(side="left", padx=20)

    # --- List Section ---
    list_frame = ctk.CTkFrame(frame, corner_radius=10)
    list_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    ctk.CTkLabel(list_frame, text="Existing Discounts", font=("Roboto Medium", 16)).pack(anchor="w", padx=20, pady=10)

    # Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Roboto", 12), rowheight=30)
    
    cols = ("ID", "Code", "Type", "Value", "Active")
    tree = ttk.Treeview(list_frame, columns=cols, show="headings")
    
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_discounts():
        for item in tree.get_children():
            tree.delete(item)
        discounts = discount_model.get_all_discounts()
        for d in discounts:
            # d: (id, code, type, value, is_active)
            status = "Yes" if d[4] else "No"
            tree.insert("", "end", values=(d[0], d[1], d[2], d[3], status))

    load_discounts()

    # Actions
    action_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
    action_frame.pack(pady=10)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        did = item['values'][0]
        if messagebox.askyesno("Confirm", "Delete this discount?"):
            discount_model.delete_discount(did)
            load_discounts()

    def toggle_selected():
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        did = item['values'][0]
        current_status = (item['values'][4] == "Yes")
        discount_model.toggle_active(did, current_status)
        load_discounts()

    ctk.CTkButton(action_frame, text="Toggle Active", command=toggle_selected, fg_color="#f0ad4e", hover_color="#ec971f").pack(side="left", padx=10)
    ctk.CTkButton(action_frame, text="Delete", command=delete_selected, fg_color="#d9534f", hover_color="#c9302c").pack(side="left", padx=10)

    return frame
