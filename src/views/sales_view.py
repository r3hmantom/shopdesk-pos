import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.product_model import ProductModel
from src.models.sales_model import SalesModel
from src.models.customer_model import CustomerModel
from src.models.discount_model import DiscountModel
from src.models.config_model import ConfigModel

from src.utils.receipt_generator import ReceiptGenerator

def build_sales_frame(parent, auth_controller):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    product_model = ProductModel()
    sales_model = SalesModel()
    customer_model = CustomerModel()
    discount_model = DiscountModel()
    config_model = ConfigModel()
    
    cart = [] 
    current_customer = None

    # --- Left Panel: Product Search & List ---
    left_panel = ctk.CTkFrame(frame, corner_radius=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Search Bar
    search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    search_frame.pack(fill="x", padx=10, pady=10)
    
    search_var = tk.StringVar()
    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, placeholder_text="Search Product...", height=40, font=("Roboto", 14))
    search_entry.pack(fill="x")

    # Product List (Treeview)
    # Need a frame to hold treeview and scrollbar
    tree_container = ctk.CTkFrame(left_panel, fg_color="transparent")
    tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Roboto", 12), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Roboto Medium", 12), background="#e0e0e0")

    prod_columns = ("ID", "Name", "Price", "Stock")
    prod_tree = ttk.Treeview(tree_container, columns=prod_columns, show="headings", selectmode="browse")
    
    prod_tree.heading("ID", text="ID")
    prod_tree.heading("Name", text="Name")
    prod_tree.heading("Price", text="Price")
    prod_tree.heading("Stock", text="Stock")
    
    prod_tree.column("ID", width=50, anchor="center")
    prod_tree.column("Name", width=250)
    prod_tree.column("Price", width=80, anchor="e")
    prod_tree.column("Stock", width=80, anchor="center")

    scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=prod_tree.yview)
    prod_tree.configure(yscroll=scrollbar.set)
    
    prod_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_products(query=""):
        for item in prod_tree.get_children():
            prod_tree.delete(item)
        products = product_model.get_all_products()
        for p in products:
            if query.lower() in p[1].lower() or (p[4] and query in p[4]):
                prod_tree.insert("", "end", values=(p[0], p[1], f"{p[2]:.2f}", p[3]))

    search_entry.bind("<KeyRelease>", lambda e: load_products(search_var.get()))
    load_products()

    def add_to_cart():
        selected_item = prod_tree.selection()
        if not selected_item:
            return
        item_values = prod_tree.item(selected_item[0])['values']
        p_id, p_name, p_price_str, p_stock = item_values
        p_price = float(p_price_str)
        
        # Check stock
        if int(p_stock) <= 0:
            messagebox.showwarning("Out of Stock", f"{p_name} is out of stock.")
            return
        
        if int(p_stock) <= 5:
             messagebox.showinfo("Low Stock", f"Warning: Low stock for {p_name} ({p_stock} remaining).")

        # Check if already in cart
        for item in cart:
            if item['id'] == p_id:
                if item['quantity'] < int(p_stock):
                    item['quantity'] += 1
                    item['total'] = item['quantity'] * item['price']
                else:
                    messagebox.showwarning("Stock Limit", "Cannot add more than available stock.")
                update_cart_display()
                return

        cart.append({
            'id': p_id,
            'name': p_name,
            'price': p_price,
            'quantity': 1,
            'total': p_price,
            'stock': int(p_stock)
        })
        update_cart_display()

    add_btn = ctk.CTkButton(left_panel, text="Add to Cart", command=add_to_cart, height=40, font=("Roboto Medium", 14))
    add_btn.pack(fill="x", padx=10, pady=10)

    # --- Right Panel: Cart & Checkout ---
    right_panel = ctk.CTkFrame(frame, width=400, corner_radius=10)
    right_panel.pack(side="right", fill="both", padx=10, pady=10)

    # Customer Info
    cust_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    cust_frame.pack(fill="x", padx=10, pady=10)
    
    cust_label = ctk.CTkLabel(cust_frame, text="Customer: Guest", font=("Roboto Medium", 14), anchor="w")
    cust_label.pack(side="left", fill="x", expand=True)

    def set_customer(cust):
        nonlocal current_customer
        current_customer = cust
        cust_label.configure(text=f"{cust[1]} (Pts: {cust[3]})")

    def open_customer_search():
        # Simple dialog using CTkInputDialog or Toplevel
        # Using Toplevel for custom layout
        top = ctk.CTkToplevel(parent)
        top.title("Search Customer")
        top.geometry("300x200")
        
        ctk.CTkLabel(top, text="Phone Number:").pack(pady=10)
        phone_ent = ctk.CTkEntry(top)
        phone_ent.pack(pady=5)
        
        def search():
            ph = phone_ent.get()
            c = customer_model.get_customer_by_phone(ph)
            if c:
                set_customer(c)
                top.destroy()
            else:
                messagebox.showinfo("Not Found", "Customer not found.")
        
        ctk.CTkButton(top, text="Search", command=search).pack(pady=20)

    cust_btn = ctk.CTkButton(cust_frame, text="Select Customer", width=100, height=30, command=open_customer_search)
    cust_btn.pack(side="right")

    # Cart List
    cart_label = ctk.CTkLabel(right_panel, text="Current Sale", font=("Roboto Medium", 16))
    cart_label.pack(pady=(10, 5))

    # Scrollable Frame for Cart Items
    cart_scroll_frame = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
    cart_scroll_frame.pack(fill="both", expand=True, padx=10)

    total_label = ctk.CTkLabel(right_panel, text="Total: $0.00", font=("Roboto", 24, "bold"))
    total_label.pack(pady=20)

    def change_qty(index, delta):
        item = cart[index]
        new_qty = item['quantity'] + delta
        
        if new_qty <= 0:
            del cart[index]
        else:
            # Check stock if increasing
            if delta > 0 and new_qty > item.get('stock', 9999): 
                 messagebox.showwarning("Stock Limit", "Cannot add more than available stock.")
                 return
            
            item['quantity'] = new_qty
            item['total'] = item['quantity'] * item['price']
            
        update_cart_display()

    def update_cart_display():
        for widget in cart_scroll_frame.winfo_children():
            widget.destroy()
            
        total_amount = 0
        
        for i, item in enumerate(cart):
            # Row Frame
            row = ctk.CTkFrame(cart_scroll_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            # Name
            ctk.CTkLabel(row, text=item['name'], width=120, anchor="w", font=("Roboto", 14)).pack(side="left", padx=(5,0))
            
            # Qty Controls
            qty_frame = ctk.CTkFrame(row, fg_color="transparent")
            qty_frame.pack(side="left", padx=5)
            
            btn_minus = ctk.CTkButton(qty_frame, text="-", width=30, height=25, 
                                      command=lambda idx=i: change_qty(idx, -1),
                                      fg_color="#EF4444", hover_color="#DC2626")
            btn_minus.pack(side="left", padx=2)
            
            ctk.CTkLabel(qty_frame, text=str(item['quantity']), width=30, font=("Roboto", 14)).pack(side="left", padx=2)
            
            btn_plus = ctk.CTkButton(qty_frame, text="+", width=30, height=25,
                                     command=lambda idx=i: change_qty(idx, 1),
                                     fg_color="#10B981", hover_color="#059669")
            btn_plus.pack(side="left", padx=2)
            
            # Total
            ctk.CTkLabel(row, text=f"${item['total']:.2f}", width=80, anchor="e", font=("Roboto", 14)).pack(side="right", padx=5)
            
            total_amount += item['total']
        
        total_label.configure(text=f"Total: ${total_amount:.2f}")

    def checkout():
        if not cart:
            messagebox.showwarning("Empty Cart", "Cart is empty.")
            return
        
        # Calculate initial total
        subtotal = sum(item['total'] for item in cart)
        
        # Payment Window
        pay_win = ctk.CTkToplevel(parent)
        pay_win.title("Payment & Checkout")
        pay_win.geometry("600x700")
        
        # Ensure window is visible before grabbing focus to avoid TclError
        pay_win.after(100, lambda: pay_win.grab_set())
        
        # Main Container
        main_container = ctk.CTkFrame(pay_win, corner_radius=10)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(main_container, text="Checkout", font=("Roboto Medium", 24)).pack(pady=(20, 10))
        
        # Totals Section
        totals_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        totals_frame.pack(fill="x", padx=20, pady=10)
        
        lbl_subtotal = ctk.CTkLabel(totals_frame, text=f"Subtotal: ${subtotal:.2f}", font=("Roboto", 16))
        lbl_subtotal.pack(anchor="w")
        
        lbl_discount = ctk.CTkLabel(totals_frame, text="Discount: -$0.00", font=("Roboto", 16), text_color="#10B981")
        lbl_discount.pack(anchor="w")
        
        lbl_tax = ctk.CTkLabel(totals_frame, text="Tax (10%): $0.00", font=("Roboto", 16))
        lbl_tax.pack(anchor="w")
        
        lbl_final = ctk.CTkLabel(totals_frame, text=f"Total Due: ${subtotal:.2f}", font=("Roboto", 24, "bold"))
        lbl_final.pack(anchor="w", pady=(5, 0))

        # State variables
        discount_amount = 0.0
        points_redeemed_val = 0.0
        tax_amount = 0.0
        final_total = subtotal
        # Fetch dynamic tax rate
        tax_rate_percent = config_model.get_tax_rate()
        tax_rate = tax_rate_percent / 100.0

        def update_totals():
            nonlocal final_total, tax_amount
            
            # Calculate discount
            total_discount = discount_amount + points_redeemed_val
            
            # Taxable amount (assuming tax on price after discount)
            taxable = max(0, subtotal - total_discount)
            tax_amount = taxable * tax_rate
            
            final_total = taxable + tax_amount
            
            lbl_discount.configure(text=f"Discount/Points: -${total_discount:.2f}")
            lbl_tax.configure(text=f"Tax ({tax_rate_percent}%): ${tax_amount:.2f}")
            lbl_final.configure(text=f"Total Due: ${final_total:.2f}")
            
            # Trigger update immediately
            if method_var.get() == "Split":
                # Update split hint if needed or just rely on user
                pass

        # --- Discount Section ---
        disc_frame = ctk.CTkFrame(main_container)
        disc_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(disc_frame, text="Discount Code:").pack(side="left", padx=10)
        disc_entry = ctk.CTkEntry(disc_frame, width=150, placeholder_text="Code")
        disc_entry.pack(side="left", padx=10)
        
        def apply_discount():
            nonlocal discount_amount
            code = disc_entry.get().upper()
            
            discount = discount_model.get_discount_by_code(code)
            
            if discount:
                # discount: (id, code, type, value, is_active)
                d_type = discount[2]
                d_val = float(discount[3])
                
                if d_type == "PERCENTAGE":
                    discount_amount = subtotal * (d_val / 100.0)
                    msg = f"{d_val}% Discount Applied!"
                else:
                    discount_amount = d_val
                    msg = f"${d_val} Flat Discount Applied!"
                
                messagebox.showinfo("Applied", msg, parent=pay_win)
            else:
                discount_amount = 0
                messagebox.showwarning("Invalid", "Invalid or Inactive Discount Code", parent=pay_win)
            
            update_totals()

        ctk.CTkButton(disc_frame, text="Apply", width=80, command=apply_discount).pack(side="left", padx=10)

        # --- Loyalty Section ---
        if current_customer:
            loyalty_frame = ctk.CTkFrame(main_container)
            loyalty_frame.pack(fill="x", padx=20, pady=10)
            
            avail_points = current_customer[3]
            max_redeemable_val = avail_points * 0.10
            
            ctk.CTkLabel(loyalty_frame, text=f"Loyalty Points: {avail_points} (${max_redeemable_val:.2f})").pack(side="left", padx=10)
            
            redeem_var = tk.BooleanVar()
            
            def toggle_points():
                nonlocal points_redeemed_val
                if redeem_var.get():
                    # Redeem max possible but not more than total
                    needed = subtotal - discount_amount
                    to_redeem = min(max_redeemable_val, needed)
                    points_redeemed_val = to_redeem
                else:
                    points_redeemed_val = 0.0
                update_totals()

            ctk.CTkCheckBox(loyalty_frame, text="Redeem Points", variable=redeem_var, command=toggle_points).pack(side="right", padx=10)

        # --- Payment Method Section ---
        method_frame = ctk.CTkFrame(main_container)
        method_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(method_frame, text="Payment Method", font=("Roboto Medium", 16)).pack(anchor="w", padx=10, pady=5)
        
        method_var = tk.StringVar(value="Cash")
        
        # Split Payment Inputs
        split_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        
        cash_entry = ctk.CTkEntry(split_frame, placeholder_text="Cash Amount")
        card_entry = ctk.CTkEntry(split_frame, placeholder_text="Card Amount")
        
        def on_method_change():
            if method_var.get() == "Split":
                split_frame.pack(fill="x", padx=20, pady=5)
                cash_entry.pack(side="left", fill="x", expand=True, padx=5)
                card_entry.pack(side="left", fill="x", expand=True, padx=5)
            else:
                split_frame.pack_forget()

        ctk.CTkRadioButton(method_frame, text="Cash", variable=method_var, value="Cash", command=on_method_change).pack(side="left", padx=20, pady=10)
        ctk.CTkRadioButton(method_frame, text="Card", variable=method_var, value="Card", command=on_method_change).pack(side="left", padx=20, pady=10)
        ctk.CTkRadioButton(method_frame, text="Split", variable=method_var, value="Split", command=on_method_change).pack(side="left", padx=20, pady=10)

        def process_payment():
            method = method_var.get()
            
            # Validation for Split
            if method == "Split":
                try:
                    c_val = float(cash_entry.get() or 0)
                    cd_val = float(card_entry.get() or 0)
                    if abs((c_val + cd_val) - final_total) > 0.01:
                        messagebox.showerror("Error", f"Split amounts must equal {final_total:.2f}", parent=pay_win)
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid amounts entered", parent=pay_win)
                    return

            # Create Sale
            sale_items = [{'product_id': i['id'], 'quantity': i['quantity'], 'price': i['price']} for i in cart]
            user_id = auth_controller.current_user['id']
            customer_id = current_customer[0] if current_customer else None
            
            # Record the sale
            # Note: We are recording the *final* total after discounts.
            # If points were used, we might want to record that.
            # For simplicity, we'll just record the payment method string with details if needed.
            
            final_method_str = method
            if points_redeemed_val > 0:
                final_method_str += f" + Points(${points_redeemed_val:.2f})"
            if discount_amount > 0:
                final_method_str += f" + Disc(${discount_amount:.2f})"

            sale_id = sales_model.create_sale(user_id, customer_id, final_total, final_method_str, sale_items, tax_amount=tax_amount)
            
            if sale_id:
                # Deduct points if used
                if points_redeemed_val > 0 and current_customer:
                    pts_deducted = int(points_redeemed_val / 0.10)
                    customer_model.update_loyalty_points(customer_id, -pts_deducted)
                
                # Generate Receipt
                try:
                    ReceiptGenerator.generate_receipt(
                        sale_id, 
                        auth_controller.current_user['username'], 
                        current_customer[1] if current_customer else "Guest",
                        cart, subtotal, tax_amount, (discount_amount + points_redeemed_val), final_total, final_method_str
                    )
                except Exception as e:
                    print(f"Receipt Gen Error: {e}")

                # Refresh customer display
                if current_customer:
                    updated_customer = customer_model.get_customer_by_id(customer_id)
                    if updated_customer:
                        set_customer(updated_customer)
                
                messagebox.showinfo("Success", f"Sale Completed! Receipt Generated.", parent=pay_win)
                cart.clear()
                update_cart_display()
                load_products()
                pay_win.destroy()
            else:
                messagebox.showerror("Error", "Transaction Failed", parent=pay_win)

        ctk.CTkButton(main_container, text="Confirm Payment", command=process_payment, height=50, font=("Roboto Medium", 16), fg_color="#5cb85c", hover_color="#4cae4c").pack(side="bottom", fill="x", padx=20, pady=20)

    checkout_btn = ctk.CTkButton(right_panel, text="Checkout", command=checkout, height=50, font=("Roboto Medium", 18))
    checkout_btn.pack(fill="x", padx=20, pady=20)

    return frame
