import psycopg2
from psycopg2 import sql
from .config import Config

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = None
        return cls._instance

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    host=Config.DB_HOST,
                    port=Config.DB_PORT
                )
                self.conn.autocommit = True
                print("Database connected successfully.")
                self.create_tables()
            except psycopg2.Error as e:
                print(f"Error connecting to database: {e}")

    def get_cursor(self):
        if self.conn is None:
            self.connect()
        return self.conn.cursor()

    def create_tables(self):
        with self.get_cursor() as cursor:
            # Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL, -- Admin, Cashier, Manager
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    phone VARCHAR(20),
                    cnic VARCHAR(20)
                );
            """)
            
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS pin_hash VARCHAR(255);")
            except Exception:
                pass

            # Activity Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    action VARCHAR(50) NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # User Sessions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    logout_time TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)

            # Suppliers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    contact_person VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100)
                );
            """)

            # Products Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    stock_quantity INTEGER NOT NULL DEFAULT 0,
                    barcode VARCHAR(50) UNIQUE,
                    category VARCHAR(50),
                    loyalty_points INTEGER DEFAULT 0
                );
            """)
            
            # Attempt to add loyalty_points column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS loyalty_points INTEGER DEFAULT 0;")
            except Exception:
                pass # Column likely exists or other error we can ignore for now

            # Restock Orders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restock_orders (
                    id SERIAL PRIMARY KEY,
                    supplier_id INTEGER REFERENCES suppliers(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'COMPLETED'
                );
            """)

            # Customers Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) UNIQUE,
                    loyalty_points INTEGER DEFAULT 0
                );
            """)

            # Sales Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    customer_id INTEGER REFERENCES customers(id),
                    total_amount DECIMAL(10, 2) NOT NULL,
                    payment_method VARCHAR(50), -- Cash, Card, Split
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Update Sales Table for Tax
            try:
                cursor.execute("ALTER TABLE sales ADD COLUMN IF NOT EXISTS tax_amount DECIMAL(10, 2) DEFAULT 0.00;")
            except Exception:
                pass

            # Sale Items Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sale_items (
                    id SERIAL PRIMARY KEY,
                    sale_id INTEGER REFERENCES sales(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL,
                    price_at_sale DECIMAL(10, 2) NOT NULL,
                    refunded_quantity INTEGER DEFAULT 0
                );
            """)

            # Attempt to add refunded_quantity column if it doesn't exist
            try:
                cursor.execute("ALTER TABLE sale_items ADD COLUMN IF NOT EXISTS refunded_quantity INTEGER DEFAULT 0;")
            except Exception:
                pass
            
            # Discounts Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS discounts (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR(50) UNIQUE NOT NULL,
                    discount_type VARCHAR(20) NOT NULL, -- 'PERCENTAGE' or 'FIXED'
                    value DECIMAL(10, 2) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)

            # Seed Admin User if not exists
            cursor.execute("SELECT count(*) FROM users WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                # Password is 'admin123' (In a real app, hash this!)
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role, first_name, last_name)
                    VALUES ('admin', 'admin123', 'Admin', 'System', 'Admin')
                """)
                print("Admin user created (admin/admin123).")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
