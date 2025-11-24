import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.product_model import ProductModel

def build_inventory_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    product_model = ProductModel()

    # Header
    header = ctk.CTkFrame(frame, height=60, corner_radius=0, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    
    title = ctk.CTkLabel(header, text="Inventory Management", font=("Roboto Medium", 24))
    title.pack(side="left")

    # Filter/Search
    search_frame = ctk.CTkFrame(header, fg_color="transparent")
    search_frame.pack(side="right")
    
    search_var = tk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, placeholder_text="Search by Name or Category", width=300)
    search_entry.pack(side="left", padx=10)

    # Treeview Container
    tree_frame = ctk.CTkFrame(frame, corner_radius=10)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Style Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Roboto", 12), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Roboto Medium", 12), background="#e0e0e0")
    
    columns = ("ID", "Name", "Category", "Price", "Stock", "Barcode", "Loyalty Pts")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.column("Name", width=200)
    tree.column("Loyalty Pts", width=80)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
    scrollbar.pack(side="right", fill="y", padx=2, pady=2)

    def load_inventory(query=""):
        for item in tree.get_children():
            tree.delete(item)
        
        products = product_model.get_all_products()
        for p in products:
            p_id, p_name, p_price, p_stock, p_barcode, p_category = p[:6]
            p_loyalty = p[6] if len(p) > 6 else 0

            if query.lower() in p_name.lower() or (p_category and query.lower() in p_category.lower()):
                tree.insert("", "end", values=(p_id, p_name, p_category, f"{p_price:.2f}", p_stock, p_barcode, p_loyalty))

    search_entry.bind("<KeyRelease>", lambda e: load_inventory(search_var.get()))
    load_inventory()

    # Edit Functionality
    def edit_selected_product():
        selected = tree.selection()
        if not selected:
            return
        
        item_values = tree.item(selected[0])['values']
        p_id = item_values[0]
        
        product = product_model.get_product_by_id(p_id)
        if not product:
            return

        # Edit Window
        edit_win = ctk.CTkToplevel(parent)
        edit_win.title("Edit Product")
        edit_win.geometry("400x550")
        edit_win.grab_set()

        ctk.CTkLabel(edit_win, text="Edit Product Details", font=("Roboto Medium", 18)).pack(pady=20)

        fields = ["Name", "Price", "Stock", "Barcode", "Category", "Loyalty Points"]
        entries = {}
        
        current_vals = {
            "Name": product[1],
            "Price": product[2],
            "Stock": product[3],
            "Barcode": product[4],
            "Category": product[5],
            "Loyalty Points": product[6] if len(product) > 6 else 0
        }

        for field in fields:
            row = ctk.CTkFrame(edit_win, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=field, width=100, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row)
            entry.insert(0, str(current_vals[field]))
            entry.pack(side="left", fill="x", expand=True)
            entries[field] = entry

        def save_changes():
            try:
                name = entries["Name"].get()
                price = float(entries["Price"].get())
                stock = int(entries["Stock"].get())
                barcode = entries["Barcode"].get()
                category = entries["Category"].get()
                loyalty = int(entries["Loyalty Points"].get())
                
                if product_model.update_product(p_id, name, price, stock, barcode, category, loyalty):
                    load_inventory(search_var.get())
                    edit_win.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update product")
            except ValueError:
                messagebox.showerror("Error", "Invalid input format")

        ctk.CTkButton(edit_win, text="Save Changes", command=save_changes).pack(pady=30)

    # Action Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=20)
    
    ctk.CTkButton(btn_frame, text="Refresh List", command=lambda: load_inventory(search_var.get()), fg_color="gray").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Edit Selected", command=edit_selected_product).pack(side="left", padx=10)

    return frame
