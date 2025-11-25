import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from src.models.supplier_model import SupplierModel
from src.models.product_model import ProductModel

def build_restock_frame(root):
    frame = ctk.CTkFrame(root, fg_color="transparent")
    
    product_model = ProductModel()
    supplier_model = SupplierModel()
    
    # Header
    ctk.CTkLabel(frame, text="Inventory Restock", font=("Roboto Medium", 24)).pack(pady=(30, 20))

    # Content Card
    content_card = ctk.CTkFrame(frame, width=600, corner_radius=15)
    content_card.pack(pady=20, padx=20)

    ctk.CTkLabel(content_card, text="Update Stock Level", font=("Roboto Medium", 18)).pack(pady=(30, 20))

    # Form
    form_frame = ctk.CTkFrame(content_card, fg_color="transparent")
    form_frame.pack(pady=10)

    # Supplier Section
    ctk.CTkLabel(form_frame, text="Select Supplier", anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=5)
    
    suppliers = supplier_model.get_all_suppliers()
    supp_map = {s[1]: s[0] for s in suppliers}
    supp_options = list(supp_map.keys())
    
    supp_dropdown = ctk.CTkComboBox(form_frame, values=supp_options, width=300, state="readonly")
    if supp_options:
        supp_dropdown.set(supp_options[0])
    supp_dropdown.grid(row=1, column=0, padx=20, pady=(0, 20))

    def show_add_supplier_popup():
        popup = ctk.CTkToplevel(root)
        popup.title("Add Supplier")
        popup.geometry("400x450")
        popup.lift()  # Bring to front
        popup.focus_force() # Focus
        popup.grab_set() # Modal
        
        ctk.CTkLabel(popup, text="New Supplier", font=("Roboto Medium", 18)).pack(pady=20)
        
        name_ent = ctk.CTkEntry(popup, placeholder_text="Name")
        name_ent.pack(pady=10)
        contact_ent = ctk.CTkEntry(popup, placeholder_text="Contact Person")
        contact_ent.pack(pady=10)
        phone_ent = ctk.CTkEntry(popup, placeholder_text="Phone")
        phone_ent.pack(pady=10)
        email_ent = ctk.CTkEntry(popup, placeholder_text="Email")
        email_ent.pack(pady=10)
        
        def save_sup():
            if supplier_model.add_supplier(name_ent.get(), contact_ent.get(), phone_ent.get(), email_ent.get()):
                # Ensure messagebox has a parent so it appears over the popup or root correctly
                messagebox.showinfo("Success", "Supplier Added", parent=popup)
                nonlocal supp_map, supp_options
                s_list = supplier_model.get_all_suppliers()
                supp_map = {s[1]: s[0] for s in s_list}
                supp_options = list(supp_map.keys())
                supp_dropdown.configure(values=supp_options)
                if supp_options:
                     supp_dropdown.set(supp_options[0])
                popup.destroy()
            else:
                messagebox.showerror("Error", "Failed", parent=popup)
        
        ctk.CTkButton(popup, text="Save", command=save_sup).pack(pady=20)

    ctk.CTkButton(form_frame, text="+ New", command=show_add_supplier_popup, width=60, height=24).grid(row=0, column=1, padx=10)

    # Item Section
    ctk.CTkLabel(form_frame, text="Select Item", anchor="w").grid(row=2, column=0, sticky="w", padx=20, pady=5)
    
    # Fetch items
    products = product_model.get_all_products()
    product_map = {f"{p[1]} (Current: {p[3]})": p[0] for p in products}
    item_options = list(product_map.keys())
    
    item_dropdown = ctk.CTkComboBox(form_frame, values=item_options, width=300, state="readonly")
    if item_options:
        item_dropdown.set(item_options[0])
    item_dropdown.grid(row=3, column=0, padx=20, pady=(0, 20))

    ctk.CTkLabel(form_frame, text="Quantity to Add", anchor="w").grid(row=4, column=0, sticky="w", padx=20, pady=5)
    qty_entry = ctk.CTkEntry(form_frame, width=300)
    qty_entry.grid(row=5, column=0, padx=20, pady=(0, 20))

    def refresh_dropdown():
        nonlocal products, product_map, item_options
        products = product_model.get_all_products()
        product_map = {f"{p[1]} (Current: {p[3]})": p[0] for p in products}
        item_options = list(product_map.keys())
        item_dropdown.configure(values=item_options)
        if item_options:
            item_dropdown.set(item_options[0])
        else:
            item_dropdown.set("")

    # Let's rewrite show_add_product_popup here to be safe
    def show_add_product_popup():

        popup = ctk.CTkToplevel(root)
        popup.title("Add New Product")
        popup.geometry("400x550")
        popup.grab_set()

        ctk.CTkLabel(popup, text="New Product Details", font=("Roboto Medium", 18)).pack(pady=20)

        def add_field(label):
            ctk.CTkLabel(popup, text=label, anchor="w").pack(anchor="w", padx=40, pady=(5, 0))
            entry = ctk.CTkEntry(popup)
            entry.pack(fill="x", padx=40, pady=5)
            return entry

        name_entry = add_field("Product Name")
        price_entry = add_field("Price")
        stock_entry = add_field("Initial Stock")
        barcode_entry = add_field("Barcode (Optional)")
        category_entry = add_field("Category (Optional)")
        loyalty_entry = add_field("Loyalty Points (Default 0)")

        def save_product():
            name = name_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()
            barcode = barcode_entry.get()
            category = category_entry.get()
            loyalty = loyalty_entry.get()

            if not name or not price or not stock:
                messagebox.showerror("Error", "Name, Price, and Stock are required.")
                return

            try:
                price = float(price)
                stock = int(stock)
                loyalty = int(loyalty) if loyalty else 0
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric values.")
                return

            success = product_model.add_product(name, price, stock, barcode, category, loyalty)
            if success:
                messagebox.showinfo("Success", "Product added successfully!")
                refresh_dropdown()
                popup.destroy()
            else:
                messagebox.showerror("Error", "Failed to add product.")

        ctk.CTkButton(popup, text="Save Product", command=save_product).pack(pady=30)

    def perform_restock():
        item_text = item_dropdown.get()
        qty = qty_entry.get()
        supp_name = supp_dropdown.get()
        
        if not item_text:
            messagebox.showerror("Error", "Please select an item.")
            return

        if not qty.isdigit() or int(qty) <= 0:
            messagebox.showerror("Error", "Please enter a valid positive quantity.")
            return
            
        product_id = product_map.get(item_text)
        supp_id = supp_map.get(supp_name)
        
        if product_id:
            if supp_id:
                success = supplier_model.create_restock_order(supp_id, product_id, int(qty))
            else:
                success = product_model.update_stock(product_id, int(qty))
                
            if success:
                messagebox.showinfo("Success", f"Successfully added {qty} units.")
                refresh_dropdown()
                qty_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to update stock.")

    # Buttons
    ctk.CTkButton(content_card, text="Update Stock", command=perform_restock, width=200, height=40, font=("Roboto Medium", 14)).pack(pady=(10, 10))

    ctk.CTkButton(content_card, text="+ Create New Product", command=show_add_product_popup, fg_color="transparent", text_color="#3B82F6", hover_color="#eee").pack(pady=(0, 30))

    return frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Restock Screen")
    # Full screen setup
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    try:
        root.state("zoomed") # For Windows
    except tk.TclError:
        # Fallback for Linux
        root.attributes("-zoomed", True)
    # root.attributes('-fullscreen', True) # For Linux/Kiosk mode if preferred
    
    frame = build_restock_frame(root)
    frame.pack(fill="both", expand=True)
    
    # Escape to exit for testing
    root.bind("<Escape>", lambda e: root.destroy())
    
    root.mainloop()
