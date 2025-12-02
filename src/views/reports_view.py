import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from src.models.reports_model import ReportsModel
from datetime import datetime, timedelta

def build_reports_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    reports_model = ReportsModel()

    ctk.CTkLabel(frame, text="Reports & Analytics", font=("Roboto Medium", 24)).pack(pady=(20, 10))

    # Tabview
    tabview = ctk.CTkTabview(frame)
    tabview.pack(fill="both", expand=True, padx=20, pady=10)

    tabview.add("Sales")
    tabview.add("Cashier")
    tabview.add("Products")

    # --- Tab 1: Sales Reports ---
    tab_sales = tabview.tab("Sales")

    controls_frame = ctk.CTkFrame(tab_sales, fg_color="transparent")
    controls_frame.pack(fill="x", padx=10, pady=10)

    # Treeview Setup
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Roboto", 11), rowheight=25)

    sales_tree_frame = ctk.CTkFrame(tab_sales, fg_color="transparent")
    sales_tree_frame.pack(fill="both", expand=True, padx=10)
    
    cols = ("Date", "Transactions", "Revenue", "Tax")
    sales_tree = ttk.Treeview(sales_tree_frame, columns=cols, show="headings")
    for col in cols:
        sales_tree.heading(col, text=col)
    sales_tree.pack(fill="both", expand=True)

    lbl_total_sales = ctk.CTkLabel(controls_frame, text="Total Revenue: $0.00", font=("Roboto Medium", 16))
    lbl_total_sales.pack(side="right", padx=10)

    def load_sales_report(period):
        for item in sales_tree.get_children():
            sales_tree.delete(item)
        
        end_date = datetime.now().date()
        if period == "Today":
            start_date = end_date
        elif period == "Last 7 Days":
            start_date = end_date - timedelta(days=7)
        elif period == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date

        data = reports_model.get_sales_by_date_range(start_date, end_date)
        total_rev = 0
        total_tax = 0
        if data:
            for row in data:
                revenue = row[2] if row[2] else 0
                tax = row[3] if len(row) > 3 and row[3] else 0
                sales_tree.insert("", "end", values=(row[0], row[1], f"${revenue:.2f}", f"${tax:.2f}"))
                total_rev += revenue
                total_tax += tax
        
        lbl_total_sales.configure(text=f"Total Revenue: ${total_rev:.2f} | Tax: ${total_tax:.2f}")

    ctk.CTkButton(controls_frame, text="Today", command=lambda: load_sales_report("Today"), width=100).pack(side="left", padx=5)
    ctk.CTkButton(controls_frame, text="Last 7 Days", command=lambda: load_sales_report("Last 7 Days"), width=100).pack(side="left", padx=5)
    ctk.CTkButton(controls_frame, text="Last 30 Days", command=lambda: load_sales_report("Last 30 Days"), width=100).pack(side="left", padx=5)

    # --- Tab 2: Cashier Performance ---
    tab_cashier = tabview.tab("Cashier")

    c_cols = ("Cashier", "Transactions", "Total Sales")
    cashier_tree = ttk.Treeview(tab_cashier, columns=c_cols, show="headings")
    for col in c_cols:
        cashier_tree.heading(col, text=col)
    cashier_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_cashier_report():
        for item in cashier_tree.get_children():
            cashier_tree.delete(item)
        data = reports_model.get_sales_by_cashier()
        if data:
            for row in data:
                revenue = row[2] if row[2] else 0
                cashier_tree.insert("", "end", values=(row[0], row[1], f"${revenue:.2f}"))

    ctk.CTkButton(tab_cashier, text="Refresh", command=load_cashier_report).pack(pady=10)
    load_cashier_report()

    # --- Tab 3: Product Performance ---
    tab_product = tabview.tab("Products")

    p_cols = ("Product", "Units Sold", "Revenue Generated")
    prod_tree = ttk.Treeview(tab_product, columns=p_cols, show="headings")
    for col in p_cols:
        prod_tree.heading(col, text=col)
    prod_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_product_report():
        for item in prod_tree.get_children():
            prod_tree.delete(item)
        data = reports_model.get_product_performance()
        if data:
            for row in data:
                revenue = row[2] if row[2] else 0
                prod_tree.insert("", "end", values=(row[0], row[1], f"${revenue:.2f}"))

    ctk.CTkButton(tab_product, text="Refresh", command=load_product_report).pack(pady=10)
    load_product_report()

    # Initial Load
    load_sales_report("Today")

    return frame
