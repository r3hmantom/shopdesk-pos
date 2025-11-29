import tkinter as tk
from tkinter import ttk, messagebox
import sys

def build_payment_frame(root):
    main_frame = tk.Frame(root, bg="#F3F4F6")
    
    # Header
    header = tk.Frame(main_frame, bg="#1F2937", height=70)
    header.pack(fill="x")
    tk.Label(header, text="Checkout & Payment", font=("Helvetica", 20, "bold"), bg="#1F2937", fg="white").pack(side="left", padx=20, pady=15)

    # Main Content Area - Split View
    content_area = tk.Frame(main_frame, bg="#F3F4F6")
    content_area.pack(fill="both", expand=True, padx=40, pady=40)

    # Left Side: Order Summary
    left_panel = tk.Frame(content_area, bg="white", bd=1, relief="solid")
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
    
    tk.Label(left_panel, text="Order Summary", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=20, anchor="w", padx=20)

    # Hardcoded Cart
    cart_items = [
        {"name": "Apple", "price": 1.50, "qty": 2},
        {"name": "Banana", "price": 0.80, "qty": 5},
        {"name": "Milk", "price": 3.00, "qty": 1},
        {"name": "Bread", "price": 2.50, "qty": 2},
        {"name": "Eggs (Dozen)", "price": 4.00, "qty": 1},
    ]
    total_amount = sum(item["price"] * item["qty"] for item in cart_items)

    # Treeview for items
    columns = ("item", "qty", "price", "total")
    tree = ttk.Treeview(left_panel, columns=columns, show="headings", height=15)
    tree.heading("item", text="Item")
    tree.heading("qty", text="Qty")
    tree.heading("price", text="Price")
    tree.heading("total", text="Total")
    
    tree.column("item", width=200)
    tree.column("qty", width=50, anchor="center")
    tree.column("price", width=80, anchor="e")
    tree.column("total", width=80, anchor="e")
    
    # Style the treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
    style.configure("Treeview", font=("Helvetica", 10), rowheight=30)

    for item in cart_items:
        tree.insert("", tk.END, values=(item["name"], item["qty"], f"${item['price']:.2f}", f"${item['price'] * item['qty']:.2f}"))
    
    tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # Total Display
    total_frame = tk.Frame(left_panel, bg="#F9FAFB", height=60)
    total_frame.pack(fill="x", side="bottom")
    tk.Label(total_frame, text="Total Amount:", font=("Helvetica", 14), bg="#F9FAFB", fg="#555").pack(side="left", padx=20, pady=15)
    tk.Label(total_frame, text=f"${total_amount:.2f}", font=("Helvetica", 20, "bold"), bg="#F9FAFB", fg="#10B981").pack(side="right", padx=20, pady=15)


    # Right Side: Payment Methods & Flows
    right_panel = tk.Frame(content_area, bg="white", bd=1, relief="solid")
    right_panel.pack(side="right", fill="both", expand=True)
    
    # Container for dynamic content in right panel
    action_container = tk.Frame(right_panel, bg="white")
    action_container.pack(fill="both", expand=True, padx=30, pady=30)

    def clear_action_container():
        for widget in action_container.winfo_children():
            widget.destroy()

    def show_payment_options():
        clear_action_container()
        tk.Label(action_container, text="Select Payment Method", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=(0, 30))
        
        btn_style = {"font": ("Helvetica", 14), "bg": "#3B82F6", "fg": "white", "activebackground": "#2563EB", "activeforeground": "white", "relief": "flat", "cursor": "hand2", "width": 20}
        
        tk.Button(action_container, text="💵 Cash", **btn_style, command=show_cash_flow).pack(pady=10, ipady=10)
        tk.Button(action_container, text="💳 Card", **btn_style, command=show_card_flow).pack(pady=10, ipady=10)
        tk.Button(action_container, text="➗ Split Payment", **btn_style, command=show_split_flow).pack(pady=10, ipady=10)

    def show_success_screen(method):
        clear_action_container()
        tk.Label(action_container, text="✅", font=("Helvetica", 60), bg="white", fg="#10B981").pack(pady=(50, 20))
        tk.Label(action_container, text="Payment Successful!", font=("Helvetica", 24, "bold"), bg="white", fg="#10B981").pack(pady=10)
        tk.Label(action_container, text=f"Paid via {method}", font=("Helvetica", 14), bg="white", fg="#666").pack(pady=10)
        
        tk.Button(action_container, text="New Transaction", font=("Helvetica", 12, "bold"), bg="#4B5563", fg="white", relief="flat", command=show_payment_options).pack(pady=40, ipadx=20, ipady=10)

    def show_failure_screen(reason):
        clear_action_container()
        tk.Label(action_container, text="❌", font=("Helvetica", 60), bg="white", fg="#EF4444").pack(pady=(50, 20))
        tk.Label(action_container, text="Payment Failed", font=("Helvetica", 24, "bold"), bg="white", fg="#EF4444").pack(pady=10)
        tk.Label(action_container, text=f"Reason: {reason}", font=("Helvetica", 14), bg="white", fg="#666").pack(pady=10)
        
        tk.Button(action_container, text="Try Again", font=("Helvetica", 12, "bold"), bg="#4B5563", fg="white", relief="flat", command=show_payment_options).pack(pady=40, ipadx=20, ipady=10)

    def show_cash_flow():
        clear_action_container()
        tk.Label(action_container, text="Cash Payment", font=("Helvetica", 18, "bold"), bg="white", fg="#333").pack(pady=(0, 20))
        tk.Label(action_container, text=f"Total Due: ${total_amount:.2f}", font=("Helvetica", 14), bg="white", fg="#666").pack(pady=10)
        
        tk.Label(action_container, text="Amount Tendered", font=("Helvetica", 12), bg="white").pack(anchor="w", padx=40)
        entry = tk.Entry(action_container, font=("Helvetica", 16), bd=2, relief="groove")
        entry.pack(fill="x", padx=40, pady=5, ipady=5)
        entry.focus()
        
        def process():
            try:
                tendered = float(entry.get())
                if tendered >= total_amount:
                    change = tendered - total_amount
                    messagebox.showinfo("Change", f"Please return change: ${change:.2f}")
                    show_success_screen("Cash")
                else:
                    messagebox.showerror("Error", "Insufficient amount.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")

        btn_frame = tk.Frame(action_container, bg="white")
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="Confirm Pay", font=("Helvetica", 12, "bold"), bg="#10B981", fg="white", relief="flat", command=process).pack(side="left", padx=10, ipadx=20, ipady=5)
        tk.Button(btn_frame, text="Cancel", font=("Helvetica", 12), bg="#E5E7EB", fg="#333", relief="flat", command=show_payment_options).pack(side="left", padx=10, ipadx=20, ipady=5)

    def show_card_flow():
        clear_action_container()
        tk.Label(action_container, text="Card Payment", font=("Helvetica", 18, "bold"), bg="white", fg="#333").pack(pady=(0, 20))
        tk.Label(action_container, text="Please swipe, insert, or tap card...", font=("Helvetica", 14, "italic"), bg="white", fg="#666").pack(pady=40)
        
        # Simulation buttons
        sim_frame = tk.Frame(action_container, bg="white")
        sim_frame.pack(pady=20)
        tk.Button(sim_frame, text="Simulate Success", bg="#D1FAE5", fg="#065F46", relief="flat", command=lambda: show_success_screen("Card")).pack(side="left", padx=10, ipadx=10, ipady=5)
        tk.Button(sim_frame, text="Simulate Decline", bg="#FEE2E2", fg="#991B1B", relief="flat", command=lambda: show_failure_screen("Card Declined")).pack(side="left", padx=10, ipadx=10, ipady=5)
        
        tk.Button(action_container, text="Cancel", font=("Helvetica", 12), bg="#E5E7EB", fg="#333", relief="flat", command=show_payment_options).pack(pady=20, ipadx=20, ipady=5)

    def show_split_flow():
        clear_action_container()
        tk.Label(action_container, text="Split Payment", font=("Helvetica", 18, "bold"), bg="white", fg="#333").pack(pady=(0, 20))
        tk.Label(action_container, text=f"Total Due: ${total_amount:.2f}", font=("Helvetica", 14), bg="white", fg="#666").pack(pady=10)
        
        form = tk.Frame(action_container, bg="white")
        form.pack(pady=20)
        
        tk.Label(form, text="Cash Amount:", font=("Helvetica", 12), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        cash_entry = tk.Entry(form, font=("Helvetica", 12), bd=2, relief="groove")
        cash_entry.grid(row=0, column=1, padx=10, pady=10, ipady=3)
        
        tk.Label(form, text="Card Amount:", font=("Helvetica", 12), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        card_entry = tk.Entry(form, font=("Helvetica", 12), bd=2, relief="groove")
        card_entry.grid(row=1, column=1, padx=10, pady=10, ipady=3)
        
        def process():
            try:
                c = float(cash_entry.get() or 0)
                cd = float(card_entry.get() or 0)
                if abs((c + cd) - total_amount) < 0.01:
                    show_success_screen("Split (Cash & Card)")
                else:
                    messagebox.showerror("Error", f"Total must equal {total_amount:.2f}. Current: {(c+cd):.2f}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")

        btn_frame = tk.Frame(action_container, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Confirm Pay", font=("Helvetica", 12, "bold"), bg="#10B981", fg="white", relief="flat", command=process).pack(side="left", padx=10, ipadx=20, ipady=5)
        tk.Button(btn_frame, text="Cancel", font=("Helvetica", 12), bg="#E5E7EB", fg="#333", relief="flat", command=show_payment_options).pack(side="left", padx=10, ipadx=20, ipady=5)

    # Initialize
    show_payment_options()
    
    return main_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Payment Screen")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    
    if sys.platform.startswith('win'):
        root.state("zoomed")
    else:
        root.attributes("-zoomed", True)
    
    frame = build_payment_frame(root)
    frame.pack(fill="both", expand=True)
    
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
