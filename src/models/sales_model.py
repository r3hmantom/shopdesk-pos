from src.database import Database

class SalesModel:
    def __init__(self):
        self.db = Database()

    def create_sale(self, user_id, customer_id, total_amount, payment_method, items, tax_amount=0.0):
        """
        items: list of dicts {'product_id': int, 'quantity': int, 'price': float}
        """
        conn = self.db.conn
        if not conn:
            self.db.connect()
            conn = self.db.conn
            
        cursor = conn.cursor()
        try:
            # Start transaction
            cursor.execute("BEGIN")

            # 1. Create Sale Record
            cursor.execute("""
                INSERT INTO sales (user_id, customer_id, total_amount, payment_method, tax_amount)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, customer_id, total_amount, payment_method, tax_amount))
            sale_id = cursor.fetchone()[0]

            # 2. Insert Sale Items and Update Stock
            total_loyalty_points = 0
            
            for item in items:
                # Fetch product loyalty points
                cursor.execute("SELECT loyalty_points FROM products WHERE id = %s", (item['product_id'],))
                res = cursor.fetchone()
                p_points = res[0] if res else 0
                total_loyalty_points += (p_points * item['quantity'])

                cursor.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, price_at_sale)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, item['product_id'], item['quantity'], item['price']))

                # Update Stock
                cursor.execute("""
                    UPDATE products
                    SET stock_quantity = stock_quantity - %s
                    WHERE id = %s
                """, (item['quantity'], item['product_id']))

            # 3. Update Customer Loyalty Points
            if customer_id:
                cursor.execute("""
                    UPDATE customers 
                    SET loyalty_points = loyalty_points + %s 
                    WHERE id = %s
                """, (total_loyalty_points, customer_id))

            cursor.execute("COMMIT")
            return sale_id

        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"Error processing sale: {e}")
            return None
        finally:
            cursor.close()

    def get_sales_history(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT s.id, s.total_amount, s.payment_method, s.timestamp, u.username 
            FROM sales s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.timestamp DESC
        """)
        return cursor.fetchall()

    def get_sale_by_id(self, sale_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
        return cursor.fetchone()

    def get_sale_items(self, sale_id):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT si.id, p.name, si.quantity, si.price_at_sale, si.product_id, si.refunded_quantity 
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        """, (sale_id,))
        return cursor.fetchall()

    def get_customer_receipts(self, customer_id):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT id, timestamp, total_amount, payment_method 
            FROM sales 
            WHERE customer_id = %s 
            ORDER BY timestamp DESC
        """, (customer_id,))
        return cursor.fetchall()

    def process_refund_item(self, sale_item_id, product_id, quantity_to_refund):
        conn = self.db.conn
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN")

            # 1. Get current refund status and sale info
            cursor.execute("""
                SELECT si.quantity, si.refunded_quantity, s.customer_id
                FROM sale_items si
                JOIN sales s ON si.sale_id = s.id
                WHERE si.id = %s
            """, (sale_item_id,))
            res = cursor.fetchone()
            if not res:
                return False, "Item not found"
            
            original_qty, refunded_qty, customer_id = res
            
            if refunded_qty + quantity_to_refund > original_qty:
                return False, "Cannot refund more than original quantity"

            # 2. Update sale_items
            cursor.execute("""
                UPDATE sale_items
                SET refunded_quantity = refunded_quantity + %s
                WHERE id = %s
            """, (quantity_to_refund, sale_item_id))

            # 3. Update Product Stock
            cursor.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity + %s
                WHERE id = %s
            """, (quantity_to_refund, product_id))

            # 4. Revert Loyalty Points (if applicable)
            if customer_id:
                cursor.execute("SELECT loyalty_points FROM products WHERE id = %s", (product_id,))
                p_res = cursor.fetchone()
                if p_res:
                    points_per_item = p_res[0]
                    points_to_deduct = points_per_item * quantity_to_refund
                    
                    cursor.execute("""
                        UPDATE customers
                        SET loyalty_points = GREATEST(0, loyalty_points - %s)
                        WHERE id = %s
                    """, (points_to_deduct, customer_id))

            cursor.execute("COMMIT")
            return True, "Refund processed successfully"

        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"Error processing refund: {e}")
            return False, str(e)
        finally:
            cursor.close()
