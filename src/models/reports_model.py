from src.database import Database

class ReportsModel:
    def __init__(self):
        self.db = Database()

    def get_sales_by_date_range(self, start_date, end_date):
        cursor = self.db.get_cursor()
        # start_date and end_date should be date objects or strings 'YYYY-MM-DD'
        query = """
            SELECT DATE(timestamp) as sale_date, COUNT(id) as total_transactions, SUM(total_amount) as total_revenue, SUM(tax_amount) as total_tax
            FROM sales
            WHERE DATE(timestamp) BETWEEN %s AND %s
            GROUP BY DATE(timestamp)
            ORDER BY sale_date DESC
        """
        cursor.execute(query, (start_date, end_date))
        return cursor.fetchall()

    def get_sales_by_cashier(self):
        cursor = self.db.get_cursor()
        query = """
            SELECT u.username, COUNT(s.id) as total_sales, SUM(s.total_amount) as total_revenue
            FROM sales s
            JOIN users u ON s.user_id = u.id
            GROUP BY u.username
            ORDER BY total_revenue DESC
        """
        cursor.execute(query)
        return cursor.fetchall()

    def get_product_performance(self):
        cursor = self.db.get_cursor()
        query = """
            SELECT p.name, SUM(si.quantity) as total_sold, SUM(si.quantity * si.price_at_sale) as total_revenue
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            GROUP BY p.name
            ORDER BY total_sold DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
