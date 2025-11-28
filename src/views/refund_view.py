import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.sales_model import SalesModel

def build_refund_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    sales_model = SalesModel()
    
    # Header
    header = ctk.CTkFrame(frame, height=70, corner_radius=0, fg_color="#B91C1C") 
    header.pack(fill="x")
    ctk.CTkLabel(header, text="Process Refund", font=("Roboto Medium", 20), text_color="white").pack(side="left", padx=20, pady=15)

    # Main Content
    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=20)

    # Split Layout
    paned = tk.PanedWindow(content, orient=tk.HORIZONTAL, sashwidth=5, bg="#f0f0f0")
    paned.pack(fill="both", expand=True)

    # --- Left Panel: Recent Transactions ---
    left_panel = ctk.CTkFrame(paned, corner_radius=10)
    paned.add(left_panel, width=400)

    ctk.CTkLabel(left_panel, text="Recent Transactions", font=("Roboto Medium", 16)).pack(pady=15)
    
    # Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Roboto", 11), rowheight=25)
    
    hist_columns = ("ID", "Date", "Total")
    hist_tree = ttk.Treeview(left_panel, columns=hist_columns, show="headings")
    hist_tree.heading("ID", text="ID")
    hist_tree.heading("Date", text="Date")
    hist_tree.heading("Total", text="Total")
    
    hist_tree.column("ID", width=50, anchor="center")
    hist_tree.column("Date", width=150, anchor="center")
    hist_tree.column("Total", width=80, anchor="e")
    
    hist_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def load_history():
        for item in hist_tree.get_children():
            hist_tree.delete(item)
        sales = sales_model.get_sales_history()
        for s in sales:
            ts = s[3].strftime("%Y-%m-%d %H:%M") if s[3] else ""
            hist_tree.insert("", "end", values=(s[0], ts, f"${s[1]:.2f}"))

    ctk.CTkButton(left_panel, text="Refresh List", command=load_history, fg_color="gray").pack(pady=10)
    load_history()

    # --- Right Panel: Search & Details ---
    right_panel = ctk.CTkFrame(paned, fg_color="transparent")
    paned.add(right_panel)

    # Search Bar
    search_card = ctk.CTkFrame(right_panel, corner_radius=10)
    search_card.pack(fill="x", pady=(0, 20), padx=(10, 0))
    
    ctk.CTkLabel(search_card, text="Find Transaction by ID", font=("Roboto Medium", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    
    search_row = ctk.CTkFrame(search_card, fg_color="transparent")
    search_row.pack(fill="x", padx=20, pady=(0, 15))
    
    tid_entry = ctk.CTkEntry(search_row, placeholder_text="Transaction ID", width=200)
    tid_entry.pack(side="left", padx=(0, 10))
    
    # Results Area
    results_card = ctk.CTkFrame(right_panel, corner_radius=10)
    results_card.pack(fill="both", expand=True, padx=(10, 0))
    
    details_frame = ctk.CTkScrollableFrame(results_card, fg_color="transparent")
    details_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_transaction_details(sale):
        for widget in details_frame.winfo_children():
            widget.destroy()

        sale_id = sale[0]
        total = sale[3]
        date = sale[5]
        
        ctk.CTkLabel(details_frame, text=f"Transaction #{sale_id}", font=("Roboto Medium", 18)).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(details_frame, text=f"Date: {date}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(details_frame, text=f"Total Amount: ${total}", font=("Roboto Medium", 16), text_color="#10B981").pack(anchor="w", pady=(10, 20))
        
        items = sales_model.get_sale_items(sale_id)
        
        if not items:
             ctk.CTkLabel(details_frame, text="No items found.").pack()
             return

        # Header
        header_row = ctk.CTkFrame(details_frame, fg_color="#eee", height=30)
        header_row.pack(fill="x", pady=5)
        ctk.CTkLabel(header_row, text="Select", width=50).pack(side="left")
        ctk.CTkLabel(header_row, text="Item Name", width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(header_row, text="Qty", width=50).pack(side="left")
        ctk.CTkLabel(header_row, text="Price", width=80).pack(side="left")
        ctk.CTkLabel(header_row, text="Status", width=100).pack(side="left")

        check_vars = []
        
        for item in items:
            sale_item_id, name, qty, price, prod_id = item[:5]
            refunded_qty = item[5] if len(item) > 5 else 0
            remaining_qty = qty - refunded_qty

            row = ctk.CTkFrame(details_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            var = tk.IntVar()
            check_vars.append((var, sale_item_id, prod_id, remaining_qty, name))
            
            chk_frame = ctk.CTkFrame(row, fg_color="transparent", width=50)
            chk_frame.pack(side="left")
            
            if remaining_qty > 0:
                ctk.CTkCheckBox(chk_frame, text="", variable=var, width=20).pack(anchor="center")
            
            ctk.CTkLabel(row, text=name, width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(qty), width=50).pack(side="left")
            ctk.CTkLabel(row, text=f"${price:.2f}", width=80).pack(side="left")
            
            status_text = "Refunded" if remaining_qty == 0 else (f"Partially ({refunded_qty})" if refunded_qty > 0 else "Sold")
            ctk.CTkLabel(row, text=status_text, width=100, text_color="gray").pack(side="left")
            
        def process_refund():
            items_to_refund = []
            for var, si_id, p_id, max_qty, item_name in check_vars:
                if var.get() == 1:
                    items_to_refund.append((si_id, p_id, max_qty, item_name))
            
            if not items_to_refund:
                messagebox.showwarning("Warning", "No items selected.")
                return
            
            if not messagebox.askyesno("Confirm", f"Refund {len(items_to_refund)} items?"):
                return

            success_count = 0
            for si_id, p_id, qty, item_name in items_to_refund:
                success, msg = sales_model.process_refund_item(si_id, p_id, qty)
                if success:
                    success_count += 1
                else:
                    messagebox.showerror("Error", f"Failed to refund {item_name}: {msg}")
            
            if success_count > 0:
                messagebox.showinfo("Success", f"Processed {success_count} refunds.")
                show_transaction_details(sale)

        ctk.CTkButton(details_frame, text="Process Refund", command=process_refund, fg_color="#DC2626", hover_color="#B91C1C").pack(pady=30)

    def search_transaction():
        tid = tid_entry.get()
        if not tid or not tid.isdigit():
             messagebox.showwarning("Warning", "Invalid ID")
             return

        sale = sales_model.get_sale_by_id(int(tid))
        if sale:
            show_transaction_details(sale)
        else:
            for widget in details_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(details_frame, text="Transaction not found.", text_color="red").pack(pady=20)

    ctk.CTkButton(search_row, text="Search", command=search_transaction, width=80).pack(side="left")

    def on_history_select(event):
        selected = hist_tree.selection()
        if selected:
            item = hist_tree.item(selected[0])
            sale_id = item['values'][0]
            tid_entry.delete(0, tk.END)
            tid_entry.insert(0, str(sale_id))
            search_transaction()

    hist_tree.bind("<<TreeviewSelect>>", on_history_select)

    return frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Refund Screen")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    try:
        root.state("zoomed")
    except tk.TclError:
        # Fallback for Linux
        root.attributes("-zoomed", True)
    
    frame = build_refund_frame(root)
    frame.pack(fill="both", expand=True)
    
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
