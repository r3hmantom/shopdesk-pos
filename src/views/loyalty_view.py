import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from src.models.customer_model import CustomerModel

def build_loyalty_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    customer_model = CustomerModel()
    
    ctk.CTkLabel(frame, text="Customer Loyalty & Profiles", font=("Roboto Medium", 24)).pack(pady=(30, 20))

    # --- Search Section ---
    search_frame = ctk.CTkFrame(frame, corner_radius=10)
    search_frame.pack(pady=20, padx=20)
    
    ctk.CTkLabel(search_frame, text="Search by Phone:", font=("Roboto", 16)).pack(side="left", padx=20, pady=20)
    phone_entry = ctk.CTkEntry(search_frame, width=200, font=("Roboto", 16))
    phone_entry.pack(side="left", padx=10, pady=20)
    
    # --- Details Section ---
    details_frame = ctk.CTkFrame(frame, corner_radius=10, border_width=2, border_color="#ddd", fg_color="white")
    details_frame.pack(pady=20, padx=50, fill="x")
    
    name_label = ctk.CTkLabel(details_frame, text="Name: -", font=("Roboto", 18), text_color="black")
    name_label.pack(pady=20)
    
    points_label = ctk.CTkLabel(details_frame, text="Loyalty Points: -", font=("Roboto", 18), text_color="black")
    points_label.pack(pady=(0, 20))
    
    # Receipt History Button
    history_btn = ctk.CTkButton(details_frame, text="View Purchase History", width=200, state="disabled", command=lambda: show_history_popup(current_customer_id))
    history_btn.pack(pady=(0, 20))

    current_customer_id = None

    def search_customer():
        nonlocal current_customer_id
        phone = phone_entry.get()
        customer = customer_model.get_customer_by_phone(phone)
        
        if customer:
            current_customer_id = customer[0]
            name_label.configure(text=f"Name: {customer[1]}")
            points_label.configure(text=f"Loyalty Points: {customer[3]}")
            history_btn.configure(state="normal")
        else:
            current_customer_id = None
            name_label.configure(text="Name: Not Found")
            points_label.configure(text="Loyalty Points: -")
            history_btn.configure(state="disabled")
            if messagebox.askyesno("Not Found", "Customer not found. Create new?"):
                create_customer_popup(phone)

    from src.models.sales_model import SalesModel
    from src.utils.receipt_generator import ReceiptGenerator
    sales_model = SalesModel()

    def show_history_popup(cid):
        if not cid: return
        
        popup = ctk.CTkToplevel(parent)
        popup.title("Purchase History")
        popup.geometry("600x400")
        
        sales = sales_model.get_customer_receipts(cid)
        
        if not sales:
            ctk.CTkLabel(popup, text="No purchase history found.").pack(pady=20)
            return

        # List of Receipts
        sf = ctk.CTkScrollableFrame(popup, width=550, height=350)
        sf.pack(fill="both", expand=True, padx=10, pady=10)
        
        for s in sales:
            # s: id, timestamp, total, method
            sid, ts, total, method = s
            row = ctk.CTkFrame(sf)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=f"#{sid}", width=40).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(ts), width=150).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"${total:.2f}", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=method, width=120).pack(side="left", padx=5)
            
            def view_receipt(sale_id=sid):
                import os
                receipt_dir = ReceiptGenerator.get_receipt_dir()
                r_path = os.path.join(receipt_dir, f"receipt_{sale_id}.txt")
                
                if os.path.exists(r_path):
                    try:
                        if os.name == 'nt':
                            os.startfile(r_path)
                        else:
                            import subprocess
                            subprocess.call(['xdg-open', r_path])
                    except:
                        messagebox.showinfo("Info", f"Receipt file located at {r_path}")
                else:
                    messagebox.showwarning("Missing", f"Receipt file not found at:\n{r_path}")
            
            ctk.CTkButton(row, text="View", width=60, command=view_receipt).pack(side="right", padx=5)

    ctk.CTkButton(search_frame, text="Search", command=search_customer, width=100).pack(side="left", padx=20)

    # --- Create Customer Popup ---
    def create_customer_popup(phone_val=""):
        popup = ctk.CTkToplevel(parent)
        popup.title("Add Customer")
        popup.geometry("400x300")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="Name:").pack(pady=(20, 5))
        name_ent = ctk.CTkEntry(popup)
        name_ent.pack(pady=5)
        
        ctk.CTkLabel(popup, text="Phone:").pack(pady=(10, 5))
        phone_ent = ctk.CTkEntry(popup)
        phone_ent.insert(0, phone_val)
        phone_ent.pack(pady=5)
        
        def save():
            name = name_ent.get()
            phone = phone_ent.get()
            if name and phone:
                cid = customer_model.create_customer(name, phone)
                if cid:
                    messagebox.showinfo("Success", "Customer created!")
                    popup.destroy()
                    phone_entry.delete(0, tk.END)
                    phone_entry.insert(0, phone)
                    search_customer()
                else:
                    messagebox.showerror("Error", "Could not create customer.")
            else:
                messagebox.showwarning("Input", "Name and Phone required.")

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=30)

    ctk.CTkButton(frame, text="Add New Customer", command=create_customer_popup, fg_color="#5cb85c", hover_color="#4cae4c").pack(pady=10)

    return frame
