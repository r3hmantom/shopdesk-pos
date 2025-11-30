import os
from datetime import datetime

class ReceiptGenerator:
    @staticmethod
    def get_receipt_dir():
        # Get directory of this file (src/utils)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to src, then up to root (sda-pos)
        project_root = os.path.dirname(os.path.dirname(current_dir))
        return os.path.join(project_root, "receipts")

    @staticmethod
    def generate_receipt(sale_id, cashier_name, customer_name, items, subtotal, tax, discount, total, payment_method):
        receipt_dir = ReceiptGenerator.get_receipt_dir()
        if not os.path.exists(receipt_dir):
            os.makedirs(receipt_dir)
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = os.path.join(receipt_dir, f"receipt_{sale_id}.txt")
        
        lines = []
        lines.append("="*40)
        lines.append("          SDA POS SYSTEM          ")
        lines.append("="*40)
        lines.append(f"Date: {timestamp}")
        lines.append(f"Sale ID: {sale_id}")
        lines.append(f"Cashier: {cashier_name}")
        if customer_name:
            lines.append(f"Customer: {customer_name}")
        lines.append("-" * 40)
        lines.append(f"{'Item':<20} {'Qty':<5} {'Price':<10}")
        lines.append("-" * 40)
        
        for item in items:
            # item: {'name': str, 'quantity': int, 'price': float, ...}
            name = item['name'][:20]
            qty = item['quantity']
            price = item['price'] * qty
            lines.append(f"{name:<20} {qty:<5} ${price:.2f}")
            
        lines.append("-" * 40)
        lines.append(f"Subtotal:   ${subtotal:.2f}")
        lines.append(f"Tax (10%):  ${tax:.2f}")
        lines.append(f"Discount:  -${discount:.2f}")
        lines.append(f"Total:      ${total:.2f}")
        lines.append("-" * 40)
        lines.append(f"Payment: {payment_method}")
        lines.append("="*40)
        lines.append("      Thank you for shopping!      ")
        lines.append("="*40)
        
        content = "\n".join(lines)
        
        try:
            with open(filename, "w") as f:
                f.write(content)
            return filename
        except Exception as e:
            print(f"Error saving receipt: {e}")
            return None

